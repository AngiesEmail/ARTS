







教程 24
阴影图2

原文： http://ogldev.atspace.co.uk/www/tutorial24/tutorial24.html
CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

背景
在之前的教程中，我们学习了阴影图技术背后的基本原理，并学习了如何在纹理中渲染深度信息并通过从深度缓冲中采样将其显示在屏幕上。这个教程我们将利用这些技术将阴影本身显示在屏幕上制作我们真正想要的阴影效果。
我们已经知道阴影图是一个有两个pass通道的技术（二次渲染），第一个pass通道我们是从光源的角度来渲染场景。现在我们看在第一次pass渲染通道中Z分量的位置向量经历了哪些过程：

通常情况下顶点着色器中的顶点位置是定义在本地坐标系的；
顶点着色器将顶点位置从本地空间转换到裁剪空间并继续传往渲染管线（关于裁剪空间可在教程12中复习回顾）；
光栅化阶段光栅器会进行透视分割（位置向量除以它的W分量），将位置向量从裁剪空间转换到NDC空间。在NDC空间中所有最后显示到屏幕上的点的X,Y,Z分量都被转化到[-1,1]范围内，超出范围的部分都会被裁剪掉。
光栅器将位置向量的X和Y分量映射到帧缓冲空间中（例如：800x600, 1024x768等等），也就是将位置向量变换到屏幕空间中了。
光栅器在收到的屏幕空间坐标系下的三角形的三个顶点之间进行插值，从而为三角形中的每个点都创建一个自己的坐标，其中Z值（也在[-1,1]范围内）也是插值得到的因此每个像素都有它自己的深度信息。
由于第一轮渲染时颜色的写入被禁止，因此此时片元着色器无效，但深度测试依然会进行。为了让当前像素的深度值与缓存中的像素的深度值进行比较，我们可以使用像素的屏幕坐标来从深度缓存中获取像素的深度值。如果当前像素的深度值比缓存中的小，则更新缓存（如果颜色写入开启，则颜色缓存中的值也会被更新）。

通过上面的过程我们知道了从光源的角度深度值是如何计算和存储的，接下来在第二次渲染的过程中，我们要从相机的角度来进行场景渲染所以我们会得到不同的深度信息。不过两次得到的深度信息我们都是需要的：一个使得三角形图元能够按顺序能够正确绘制在屏幕上，另一个用来检查哪些片元位于阴影中哪些不在。实现阴影图的技巧就是在3D渲染管线中维护两个位置向量和两个WVP矩阵。其中一个WVP矩阵从光源的角度算出，而另一个从相机角度计算得到。顶点着色器还是正常接收一个局部坐标系下定义的位置向量，但它会输出两个向量：

gl_Position内置变量，它是经过相机的WVP矩阵变换之后的结果；
另一个是一个普通向量，它是经过光源WVP变换矩阵变换得到的。

gl_Position向量会经历上述的一系列处理过程（…变换到NDC空间中…等等），然后会用于常规的光栅化阶段。第二个普通向量只会被光栅化阶段的光栅器在三角形面上进行插值处理并为每一个片段着色器提供它自己的值。所以现在当我们从从光源的角度看时，对于每一个物理像素我们都有原三角形中同一个点的裁剪空间坐标与之对应。很可能某个物理像素从两个角度看是不同的，但它在三角形中的位置实际是一样的。最后要做的就是用那个裁剪空间坐标来从shadow map中取深度值了。之后我们就可以将阴影纹理中的深度值与位于裁剪坐标系中的深度值进行比较，如果存储的剪裁坐标的深度值比较小，那就意味着像素位于阴影中（因为另一个像素和该像素有相同的裁剪空间坐标但另一个的深度值更小）。
那如何从片段着色器中获取经过光源WVP矩阵在裁剪空间坐标系下变换后的深度信息呢？

由于片段着色器将接收到的裁剪空间下的坐标看做一个标准的顶点属性，光栅化程序不会对其进行透视分割（只有传到gl_position变量中的顶点才会自动执行透视分割）。但在shader中我们可以很方便的来手动实现这一功能，我们将这个向量除以其W分量就将其变换到NDC空间中了；
我们知道在NDC空间中，顶点的X，Y分量都位于[-1，1]范围内，在上面的第四步中光栅化程序将NDC空间中的坐标映射到屏幕空间中，并且用它们来存放深度信息。现在我们想要从中提取出深度信息，为此我们需要一个位于[0，1]范围内的纹理坐标。如果我们将范围在[-1，1]之间的NDC空间坐标线性的映射到[0，1]的范围中，那么就会得到一个纹理坐标，这个纹理坐标会映射到阴影纹理的同一位置。例如：在NDC空间中一个顶点的X坐标为0，现在纹理的宽度为800，那么位于NDC空间中的0需要被映射到纹理坐标空间中的0.5（因为0位于[-1，1]的中点）。纹理空间中的0.5被映射到纹理上面的400，而这同样是光栅器执行屏幕空间转换时需要对其进行计算的地方。
将X和Y坐标从NDC空间变换到纹理空间的方法如下：
u = 0.5 * X + 0.5
v = 0.5 * Y + 0.5

源代码详解
(lighting_technique.h:80)
class LightingTechnique : public Technique {
    public:
    ... 
        void SetLightWVP(const Matrix4f& LightWVP);
        void SetShadowMapTextureUnit(unsigned int TextureUnit);
    ...
    private:
        GLuint m_LightWVPLocation;
        GLuint m_shadowMapLocation;
...
这里LightingTechnique类需要两个新的属性变量。一个从光源视角计算得到的WVP矩阵，一个是用来存放阴影图的纹理单元。我们会继续使用纹理单元0来存放映射匹配到模型上的普通纹理，并且会用于纹理单元1以存放阴影纹理。
(lighting.vs)
#version 330

layout (location = 0) in vec3 Position;
layout (location = 1) in vec2 TexCoord;
layout (location = 2) in vec3 Normal;

uniform mat4 gWVP;
uniform mat4 gLightWVP;
uniform mat4 gWorld;

out vec4 LightSpacePos;
out vec2 TexCoord0;
out vec3 Normal0;
out vec3 WorldPos0;

void main()
{
    gl_Position = gWVP * vec4(Position, 1.0);
    LightSpacePos = gLightWVP * vec4(Position, 1.0);
    TexCoord0 = TexCoord;
    Normal0 = (gWorld * vec4(Normal, 0.0)).xyz;
    WorldPos0 = (gWorld * vec4(Position, 1.0)).xyz;
}
这里，LightingTechnique类的顶点着色器已经更新，添加了部分新的内容。我们又加入了一个WVP矩阵的一致变量，和一个作为输出的的4维向量，这个向量包含了经过光源WVP矩阵变换后位置的裁剪空间坐标。可以看到，顶点着色器中第一次渲染通道中的gWVP变量和这里的gLightWVP变量有着相同的矩阵，那里的gl_Position变量会得到和这里的LightSpacePos变量相同的结果值。 
但由于LightSpacePos只是个标准的向量，它不会像gl_Position那样自动被透视分割，我们要手动在下面的片段着色器中进行该操作。
(lighting.fs:58)
float CalcShadowFactor(vec4 LightSpacePos)
{
    vec3 ProjCoords = LightSpacePos.xyz / LightSpacePos.w;
    vec2 UVCoords;
    UVCoords.x = 0.5 * ProjCoords.x + 0.5;
    UVCoords.y = 0.5 * ProjCoords.y + 0.5;
    float z = 0.5 * ProjCoords.z + 0.5;
    float Depth = texture(gShadowMap, UVCoords).x;
    if (Depth < (z + 0.00001))
        return 0.5;
    else
        return 1.0;
}
这个函数是在片段着色器中用来计算像素的阴影参数的。阴影参数是光源方程中的一个新参数。 
我们这只是将光源方程计算的颜色结果值和这个阴影参数相乘，使定义在阴影中的像素亮度有所衰减。这个函数的参数是来自顶点着色器经过插值后的LightSpacePos向量。首先第一步是要进行透视变换(将XYZ分量除以W分量)，从而将向量转换到NDC空间。然后准备一个2D坐标向量作为纹理坐标，之后按照上面背景介绍中的公式将透视分割后的LightSpacePos向量从NDC空间转换到纹理坐标空间来初始化这个纹理坐标向量。纹理坐标是用来从阴影图中获取深度数据的，这个深度指的是场景中所有投影到这个像素上的点中最近的那个点的深度。我们将上面阴影图的深度值和当前像素的深度值进行比较，如果阴影图的深度值小，也就是阴影离相机近，那么就返回0.5作为阴影参数，反之就返回1.0表示没有阴影。另外，来自NDC空间的Z分量也要经历从(-1,1)范围到(0,1)范围的转换，因为我们在比较的时候必须得要在相同的空间内。注意这里我们实际在当前的像素深度上加了一个很小的校正值来避免处理浮点数造成的精度错误。
(lighting.fs:72)
vec4 CalcLightInternal(BaseLight Light, vec3 LightDirection, vec3 Normal, float ShadowFactor)
{
    ...
    return (AmbientColor + ShadowFactor * (DiffuseColor + SpecularColor));
}
光照计算的核心函数没有什么大的变化，调用者必须将阴影参数传进来并调整漫射光和镜面反射光的颜色值。环境光就不受阴影的影响了，因为根据定义环境光是无处不在的没有阴影这一说。
(lighting.fs:97)
vec4 CalcDirectionalLight(vec3 Normal)
{
    return CalcLightInternal(gDirectionalLight.Base, gDirectionalLight.Direction, Normal, 1.0);
}
我们的阴影图的实现目前只适应于聚光灯光源，为了计算光源的WVP矩阵我们既需要光源的位置，还要光源的方向，位置和方向是点光源或平行光所不都具有的。以后我们会将确实的部分再加上，现在对于平行光就简单设置阴影参数为1了。
(lighting.fs:102)
vec4 CalcPointLight(struct PointLight l, vec3 Normal, vec4 LightSpacePos)
{
    vec3 LightDirection = WorldPos0 - l.Position;
    float Distance = length(LightDirection);
    LightDirection = normalize(LightDirection);
    float ShadowFactor = CalcShadowFactor(LightSpacePos);

    vec4 Color = CalcLightInternal(l.Base, LightDirection, Normal, ShadowFactor);
    float Attenuation = l.Atten.Constant +
        l.Atten.Linear * Distance +
        l.Atten.Exp * Distance * Distance;

    return Color / Attenuation;
}
聚光灯光源其实是在点光源的基础上计算出来的，这里这个函数接受了一个光源空间位置的一个新的参数LightSpacePos，并计算阴影参数，然后将其传给 CalcLightInternal()函数。
(lighting.fs:117)
vec4 CalcSpotLight(struct SpotLight l, vec3 Normal, vec4 LightSpacePos)
{
    vec3 LightToPixel = normalize(WorldPos0 - l.Base.Position);
    float SpotFactor = dot(LightToPixel, l.Direction);

    if (SpotFactor > l.Cutoff) {
        vec4 Color = CalcPointLight(l.Base, Normal, LightSpacePos);
        return Color * (1.0 - (1.0 - SpotFactor) * 1.0/(1.0 - l.Cutoff));
    }
    else {
        return vec4(0,0,0,0);
    }
}
这里聚光灯光源计算函数只是将光源空间位置LightSpacePos传给点光源计算函数。
(lighting.fs:131)
void main()
{
    vec3 Normal = normalize(Normal0);
    vec4 TotalLight = CalcDirectionalLight(Normal);

    for (int i = 0 ; i < gNumPointLights ; i++) {
        TotalLight += CalcPointLight(gPointLights[i], Normal, LightSpacePos);
    }

    for (int i = 0 ; i < gNumSpotLights ; i++) {
        TotalLight += CalcSpotLight(gSpotLights[i], Normal, LightSpacePos);
    }

    vec4 SampledColor = texture2D(gSampler, TexCoord0.xy);
    FragColor = SampledColor * TotalLight;
}
最后就是片段着色器的主函数了。对于聚光灯光源和点光源我们都传入了相同的光源空间位置向量LightSpacePos，虽然只有聚光灯光源会支持(因为传入的光源WVP矩阵都是以聚光灯光源计算的),这个限制之后我们会修正。lightingTechnique类中代码的改变已经介绍了，下面看应用代码。
(tutorial24.cpp:86)
m_pLightingEffect = new LightingTechnique();

if (!m_pLightingEffect->Init()) {
    printf("Error initializing the lighting technique\n");
    return false;
}

m_pLightingEffect->Enable();
m_pLightingEffect->SetSpotLights(1, &m_spotLight);
m_pLightingEffect->SetTextureUnit(0);
m_pLightingEffect->SetShadowMapTextureUnit(1);
这段创建lightingTechnique类对象的代码属于Init()函数的一部分，所以它只会在程序启动的时候执行一次，这里设置了一致变量来防止其随着帧的改变而变动。我们使用0号纹理单元作为标准纹理单元(模型原有的纹理)，另外阴影纹理存在1号纹理单元中。注意着色器程序必须要在一直变量创建之前开启，这些一致变量只要在程序没有重新连接前是一直保持不变的，这样会很方便因为可以灵活地在着色器程序之间切换，只需要关心那些动态的一致变量就好了，那些静态的一致变量在最开始初始化一次之后就不会再变了。
(tutorial24.cpp:129)
virtual void RenderSceneCB()
{
    m_pGameCamera->OnRender();
    m_scale += 0.05f;

    ShadowMapPass();
    RenderPass();

    glutSwapBuffers();
}
在住渲染函数内没有发生变化，开始先设置相机和旋转模型mesh的scale因子这些全局变量，然后分别执行阴影通道和渲染通道。
(tutorial24.cpp:141)
virtual void ShadowMapPass()
{
    m_shadowMapFBO.BindForWriting();

    glClear(GL_DEPTH_BUFFER_BIT);

    m_pShadowMapEffect->Enable();

    Pipeline p;
    p.Scale(0.1f, 0.1f, 0.1f);
    p.Rotate(0.0f, m_scale, 0.0f);
    p.WorldPos(0.0f, 0.0f, 3.0f);
    p.SetCamera(m_spotLight.Position, m_spotLight.Direction, Vector3f(0.0f, 1.0f, 0.0f));
    p.SetPerspectiveProj(30.0f, WINDOW_WIDTH, WINDOW_HEIGHT, 1.0f, 50.0f);
    m_pShadowMapEffect->SetWVP(p.GetWVPTrans());
    m_pMesh->Render();

    glBindFramebuffer(GL_FRAMEBUFFER, 0);
}
这个基本上和之前教程的阴影通道相同，唯一的变化是每次渲染之前都要开启阴影图，因为我们要在这个阴影计算和光照计算两个着色器程序之间之间进行切换。需要注意的一点是：虽然我们场景中既有一个mesh网格模型又有作为地面的矩形模型，但只有mesh网格模型会渲染到阴影纹理中，因为地面是不会投出阴影的，所以这里根据模型的类型也可以对模型渲染进行一些优化。
(tutorial24.cpp:168)
virtual void RenderPass()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    m_pLightingEffect->Enable();

    m_pLightingEffect->SetEyeWorldPos(m_pGameCamera->GetPos()); 
    m_shadowMapFBO.BindForReading(GL_TEXTURE1);

    Pipeline p;
    p.SetPerspectiveProj(30.0f, WINDOW_WIDTH, WINDOW_HEIGHT, 1.0f, 50.0f);

    p.Scale(10.0f, 10.0f, 10.0f);
    p.WorldPos(0.0f, 0.0f, 1.0f);
    p.Rotate(90.0f, 0.0f, 0.0f);
    p.SetCamera(m_pGameCamera->GetPos(), m_pGameCamera->GetTarget(), m_pGameCamera->GetUp());
    m_pLightingEffect->SetWVP(p.GetWVPTrans());
    m_pLightingEffect->SetWorldMatrix(p.GetWorldTrans());
    p.SetCamera(m_spotLight.Position, m_spotLight.Direction, Vector3f(0.0f, 1.0f, 0.0f));
    m_pLightingEffect->SetLightWVP(p.GetWVPTrans());
    m_pGroundTex->Bind(GL_TEXTURE0);
    m_pQuad->Render();

    p.Scale(0.1f, 0.1f, 0.1f);
    p.Rotate(0.0f, m_scale, 0.0f);
    p.WorldPos(0.0f, 0.0f, 3.0f);
    p.SetCamera(m_pGameCamera->GetPos(), m_pGameCamera->GetTarget(), m_pGameCamera->GetUp());
    m_pLightingEffect->SetWVP(p.GetWVPTrans());
    m_pLightingEffect->SetWorldMatrix(p.GetWorldTrans());
    p.SetCamera(m_spotLight.Position, m_spotLight.Direction, Vector3f(0.0f, 1.0f, 0.0f));
    m_pLightingEffect->SetLightWVP(p.GetWVPTrans());
    m_pMesh->Render();
}
一开始渲染通道和之前的一样，我们先清空深度缓冲和颜色缓冲，使用光照渲染着色器代替阴影图渲染着色器并绑定阴影图的FBO到纹理单元1号以供读取。然后我们渲染矩形作为地面，从而阴影可以投在地面上。地面稍微放大了一些，并绕X轴旋转90度调整好位置(地面原本是朝向相机的)。要注意WVP矩阵是如何随着相机的位置的不同而变化的，而对于光源WVP我们直接将相机置于光源位置就是固定的了。另外由于矩形地面模型本来是没有纹理的我们就手动为其绑定一个纹理贴图，mesh网格模型的渲染也是这样。 


