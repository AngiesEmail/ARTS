







教程 23
阴影图1

原文： http://ogldev.atspace.co.uk/www/tutorial23/tutorial23.html
CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

背景
阴影和光是紧密联系的，正如你需要光才能投射出阴影。有许多的技术可以生成阴影，在接下来的两个章节中我们将学习一种基础而简单的技术-阴影图。
当涉及到光栅化和阴影的问题时，你可能会问这个像素是否位于阴影中?或者说，从光源到像素的路径是否通过其他物体？如果是，这个像素可能位于阴影中（假定其他的物体不透明），否则，则像素不位于阴影中。从某种程度上讲，这个问题类似于我们在之前的教程中问的问题：如何确定当两个物体重叠时，我们看到的是比较近的那个？如果我们把相机放在光源的位置，那么这两个问题就是一会儿事儿了。我们希望在深度测试中落后的像素是因为像素处于阴影中。只有在在深度测试中获胜的像素才会受到光的照射。这些像素都是直接和光源接触的，其间没有任何东西会遮蔽它们。这就是在阴影图背后的原理。
看似深度测试可以帮助我们检测一个像素是否位于阴影中，但是还有一个问题：相机和光源并不总是位于同一个地方。深度测试通常用于解决从相机角度看物体是否可见的问题。那么当光源处于远处的时候，我们如何利用深度测试来进行阴影测试？解决方案是渲染场景两次。首先从光源的角度来看，此时渲染通道的结果并没有存储到颜色缓冲区中，相反，离光源最近的深度值被渲染到应用程序创建的深度缓冲区中（而不是由GLUT自动生成的）；其次，从摄像机的角度来看场景，我们创建的深度缓冲区被绑定到片元着色器以便读取。对于每一个像素，我们从这个深度缓冲区中取出相应的深度值，同时我们也计算这个像素到光源的距离。有时候这两个深度值是相等的。说明这个像素与光源最近，因此它的深度值才会被写进深度缓冲区，此时，这个像素就被认为处于光照中会和正常情况一样去计算它的颜色。如果这两个深度值不同，意味着从光源看这个像素时有其他像素遮挡了它，这种情况下我们在颜色计算中要增加阴影因子来模仿阴影效果。看下面这幅图： 

以上场景由两个对象组成——物体表面和立方体。光源是位于左上角并且指向立方体。在第一次渲染过程中，我们从光源的角度呈现深度缓冲区。看图中A，B，C这3个点。当B被渲染时，它的深度值进入深度缓冲区，因为在B和光源之间没有任何东西，我们默认它是那条线上离光源最近的点。然而当A和C被渲染的时候，它们在深度缓冲区的同一个点上“竞争”。两个点都在同一条来自光源的直线上，所以在透视投影后，光栅器发现这两个点需要去往屏幕上的同一个像素。这就是深度测试，最后C点“赢”了，则C点的深度值被写入了深度缓存中。
在第二个渲染过程中，我们从摄像机的角度渲染表面和立方体。我们在着色器中除了为每个像素做一些计算，我们还计算从光源到像素之间的距离，并和在深度缓冲区中对应的深度值进行比较。当我们光栅化B点时，这两个值应该是差不多相等的（可能由于插值的不同和浮点类型的精度问题会有一些差距），因此我们认为B不在阴影中而和往常一样进行计算。当光栅化A点的时候，我们发现储存的深度值明显比A到光源的距离要小。所以我们认为A在阴影中，并且在A点上应用一些阴影参数，使它比以往暗一些。
简言之，这就是阴影映射算法（我们在第一次渲染通道中渲染的深度缓冲称为“阴影图”），我们将分两个阶段学习它。在第一个阶段（本节）我们将学习如何将深度信息渲染到阴影图中，渲染一个由应用程序创建的纹理，被称为 ‘纹理渲染 ；我们将使用一个简单的纹理映射技术在屏幕上显示阴影图，这是一个很好的调试过程，为了得到完整的阴影效果，正确的绘制阴影图是至关重要的。在下一节我们将看见如何使用阴影图来计算顶点“是否处于阴影中”。
这一节我们使用的模型是一个简单的可以用来显示阴影图的四边形网格。这个四边形是由两个三角形组成的，并设置纹理坐标使它们覆盖整个纹理。当四边形被渲染的时候，纹理坐标被光栅器插值，于是就可以采样整个纹理并将其显示在屏幕上。
源代码详解
(shadow_map_fbo.h:50)
class ShadowMapFBO
{
    public:
        ShadowMapFBO();

        ~ShadowMapFBO();

        bool Init(unsigned int WindowWidth, unsigned int WindowHeight);

        void BindForWriting();

        void BindForReading(GLenum TextureUnit);

    private:
        GLuint m_fbo;
        GLuint m_shadowMap;
};
在OpenGL中3d管线输出的结果称为‘帧缓冲对象‘（简称FBO）。FBO可以挂载颜色缓冲（在屏幕上显示）、深度缓冲区和一些有其他用处的缓冲区。当glutInitDisplayMode()被调用的时候，它使用一些特定的参数来创建默认的帧缓存，这个帧缓存被窗口系统所管理，不会被OpenGL删除。除了默认的帧缓存，应用程序可以创建自己的FBOs。在应用程序的控制下，这些对象可以被操作以用于不同的技术当中。ShadowMapFBO类为FBO提供一个容易操作的接口，会被FBO用来实现阴影图技术。ShadowMapFBO类内部有两个OpenGL句柄，其中‘m_fbo’句柄代表真正的FBO，FBO封装了帧缓存所有的状态，一旦这个对象被创建并设置合适的参数，我们就可以简单的通过绑定不同的对象来改变帧缓存。注意只有默认的帧缓存才可以在屏幕上显示。应用程序创建的帧缓存只能用于”离屏渲染“，这个可以说是一个中间的渲染过程（比如我们的阴影图缓冲区），稍后可以用于屏幕上的“真实”渲染通道。
就其本身而言，帧缓存只是一个占位符，为了使它变得可用，我们需要把纹理依附于一个或者更多的可用的挂载点，纹理含有帧缓存实际的内存空间。OpenGL定义了下面的一些附着点:

COLOR_ATTACHMENTi:附着到这里的纹理将接收来自片元着色器的颜色。‘i’ 后缀意味着可以有多个纹理同时被附着为颜色附着点。在片元着色器中有一个机制可以确保同时渲染多个颜色到缓冲区。
DEPTH_ATTACHMENT:附着在上面的纹理将收到深度测试的结果。
STENCIL_ATTACHMENT:附着在上面的纹理将充当模板缓冲区。模板缓冲区限制了光栅化的区域，可被用于不同的技术。
DEPTH_STENCIL_ATTACHMENT:这仅是一个深度和模板缓冲区的结合，因为它俩经常被一起使用。

对于阴影映射技术，我们只需要一个深度缓冲。成员属性“m_shadowmap“是附加到DEPTH_ATTACHMENT附着点的纹理句柄。ShadowMapFBO也提供了一些方法，主要用在渲染功能上。在开始第二次渲染的时候，我们要在渲染到阴影图和BindForReading()之前调用BindForWriting()。
(shadow_map_fbo.cpp:43)
glGenFramebuffers(1, &m_fbo);
这里我们创建FBO。和纹理与缓冲区这些对象的创建方式一样，我们指定一个GLuints数组的地址和它的大小，这个数组被句柄填充。
(shadow_map_fbo.cpp:46)
glGenTextures(1, &m_shadowMap);
glBindTexture(GL_TEXTURE_2D, m_shadowMap);
glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, WindowWidth, WindowHeight, 0, GL_DEPTH_COMPONENT, GL_FLOAT, NULL);
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
接下来我们创建纹理来作为阴影图。在一般情况下，这是一个标准的有特定配置的2D纹理，使其用于达到以下目的：

纹理的内部格式是 GL_DEPTH_COMPONENT 。和之前不同，之前我们通常将纹理的内部格式设置为与颜色有关的类型如（GL_RGB），这里我们将其设置为 GL_DEPTH_COMPONENT，意味着纹理中的每个纹素都存放着一个单精度浮点数用于存放已经标准化后的深度值。
glTexImage2D的最后一个参数是空，意味着我们不提供任何用于初始化buffer的数据，因为我们想让buffer包含每一帧的深度值并且每一帧的深度值都可能会变化。无论我们何时开始一个新的帧，我们都要用glClear()清除buffer。这些是我们在初始化过程中要做的。
我们告诉OpenGL如果纹理坐标越界，需要将其截断到[0，1]之间。当以相机为视口的投影窗口超过以光源为视口的投影窗口时会发生纹理坐标越界。为了避免不好的现象比如由于wraparound的原因阴影在别的地方重复出现，我们要截断纹理坐标。 
(shadow_map_fbo.cpp:54)

glBindFramebuffer(GL_FRAMEBUFFER, m_fbo);
我们已经生成FBO纹理对象，并为阴影图配置了纹理对象，现在我们需要把纹理对象附到FBO。我们要做的第一件事就是绑定FBO，之后所有对FBO的操作都会对它产生影响。这个函数的参数是FBO句柄和所需的target。target可以是GL_FRAMEBUFFER,GL_DRAW_FRAMEBUFFER或者GL_READ_FRAMEBUFFER。GL_READ_FRAMEBUFFE在我们想调用glReadPixels（本教程中不会使用）从FBO中读取内容时会用到；当我们想要把场景渲染进入FBO时需要使用GL_DRAW_FRAMEBUFFE；当我们使用GL_FRAMEBUFFER时，FBO的读写状态都会被更新，建议这样初始化FBO；当我们真正开始渲染的时候我们会使用GL_DRAW_FRAMEBUFFER。
(shadow_map_fbo.cpp:55) 
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, m_shadowMap, 0);
这里我们把shadow map纹理附着到FBO的深度附着点上。这个函数最后一个参数指明要用的Mipmap层级。Mipmap层是纹理贴图的一个特性，以不同分辨率展现一个纹理。0代表最大的分辨率，随着层级的增加，纹理的分辨率会越来越小。将Mipmap纹理和三线性滤波结合起来能产生更好的结果。这里我们只有一个mipmap层，所以我们使用0。我们让shadow map句柄作为第四个参数。如果这里我们使用0，那么当前的纹理(在上面的例子是深度）将从指定的附着点上脱落。
(shadow_map_fbo.cpp:58)
glDrawBuffer(GL_NONE);
glReadBuffer(GL_NONE);
因为我们没打算渲染到color buffer（只输出深度），我们通过上面的函数来禁止向颜色缓存中写入。默认情况下，颜色缓存会被绑定在GL_COLOR_ATTACHMENT0上，但是我们的FBO中甚至不会包含一个纹理缓冲区，所以，最好明确的告诉OpenGL我们的目的。这个函数可用的参数是GL_NONE和GL_COLOR_ATTACHMENT0到 GL_COLOR_ATTACHMENTm，‘m’是（GL_MAX_COLOR_ATTACHMENTS–1）。这些参数只对FBOs有效。如果用了默认的framebuffer，那么有效的参数是GL_NONE, GL_FRONT_LEFT,GL_FRONT_RIGHT,GL_BACK_LEFT和GL_BACK_RIGHT，这使你可以直接将场景渲染到front buffer或者back buffer（每一个都有左left和right buffer）。我们也将从缓存中的读取操作设置为GL_NONE（注意，我们不打算调用glReadPixel APIs中的任何一个函数）。这主要是为了避免因GPU只支持 opengl3.x而不支持4.x而出现问题。
(shadow_map_fbo.cpp:61)
GLenum Status = glCheckFramebufferStatus(GL_FRAMEBUFFER);

if (Status != GL_FRAMEBUFFER_COMPLETE) {
    printf("FB error, status: 0x%x\n", Status);
    return false;
}
当我们完成FBO的配置后，一定要确认其状态是否为OpenGL定义的“complete”，确保没有错误出现并且framebuffer现在是可用的了。上面就是检验这个的代码。 
(shadow_map_fbo.cpp:72)
void ShadowMapFBO::BindForWriting()
{
    glBindFramebuffer(GL_DRAW_FRAMEBUFFER, m_fbo);
}
在渲染过程中我们需要将渲染目标在shadow map和默认的framebuffer之间进行切换。在第二个渲染过程中，我们要绑定shadow map作为输入。这个函数和下一个函数将这个工作封装起来便于调用。上面的函数仅绑定FBO用于写入数据，在第一次渲染之前我们将调用它。
(shadow_map_fbo.cpp:78)
void ShadowMapFBO::BindForReading(GLenum TextureUnit)
{
    glActiveTexture(TextureUnit);
    glBindTexture(GL_TEXTURE_2D, m_shadowMap);
}
这个函数在第二次渲染之前被调用以绑定shadow map用于读取数据。注意我们是绑定纹理对象而不是FBO本身。这个函数的参数是纹理单元，并把shadow map绑定到这个纹理单元上。这个纹理单元的索引一定要和着色器同步（因为着色器有一个sampler2D一致变量用来访问这个纹理）。注意glActiveTexture的参数是纹理索引的枚举值（比如GL_TEXTURE0,GL_TEXTURE1等），着色器中的一致变量只需要索引值本身（如0，1等），这可能会导致很多bug出现。
(shadow_map.vs)
#version 330

layout (location = 0) in vec3 Position;
layout (location = 1) in vec2 TexCoord;
layout (location = 2) in vec3 Normal;

uniform mat4 gWVP;

out vec2 TexCoordOut;

void main()
{
    gl_Position = gWVP * vec4(Position, 1.0);
    TexCoordOut = TexCoord;
}
我们将在两次的渲染中都使用同一着色器程序。顶点着色器在两次渲染过程中都用得到，而片元着色器将只在第二次渲染过程中被使用。因为我们在第一次渲染过程中禁止把数据写入颜色缓存，所以就没用到片元着色器。上面的顶点着色器是十分简单的，它仅仅是通过WVP矩阵将位置坐标变换到裁剪坐标系中，并将纹理坐标传递到片元着色器中。在第一次的渲染过程中，纹理坐标是多余的（因为没有片元着色器）。然而，这没有实际的影响。可以看出，从着色器角度来看，无论这是一个渲染深度的过程还是一个真正的渲染过程都没有什么不同，而真正不同的地方是应用程序在第一次渲染过程传递的是以光源为视口的WVP矩阵，而在第二次渲染过程传递的是以相机为视口的WVP矩阵。在第一次的渲染过程Z buffer将用最靠近光源位置的Z值所填充，在第二次渲染过程中，Z buffer将被最靠近相机位置的Z值所填充。在第二次渲染过程中我们需要使用片元着色器中的纹理坐标，因为我们将从shadow map（此时它是着色器的输入）中进行采样。
(shadow_map.fs)
#version 330

in vec2 TexCoordOut;
uniform sampler2D gShadowMap;

out vec4 FragColor;

void main()
{
    float Depth = texture(gShadowMap, TexCoordOut).x;
    Depth = 1.0 - (1.0 - Depth) * 25.0;
    FragColor = vec4(Depth);
}
这是在渲染过程中用来显示shadow map的片元着色器。2D纹理坐标用来从shadow map中进行采样。Shadow map纹理是以GL_DEPTH_COMPONENT类型为内部格式而创建的，意味着纹理中每一个纹素都是一个单精度的浮点型数据而不是一种颜色。这就是为什么在采样的过程中要使用’.x’。当我们显示深度缓存中的内容时，我们可能遇到的一个情况是渲染的结果不够清楚。所以，在我们从shadow map中采样获得深度值后，为使效果明显，我们放大当前点的距离到远边缘(此处Z为1)，然后再用1减去这个放大后值。我们将这个值作为片元的每个颜色通道的值，意味着我们将得到一些灰度的变化（远裁剪面处是白色，近裁剪面处是黑色）。
现在我们如何结合上面的这些代码片段来创建应用程序。
(tutorial23.cpp:106)
virtual void RenderSceneCB()
{
    m_pGameCamera->OnRender();
    m_scale += 0.05f;

    ShadowMapPass();
    RenderPass();

    glutSwapBuffers();
}
主渲染程序随着大部分的功能移到其他函数中变得更加简单了。我们先处理全局的东西，比如更新相机的位置和用来旋转对象的类成员。然后我们调用一个ShadowMapPass()函数将深度信息渲染到shadow map纹理中，接着用RenderPass()函数来显示这个纹理。最后调用glutSwapBuffer()来将最终结果显示到屏幕上。 
(tutorial23.cpp:117)
virtual void ShadowMapPass()
{
    m_shadowMapFBO.BindForWriting();

    glClear(GL_DEPTH_BUFFER_BIT);

    Pipeline p;
    p.Scale(0.1f, 0.1f, 0.1f);
    p.Rotate(0.0f, m_scale, 0.0f);
    p.WorldPos(0.0f, 0.0f, 5.0f);
    p.SetCamera(m_spotLight.Position, m_spotLight.Direction, Vector3f(0.0f, 1.0f, 0.0f));
    p.SetPerspectiveProj(20.0f, WINDOW_WIDTH, WINDOW_HEIGHT, 1.0f, 50.0f);
    m_pShadowMapTech->SetWVP(p.GetWVPTrans());

    m_pMesh->Render();

    glBindFramebuffer(GL_FRAMEBUFFER, 0);
}
在渲染Shadow map之前我们先绑定FBO。从现在起，所有的深度值将被渲染到shadow map中，同时舍弃颜色的写入过程。我们只在渲染开始之前清除深度缓冲区，之后我们为了渲染mesh（例子为一个坦克）初始化了一个pipeline类对象。这里值得注意的一点是相机相关设置是基于聚光灯的位置和方向的。我们先渲染mesh，然后通过绑定FBO为0来切换回默认的framebuffer。
(tutorial23.cpp:135)
virtual void RenderPass()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    m_pShadowMapTech->SetTextureUnit(0);
    m_shadowMapFBO.BindForReading(GL_TEXTURE0);

    Pipeline p;
    p.Scale(5.0f, 5.0f, 5.0f);
    p.WorldPos(0.0f, 0.0f, 10.0f);
    p.SetCamera(m_pGameCamera->GetPos(), m_pGameCamera->GetTarget(), m_pGameCamera->GetUp());
    p.SetPerspectiveProj(30.0f, WINDOW_WIDTH, WINDOW_HEIGHT, 1.0f, 50.0f);
    m_pShadowMapTech->SetWVP(p.GetWVPTrans());
    m_pQuad->Render();
}
在第二个渲染过程开始前，我们先清除颜色和深度缓存，这些缓冲区属于默认的帧缓存。我们告诉着色器使用纹理单元0，并绑定阴影图用来读取其中的数据。从这里开始处理就都和以前一样了。我们放大四边形，把它直接放在相机的前面并渲染它。在光栅化期间进行采样阴影图并将其显示到模型上。
注意：在这个教程的代码中，当网格文件没有指定一个纹理时，我们不再自动加载一个白色的纹理，因为现在可以绑定阴影图来代替。如果网格不包含纹理我们就什么都不绑定，而是调用代码让其绑定自己的纹理。 


