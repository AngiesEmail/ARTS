







教程 26
法线贴图

原文： http://ogldev.atspace.co.uk/www/tutorial26/tutorial26.html
CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

背景
之前的我们的光线着色器类已经可以达到很不错的效果了，光线效果通过插值计算遍布到整个模型表面，使整个场景看上去比较真实，但这个效果还可以进行更好的优化。事实上，有时插值计算反而会影响场景的真实性，尤其是用材质来表现一些凹凸不平的纹理的时候，插值会让模型表面看上去太平坦了，例如下图的例子： 
 
左边的图片效果明显比右边的要好，左边的更好的表现了石头纹理的崎岖不平，而右边的则看上去太平滑。左图的效果是使用一种叫做法线贴图（又称凹凸贴图）的技术渲染的，这边教程的主题就是这种技术。
之前我们是在三角形的三个顶点法向量之间进行平滑插值来得到三角形上每个点的法向量，这样表面会比较光滑，而法线贴图的思想是直接从‘法线贴图’上进行采样得到对应的法线方向，这样更加接近现实，因为绝大多数物体表面（尤其是游戏中）并不是那样光滑的，而是按照凹凸表面各个位置的不同方向来反射照过来的光线，不会像我们插值计算的那样平滑一致。对于每一张纹理贴图，那些表面上的所有法向量都是可以被计算并且存储在我们所谓的法线贴图里的。在片段着色器阶段进行光照计算的时候，每个像素的特定法线也是根据纹理坐标采样来获取使用。下面的图片展示了法线贴图和常规贴图中法线的不同： 

现在我们有了我们的法线贴图，里面存储了真实的或者说至少是接近真实的表面法线。那我们可以简单的直接用它吗？不是的，考虑一下上面的带有砖块纹理的立方体，六个面贴有相同的纹理贴图，但是六张相同贴图的方向并不一样，所以对应的法向量在任意光线的照射下也应该是不一样的。如果我们直接使用同一张法线纹理，不做相应的修改，就会得到错误的结果，因为相同的法线应用到六个方向不同的表面上是不可能正确的！例如，上表面上的点的的法向量通常为（0，1，0），即使是非常凹凸不平的表面，对应底部表面上的点的法向量也都是（0，-1，0）。重点是法向量是在它们私有的坐标空间中定义的，因此必要进行变换，使它们可以在世界坐标空间中正确的参与光照计算。某种意义上说，这个概念和顶点法向量的变换方式类似，顶点法向量定义在物体本地坐标空间下，然后我们通过用世界矩阵变换把他们转换到世界空间。
首先这里要定义法线的本地坐标系，坐标系需要三个正交单位向量。由于法线是2D纹理的的一部分，而2D纹理有两个正交单位向量U和V，因此通常做法是将X分量对应到U轴，而Y分量对应到V轴。注意U是从左到右的，而V是从下往上的（那个坐标系的原点位于纹理的左下角）。Z分量则是垂直于纹理，垂直于X和Y轴的了。 

现在法向量就可以根据那个坐标系定义了，并存储在纹理的RGB文素中。注意即使是在非常凹凸不平的表面，我们仍然认为法线的方向是从纹理朝外的。例如：Z分量主导的一个分量，X和Y分量只能起到让其略微倾斜的作用。将XYZ向量存储在RGB文素中会使得法线纹理像下图那样偏蓝色： 
 
下面这几个是这张法线纹理顶行的五个文素值（从左到右）：(136,102,248), (144,122,255), (141,145,253), (102, 168, 244) 和 (34,130,216)。这里Z分量的主导性很明显。
接下来我们需要做的是检查模型中所有的三角面，并且按照每个顶点的纹理坐标匹配其在法线纹理上的坐标的方式，将法线纹理映射到每个三角面上。例如，如果给出的三角形的纹理坐标是(0.5,0), (1, 0.5) 和 (0,1)。那么法线纹理会按如下的方式放置： 
 
上图中左下角的坐标系代表了物体的本地坐标系。
除了纹理坐标，三个顶点还有代表他们位置的本地空间3d坐标。当我们将纹理贴图放到上面的三角形上面后，我们实际上是给贴图的UV坐标赋了本地空间下的对应的值。如果现在我们计算出在物体本地坐标空间UV的值（同时通过U和V的差积计算出对应的法向量），我们将可以得到一个将法向量从贴图变换到物体本地坐标空间的变换矩阵，那样就可以继而变换到世界坐标空间并且参与光照计算。通常U向量我们称之为Tangent，而V向量我们称之为Bitangent，其中我们需要推导的的变换矩阵称为TBN矩阵(Tangent-Bitangent-Normal)。这些TBN向量定义了一个叫做Tangent（或者说纹理）空间的坐标系。所以，法线纹理中的法向量是存储在Tangent/纹理空间中的。接下来我们将研究如何计算物体空间下U和V向量的值。
现在看图中一个更加一般化的三角形，三角形三个顶点位于位置P0，P1和P2，对应纹理坐标为(U0,V0), (U1,V1) and (U2,V2)： 

我们要找到物体本地空间下的向量T（表示tangent）和B（表示bitangent）。我们可以看到两个三角形边E1和E2可以写成T和B的线性组合： 

也可以写成下面的形式： 

现在可以很容易的转换成矩阵公式的形式： 

现在想把矩阵转换到等式的右边，为此可以两边乘以上面标红的矩阵的逆矩阵： 

计算如下: 

算出逆矩阵的值得到： 

我们可以对网格中的每一个三角形执行上述过程，并且为每个三角形都计算出tangent向量和bitangent向量（对三角形的三个顶点来说这两个向量都是一样的）。通常的做法是为每一个顶点都保存一个tangent/bitangent值，每个顶点的tangent/bitangent值由共享这个顶点的所有三角面的平均tangent/bitangent值确定（这与顶点法线是一样的）。这样做的原因是使整个三角面的效果比较平滑，防止相邻三角面之间的不平滑过渡。这个坐标系空间的第三个分量——法线分量，是tangent和bitangent的叉乘积。这样Tangent-Bitangent-Normal三个向量就能作为纹理坐标空间的基向量，并且实现将法线由法线纹理空间到模型局部空间的转换。接下来需要做的就是将法线变换到世界坐标系之下，并使之参与光照计算。不过我们可以对此进行一点优化，即将Tangent-Bitangent-Normal坐标系变换到世界坐标系下来，这样我们就能直接将纹理中的法线变换到世界坐标系中去。
在这一节中我们需要做下面几件事：

将tangent向量传入到顶点着色器中；
将tangent向量变换到世界坐标系中并传入到片元着色器；
在片元着色器中使用tangent向量和法线向量（都处于世界坐标系下）来计算出bitangent向量；
通过tangent-bitangent-normal矩阵生成一个将法线信息变换到世界坐标系中的变换矩阵；
从法线纹理中采样得到法线信息；
通过使用上述的矩阵将法线信息变换到世界坐标系中；
继续和往常一样进行光照计算。

在我们的代码中有一点需要格外强调，在像素层次上，我们的tangent-bitangent-normal实际上并不是真正的正交基（三个单位向量互相垂直）。造成这种情况的原因有两个：首先对于每个顶点的tangent向量和法线向量，我们是通过对共享此顶点的所有三角面求平均值得到的；其次我们在像素层面看到的tangent向量和法线向量是经过光栅器插值得到的结果。这使得我们的tangent-bitangnet-normal矩阵丧失了他们的“正交特性”。但是为了将法线信息从纹理坐标系变换到世界坐标系我们需要一个正交基。解决方案是使用Gram-Schmidt进行处理。这个方案能够将一组基向量转换成正交基。这个方案大致如下：从基向量中选取向量 ‘A’ 并对其规范化，之后选取基向量中的向量 ‘B’ 并将其分解成两个分向量（两个分向量的和为‘B’），其中一个分向量沿着向量‘A’的方向，另一个分量则垂直于‘A’向量。现在用这个垂直于‘A’向量的分量替换‘B’向量并且对其规范化。按照这样的方法对所有基向量进行处理。
这样的最终结果是，虽然我们并没有使用数学上正确的TBN向量，但我们实现了必要的平滑效果，避免三角形边界上的明显间隔。
源代码详解
(mesh.h:33)
struct Vertex
{
    Vector3f m_pos;
    Vector2f m_tex;
    Vector3f m_normal;
    Vector3f m_tangent;

    Vertex() {}

    Vertex( const Vector3f& pos, 
            const Vector2f& tex, 
            const Vector3f& normal, 
            const Vector3f& Tangent )
    {
        m_pos = pos;
        m_tex = tex;
        m_normal = normal;
        m_tangent = Tangent;
    }
};
这是我们新的的顶点结构体，增加了一个tangent向量。至于bitangent向量我们会在片元着色器中进行计算。需要注意的是切线空间的法线与普通的三角形法线是一样的（因为纹理与三角是平行的）。因此虽然顶点法线位于两个不同的坐标系之中但是他们实际上是一样的。
for (unsigned int i = 0 ; i < Indices.size() ; i += 3) {
    Vertex& v0 = Vertices[Indices[i]];
    Vertex& v1 = Vertices[Indices[i+1]];
    Vertex& v2 = Vertices[Indices[i+2]];

    Vector3f Edge1 = v1.m_pos - v0.m_pos;
    Vector3f Edge2 = v2.m_pos - v0.m_pos;

    float DeltaU1 = v1.m_tex.x - v0.m_tex.x;
    float DeltaV1 = v1.m_tex.y - v0.m_tex.y;
    float DeltaU2 = v2.m_tex.x - v0.m_tex.x;
    float DeltaV2 = v2.m_tex.y - v0.m_tex.y;

    float f = 1.0f / (DeltaU1 * DeltaV2 - DeltaU2 * DeltaV1);

    Vector3f Tangent, Bitangent;

    Tangent.x = f * (DeltaV2 * Edge1.x - DeltaV1 * Edge2.x);
    Tangent.y = f * (DeltaV2 * Edge1.y - DeltaV1 * Edge2.y);
    Tangent.z = f * (DeltaV2 * Edge1.z - DeltaV1 * Edge2.z);

    Bitangent.x = f * (-DeltaU2 * Edge1.x - DeltaU1 * Edge2.x);
    Bitangent.y = f * (-DeltaU2 * Edge1.y - DeltaU1 * Edge2.y);
    Bitangent.z = f * (-DeltaU2 * Edge1.z - DeltaU1 * Edge2.z);

    v0.m_tangent += Tangent;
    v1.m_tangent += Tangent;
    v2.m_tangent += Tangent;
}

for (unsigned int i = 0 ; i < Vertices.size() ; i++) {
    Vertices[i].m_tangent.Normalize();
}
这部分代码是计算tangent向量的算法的实现（在“背景”中所描述的算法）。它遍历索引数组，并通过索引在顶点数组中获取组成三角面的顶点向量。为了表示三角面的两条边，我们用第二个顶点和第三个顶点分别减去第一个顶点。同样的，我们对纹理坐标也进行相似的处理来获得VU向量，并计算两条边沿着U轴和V轴的增量。‘f’为一个因子，他是“背景”中得到的最后一个等式的等号右边出现的那个因子。一旦求得了‘f’，那么用这两个矩阵的结果乘上它即可分别得到在模型局部坐标系之下tangent和bitangent向量的表示。需要注意的是这里对 bitangent向量的计算只是为了整个算法的完整性，我们真正需要的是被存放到顶点数组中的tangent向量。最后一件事就是遍历顶点数组对tangent向量进行规范化。
现在我们应该已经完全理解了这个算法的理论和实现，但是本章中不会使用这段代码。Open Asset Import库已经为我们实现了这一功能，使我们能够很方便的得到tangent向量（无论如何了解它的实现是非常重要的，也许有一天你需要自己来实现它）。我们只需要在导入模型的时候定义一个tangent变量，之后我们便可以访问aiMesh类中的‘mTangents’数组，并从这里获取tangent向量。详细实现可以参看源码。
(mesh.cpp:195)
void Mesh::Render()
{
    ...
    glEnableVertexAttribArray(3);

    for (unsigned int i = 0 ; i < m_Entries.size() ; i++) {
        ...
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (const GLvoid*)32);
    }
    ...
    glDisableVertexAttribArray(3);
}
由于顶点结构体经过了扩充，我们需要对Mesh类的渲染函数进行一些改动。这里我们启用了第四个顶点属性并且指定tangent属性的位置在距顶点开始32字节位置处（位于法线之后）。在函数最后第四个顶点属性被禁用。
(lighting.vs)
layout (location = 0) in vec3 Position;
layout (location = 1) in vec2 TexCoord;
layout (location = 2) in vec3 Normal;
layout (location = 3) in vec3 Tangent;

uniform mat4 gWVP;
uniform mat4 gLightWVP;
uniform mat4 gWorld;

out vec4 LightSpacePos;
out vec2 TexCoord0;
out vec3 Normal0;
out vec3 WorldPos0;
out vec3 Tangent0;

void main()
{
    gl_Position = gWVP * vec4(Position, 1.0);
    LightSpacePos = gLightWVP * vec4(Position, 1.0);
    TexCoord0 = TexCoord;
    Normal0 = (gWorld * vec4(Normal, 0.0)).xyz;
    Tangent0 = (gWorld * vec4(Tangent, 0.0)).xyz;
    WorldPos0 = (gWorld * vec4(Position, 1.0)).xyz;
}
这是经过修改之后的顶点着色器，没有什么大的修改，因为大部分改动都在片元着色器中。新增部分只有tangent向量传入，之后将其变换到世界坐标系中并输出到片元着色器中。
(lighting.fs:132)
vec3 CalcBumpedNormal()
{
    vec3 Normal = normalize(Normal0);
    vec3 Tangent = normalize(Tangent0);
    Tangent = normalize(Tangent - dot(Tangent, Normal) * Normal);
    vec3 Bitangent = cross(Tangent, Normal);
    vec3 BumpMapNormal = texture(gNormalMap, TexCoord0).xyz;
    BumpMapNormal = 2.0 * BumpMapNormal - vec3(1.0, 1.0, 1.0);
    vec3 NewNormal;
    mat3 TBN = mat3(Tangent, Bitangent, Normal);
    NewNormal = TBN * BumpMapNormal;
    NewNormal = normalize(NewNormal);
    return NewNormal;
}

void main()
{
    vec3 Normal = CalcBumpedNormal();
    ...
上面这段代码包含了片元着色器中的大部分改动，所有对法线的操作都被封装在CalcBumpedNormal()函数中。首先我们先对法线向量和 tangent向量进行规范化，第三行中的代码就是Gram-Schmidt处理的实现。dot(Tangent, Normal)求出了tangent向量投影到法线向量上的长度，将这个结果乘上法线向量即可得到tangent向量在沿着法线向量方向上的分量。之后我们用tangent向量减去它在法线方向上的分量即可得到其垂直于法线方向上的分量。这就是我们新的tangent向量（要记住对其进行规范化）。新的tangent向量和法线向量之间是我叉乘结果就是bitangent向量。之后我们从法线纹理中采样得到此片元的法线信息（位于切线/纹理空间）。‘gNormalMap’是一个新增加的sampler2D类型的一致变量，我们需要在绘制之前将法线纹理绑定到它上面。法线信息的存储方式与颜色一样，所以它的每个分量都处于[0，1]的范围之间。所以我们需要通过函数’f(x) = 2 * x - 1’将法线信息变换回它的原始形式。这个函数将0映射到-1，将1映射到 1。
现在我们需要将法线信息从切线空间中变换到世界坐标系中。我们用mat3类型的构造函数中的其中一个创建一个名为TNB的3x3矩阵，这个构造函数采用三个向量作为参数，这三个分量依次作为矩阵的第一行、第二行和第三行。如果你在疑惑为什么要以这样的顺序构造矩阵而不是其他的顺序，那么你只需要记住tangent对应于X轴，而bitangent对应于Y轴，至于法线向量则与Z轴相对应（参看上面的图片）。在标准的 3x3单位矩阵中，第一行对应其X轴，第二行对应其Y轴，第三行则对应其Z轴，我们只是依据这个顺序。将从纹理中提取的位于切线空间下的法线信息乘上TBN矩阵，并且将结果规范化之后再返回给调用者，这就得到了片元最终的法线信息。
本章中的示例还伴有三个JPEG文件：

‘bricks.jpg’是颜色纹理；
‘normal_map.jpg’是从’bricks.jpg’纹理中生成的法线纹理；
‘normal_up.jpg’是一个也是一个发现纹理，但是这个纹理中所有发现都是朝上的。使用这个纹理作为法线纹理时，场景的效果就像没有使用法线纹理技术一样，我们可以通过绑定这个纹理来使得我们的法线纹理失效（尽管效率不是很高）。你可以通过按‘b’键在法线纹理和普通纹理之间的切换。

法线纹理被绑定在2号纹理单元中，并且此纹理单元专门用于存放法线纹理（0号纹理单元是颜色纹理，1号纹理单元存放阴影纹理）。
注意法线纹理的生成方式：
生成法线纹理的方法有很多，在这一节中我使用gimp 来生成法线纹理，它是一个免费开源的软件，有一个专门用于生成法线纹理的插件：normal map plugin。只要安装了这个插件，选择Filters->Map->Normalmap导入想要贴在模型上的纹理，之后会有多个与发现纹理相关的参数可供选择，达到满意的效果后点击‘OK’即可。这样在gimp软件视图中原来的普通纹理就会被新生成的法线纹理所替代，用新文件名将其保存下来即可在我们的着色器中使用了。 


