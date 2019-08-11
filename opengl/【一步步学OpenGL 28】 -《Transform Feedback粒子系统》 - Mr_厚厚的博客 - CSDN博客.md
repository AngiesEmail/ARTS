# 教程 28 Transform Feedback粒子系统

原文： http://ogldev.atspace.co.uk/www/tutorial28/tutorial28.html

CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

## 背景
粒子系统是一种模拟像烟雾、灰尘、火焰、雨等自然现象的技术统称。这些自然现象的共性是它们都是由大量的小粒子组成的，并按照不同现象的特性进行特定形态的整体运动。

为了模拟由大量粒子组成的自然现象，我们通常要维护每个粒子的位置信息和其他一些属性（例如速度、颜色等等），并且在每一帧要进行下面的一些操作：

更新每一个粒子的属性。这一步通常包含一些数学计算（从简单计算到复杂计算，复杂性取决于要模拟的自然现象的复杂度）。

渲染粒子（将每个点渲染成简单的颜色或者利用billboard公告板技术实现）

在过去，步骤一通常发生在CPU上，应用将会访问顶点缓冲器，扫描里面的内容并且更新每个粒子的属性。步骤二更直接，和其他类型的渲染一样发生在GPU上。但这种方法存在两个问题：

在CPU上更新粒子需要OpenGL驱动从GPU内存中复制顶点缓冲器中的内容到CPU中（在独立显卡中这意味着要通过PCI总线传输数据）。通常我们需要模拟的现象是需要大量的粒子的，数以万计的粒子需求情况也不是少数。如果每个粒子都要占用64 bytes且运行时每秒60帧（很好的帧率了），意味着每秒钟要在GPU和CPU之间来回拷贝640K的内容60次，这会大大影响应用的性能，且随着粒子数量的增加性能也会越差。

更新粒子属性意味着在不同的数据项中运行相同的数学运算，这是一个GPU最擅长的典型的分布式计算的例子，而如果运行在CPU上则意味着要串行运行整个过程。如果CPU是多核的，那么我们可以利用它降低整体的计算时间，但这会需要在应用中做更多额外的工作。而将更新过程运行在GPU上就相当于可以直接获得并行执行的效果。

DirectX10引入了一种叫做Stream Output的新特性，对于实现粒子系统很有用。OpenGL3.0中最后也加入了该新特性并称之为Transform Feedback。该特性背后的思想是，我们可以绑定一个特殊类型的缓冲器（称其为Transform Feedback Buffer，就在几何着色器之后，当然如果几何着色器被忽略的话就是在顶点着色器之后了），并将变换之后的图元传递给该缓冲器。另外，我们可以决定是否让图元继续进行后面常规的光栅化流程。相同的缓冲器下，上一帧输出的顶点信息可以作为缓存用于下一帧的输入。在这个循环中，上面的两步可以完全发生在GPU上而不需要我们应用的参与（并不是为每一帧都绑定相应的缓冲器并设置一些状态）。下面的示意图展示了管线的新的结构：

那么在transform feedback buffer中最后到底有多少图元呢？如果没有用到几何着色器答案就简单了，只要根据当前帧的顶点数即可直接计算。但是如果用到了几何着色器，那么图元的数量就是未知的了，因为在几何着色器过程中是可以添加或者删除图元的（甚至可以包含循环和分支），我们无法总能在缓冲器中计算最终的图元数量。因此，不知道确切的顶点数量之后我们怎么绘制呢？为了解决这个困难，transform feedback引入了一种新的绘制函数，这个函数回调不需要使用顶点数量作为参数。系统会自动为每一个buffer计算顶点数量，之后当buffer缓存作为输入时可在内部使用那个计算好的顶点数量。如果多次将数据输入到transform feedback buffer中（缓冲到里面但是不作为之后的输入）相应的顶点数量也会随之更新增加。我们可以选择随时在buffer内部更新缓存偏移值，同时系统也会根据我们设置的偏移值更新顶点数量值。

在这个教程中，我们将使用transform feedback来模拟火焰效果。火焰模拟中的数学计算相对来说比较容易，因此这里我们重点介绍transform feedback的使用和实现。该框架之后也可以应用到其他类型的粒子系统。

OpenGL有一个强制限制，就是在同一个绘制回调中相同的资源不可以同时绑定作为输入和输出。这意味着如果我们想在顶点缓冲器中更新粒子，我们实际需要两个transform feedback buffer并交替使用它们。在第0帧，我们将在buffer A中更新粒子，并在buffer B中渲染粒子。然后在第1帧中我们将在buffer B中更新粒子，在buffer A中渲染粒子。当然所有这些使用者是无需关心的。

此外，我们也有两个着色器：一个负责更新粒子，另一个负责渲染粒子。我们也会使用前面教程中介绍的公告板技术来渲染。

## 源代码详解

```
(particle_system.h:29)
class ParticleSystem
{
public:
    ParticleSystem();

    ~ParticleSystem();

    bool InitParticleSystem(const Vector3f& Pos);

    void Render(int DeltaTimeMillis, const Matrix4f& VP, const Vector3f& CameraPos);

private:

    bool m_isFirst;
    unsigned int m_currVB;
    unsigned int m_currTFB;
    GLuint m_particleBuffer[2];
    GLuint m_transformFeedback[2];
    PSUpdateTechnique m_updateTechnique;
    BillboardTechnique m_billboardTechnique;
    RandomTexture m_randomTexture;
    Texture* m_pTexture;
    int m_time;
};
```
ParticleSystem类封装了所有管理transform feedback buffer的机制，应用可以实例化ParticleSystem类并使用火焰发射器的世界坐标位置初始化它。在主渲染循环中，ParticleSystem::Render()函数会被调用，并接收三个参数：从上一个回调的毫秒时间差，视图窗口矩阵和投影矩阵的乘积，和相机的世界空间位置。

这个类还有几个属性：一个是Render()函数第一次被调用的标记变量；两个索引，一个指明当前的定点缓冲器（作为输入），另一个指定transform feedback buffer（作为输出）；还有两个顶点缓冲器句柄和两个transform feedback对象句柄；更新和渲染着色器；一个包含随机数的纹理，这个纹理将会贴到离子上；最后还有当前的全局时间变量。

```
(particle_system.cpp:31)
struct Particle
{
    float Type; 
    Vector3f Pos;
    Vector3f Vel; 
    float LifetimeMillis; 
};
```
每一个粒子都可用上面的结构体来表示。一个例子可以是一个发射器，可以是发射器分裂产生的shell或者secondary shell。发射器是静态的，负责产生其他粒子，且在系统中是独一无二的。发射器周期性的创建shell粒子，并往上发射出去，几秒后shells爆炸分裂出secondary shells并飞向随机方向。除了发射器，所有的粒子都有它们的生命周期，系统以毫秒为时间单位计算它们。当粒子的生命周期达到一定时间后就会被移除。另外每个粒子都有它们的位置和速度。当一个粒子被创建后会被给予一个速度向量，这个速度会受到重力的影响使其下落。在每一帧，我们使用速度向量来更新粒子的世界坐标，然后使用更新的坐标来渲染粒子。

```
(particle_system.cpp:67)
bool ParticleSystem::InitParticleSystem(const Vector3f& Pos)
{ 
    Particle Particles[MAX_PARTICLES];
    ZERO_MEM(Particles);

    Particles[0].Type = PARTICLE_TYPE_LAUNCHER;
    Particles[0].Pos = Pos;
    Particles[0].Vel = Vector3f(0.0f, 0.0001f, 0.0f);
    Particles[0].LifetimeMillis = 0.0f;

    glGenTransformFeedbacks(2, m_transformFeedback); 
    glGenBuffers(2, m_particleBuffer);

    for (unsigned int i = 0; i < 2 ; i++) {
        glBindTransformFeedback(GL_TRANSFORM_FEEDBACK, m_transformFeedback[i]);
        glBindBuffer(GL_ARRAY_BUFFER, m_particleBuffer[i]);
        glBufferData(GL_ARRAY_BUFFER, sizeof(Particles), Particles, GL_DYNAMIC_DRAW);
        glBindBufferBase(GL_TRANSFORM_FEEDBACK_BUFFER, 0, m_particleBuffer[i]);
    }
```
这是粒子系统初始化的第一部分。我们在栈上为所有的粒子开辟空间，并只初始化第一个粒子作为发射器（其他的粒子在渲染时再创建）。发射器的位置也是所有要创建的粒子的起点，发射器的速度也是所有新创建粒子的初始速度（发射器自己是静止的）。我们将要使用两个transform feedback缓冲器并在他们之间切换（使用其中一个绘制输出的同时，使用另一个作为输入，反之亦然）。我们可以使用glGenTransformFeedbacks函数创建两个transform feedback对象，它们封装了所有绑定到它们上面的状态。另外创建两个缓冲器对象，分别用于两个transform feedback对象，对于这两个对象我们将进行一系列相同的操作（见下文）。

开始我们先使用glBindTransformFeedback()函数将一个transform feedback对象绑定到GL_TRANSFORM_FEEDBACK目标上，这样该transform feedback对象就变成当前对象，下面和transform feedback相关的操作就都是针对当前对象的。然后将对应的缓冲器对象绑定到GL_ARRAY_BUFFER上，使其成为一个常规的顶点缓冲器，并加载粒子数组的数据内容到缓冲器里面。最后我们绑定相应的缓冲器对象到GL_TRANSFORM_FEEDBACK_BUFFER目标上面，并定义缓冲器索引值为0，使该缓冲器成为一个索引位置为0的transform feedback缓冲器。事实上我们可以将多个缓冲器绑定到不同的索引位置上，这样图元可以输入到不同的缓冲器中，这里我们只需要一个缓冲器。现在我们就有了两个transform feedback对象和对应的两个缓冲器对象，两个缓冲器对象既可以作为顶点缓冲器也可以作为transform feedback缓冲器。

InitParticleSystem()函数剩下的部分就不需要再重复解释了，并没有什么新内容，我们只需简单初始化两个着色器对象（ParticleSystem类的成员），并设置其中一些静态状态，以及加载将要贴到粒子上的纹理。

```
(particle_system.cpp:124)
void ParticleSystem::Render(int DeltaTimeMillis, const Matrix4f& VP, const Vector3f& CameraPos)
{
    m_time += DeltaTimeMillis;

    UpdateParticles(DeltaTimeMillis);

    RenderParticles(VP, CameraPos);

    m_currVB = m_currTFB;
    m_currTFB = (m_currTFB + 1) & 0x1;
}
```
这是ParticleSystem类的主渲染函数，负责更新全局计时器，并在两个缓存之间进行切换（’m_currVB’是当前顶点缓冲器索引初始化为0，而’m_currTFB’是当前transform feedback缓冲器初始化为1）。这个函数的主要作用是调用两个更新粒子属性的私有方法并进行渲染。下面看如何更新粒子。

```
(particle_system.cpp:137)
void ParticleSystem::UpdateParticles(int DeltaTimeMillis)
{
m_updateTechnique.Enable();
m_updateTechnique.SetTime(m_time);
m_updateTechnique.SetDeltaTimeMillis(DeltaTimeMillis);

m_randomTexture.Bind(RANDOM_TEXTURE_UNIT);

开始先启用相应的着色器并设置其中的一些动态状态。着色器要知道从上一帧到这一帧的时间间隔，因为在计算粒子的位移公式中需要用到这个参数，另外还需要一个全局的时间参数作为随机数种子来访问随机纹理。我们声明一个GL_TEXTURE3纹理单元来绑定随机纹理。这个随机纹理是用来为产生的粒子提供运动方向的，而不是提供颜色信息（后面会介绍纹理是如何创建的）。

glEnable(GL_RASTERIZER_DISCARD);

这个个函数回调用到了我们之前没有接触过的东西。由于该渲染回调到该函数的唯一目的就是为了更新transform feedback缓冲器，然后我们想截断图元传递流，并阻止它们经光栅化后显示到屏幕上。阻止的这些渲染操作之后将会在另一个渲染回调中再执行。使用GL_RASTERIZER_DISCARD标志作为参数调用glEnable()函数，告诉渲染管线在transform feedback可选阶段之后和到达光栅器前抛弃所有的图元。

glBindBuffer(GL_ARRAY_BUFFER, m_particleBuffer[m_currVB]); 
glBindTransformFeedback(GL_TRANSFORM_FEEDBACK, m_transformFeedback[m_currTFB]);

接下来的两个函数用来切换我们创建的两个缓冲器。’m_currVB’（0或1）作为顶点缓存数组的一个索引，并且我们将这个缓存绑定到GL_ARRAY_BUFFER上作为输入。’m_currTFB’（总是和’m_currVB’相反）作为transform feedback对象数组的一个索引并且我们将其绑定到GL_TRANSFORM_FEEDBACK目标上，使其成为当前的 transform feedback（连同附着在其上的状态——实际的缓存）。

glEnableVertexAttribArray(0);
glEnableVertexAttribArray(1);
glEnableVertexAttribArray(2);
glEnableVertexAttribArray(3);

    glVertexAttribPointer(0,1,GL_FLOAT,GL_FALSE,sizeof(Particle),0); // type
    glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,sizeof(Particle),(const GLvoid*)4); // position
    glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,sizeof(Particle),(const GLvoid*)16); // velocity
    glVertexAttribPointer(3,1,GL_FLOAT,GL_FALSE,sizeof(Particle),(const GLvoid*)28); // lifetime

上面这几个函数我们之前都使用过，都是根据顶点缓冲区中的数据设置顶点属性。后面会看到我们如何保证输入的结构和输出结构保持一致的。

glBeginTransformFeedback(GL_POINTS);

The real fun starts here. glBeginTransformFeedback() makes transform feedback active. All the draw calls after that, and until glEndTransformFeedback() is called, redirect their output to the transform feedback buffer according to the currently bound transform feedback object. This function also takes a topology parameter. The way transform feedback works is that only complete primitives (i.e. lists) can be written into the buffer. This means that if you draw four vertices in triangle strip topology or six vertices in triangle list topology, you end up with six vertices (two triangles) in the feedback buffer in both cases. The available topologies to this function are therefore:

有趣的部分来了。我们调用glBeginTransformFeedback()函数来激活transform feedback。在这之后的所有绘制的结果（直到glTransformFeedback()被调用）都会被输入到当前的transform feedback缓存中（根据当前绑定的transform feedback对象）。这个函数需要一个拓扑结构变量作为参数。由于Transform feedback工作的方式，只有完整的图元才能被写入到缓存中。这个意思就是如果你绘制四个顶点（其拓扑结构是triangle strip），或者六个顶点（其拓扑结构是triangle list），不论你使用哪种方式最后输入到这个缓存中的数据都将是六个顶点（两个三角形）。对于这个函数的参数可以是下面这几个：


GL_POINTS - the draw call topology must also be GL_POINTS.
GL_LINES - the draw call topology must be GL_LINES, GL_LINE_LOOP or GL_LINE_STRIP.
GL_TRIANGLES - the draw call topology must be GL_TRIANGLES, GL_TRIANGLE_STRIP or GL_TRIANGLE_FAN.

if (m_isFirst) {
    glDrawArrays(GL_POINTS, 0, 1);
    m_isFirst = false;
}
else {
    glDrawTransformFeedback(GL_POINTS, m_transformFeedback[m_currVB]);
} 

如之前所说，我们不知道在缓存中有多少个顶点，但transform feedback支持这种情况。因为我们频繁的生成和删除粒子是基于发射器和每个粒子的生命周期，我们不可能告诉绘制函数有多少个粒子需要绘制。除了第一次渲染之外都是这样。在进行第一次渲染时我们知道在顶点缓冲区只包含发射器粒子，并且系统之前没有transform feedback相关的记录（第一帧渲染之后我们都没使用过它），所以它也不知道缓存中到底存放了多少粒子。这就是为什么第一次绘图一定要明确的使用一个标准的glDrawArrays()来绘制。在其他情况下，我们都会调用glDrawTransformFeedback()来完成绘制。这个函数不需要被告知有多少顶点需要渲染，它仅仅检查输入缓存中的数据并将之前写入到这个缓存中的顶点数据全部渲染出来（只有当它被绑定作为一个transform feedback缓存时才行）。

glDrawTransformFeedback()需要两个参数。第一个参数是绘制的图元的拓扑结构，第二个参数是当前被绑定到顶点缓冲区上的transform feedback对象。记住当前绑定的transform feedback对象是m_transformFeedback[m_currTFB]。这是绘制函数的目标缓冲区。将要处理的顶点的个数来自于在上一次在这个函数中被绑定到GL_TRANSFORM_FEEDBACK目标上的transform feedback对象。有点混乱，我们只需要简单的记住当我们向transform feedback对象#1中写入的时候，就从transform feedback对象#0中得到顶点的个数来进行绘制，反之亦然。现在的输入将作为以后的输出。

glEndTransformFeedback();

每一次调用glBeginTransformFeedback()之后一定要记得调用glEndTransformFeedback()。如果漏掉这个函数，将会出现很大的问题。

glDisableVertexAttribArray(0);
glDisableVertexAttribArray(1);
glDisableVertexAttribArray(2);
glDisableVertexAttribArray(3);
}

```
这一部分是很常见的，当运行到这里的时候，所有的粒子都已经被更新过了，接下来让我们看看如何对更新之后的粒子进行渲染。

```
(particle_system.cpp:177)
void ParticleSystem::RenderParticles(const Matrix4f& VP, const Vector3f& CameraPos)
{
    m_billboardTechnique.Enable();
    m_billboardTechnique.SetCameraPosition(CameraPos);
    m_billboardTechnique.SetVP(VP);
    m_pTexture->Bind(COLOR_TEXTURE_UNIT);

我们通过启用billboarding技术对粒子进行渲染，在渲染之前我们为这个着色器设置了一些参数。每个粒子将被扩展为一个四边形平面，这里绑定的纹理最终会被映射到这个平面上。

    glDisable(GL_RASTERIZER_DISCARD);

在我们将数据写入到transform feedback缓存中时，光栅化被禁用了。我们使用其glDisable()函数来启用光栅器。

    glBindBuffer(GL_ARRAY_BUFFER, m_particleBuffer[m_currTFB]);

当我们写数据进transform feedback缓存时，我们将m_transformFeedback[m_currTFB]绑定位为transform feedback对象，附着在那个对象上的顶点缓冲区就是m_particleBuffer[m_currTFB]。我们现在绑定这个缓存来为渲染提供输入顶点。

    glEnableVertexAttribArray(0);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Particle), (const GLvoid*)4); // position

    glDrawTransformFeedback(GL_POINTS, m_transformFeedback[m_currTFB]);

    glDisableVertexAttribArray(0);
}
```
在transform feedback缓存中的粒子有四个属性。但是在渲染粒子的时候，我们只需要知道粒子的位置信息，所以我们只启用了位置属性对应的位置，同时我们确定间隔（相邻的同属性之间的距离）为sizeof(Particle),而其他的三个属性被我们忽略。
同样，我们还是使用glDrawTransformFeedback()来绘制。第二个参数是transform feedback对象（该对象被匹配到输入的顶点缓冲区）。这个对象知道有多少个顶点要被绘制。

```
(ps_update_technique.cpp:151)
bool PSUpdateTechnique::Init()
{
    if (!Technique::Init()) {
        return false;
    }

    if (!AddShader(GL_VERTEX_SHADER, pVS)) {
        return false;
    }

    if (!AddShader(GL_GEOMETRY_SHADER, pGS)) {
        return false;
    }

    const GLchar* Varyings[4]; 
    Varyings[0] = "Type1";
    Varyings[1] = "Position1";
    Varyings[2] = "Velocity1"; 
    Varyings[3] = "Age1";

    glTransformFeedbackVaryings(m_shaderProg, 4, Varyings, GL_INTERLEAVED_ATTRIBS); 

    if (!Finalize()) {
        return false;
    }

    m_deltaTimeMillisLocation = GetUniformLocation("gDeltaTimeMillis");
    m_randomTextureLocation = GetUniformLocation("gRandomTexture");
    m_timeLocation = GetUniformLocation("gTime");
    m_launcherLifetimeLocation = GetUniformLocation("gLauncherLifetime");
    m_shellLifetimeLocation = GetUniformLocation("gShellLifetime");
    m_secondaryShellLifetimeLocation = GetUniformLocation("gSecondaryShellLifetime");

    if (m_deltaTimeMillisLocation == INVALID_UNIFORM_LOCATION ||
        m_timeLocation == INVALID_UNIFORM_LOCATION ||
        m_randomTextureLocation == INVALID_UNIFORM_LOCATION) {
        m_launcherLifetimeLocation == INVALID_UNIFORM_LOCATION ||
        m_shellLifetimeLocation == INVALID_UNIFORM_LOCATION ||
        m_secondaryShellLifetimeLocation == INVALID_UNIFORM_LOCATION) {
        return false;
    }

    return true;
}
```
现在应该大致了解了我们为什么要创建transform feedback对象，将一个缓冲附加到这个对象并且将场景渲染到这个缓存中。但这仍然有一个问题：到底是什么进入到了feedback缓存中？是一个完整的顶点？我们可以指定顶点属性的一个子集么?它们之间的顺序是怎样的？上面的代码解释了这些问题，这个函数用于初始化PSUpdateTechique，这个类是负责对粒子属性进行更新的着色器。我们在glBeginTransformFeedback()和glEndTransformFeedback()之间使用它。为了指定要输入进缓存中的属性，我们需要在着色器程序对象链接之前调用glTransformFeedbackVaryings()。这个函数有四个参数：程序对象、属性名的字符串数组、在数组中的字符串数量、以及一个标记值（``GL_INTERLEAVED_ATTRIBS或者GL_SEPARATE_ATTRIBS``）。数组中的字符串都必须上一个着色器阶段输出的属性的名字（必须是在FS之前，可以是VS或者GS）。当 transform feedback被激活的时候，每个顶点的这些属性将被写进缓存中。属性的顺序和数组中的顺序一样。至于glTransformFeedbackVaryings()函数的最后的一个参数是告诉OpenGL是把所有的属性作为一个结构体输入到一个缓存中（GL_INTERLEAVER_ATTRIBS）还是把每一个属性都输出到单独的缓存中(GL_SEPARATE_ATTRIBS)中。如果你使用``GL_SEPARATE_ATTRIBS``,则只需要绑定一个缓存即可；但是如果你使用``GL_SEPARATE_ATTRIBS``,那么你需要为每一个属性都绑定一个缓存（绑定的位置需要与属性的所在的槽相对应），缓存绑定的位置可以通过glBindBufferBase()函数的第二个参数来指定。此外，绑定的缓存的数量也是有明确限制的，其数量不允许超过``GL_MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS``（通常是4）。

除了glTransformFeedbackVaryings()，其他的代码都是比较常见的。但是注意在这个着色器中我们并没有使用片元着色器，因为我们在更新粒子的时候禁用了光栅化，所以我们不需要FS。

```
(ps_update.vs)
#version 330

layout (location = 0) in float Type;
layout (location = 1) in vec3 Position;
layout (location = 2) in vec3 Velocity;
layout (location = 3) in float Age;

out float Type0;
out vec3 Position0;
out vec3 Velocity0;
out float Age0;

void main()
{
    Type0 = Type;
    Position0 = Position;
    Velocity0 = Velocity;
    Age0 = Age;
}
```
这是负责粒子更新的顶点着色器代码。如你所见，这里面十分的简单，它所做的一切都是将顶点属性传递到GS(重头戏开始的地方)。

```
(ps_update.gs)
#version 330

layout(points) in;
layout(points) out;
layout(max_vertices = 30) out;

in float Type0[];
in vec3 Position0[];
in vec3 Velocity0[];
in float Age0[];

out float Type1;
out vec3 Position1;
out vec3 Velocity1;
out float Age1;

uniform float gDeltaTimeMillis;
uniform float gTime;
uniform sampler1D gRandomTexture;
uniform float gLauncherLifetime;
uniform float gShellLifetime;
uniform float gSecondaryShellLifetime;

#define PARTICLE_TYPE_LAUNCHER 0.0f
#define PARTICLE_TYPE_SHELL 1.0f
#define PARTICLE_TYPE_SECONDARY_SHELL 2.0f

```
在几何着色器中，首先对我们需要的一些属性进行了定义，它会接收一些顶点属性，同时也会输出一些顶点属性。我们从VS中得到的所有属性都会被输出到transform feedback缓存中（在进行一些处理之后）。同时这里也声明了一些一致变量，通过这些一致变量我们可以设置发射器的频率，shell和secondary shell的生命周期（发射器根据它的频率生成一个shell并且在shell的生命周期结束的时候，shell分裂成多个secondary shell）。

```
vec3 GetRandomDir(float TexCoord)
{
    vec3 Dir = texture(gRandomTexture, TexCoord).xyz;
    Dir -= vec3(0.5, 0.5, 0.5);
    return Dir;
}
```
我们使用这个函数来为shell生成一个随机的的方向。方向被储存在一个1D纹理（纹理的元素是浮点型的3D向量）。我们稍后将看见如何用随机向量来填充纹理。这个函数仅仅只有一个浮点类型参数并且使用它来从纹理中采样。因为在纹理中的所有的值都是在[0.0 - 1.0]之间，我们把采样的结果减去向量[0.5，0.5，0.5]，这样做是为了把值的范围映射到[-0.5 -0.5]之间，这样获得的向量就可以朝向任意方向了。

```
void main()
{
    float Age = Age0[0] + gDeltaTimeMillis;

    if (Type0[0] == PARTICLE_TYPE_LAUNCHER) {
        if (Age >= gLauncherLifetime) {
            Type1 = PARTICLE_TYPE_SHELL;
            Position1 = Position0[0];
            vec3 Dir = GetRandomDir(gTime/1000.0);
            Dir.y = max(Dir.y, 0.5);
            Velocity1 = normalize(Dir) / 20.0;
            Age1 = 0.0;
            EmitVertex();
            EndPrimitive();
            Age = 0.0;
        }

        Type1 = PARTICLE_TYPE_LAUNCHER;
        Position1 = Position0[0];
        Velocity1 = Velocity0[0];
        Age1 = Age;
        EmitVertex();
        EndPrimitive();
    }

GS的主函数包含粒子的处理过程。首先我们判断粒子存在的时间是否到达其生命周期，然后再根据粒子的不同类型进行不同的处理。上面的代码处理发射器粒子的情况。如果发射器的生命周期结束，我们生成一个 shell 粒子和把它送进transform feedback缓存中。shell粒子以发射器的位置作为起始位置并通过从随机纹理中进行采样来获得粒子的速度矢量。我们使用全局时间作为伪随机数种子（虽然不是真正的随机数但是还是能满足我们的需要了），之后我们需要确保方向向量的Y值是大于等于0.5的，这样shell粒子才会是始终朝向天空发射的。最后这个方向向量被标准化并除以20作为速度矢量（你可以根据你自己的系统做一个调整）。新粒子的年龄当然是为0，我们也重设发射器的年龄使得发射器可以再次通过这个逻辑发射粒子。此外，我们总是会将发射器重新输出到缓存中（因为发射器始终都存在场景中的）。

    else {
        float DeltaTimeSecs = gDeltaTimeMillis / 1000.0f;
        float t1 = Age0[0] / 1000.0;
        float t2 = Age / 1000.0;
        vec3 DeltaP = DeltaTimeSecs * Velocity0[0];
        vec3 DeltaV = vec3(DeltaTimeSecs) * (0.0, -9.81, 0.0);

在我们开始处理shell和secondary shell之前，我们需要定义一些相关的变量。DeltaTimeSecs是存放将毫秒转化为秒的间隔时间。我们也将粒子（t1）的旧年龄和粒子（t2）的新年龄转换成秒为单位。在位置坐标上的改变根据公式'position = time * velocity'来计算。最后我们通过重力向量乘以DeltaTimeSecs来计算速度的改变量，粒子在其产生的时候获得一个速度矢量，但是在这之后唯一影响它的就是重力（忽略风等）。在地球上一个下落物体的重力加速度为9.81，因为重力的方向是向下的，所以我们重力向量的Y分量设置为负，X和Z分量设置为0。

        if (Type0[0] == PARTICLE_TYPE_SHELL) {
            if (Age < gShellLifetime) {
                Type1 = PARTICLE_TYPE_SHELL;
                Position1 = Position0[0] + DeltaP;
                Velocity1 = Velocity0[0] + DeltaV;
                Age1 = Age;
                EmitVertex();
                EndPrimitive();
            }
            else {
                for (int i = 0 ; i < 10 ; i++) {
                    Type1 = PARTICLE_TYPE_SECONDARY_SHELL;
                    Position1 = Position0[0];
                    vec3 Dir = GetRandomDir((gTime + i)/1000.0);
                    Velocity1 = normalize(Dir) / 20.0;
                    Age1 = 0.0f;
                    EmitVertex();
                    EndPrimitive();
                }
            }
        }

我们现在把注意力放在shell粒子的处理上。只要这个例子的年龄还没有达到它的生命周期，它将会一直被保存在系统中，我们只需要基于之前算的变化量来更新它的坐标和速度即可。一旦它达到它的生命周期，它将会被删除并且生成10个secondary粒子来代替它，之后把这十个粒子输出到缓存中。这些新生成的粒子都会获得当前 shell粒子的位置属性，至于速度则通过上面提到的方法来获取一个随机的速度矢量。对于Secondary shell 粒子，我们不会限制其方向，它可以向任意方向发射，这样看起来才会像是真的。

        else {
            if (Age < gSecondaryShellLifetime) {
                Type1 = PARTICLE_TYPE_SECONDARY_SHELL;
                Position1 = Position0[0] + DeltaP;
                Velocity1 = Velocity0[0] + DeltaV;
                Age1 = Age;
                EmitVertex();
                EndPrimitive();
            }
        }
    }
}
```
secondary shell的处理和shell的处理是相似的，不同的是当它达到生命周期的时候，它直接被删除并且没有新的粒子生成。

```
(random_texture.cpp:37)
bool RandomTexture::InitRandomTexture(unsigned int Size)
{
    Vector3f* pRandomData = new Vector3f[Size];

    for (unsigned int i = 0 ; i < Size ; i++) {
        pRandomData[i].x = RandomFloat();
        pRandomData[i].y = RandomFloat();
        pRandomData[i].z = RandomFloat();
    }

    glGenTextures(1, &m_textureObj);
    glBindTexture(GL_TEXTURE_1D, m_textureObj);
    glTexImage1D(GL_TEXTURE_1D, 0, GL_RGB, Size, 0.0f, GL_RGB, GL_FLOAT, pRandomData);
    glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_REPEAT); 

    delete [] pRandomData;

    return GLCheckError();
}
```

RandomTexture类是一个十分有用的工具，它能够为着色器程序提供随机数据。这是一个以GL_RGB为内部格式的1D纹理并且是浮点类型的。这意味着每一个元素是3个浮点类型值组成的一个向量。注意我们设置其覆盖模式为GL_REPEAT。这允许我们使用任意的纹理坐标来进行纹理纹理。如果纹理坐标是超过1.0，它简单的被折回到合理的范围，所以它总是能够得到一个合法的值。在这个教程中random texture都是被绑定在3号纹理单元上的。你可以看见在头文件engine_common.h里看到纹理单元的设置。 


