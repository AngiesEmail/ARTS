







教程18
漫射光

原文： http://ogldev.atspace.co.uk/www/tutorial16/tutorial18.html
CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

背景
漫射光和环境光的主要不同是漫射光的特性依赖光线的方向，而环境光完全忽略光的方向。当只有环境光时整个场景是被均匀照亮的，而漫射光使物体朝向它的那一面比其他背向光的面要更亮。漫射光还增加了一个光强度的变化现象，光的强度大小还取决于光线和物体表面的角度，这个概念可以在下图看出：

假想两边的光线的长度是一样的，唯一不同的是他们的方向。按照漫射光的模型，左边物体的表面要比右边的物体要亮，因为右边光线的入射角比左边的大很多。实际上左边的亮度是能达到的最大亮度了，因为它是垂直入射。
漫射光模型是建立在兰伯特余弦定律上的，光想的强度和观察者视线与物体表面法线夹角的余弦值成正比（夹角越大光强度越小）。注意这里略有变化，我么使用的是光线的方向而不是观察者视线（在镜面发射中用到）的方向。
为了计算光的强度我们要引入光线和物体表面法线（兰伯特定律中更加通用的概念叫做’directionaly proportional’）夹角的余弦值作为一个参数变量。看下面这幅图：

图中四条光线以不同的角度照到表面上（光线仅仅是方向不同），绿色的箭头是表面法向量，从表面垂直往外发出。光线A的强度是最大的，因为光线A和法线的夹角为0，余弦值为最大的1，也就是这个光线的强度（三个通道的三个0-1的值）和表面颜色相乘每个颜色通道都是乘以1，这是漫射光强度最大的情况了。光线B以一定角度（0-90之间）照射到表面，这个角度就是光线和法线的夹角，那么夹角的余弦值应该在0-1之间，表面颜色值最后要和这个角度的余弦值相乘，那么得到的光的强度一定是比光线A要弱的。
对于光线C和D情况又不同了。C从表面的一侧入射，光线和表面的夹角为0，和法线垂直，对应的余弦值为0，这会导致光线C对表面照亮没有任何效果。光线D从表面的背面入射和法线成钝角，余弦值为负比0还小甚至小到-1。所以光线D和C一样都对物体表面没有照亮作用。
通过上面的分析我们可以得到一个很重要的结论：光线如果要对物体表面的亮度产生影响，那么光线和法线的角度要在0-90度之间但不包含90度。
可以看到表面法线对漫射光的计算很重要。上面的例子是很简化的：表面是平坦的直线只需要考虑一条法线。而真实世界中的物体有无数的多边形组成，每个多边形的法线和附近的多边形基本都不一样。例如：

因为一个多边形面上分布的任意法向量都是一样的，足以用其中一个代表来计算顶点着色器中的漫射光。一个三角形上的三个顶点会有相同的颜色而且整个三角形面的颜色都相同，但这样看上去效果并不好，每个多边形之间的颜色值都不一样这样我们会看到多边形之间边界的颜色变化不平滑，因此这个明显是需要进行优化的。
优化的办法中使用到一个概念叫做‘顶点法线’。顶点法线是共用一个顶点的所有三角形法线的平均值。事实上我们并没有在顶点着色器中计算漫射光颜色，而只是将顶点法线作为一个成员属性传给片段着色器。光栅器会得到三个不同的法向量并对其之间进行插值运算。片段着色器将会对每个像素计算其特定的插值法向量对应的颜色值。这样使用那个插值后得到的每个像素特定法向量，我们对漫射光的计算可以达到像素级别。效果是光照效果在每个相邻三角形面之间会平滑的变化。这种技术叫做Phong着色（Phong Shading）。下面是顶点法线插值后的样子：

但是我们会发现之前教程用的那个金字塔模型使用上面这些插值后的法向量计算优化后看上去很奇怪，有点想还是用本来没插值的法向量。这里是因为金字塔面很少，在后面更复杂的模型中使用上面的插值优化方法模型就会看上去更加平滑真实。
最有一点要关心的是漫射光计算所在的坐标空间。顶点和他们的法线都定义在本地坐标系空间，并且都在顶点着色器中被我们提供给shader的WVP矩阵进行了变换，然后到裁剪空间。然而，在世界坐标系中来定义光线的方向才是最合理的，毕竟光线的方向决定于世界空间中某个地方的光源将光线投射到某个方向（甚至太阳都是在世界空间中，只是距离极远）。所以，在计算之前，我们首先要将法线向量变换到世界坐标系空间。
代码详解
(lighting_technique.h:25)
struct DirectionalLight
{
    Vector3f Color;
    float AmbientIntensity;
    Vector3f Direction;
    float DiffuseIntensity;
};
这是新的平行光的数据结构，有两个新的成员变量：方向是定义在世界空间的一个3维向量，漫射光光照强度是一个浮点数（和环境光的用法一样）。
(lighting.vs)
#version 330

layout (location = 0) in vec3 Position;
layout (location = 1) in vec2 TexCoord;
layout (location = 2) in vec3 Normal;

uniform mat4 gWVP;
uniform mat4 gWorld;

out vec2 TexCoord0;
out vec3 Normal0;

void main()
{
    gl_Position = gWVP * vec4(Position, 1.0);
    TexCoord0 = TexCoord;
    Normal0 = (gWorld * vec4(Normal, 0.0)).xyz;
}
这是更新了的顶点着色器，有一个新的顶点属性：法向量，这个法向量要由应用程序提供。另外世界变换有其自己的一致变量我们要和WVP变换矩阵一并提供。顶点着色器通过世界世界变换矩阵将法向量变换到世界空间并传递给片断着色器。注意这时候3维向量扩展成了4维向量，和4维世界变换矩阵相乘后又降回3维(…).xyz。GLSL的这种能力称作调配‘swizzling’，使向量操作非常灵活。比如，一个3维向量v(1,2,3)，那么vec4 n = v.zzyy中4维向量n的内容为：（3,3,2,2）。注意如果我们要扩展3维向量到4维我们必须将第四个分量设置为0，这会使世界变换矩阵的变换效果（第4列）失效，因为向量不能像点一样移动，之只能缩放和旋转。
(lighting.fs:1)
#version 330

in vec2 TexCoord0;
in vec3 Normal0;

out vec4 FragColor;

struct DirectionalLight
{
    vec3 Color;
    float AmbientIntensity;
    float DiffuseIntensity;
    vec3 Direction;
};
这里是片段着色器的开始，它现在接受到插值后并在顶点着色器中转换到世界空间的顶点法向量。平行光的数据结构也扩展了来和C++中的对应匹配并且包含了新的光属性。
(lighting.fs:19)
void main()
{
    vec4 AmbientColor = vec4(gDirectionalLight.Color * gDirectionalLight.AmbientIntensity, 1.0f);
    // 环境光颜色参数的计算没有变化，我们计算并存储它然后用在下面最终的公式中。

    float DiffuseFactor = dot(normalize(Normal0), -gDirectionalLight.Direction);
    // 这是漫射光计算的核心。我们通过对光源向量和法线向量做点积计算他们之间夹角的余弦值。这里有三个注意点：
    1. 从顶点着色器传来的法向量在使用之前是经过单位化了的，因为经过插值之后法线向量的长度可能会变化不再是单位向量了；
    2.光源的方向被反过来了，因为本来光线垂直照射到表上时的方向和法线向量实际是相反的成180度角，计算的时候将光源方向取反那么垂直入射时和法线夹角为0，这时才和我们的计算相符合。
    3.光源向量不是单位化的。如果对所有像素的同一个向量都进行反复单位化会很浪费GPU资源。因此我们只要保证应用程序传递的向量在draw call之前被单位化即可。

    vec4 DiffuseColor;
    if (DiffuseFactor > 0) {
        DiffuseColor = vec4(gDirectionalLight.Color * gDirectionalLight.DiffuseIntensity * DiffuseFactor, 1.0f);
    }
    else {
        DiffuseColor = vec4(0, 0, 0, 0);
    }

    // 这里我们根据光的颜色、漫射光强度和光的方向来计算漫射光的部分。如果漫射参数是负的或者为0意味着光线是以一个钝角射到物体表面的（从水平一侧或者表面的背面）,这时候光照是没有效果的同时漫射光的颜色参数会被初始化设置为零。如果夹角大于0我们就可以进行计算漫射光的颜色值了，将基本的颜色值和漫射光强度常量相乘，最后使用漫射参数DiffuseFactor对最后结果进行缩放。如果光是垂直入射那么漫射参数会是1，光的亮度最大。

    FragColor = texture2D(gSampler, TexCoord0.xy) * (AmbientColor + DiffuseColor);
}
这是最后的光照计算了。我们加入了环境光和漫射光的部分，并将结果和从纹理中取样得到的颜色相乘。现在可以看到即使漫射光方向太偏（照到反面或者从水平一侧）没有对表面起到照亮效果，环境光仍然能照亮物体，当然环境光也得要存在。
(lighting_technique.cpp:144)
void LightingTechnique::SetDirectionalLight(const DirectionalLight& Light)
{
    glUniform3f(m_dirLightLocation.Color, Light.Color.x, Light.Color.y, Light.Color.z);
    glUniform1f(m_dirLightLocation.AmbientIntensity, Light.AmbientIntensity);
    Vector3f Direction = Light.Direction;
    Direction.Normalize();
    glUniform3f(m_dirLightLocation.Direction, Direction.x, Direction.y, Direction.z);
    glUniform1f(m_dirLightLocation.DiffuseIntensity, Light.DiffuseIntensity);
}
这个函数将平行光的参数传递到着色器中，可以看到平行光的数据结构经过扩展后既包含了光的方向向量还包含了漫射光强度。注意方向向量在设置到shader着色器之前已经经过了单位化处理。同时LightingTechnique类也获取了光的方向和强度一致变量的的位置，也获得了世界变换矩阵的位置，另外还有一个设置世界变换矩阵的函数。这些目前都很常规没有放太多代码解释，具体的可以在源码里看。
tutorial18.cpp:35)
struct Vertex
{
    Vector3f m_pos;
    Vector2f m_tex;
    Vector3f m_normal;

    Vertex() {}

    Vertex(Vector3f pos, Vector2f tex)
    {
        m_pos = pos;
        m_tex = tex;
        m_normal = Vector3f(0.0f, 0.0f, 0.0f);
    }
};
这里最新的顶点的数据结构现在包含了法线向量，构造函数自动将其初始化为零，并且我们有一个专门的函数来遍历扫描所有的顶点并计算法向量。
(tutorial18.cpp:197)
void CalcNormals(const unsigned int* pIndices, unsigned int IndexCount, Vertex* pVertices, unsigned int VertexCount)
{
    for (unsigned int i = 0 ; i < IndexCount ; i += 3) {
        unsigned int Index0 = pIndices[i];
        unsigned int Index1 = pIndices[i + 1];
        unsigned int Index2 = pIndices[i + 2];
        Vector3f v1 = pVertices[Index1].m_pos - pVertices[Index0].m_pos;
        Vector3f v2 = pVertices[Index2].m_pos - pVertices[Index0].m_pos;
        Vector3f Normal = v1.Cross(v2);
        Normal.Normalize();

        pVertices[Index0].m_normal += Normal;
        pVertices[Index1].m_normal += Normal;
        pVertices[Index2].m_normal += Normal;
    }

    for (unsigned int i = 0 ; i < VertexCount ; i++) {
        pVertices[i].m_normal.Normalize();
    }
}
这个函数参数取得了顶点数组和索引数组，根据索引搜索取出每个三角形的三个顶点并计算其法向量。第一个循环中我们只累加计算三角形每个顶点的法向量。对于每个三角形法向量都是通过计算从第一个顶点出发到其他两个顶点的两条边向量的差积得到的。在向量累加之前要求先将其单位化，因为差积运算后的结果不一定是单位向量。第二个循环中，我们只遍历顶点数组（索引我们不关心了）并单位化每个顶点的法向量。这样操作等同于将累加的向量进行平均处理并留下一个为单位长度的顶点法线。这个函数在顶点缓冲器创建之前调用，在缓冲器中计算顶点法线，当然此时缓冲期中还会计算其他的一些顶点属性。
(tutorial18.cpp:131)
    const Matrix4f& WorldTransformation = p.GetWorldTrans();
    m_pEffect->SetWorldMatrix(WorldTransformation);
    ...
    glEnableVertexAttribArray(2);
    ...
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (const GLvoid*)20);
    ...
    glDisableVertexAttribArray(2);
这是渲染循环中的主要变化，管线类有一个新的函数来提供世界变换矩阵（另外还有WVP变换矩阵）。世界变换矩阵是在缩放变换、旋转变换和平移变换时计算的。我们可以启用或禁用第三个顶点属性数组并且可以定义每个顶点法向量在顶点缓冲器中的偏移值。这里偏移值为20，因为之前已经被位置向量占用了12bytes，纹理坐标占用了8bytes。
为了实现这个教程中的图片效果我们还要定义漫射光强度和光的方向，这个是在tutorial18类中的构造函数中完成的。漫射光强度设置为0.8，光的方向从左向右。环境光强度逐渐动态地衰弱到0来增强体现漫射光的效果。你可以使用键盘的z和x键来调整漫射光强度（之前教程中是使用a和s键来调整环境光强度的）。
数学理论提示
很多网上的资源说要使用世界变换矩阵逆矩阵的转置来变换法向量，虽然没错，但我们通常不需要考虑那么远。我们的世界矩阵总是正交的（他们的向量都正交）。由于正交矩阵的逆和正交矩阵的转置是相同的，那么正交矩阵逆的转置实际就是其转置的转置，所以还是本来的矩阵。只要我们避免让图形变形扭曲（不成比例的在各轴线上进行缩放）那么就不会有问题的。 


