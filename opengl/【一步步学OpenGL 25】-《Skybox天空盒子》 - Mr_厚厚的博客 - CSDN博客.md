# 教程 25 Skybox天空盒子

原文： http://ogldev.atspace.co.uk/www/tutorial25/tutorial25.html

CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

## 背景
天空盒子是一种让场景看上去更广阔无垠的一种视觉技术，用无缝对接的封闭纹理将摄像机的视口360度无死角的包裹起来。封闭纹理通常是天空纹理和地形纹理(山脉、高楼大厦等)组合而成，当玩家在周围环境中探索的时候，视角中除了真实模型的其他空余部分被封闭纹理所完全填充充当背景。下面是一张‘半条命’游戏中天空盒子的示例图：

天空盒子的一种实现方法是渲染一个巨大的正六面体封闭盒子纹理，并将相机置于中心，当摄像机移动的时候封闭纹理也跟着移动，所以看上去永远走不到场景中的视平线边缘，就跟我们现实中慢慢行走却永远走不到地平线边缘类似的效果。另外天空和大地拼接在一起的纹理还和一个生活经验吻合：就是我们说天空在遥远的地平线处看上去接触到了大地，但是往前走地平线还在那个遥远的地方永远也过不去。正六面体天空盒子是一种典型的天空盒子纹理，它是用六张边缘无缝对接的正方形纹理拼接而成的，观察者在内部看上去是一个连续的背景，例如下面的纹理：
 
将上面纹理之间的白色边缘去掉并将六张纸片折叠拼成盒子就可以得到一个符合上面要求的天空盒子了。OpenGL中这种纹理叫做立方体贴图(Cubemap)。为了从立方体贴图中采样，我们要采用3d纹理坐标而不是我们之前用的2d纹理坐标了。纹理采样器将3d纹理坐标看做一个向量，找出该文素位于立方体的哪一个面上并从那个面上取出需要的文素。这个过程可以从下面的图片中看到（从上往下看盒子）：

最合理的面的选择是基于纹理坐标中的那个最大分量的。在上面的例子中，我们可以看到Z分量是最大的(由于是从上往下看导致Y分量我们看不到，就先假设Y分量比Z分量小)。另外上面Z分量是正向的，因此采样器会从标记为‘PosZ’的面获取文素(其他的五个面还有’NegZ’,’PosX’,’NegX’,’PosY’和’NegY’)。

天空盒子技术除了用上面的立方体实现，还可以用球面来实现。主要区别是在球面上所有文素的方向向量长度都是相等的，因为都是半径，但在立方体中就不一样了。不过他们从面上取文素的机制是一样的。球面实现的天空空盒子叫做穹顶(skydome)，这也是这篇教程中demo里采用的天空盒子，当然你应该两种方法都尝试看哪个效果更好。

## 源代码详解

```
(ogldev_cubemap_texture.h:28)
class CubemapTexture
{
public:

    CubemapTexture(const string& Directory,
        const string& PosXFilename,
        const string& NegXFilename,
        const string& PosYFilename,
        const string& NegYFilename,
        const string& PosZFilename,
        const string& NegZFilename);

    ~CubemapTexture();

    bool Load();

    void Bind(GLenum TextureUnit);

private:

    string m_fileNames[6];
    GLuint m_textureObj;
};
```
这个类封装了OpenGL中CubeMap纹理的实现并提供了两个简单的接口函数用于加载和使用该纹理。这个类的构造函数的参数包括纹理的文件目录和cubemap六个面的图片的文件名。简单起见，我们假设所有的图片文件都在同一个文件目录下，程序启动的时候我们要调用一次Load()函数来加载图像文件并创建OpenGL纹理对象。类有两个属性变量，一个是保存六张图片绝对路径的m_fileNames，另一个是OpenGL纹理对象句柄，这个句柄可以让我们访问cubemap所有的六个面。在运行时必须要使用合适的纹理单元调用Bind()函数来使shader着色器能够得到cubemap。

```
(cubemap_texture.cpp:60)
bool CubemapTexture::Load()
{
    glGenTextures(1, &m_textureObj);
    glBindTexture(GL_TEXTURE_CUBE_MAP, m_textureObj);

    Magick::Image* pImage = NULL;
    Magick::Blob blob;

    for (unsigned int i = 0 ; i < ARRAY_SIZE_IN_ELEMENTS(types) ; i++) {
        pImage = new Magick::Image(m_fileNames[i]);

        try { 
            pImage->write(&blob, "RGBA");
        }
        catch (Magick::Error& Error) {
            cout << "Error loading texture '" << m_fileNames[i] << "': " << Error.what() << endl;
            delete pImage;
            return false;
        }

        glTexImage2D(types[i], 0, GL_RGB, pImage->columns(), pImage->rows(), 0, GL_RGBA,
            GL_UNSIGNED_BYTE, blob.data());
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE);

        delete pImage;
    } 

    return true;
}
```
这个函数开始先创建一个纹理对象来加载cubemap纹理，这个对象绑定到了一个特殊的GL_TEXTURE_CUBE_MAP目标对象上。之后我们通过循环来遍历cubemap的六个面枚举(GL_TEXTURE_CUBE_MAP_POSITIVE_X, GL_TEXTURE_CUBE_MAP_NEGATIVE_X等等)，六个枚举变量对应于m_fileNames的六个文件路径属性字符串。遍历过程中，通过ImageMagick框架依次加载六个图片文件，然后通过glTexImage2D()函数将资源数据传给OpenGL，注意每一次调用这个函数都要使用对应面的合适的GL枚举类型，因此枚举类型和文件路径数组m_fileNames必须是一一对应的。cubemap加载解析结束后，我们还需要做一些参数配置。除了GL_TEXTURE_WRAP_R其他的参数我们应该都很熟悉了，这个枚举参数指的就是纹理坐标的第三维，和其他维度的设置方法一样。

```
(cubemap_texture.cpp:95)
void CubemapTexture::Bind(GLenum TextureUnit)
{
    glActiveTexture(TextureUnit);
    glBindTexture(GL_TEXTURE_CUBE_MAP, m_textureObj);
}
```
在纹理用于绘制天空盒子之前这个函数必须要先调用，函数绑定的目标是GL_TEXTURE_CUBE_MAP，和我们在Load()函数中用的是同一个。

```
(skybox_technique.h:25)
class SkyboxTechnique : public Technique {
public:

    SkyboxTechnique();

    virtual bool Init();

    void SetWVP(const Matrix4f& WVP);
    void SetTextureUnit(unsigned int TextureUnit);

private:

    GLuint m_WVPLocation;
    GLuint m_textureLocation;
};
```
天空盒子是使用它自己的着色器函数来渲染的，函数调用只需要定义两个属性变量：一个将天空盒子纹理变换投影到屏幕的WVP矩阵和对应的纹理单元。看下面的内部结构：

```
(skybox.vs)
#version 330

layout (location = 0) in vec3 Position;

uniform mat4 gWVP;

out vec3 TexCoord0;

void main()
{
    vec4 WVP_Pos = gWVP * vec4(Position, 1.0);
    gl_Position = WVP_Pos.xyww;
    TexCoord0 = Position;
}
```
这个是天空盒子的顶点着色器代码，看上去很简单，但是一定要注意其中的技巧。第一个技巧是，虽然我们仍然是将输入的位置向量使用WVP矩阵进行变换，但是传给片段着色器的位置向量中的Z分量我们改成了W分量，这样会有什么结果呢？顶点着色器之后，光栅器将获得gl_Position向量，并进行透视分割以完成投影变换(将各分量除以W分量)。我们将Z分量设置成W分量的值可以保证透视分割后位置向量最终的Z分量值为1.0。Z分量为1意味着永远处于Z轴最远处，在深度测试中相对于其他物体模型天空盒子将永远处于劣势，因此天空盒子就总是作为其他物体的背景了，而其他物体会一直渲染在背景前面，这也是我们想要的效果。

第二个技巧是我们使用天空盒子自身坐标系中顶点的原始坐标来作为3D纹理坐标。为什么这样合理呢？因为对cubemap纹理采样时是从中心发射一个向量到立方体盒子或者球面上的，因此盒子表面上点的坐标恰好就是纹理坐标。顶点着色器将物体自身坐标系中的顶点坐标作为纹理坐标创给片段着色器(立方体是有8个顶点的，球体会有更多)，然后光栅器会在顶点之间差值得到每个像素的位置，从而就可以利用每个像素的位置进行采样了。

```
(skybox.fs)
#version 330

in vec3 TexCoord0;

out vec4 FragColor;

uniform samplerCube gCubemapTexture;

void main()
{
    FragColor = texture(gCubemapTexture, TexCoord0);
}
```
片段着色器就极其简单了，唯一值得一提的是我们这里是要使用’samplerCube’而不是’sampler2D’以获取cubemap的纹理。

```
(skybox.h:27)
class SkyBox
{
public:
    SkyBox(const Camera* pCamera, const PersProjInfo& p);

    ~SkyBox();

    bool Init(const string& Directory,
        const string& PosXFilename,
        const string& NegXFilename,
        const string& PosYFilename,
        const string& NegYFilename,
        const string& PosZFilename,
        const string& NegZFilename);

    void Render();

private: 
    SkyboxTechnique* m_pSkyboxTechnique;
    const Camera* m_pCamera;
    CubemapTexture* m_pCubemapTex;
    Mesh* m_pMesh;
    PersProjInfo m_persProjInfo;
};
```
渲染天空盒子的过程中需要几个组件：一个着色器对象、一个cubemap纹理和一个立方体或者气体模型。为了简化使用，同一个盒子内的所有组件都封装在一个类中。在程序启动时就马上使用文件目录和cubemap纹理的文件名来进行天空盒子的初始化，然后会在运行时通过调用Render()函数来渲染天空盒子。单纯一个函数的调用就起到很多方面的作用，注意除了上面的组件，这个类还可以访问相机对象和透视变换的信息(FOV，Z以及屏幕尺寸)，这也是为什么它能够合理的封装管线类。

```
void SkyBox::Render()
{
    m_pSkyboxTechnique->Enable();

    GLint OldCullFaceMode;
    glGetIntegerv(GL_CULL_FACE_MODE, &OldCullFaceMode);
    GLint OldDepthFuncMode;
    glGetIntegerv(GL_DEPTH_FUNC, &OldDepthFuncMode);

    glCullFace(GL_FRONT);
    glDepthFunc(GL_LEQUAL);

    Pipeline p; 
    p.Scale(20.0f, 20.0f, 20.0f);
    p.Rotate(0.0f, 0.0f, 0.0f);
    p.WorldPos(m_pCamera->GetPos().x, m_pCamera->GetPos().y, m_pCamera->GetPos().z);
    p.SetCamera(m_pCamera->GetPos(), m_pCamera->GetTarget(), m_pCamera->GetUp());
    p.SetPerspectiveProj(m_persProjInfo);
    m_pSkyboxTechnique->SetWVP(p.GetWVPTrans());
    m_pCubemapTex->Bind(GL_TEXTURE0);
    m_pMesh->Render(); 

    glCullFace(OldCullFaceMode); 
    glDepthFunc(OldDepthFuncMode);
}
```
这个函数用来负责天空盒子的渲染。开始先要启动天空盒子着色器，然后是一个新的OpenGL接口函数：glGetIntegerv()，这个函数可以返回OpenGL的状态。第一个参数就是状态的枚举，第二个参数是一个整型数组的引用地址，数组用来接收返回的状态(这个例子中只要一个整数就够了)。事实上我们是可以使用类似Get* 这样的函数来获取不同值类型的状态的，像：glGetIntegerv(), glGetBooleanv(), glGetInteger64v(), glGetFloatv() and glGetDoublev()。这里使用glGetIntegerv()的原因是我们要刻意改变glut_backend.cpp中一些通用的状态值，应用于这里所有的教程中，而且我们想在不影响其他部分的代码的前提下那样做。一个办法就是取出现在的状态，然后进行想要的改变，并且最后要将原本的状态值还原，这样其他系统就不需要知道这些状态的改变了。

第一个要改变的是表面剔除模式。通常，我们会剔除掉背向相机看不到的三角形图元，而对于天空盒子来说，相机是置于盒子内部的，所以我们想看到盒子的正面(内部)而不是背面(外部)。问题是，对于用到的一般的球体模型，外部的三角形是作为正面而内部的三角形是背面(这个取决于定点排列的顺序)。我们要么改变模型，要么就用相反的OpenGL剔除模式。事实是更倾向于选择后者的，因此同一个球体可以保持一般化用于其他地方，因此就要告诉OpenGL剔除去正面的三角形了。

第二个要改变的是深度测试函数模式。默认的，我们是告诉OpenGL，输入的片元如果比存储的片元Z值小就认为赢得深度测试而被渲染，但是对于天空盒子，Z值总是最远的边界，如果深度测试函数模式设置为‘小于’，天空盒子会被裁剪掉，为了让盒子成为场景的一部分我们要将深度测试函数模式改为‘小于等于’。

这个函数要做的另一件事情是计算WVP矩阵。注意对于天空盒子来说，世界坐标系的中心位于相机处，从而保证相机始终在天空盒子中心。之后cubemap的纹理贴图绑定到纹理单元0号上(天空盒子着色器初始化时设置的也是0号纹理单元)，然后球面网格被渲染，最后原本的剔除模式和深度测试函数被还原。

有一个有趣的性能技巧是，将天空盒子的渲染放到所有其他模型最后。因为，我们知道天空盒子总是位于其他所有模型之后的，一些GPU会有优化机制使得在执行片段着色器之前就可以进行早期的深度测试，并丢弃那些测试失败的片元，这样对于提高天空盒子的渲染效率是很有用的，因为只需要对那些没被其他模型所覆盖的背景图元执行着色器即可。但是为了生效，我们必须获取封装了所有Z值的深度缓冲，那样当天空盒子要渲染时所有要用到的信息就都已经准备好了。 


