# 教程17 环境光

原文： http://ogldev.atspace.co.uk/www/tutorial16/tutorial16.html

CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

## 背景
光照是是3D图形领域中一个最重要的对象之一。光照模型对于场景的渲染很重要，可以增添很多真实性效果。之所以叫做‘光照模型’是因为你不能去准确的去模拟现实世界的光照过程，因为现实中的光照是由大量的叫做‘光子’的粒子组成，并且同时有波动性和离子性（光的波粒二象性）。如果要在程序中对每一个光子都进行相应的计算的话很快那么就会超出计算机的处理能力了，计算量太大。 
因此，在过去的几年中人们建立了几种光照模型，来模拟光照射到物体上的主要效果并使物体可见。随着3D领域的快速发展和强大的计算机的出现这些模型也相应演变的越来越复杂。后面的教程中我们会学习几种基本的容易实现的光照模型，同时这些基本模型也是对场景效果表现最显著的。

基本的光照模型主要包括‘环境光/漫反射/镜面反射’。环境光是在晴天室外到处看到的光的类型，虽然太阳光穿过天空云层以不同角度照射到大地上，有很多地方肯定会被遮挡，但多数物体都是可见的，即使是在阴影下。这是因为光照射到物体上后都会向四处弹射，所以即使太阳光没有直接照射到的物体仍然可以发亮被看到。即使是房间里的一个灯泡也会和太阳光的原理一样散射环境光，因为房间不是很大所有的物体都被几乎均匀的点亮。环境光也就被建模为一个没有光源、没有方向并且对场景中的所有物体产生相同的点亮效果的一种光。

漫反射光强调的是光照射到物体表面的角度对物体亮度效果的影响。当光照射到物体的一面时这一面就会比其他一面要亮（其他面没有直接面向光源）。之前我们只说看到太阳光发射没有特定方向的环境光，但太阳光还有一个散射的特性，当太阳光照射到一个建筑物上时会看到照射到的一面比其他面要亮，漫反射光最重要的特性就是光的方向。

镜面反射光与其说是光本身的特性不如说是物体的一种属性，这种属性 是在入射光和观察者的视角都在某个特定的角度时会使物体高度发光，比如在晴天会看到小汽车的某个边缘会格外的发光耀眼。计算镜面反射光既要考虑光的入射角度又要考虑观察者的视角位置。

在3D应用中通常不需要直接分别创建环境光、漫反射和镜面反射光的光源，而是可以使用像室外的太阳、室内的灯泡或者洞穴里的手电筒这些光源。这些光源类型通常是有那三种光照模型和其他一些特殊属性的一些不同组合性质的光源。例如，一个手电筒会发出锥形的光源，离手电筒太远的物体根本不会被照亮。

下面的教程我们将会创建几种有用的光源类型同时学习基本的光照模型。 

首先我们先学习一种叫做‘平行光directional light’的光源。平行光有特定的方向但是没有特定的光源，就是说所有的光都互相平行，平行光的方向使用一个向量来定义，并且这个向量将会在场景中所有物体的光照计算中用到，不管在什么位置。太阳光其实和平行光差不多了，如果非要考虑计算照射到两个建筑物上的太阳光之间的精确角度的话，会发现这这两束光基本上是平行的（会有极小的偏差），因为太阳离地球15000万千米远，因此我们可以直接不考虑太阳的位置，只考虑其方向就可以了。

平行光的另外一个重要性质是不管它离物体多远亮度是不变的（没有实际位置，不考虑光的衰减），这个和之后要学习的另外一种光源：点光源相反，点光源会随着距离增加而逐渐衰弱（灯泡就是个很好的例子）。

下面的图片表示的是平行光的性质： 
 
我们已经知道太阳光中既有环境光的属性也有漫反射光的属性，这里我们先创建环境光的部分，下个教程再创建漫反射光的部分。

之前的教程我们学习了如何从纹理中采样颜色值。颜色有三个通道（红绿蓝），每个通道占一个byte，也就是颜色值范围是从0到255。各通道值的不同组合可以创建不同的颜色，每个通道的值都为0时是黑色，每个值都为255时是白色，其他值就是黑白之间的灰色或者彩色了。通过同时增大或者缩小各通道的值，可以在保持颜色不变的情况下使其变量或者变暗。

当白光照射到物体表面上是时反射的颜色就是物体表面的颜色，但亮度会随着光源强度变化，但还是那个颜色。如果光源是纯红色(255,0,0),那么反射的颜色也是偏红色了，因为红光没有绿色或蓝色通道的光可以从物体表面反射回来，如果同时物体表面是纯蓝色的话那结果就是纯黑色了。光只能暴露显示物体的实际颜色，但不能往上添加颜色。

光源的颜色我们会定义为一个包含三个浮点数的三元组，浮点数介于[0,1]之间（之后会和物体表面的颜色相乘，相当于各通道的颜色饱和率）。光源的颜色（那个三元组）和物体表面的颜色相乘就可以得到反射回来的颜色了。同时，我们还想将环境光的强度因素加入其中，那么环境光的强度参数就可以定义为一个[0，1]之间的一个单一的浮点数，然后和之前计算得到的反射回来的颜色值的每个通道都相乘，从而得到最终的颜色值。

下面的公式总结了环境光的计算过程：

在这个教程的示例代码中你可以通过调整‘a’和‘s’这两个参数来增大或者减小环境光的强度，看环境光对贴了纹理的金字塔模型的表面效果的影响。这里只有平行光中环境光的那一部分所以还没有引入方向的概念，下个教程中学习漫射光的时候就会加入光的方向了，这里暂时会看到金字塔会被均匀的照亮，不管从哪个角度去看。

环境光在很多情况下会被尽量的避免去考虑，因为它看上去有点太人工化，简单的实现并不会使场景更真实。使用一些更高级的技术比如全局光照会减少对环境光的需求，因为其实还要考虑光从物体表面反射后又照到其他物体上的事实。由于还没有到后面那些高级模型的学习阶段，这里就只是添加少量的环境光来避免出现物体一面被照亮而另一面完全是黑色的现象，因为最后要使光线看上去真实好看还需要调整很多的参数和其他不同的一些工作。


## 源代码详解
从现在开始我们的示例工程代码会变得越来越复杂，这个教程中，除了实现环境光，我们还会很大程度上重新组织构建我们的工程代码，使其方便用于后面的教程中，源码主要的变化有：

将shader的管理封装在一个Technique类中，包括编译和链接的一些工作。然后我们可以在Technique类的继承类中实现我们的一些可见效果。

将GLUT的初始化和回调管理移到GLUTBackend组件中，这个组件会注册接受来自GLUT的回调调用并将回调使用一个叫做ICallbacks的C++接口传送到应用中。
将主函数cpp文件中的全局函数和变量移到一个应用程序可以调用的类中，后面我们会将这个类扩展成一个用于所有应用的基础类，来提供通用的方法。这种架构设计方式在很多游戏引擎和框架中很流行。

除了光照模型定义的部分代码，这个教程中的多数代码都没有更新变化，只是将它们按照上面的方式重新组织了，所以只有下面的一些新的头文件更新了。

```
(glut_backend.h:24)
void GLUTBackendInit(int argc, char** argv);

bool GLUTBackendCreateWindow(unsigned int Width, unsigned int Height, unsigned int bpp, bool isFullScreen, const char* pTitle);
```
GLUT的很多变量生命的代码全都移到了一个”GLUT backend”组件中，这样就可以用上面的函数更加简单方便的来初始化GLUT以及创建一个窗口。

```
(glut_backend.h:28)
void GLUTBackendRun(ICallbacks* pCallbacks);
```
GLUT初始化并创建一个窗口之后下一步是使用上面的一个包装函数来执行GLUT主循环。这里添加的一点是一个ICallbacks接口来用于注册GLUT回调函数，这样就不用在每个应用中都在自己的GLUT中注册这些回调，还要注册他们自己的私有函数并将这些事件传给上面函数中定义的对象。应用的主要的类会经常实现这个接口并将自身作为参数用于GLUTBackendRun的调用。这个教程也采用了这种事件分配方法。

```
(technique.h:25)
class Technique
{
public:

   Technique();

   ~Technique();

   virtual bool Init();

   void Enable();

protected:

   bool AddShader(GLenum ShaderType, const char* pShaderText);

   bool Finalize();

   GLint GetUniformLocation(const char* pUniformName);

private:

   GLuint m_shaderProg;

   typedef std::list<GLuint> ShaderObjList;
   ShaderObjList m_shaderObjList;
};
```
在之前的教程中所有编译和链接的工作都放在主应用中，这里Technique这个类将一些通用的函数包装起来并允许衍生的类将工作集中到核心效果的展示上。

不管什么技术最开始都是要调用Init()函数进行初始化的，Technique的衍生类必须要先调用基类的Init()函数（要创建OpenGL程序对象）然后再添加衍生类自身的一些初始化操作。
Technique对象创建并初始化之后，通常下一步衍生子类会调用protected类型的AddShader()函数，来加载需要用到的GLSL着色器脚本（一段字符串序列）。最后，调用Finalize()函数来连接对象，Enable()函数实际是包装了glUseProgram()的函数，因此每当转到一个Technique对象都要及时调用这个函数并调用一个绘制函数。

这个类会一直跟随编译出的中间对象直到这个link链接调用glDeleteShader()函数来将他们删除。这个可以帮助减少你的应用消耗的资源的量。为了更好的性能表现，OpenGL应用经常在加载期间编译所有的shader而不是在运行时编译。及时移除释放掉不用的对象可以让应用减少对OpenGL资源的占用。程序对象自身会使用glDeleteProgram()在销毁阶段将自己删除掉。

```
(tutorial17.cpp:49)
class Tutorial17 : public ICallbacks
{
public:

        Tutorial17()
        {
                ...
        }

        ~Tutorial17()
        {
                ...
        }

        bool Init()
        {
                ...
        }

        void Run()
        {
             GLUTBackendRun(this);
        }

        virtual void RenderSceneCB()
        {
                ...
        }

        virtual void IdleCB()
        {
                ...
        }

        virtual void SpecialKeyboardCB(int Key, int x, int y)
        {
                ...
        }

        virtual void KeyboardCB(unsigned char Key, int x, int y)
        {
                ...
        }

        virtual void PassiveMouseCB(int x, int y)
        {
                ...
        }

private:

        void CreateVertexBuffer()
        {
                ...
        }
        void CreateIndexBuffer()
        {
                ...
        }

        GLuint m_VBO;
        GLuint m_IBO;
        LightingTechnique* m_pEffect;
        Texture* m_pTexture;
        Camera* m_pGameCamera;
        float m_scale;
        DirectionalLight m_directionalLight;
};
```
这是将主程序中剩下的我们所熟悉的代码封装起来的一个类结构。Init()负责创建效果，加载纹理并创建顶点或者索引缓冲。Run()调用GLUTBackendRun()函数同时以它的对象本身为参数。由于类实现了ICallbacks接口，所有的GLUT事件都会在这个类中合适的方法中终止。另外之前全局文件区所有的全局变量现在类中都成了私有成员属性。

```
(lighting_technique.h:25)
struct DirectionalLight
{
        Vector3f Color;
        float AmbientIntensity;
};
```
这是平行光最开始的定义，现在只有环境光部分存在，而方向本身仍然是看不见不起作用的，下个教程引入漫反射光的时候我们会加入平行光的方向。上面这个数据结构包含两部分：光的颜色值和环境光的强度。光的颜色值决定着物体表面颜色值的那个通道的颜色可以反射回来以及各通道反射回来的强度。比如，光的颜色值如果是(1.0,0.5,0.0)，那么红色通道将会被完全的反射回来，绿色通道的颜色值会削弱一半，蓝色通道会完全丢失反射不回来。这也是为什么物体表面只能反射回光有的颜色（光源按照不同通道的强度有多种），太阳光也就是白光各通道都很饱满，纯白色的光的颜色值为(1.0,1.0,1.0)。

环境光强度的定义决定了光源有多亮或者多暗。纯白光的强度为1.0所以物体会被完全照亮，而0.1强度的光源找到的物体虽然能看见但是很暗淡。

```
(lighting_technique.h:31)
class LightingTechnique : public Technique
{
public:

    LightingTechnique();

    virtual bool Init();

    void SetWVP(const Matrix4f& WVP);
    void SetTextureUnit(unsigned int TextureUnit);
    void SetDirectionalLight(const DirectionalLight& Light);

private:

    GLuint m_WVPLocation;
    GLuint m_samplerLocation;
    GLuint m_dirLightColorLocation;
    GLuint m_dirLightAmbientIntensityLocation;
};
```
这里是用到Technique类的第一个例子，LightingTechnique是一个衍生的子类，可以使用基类Technique提供的像编译、链接这些通用的功能来实现对光模型的设置和操作。Init()函数在对象创建后调用，它通过简单的调用Technique::AddShader()和Techique::Finalize()函数来创建GLSL程序。

```
(lighting.fs)
#version 330

in vec2 TexCoord0;

out vec4 FragColor;

struct DirectionalLight
{
    vec3 Color;
    float AmbientIntensity;
};

uniform DirectionalLight gDirectionalLight;
uniform sampler2D gSampler;

void main()
{
    FragColor = texture2D(gSampler, TexCoord0.xy) *
            vec4(gDirectionalLight.Color, 1.0f) *
            gDirectionalLight.AmbientIntensity;
}
```
在这个教程中顶点着色器保持不变，还是负责传递位置（和WVP矩阵相乘之后）和纹理坐标。新的逻辑操作都放在了片断着色器中，这里唯一增添的部分是使用struct关键字定义了平行光的数据结构。可以看到这个结构体的关键词和在C/C++中的用法是一样的。这个结果体要保持和应用中定义的结构体一样这样应用程序才能和shader进行数据交流。然后这里有一个DirectionalLight类型的新的一致变量，变量由应用程序来进行更新。这个一致变量要在计算最终的像素颜色中用到。就是说我们是在纹理中采样获得基本颜色，然后将颜色和环境光强度相乘得到最终颜色的。这就是加入环境光的计算过程。

```
(lighting_technique.cpp:44)
m_WVPLocation = GetUniformLocation("gWVP");
m_samplerLocation = GetUniformLocation("gSampler");
m_dirLightColorLocation = GetUniformLocation("gDirectionalLight.Color");
m_dirLightAmbientIntensityLocation = GetUniformLocation("gDirectionalLight.AmbientIntensity");
```
为了从应用程序中获取DirectionalLight一致变量必须要分别获取两个区域中它的位置，LightingTechnique类中有四个GLuint位置变量，用于获取顶点着色器和片段着色器中的一致变量，WVP和取样器的位置也是这样获取的。颜色值和环境光强度通过上面的方式获得：一个是在shader重定义的一致变量的名字（gDirectionalLight），然后用点运算符获取结构体中两个区域的变量。同时设置结构体中的这些变量的值也和其他普通变量一样进行直接赋值。
LightingTechnique类提供了两种方法来设置平行光的内部变量和WVP矩阵的值。

这里你可以通过‘a’和‘s’键来增大或者减小环境光的强度，可以看一下本教程的KeyboardCB()函数，看这是怎样实现的。 


