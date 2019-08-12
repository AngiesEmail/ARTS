# 教程 22 OpenGL使用Assimp库导入3d模型

原文： http://ogldev.atspace.co.uk/www/tutorial22/tutorial22.html

CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

## 背景
通过之前的学习我们实现了很多不错的效果，但是我们并不能手能创建复杂的模型，可以想象通过代码来定义物体的每个顶点位置和其他属性是不可行的。一个盒子，金字塔或者简单的表面贴图还好说，但如果是立体的人脸怎么办？事实上在游戏中，在一些商业的游戏应用中模型的网格是由美工艺术家使用一些建模软件创建的，例如：Blender,Maya,3ds Max等。这些软件提供了强大的工具来帮助美工创建复杂的模型。模型创建好之后会保存到一个文件中，3d模型文件有很多格式，例如：OBJ格式。3d模型文件包含了模型的整个几何结构定义，然后可以导入到游戏引擎中（当然游戏引擎要能够支持该模型的格式），通过模型文件可以解析出顶点和顶点缓冲数据用于渲染。理解这些模型文件的几何定义方式以及解析方法从而加载专业的模型对将3d游戏程序提升到另一个级别是非常关键的。

自己开发一个模型解析器程序是很花时间的，因为如果想要加载不同类型的模型资源，你要学习每一种格式的内部原理并分别对其写专门的解析程序。有一些格式是很简单的但有一些模型的格式非常复杂，导致你会在这种并不是3d图形编程的重点部分上浪费大量时间精力。

因此这个教程中的方法就是使用一个外部的框架来解析加载不同的模型文件。
Assimp(Open Asset Import Library)是一个处理很多3D格式文件的开源库，包括最流行的3d格式，在Linux和Windows系统都可以很方便的使用。这个模型解析库可以很容易的整合到C/C++程序中使用。

这个教程中没有太多的理论介绍，我们直接看怎样将Assimp整合到我们的3D程序中

首先要安装Assimp：先点上面的链接去下载后安装该库。

## 源代码详解

```
(mesh.h:50)
class Mesh
{
public:
    Mesh();

    ~Mesh();

    bool LoadMesh(const std::string& Filename);

    void Render();

private:
    bool InitFromScene(const aiScene* pScene, const std::string& Filename);
    void InitMesh(unsigned int Index, const aiMesh* paiMesh);
    bool InitMaterials(const aiScene* pScene, const std::string& Filename);
    void Clear();

#define INVALID_MATERIAL 0xFFFFFFFF

    struct MeshEntry {
        MeshEntry();

        ~MeshEntry();

        bool Init(const std::vector& Vertices,
        const std::vector& Indices);

        GLuint VB;
        GLuint IB;
        unsigned int NumIndices;
        unsigned int MaterialIndex;
    };

    std::vector m_Entries;
    std::vector m_Textures;
};
```
这个Mesh类表示的是Assimp框架和我们的OpenGL程序的接口，这个类的对象使用模型文件名作为其LoadMesh()函数的参数，加载模型然后创建模型中包含的且我们的程序能够理解的顶点缓冲，索引缓冲和纹理对象数据。

使用Render()函数来渲染模型网格，Mesh类的内部结构和Assimp加载模型的方式是刚好匹配的。Assimp使用一个aiScene对象来表示加载的mesh网格，aiScene对象中包含了网格结构，且这个网格结构部分封装了模型。aiScene对象中至少包含一个网格结构，而复杂的模型就可能包含多个网格结构了。
m_Entries是Mesh类的一个成员变量，是MeshEntry结构体中的一个向量。
Mesh类中的每一个结构体都对应于aiScene对象中的一个mesh结构体，结构体中包含了顶点缓冲，索引缓冲以及材质的索引。目前，材质就指的是贴图纹理了，而网格实体是可以共享材质的因此我们还要为每个纹理（m_Textures）分别设置相应的向量。MeshEntry::MaterialIndex就指向m_Textures中的其中一个纹理。

```
(mesh.cpp:77)
bool Mesh::LoadMesh(const std::string& Filename)
{
    // Release the previously loaded mesh (if it exists)
    Clear();

    bool Ret = false;
    Assimp::Importer Importer;

    const aiScene* pScene = Importer.ReadFile(Filename.c_str(), aiProcess_Triangulate | aiProcess_GenSmoothNormals | aiProcess_FlipUVs | aiProcess_JoinIdenticalVertices);

    if (pScene) {
        Ret = InitFromScene(pScene, Filename);
    }
    else {
        printf("Error parsing '%s': '%s'\n", Filename.c_str(), Importer.GetErrorString());
    }

    return Ret;
}
```
从这个函数开始就要加载mesh了。我们在栈上创建了Assimp::Importer类的一个实例，并调用其ReadFile方法来读取文件。这个函数有两个参数：模型文件的完整路径和一些处理选项。Assimp能对加载的模型进行很多优化操作。例如，为缺失法线的模型生成法线，优化模型的结构以提高性能等，这里列举了所有的优化操作选项，我们可以根据需要来选择合适的操作选项：

aiProcess_Triangulate 它将非由三角图元组成的模型转换为三角形图元网格模型。例如：一个四边形mesh可以通过将每个四边形图元分成两个三角形图元而转换成三角形图元mesh；

aiProcess_GenSmoothNormals 为那些原来没有顶点法线的模型生成顶点法线。

aiProcess_FlipUVsv ，沿着y轴来翻转纹理坐标。这个是用来在demo中正确渲染Quake模型的。

aiProcess_JoinIdenticalVertices 使用每个顶点的一份拷贝，并通过索引获取其引用，需要的时候可以帮助节省内存。

注意这些加工方式是非重叠的位掩码，可以使用或运算将多个这些操作组合起来一起用，当然要根据导入的模型数据来选择合理的选择这些操作的。如果mesh加载成功，我们则可以获得一个指向aiScene对象的指针。这个对象包含整个模型的内容，并分布在模型不同的aiMesh结构中。然后我们调用InitFromScene()函数来初始化这个Mesh对象。

```
(mesh.cpp:97)
bool Mesh::InitFromScene(const aiScene* pScene, const std::string& Filename)
{
    m_Entries.resize(pScene->mNumMeshes);
    m_Textures.resize(pScene->mNumMaterials);

    // Initialize the meshes in the scene one by one
    for (unsigned int i = 0 ; i < m_Entries.size() ; i++) {
        const aiMesh* paiMesh = pScene->mMeshes[i];
        InitMesh(i, paiMesh);
    }

    return InitMaterials(pScene, Filename);
}
```
初始化Mesh对象，我们得要分配mesh对象的内存空间，还要准备我们要用的纹理向量以及所有的网格数据和材质。分配空间的大小可以分别从aiScene对象的mNumMeshes和mNumMaterials成员变量中获取相应数量参数。然后扫描aiScene对象的mMeshes数组并依次初始化mesh实体对象。最后就可以返回初始化后的材质了。

```
(mesh.cpp:111)
void Mesh::InitMesh(unsigned int Index, const aiMesh* paiMesh)
{
    m_Entries[Index].MaterialIndex = paiMesh->mMaterialIndex;

    std::vector Vertices;
    std::vector Indices;
    ...
```
初始化开始先记录下当前mesh的材质索引，通过索引在渲染期间为mesh网格绑定合适的纹理。然后创建两个STL向量容器来储存顶点和索引缓冲器的数据。STL向量容器有一个很好的特性：能够在连续的缓冲区中储存数据，这样使用glBufferData()函数就很容易将数据加载到OpenGL缓存中了。

```
(mesh.cpp:118)
    const aiVector3D Zero3D(0.0f, 0.0f, 0.0f);

    for (unsigned int i = 0 ; i < paiMesh->mNumVertices ; i++) {
        const aiVector3D* pPos = &(paiMesh->mVertices[i]);
        const aiVector3D* pNormal = &(paiMesh->mNormals[i]) : &Zero3D;
        const aiVector3D* pTexCoord = paiMesh->HasTextureCoords(0) ? &(paiMesh->mTextureCoords[0][i]) : &Zero3D;

        Vertex v(Vector3f(pPos->x, pPos->y, pPos->z),
                Vector2f(pTexCoord->x, pTexCoord->y),
                Vector3f(pNormal->x, pNormal->y, pNormal->z));

        Vertices.push_back(v);
    }
    ...
```
这里我们通过解析模型数据将顶点属性数据依次存放到Vertices容器中。这里使用到 aiMesh类中下面的一些方法：

mNumVertices: 顶点数量

mVertices: 包含位置属性的数组

mNormals: 包含顶点法线属性的数组

mTextureCoords: 包含纹理坐标数组，这是一个二维数组，因为每个顶点可以拥有多个纹理坐标。

总的来说我们有三个相互独立的数组，囊括了所有我们需要的顶点信息，我们可以通过这些信息来构建我们最终的顶点结构体。注意一些模型没有纹理坐标，在访问mTextureCoords数组之前我们应该通过调用HasTextureCoords()来检查纹理是否存在防止出错。此外，一个 mesh的每个顶点是可以包含多个纹理坐标的，这里我们只是简单地使用第一个纹理坐标。因此mTextureCoords二维数组始终只有第一行的值会被访问。如果纹理坐标不存在，我们就将这个顶点的纹理坐标初始化为零向量。

```
(mesh.cpp:132)
    for (unsigned int i = 0 ; i < paiMesh->mNumFaces ; i++) {
        const aiFace& Face = paiMesh->mFaces[i];
        assert(Face.mNumIndices == 3);
        Indices.push_back(Face.mIndices[0]);
        Indices.push_back(Face.mIndices[1]);
        Indices.push_back(Face.mIndices[2]);
    }
    ...
```
接下来我们创建索引缓存。aiMesh类的成员mNumFaces会告诉我们有多少个多边形，而 mFaces数组包含了顶点的索引。首先我们要确保每个多边形的顶点数都为3（加载模型的时候会要求进行三角化，但之后最好再检查确认一下防止意外）。然后我们从模型数据中解析出每个面的索引并将其存放到Indices向量中。

```
(mesh.cpp:140)
    m_Entries[Index].Init(Vertices, Indices);
}
```
最后，我们用顶点和索引向量完成MeshEntry结构体的初始化。函数MeshEntry::Init() 中没有添加新内容所以这里就不再介绍，它不过是使用glGenBuffer(),glBindBuffer()和glBufferData()来创建和添加顶点缓存和索引缓存数据。这个可以在源码中看到更多实现细节。

```
(mesh.cpp:143)
bool Mesh::InitMaterials(const aiScene* pScene, const std::string& Filename)
{
    for (unsigned int i = 0 ; i < pScene->mNumMaterials ; i++) {
        const aiMaterial* pMaterial = pScene->mMaterials[i];
       ...
```
这个函数用来加载模型所用的所有纹理。在aiScene对象中mNumMaterials属性存放材质数量，而mMaterials是一个指针数组，其中的每一个元素都指向一个aiMaterials结构体。aiMaterials结构体十分复杂，但是它通过几个API函数进行了封装隐藏了复杂的细节。 

总体来说，材质是以一个纹理的栈结构来组织的，在连续的纹理之间要应用配置好了的颜色混合以及强度函数。例如：通过混合函数可以知道应该从两张纹理中采集颜色，强度函数可能会要将最终结果再减半（参数为0.5）。颜色混合和强度函数属于aiMaterial结构体的一部分，可以从中调用。这里为了简单以及让我们的光照模型着色器效果明显，我们暂时直接忽略颜色混合和强度函数，直接用原本的纹理。

```
(mesh.cpp:165)
        m_Textures[i] = NULL;
        if (pMaterial->GetTextureCount(aiTextureType_DIFFUSE) > 0) {
            aiString Path;

            if (pMaterial->GetTexture(aiTextureType_DIFFUSE, 0, &Path, NULL, NULL, NULL, NULL, NULL) == AI_SUCCESS) {
                std::string FullPath = Dir + "/" + Path.data;
                m_Textures[i] = new Texture(GL_TEXTURE_2D, FullPath.c_str());

                if (!m_Textures[i]->Load()) {
                    printf("Error loading texture '%s'\n", FullPath.c_str());
                    delete m_Textures[i];
                    m_Textures[i] = NULL;
                    Ret = false;
                }
            }
        }
        ...
```
一个材质是可以包含多个纹理的，但并不是所有的纹理都必须包含颜色。例如，一个纹理可以是高度图、法向图、位移图等。当前我们针对光照计算的着色器程序只使用一个纹理，而我们也只关心漫反射纹理，因此我们使用aiMaterial::GetTextureCount()函数检查有多少漫反射纹理存在。这个函数以纹理类型为参数同时返回此特定类型纹理的数目。如果至少存在一个漫反射纹理，我们就可以使用aiMaterial::GetTexture()函数来获取它。这个函数的第一个参数是类型，之后是纹理索引，然后我们需要一个指向纹理文件路径的字符串指针。最后有 5 个指针参数允许我们去获取纹理的各种配置，比如混合因子、全图模式和纹理操作等。这些是可选的，现在我们忽略它们而只传递 NULL。这里我们假定模型和纹理在同一子目录中。如果模型的结构比较复杂，你可能需要在别处寻找纹理，那样的话我们可以像往常一样创建纹理对象并加载它。

```
(mesh.cpp:187)
        if (!m_Textures[i]) {
          m_Textures[i] = new Texture(GL_TEXTURE_2D, "../Content/white.png");
          Ret = m_Textures[i]->Load();
       }
    }

    return Ret;
}
```
上面这一小段代码用于处理模型加载时遇到的一些问题。有时候一个模型可能并没有纹理导致可能会看不到任何东西，因为若纹理不存在取样的结果默认为黑色。这里当我们遇到这种问题时我们为其加载一个白色的纹理（附件中可以找到这个纹理），这样所有像素的基色就变为白色了，看起来不是很好，但至少可以看到一些内容。这张纹理占用空间很小，可以在两个例子中相同的着色器中使用。

```
(mesh.cpp:197)
void Mesh::Render()
{
    glEnableVertexAttribArray(0);
    glEnableVertexAttribArray(1);
    glEnableVertexAttribArray(2);

    for (unsigned int i = 0 ; i < m_Entries.size() ; i++) {
        glBindBuffer(GL_ARRAY_BUFFER, m_Entries[i].VB);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), 0);
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(Vertex), (const GLvoid*)12);
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (const GLvoid*)20);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_Entries[i].IB);

        const unsigned int MaterialIndex = m_Entries[i].MaterialIndex;

        if (MaterialIndex < m_Textures.size() && m_Textures[MaterialIndex]) {
            m_Textures[MaterialIndex]->Bind(GL_TEXTURE0);
        }

        glDrawElements(GL_TRIANGLES, m_Entries[i].NumIndices, GL_UNSIGNED_INT, 0);
    }

    glDisableVertexAttribArray(0);
    glDisableVertexAttribArray(1);
    glDisableVertexAttribArray(2);
}
```
这个函数封装了mesh的渲染，并将其从主函数中分离出来（以前是主函数的一部分）。它遍历m_Entries数组，将数组中每个节点的顶点缓冲和索引缓冲绑定在一起。节点的材质索引用来从m_Texture数组中取出纹理对象，并将这个纹理绑定，最后执行绘制命令。现在有了多个已从文件中加载进来的mesh对象，调用Mesh::Render()函数就可以依次渲染它们了。

```
(glut_backend.cpp:112)
glEnable(GL_DEPTH_TEST);
```
最后要需要学习的是以前章节省略的。事实上如果继续使用上面的代码导入模型并渲染，场景可能会出现异常，原因是距离相机较远的三角形被绘制在了距离较近的三角形的上面。为了解决这个问题，需要开启深度测试(Depth test)，这样光栅化程序就可以比较屏幕上相同位置重叠像素的深度优先顺序，最后被绘制到屏幕上的就是深度测试后优先绘制（距离相机较近）的像素。深度测试默认不开启，上面的代码用于开启深度测试（这段代码在 GLUTBackendRun()函数中，用于OpenGl状态的初始化），不过这只是开启深度测试的第一步。（下面继续…）

```
(glut_backend.cpp:73)
glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA|GLUT_DEPTH);
```
这段代码则是对深度缓存的初始化，为了比较两个像素的深度，“旧”的像素必须被储存起来，为此，我们创建一个特殊的缓冲——深度缓冲（或叫Z缓冲器）。深度缓冲的大小与屏幕尺寸对应，这样颜色缓冲器里面的每个像素在深度缓冲器都有相应的位置，这个位置总是储存离相机最近的像素的深度值，用于在深度测试时进行比较。

```
(tutorial22.cpp:101)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
```
The last thing we need to do is to clear the depth buffer at the start of a new frame. If we don’t do that the buffer will contain old values from the previous frame and the depth of the pixels from the new frame will be compared against the depth of the pixels from the previous frame. As you can imagine, this will cause serious corruptions (try!). The glClear() function takes a bitmask of the buffers it needs to operate on. Up until now we’ve only cleared the color buffer. Now it’s time to clear the depth buffer as well. 

最后要做的是在开始渲染新的一帧的时候清除深度缓存，如果不这样做，深度缓存中将会保留上一帧中各像素的深度值，并且新一帧像素的深度会和上一帧像素的深度比较。可以想象，这会导致最后绘制出来的图象很奇怪没法看了（可以试试！）。glClear()函数接收一个它要处理的缓冲器的位掩码。之前只清除了颜色缓存，现在同时还要将深度缓存也清除掉。 


