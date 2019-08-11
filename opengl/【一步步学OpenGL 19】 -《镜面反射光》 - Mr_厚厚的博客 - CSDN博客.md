







教程19
镜面反射光

原文： http://ogldev.atspace.co.uk/www/tutorial19/tutorial19.html
CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

背景
我们在计算环境光的时候，光的强度是唯一的影响因素。然后处理漫射光的时候公式中加入了光的方向参数。镜面反射包含了上面所有的综合因素并且添加了一个新的元素：观察者的位置。镜面反射时光以一定角度照射到物体表面，同时会在法线的另一侧对称的角度上反射出去，如果观察者刚好在反射光线的路径上那么就会看到格外强烈的光线。
镜面反射最终的结果是物体在从某个角度看上去会十分明亮，而移动开后这个光亮又会消失。现实中好的镜面反射的例子是金属物体，这些物体有时候看上去由于太亮了导致看不到他本来的颜色而是直接照向你眼睛的白色的亮光。但这种属性在其他的一些材料上是没有的（比如：木头）。很多东西根本不会发光，不管光源从什么角度照射以及观察者在什么位置。所以，镜面反射光的存在更取决于反射物体的材料性质而不是光源本身。
现在看如何将观察者的位置加入到镜面反射光的计算当中，看下图：

要注意五个因素：
‘I’ 是入射光
‘N’ 是表面法线
‘R’ 反射光，和入射光’I’关于法线对称，但方向相反
‘V’ 是从入射光和反射光交点处（入射点）到观察者眼睛的向量，表示观察者视线
‘α’ 反射光’R’和观察者视线’V’的夹角
我们将使用夹角’α’来对镜面反射光现象进行建模。有一点可以看出当观察者视线和反射光重合时（夹角为0），反射光的强度最大。观察者慢慢从反射光’R’移开时，夹角慢慢变大，而我们希望随着角度增大反射光要慢慢衰弱。明显，这里又要使用差积运算来计算夹角’α’的余弦值了，这个值将作为计算镜面反射光公式的反射参数。当’α’为0时余弦值为1，这是我们反射参数的最大值。随着夹角’α’增大余弦值慢慢减小，直到夹角达到90度时就彻底没有镜面反射的效果了。当然，夹角大于90度时余弦值为负，也没有任何反射效果，也就是观察者不在反射光的路径范围内。
我们要用到’R’和’V’来计算夹角’α’。’V’可以通过世界坐标系中观察者位置和光的入射点位置的差计算得到。camera已经在世界空间进行维护了，我们只需要将它的位置传给shader着色器。另外上面的图是经过简化了的模型，光在物体表面只有一个入射点（事实上不是，这里只是为了好分析）。事实上，整个三角形都被点亮了（假设它面向光源），因此我们要计算每一个像素的镜面反射效果（和漫反射光的计算一样）。我们必须要知道每个像素在世界空间的位置，这个不难：可以将顶点变换到世界空间，让光栅器对像素的世界空间位置进行插值并将结果传给片段着色器。事实上，这个和之前教程中对法线的处理操作是一样的。
最后是要使用’I’向量（由应用传给shader）来计算反射光线’R’。如下图：

首先要强调向量没有起点的概念，所有方向相同且长度相同的向量都是同一个向量。因此，图中将入射光向量’I’复制到表面下面位置向量本身是不变的。目标是求向量’R’，根据向量的加法，’R’等于’I’+’V’。’I’是已知的，所以我们要求’V’。注意法线’N’的反向向量为’-N’，计算’I’和’-N’的点积可以得到’I’在’-N’上的投影，这也是’V’的模长度的一半。另外’V’和’N’的方向是相同的，所以只要用计算的那个投影长度乘以单位向量’N’再乘以2就是向量’V’了。用公式简单表示如下：

明白这个数学公式后可以说一个相关的知识点：GLSL提供了一个叫做’reflect’的内部函数就是做的上面这个计算。可以看下面这个函数在shader中的用法。这里得出计算镜面反射的最终公式：

开始先是将光的颜色和物体表面的颜色相乘，这个和在计算环境光以及漫反射光时一样。得到的结果再和材料的镜面反射强度参数（’M’）相乘。如果材料没有反射性能，比如木头，那么镜面反射参数就为0，整个公式的结果也就为0了，而像金属这种发光材料镜面反射能力就会很强。之后再乘以光线和观察者视线夹角的余弦值，这也是最后一个调整镜面反射光强度的参数（‘镜面参数’或者叫做‘发光参数’）。镜面参数是用来增强加剧反射光区域边缘的强度的。下面的图片展示了镜面参数为1时的效果：

下面的镜面参数为32：

镜面反射能力也被认为是材料的一种属性，因此不同的物体会有不同的镜面反射能力值。
源代码详解
(lighting_technique.h:32)

class LightingTechnique : public Technique
{
public:
...
    void SetEyeWorldPos(const Vector3f& EyeWorldPos);
    void SetMatSpecularIntensity(float Intensity);
    void SetMatSpecularPower(float Power);

private:
...
    GLuint m_eyeWorldPosLocation;
    GLuint m_matSpecularIntensityLocation;
    GLuint m_matSpecularPowerLocation;
}

LightingTechnique类中有了三个新属性：眼睛（观察者）的位置、镜面反射强度和材料的镜面参数。这三个参数都是独立于光线本身的，因为当同一束光照到不同的材料上（比如：木头和金属）时会有不同的反射发光效果。目前对材料属性的的使用模型还是很局限的，同一个绘制回调的所有三角形会得到这些属性的一样的值。如果同一个模型的不同部分的三角形图元是不同的材料，这样就不合理了。在后面的教程中讲关于mesh网格的加载时我们会在一个模块中产生不同的镜面参数值并作为顶点缓冲器的一部分（而不是shader的一个参数），这样我们就可以在同一个绘制回调中使用不同的镜面光照参数来处理三角形图元。这里简单的使用一个shader参数就可以实现效果（当然可以尝试在顶点缓冲中添加不同的镜面强度参数然后在shader中获取来实现更复杂的镜面效果）。
(lighting.vs:12)

out vec3 WorldPos0;

void main()
{
    gl_Position = gWVP * vec4(Position, 1.0);
    TexCoord0 = TexCoord;
    Normal0 = (gWorld * vec4(Normal, 0.0)).xyz;
    WorldPos0 = (gWorld * vec4(Position, 1.0)).xyz;
}

上面顶点着色器多了最后一行代码，世界变换矩阵（之前用来变换法线的那个世界变换矩阵）这里用来将顶点的世界坐标传给片段着色器。这里有一个技术点是使用两个不同的矩阵来变换本地坐标提供的同一个顶点位置，并将结果独立的传递给片段着色器。经过完整的变换（world-view-projection变换）后结果传递给系统变量’gl_Position’，然后GPU负责将它变换到屏幕空间坐标系并用来进行实际的光栅化操作。局部变换到世界空间的结果传给了一个用户自定义的属性，这个属性在光栅化阶段被进行了简单的插值，所以片段着色器中激活的每一个像素都会提供它自己的世界空间位置坐标。这种技术很普遍也很有用。

(lighting.fs:5)
in vec3 WorldPos0;
.
.
.
uniform vec3 gEyeWorldPos;
uniform float gMatSpecularIntensity;
uniform float gSpecularPower;

void main()
{
    vec4 AmbientColor = vec4(gDirectionalLight.Color * gDirectionalLight.AmbientIntensity, 1.0f);
    vec3 LightDirection = -gDirectionalLight.Direction;
    vec3 Normal = normalize(Normal0);

    float DiffuseFactor = dot(Normal, LightDirection);

    vec4 DiffuseColor = vec4(0, 0, 0, 0);
    vec4 SpecularColor = vec4(0, 0, 0, 0);

    if (DiffuseFactor > 0) {
        DiffuseColor = vec4(gDirectionalLight.Color, 1.0f) *
            gDirectionalLight.DiffuseIntensity *
            DiffuseFactor;

        vec3 VertexToEye = normalize(gEyeWorldPos - WorldPos0);
        vec3 LightReflect = normalize(reflect(gDirectionalLight.Direction, Normal));
        float SpecularFactor = dot(VertexToEye, LightReflect);
        if (SpecularFactor > 0) {
            SpecularFactor = pow(SpecularFactor, gSpecularPower);
            SpecularColor = vec4(gDirectionalLight.Color * gMatSpecularIntensity * SpecularFactor, 1.0f);
        }
    }

    FragColor = texture2D(gSampler, TexCoord0.xy) * (AmbientColor + DiffuseColor + SpecularColor);
}

片段着色器中的变化是多了三个新的一致性变量，用来存储计算镜面光线的一些属性（像眼睛的位置、镜面光强度和镜面反射参数）。环境光颜色的计算和前面两篇教程中的计算一样。然后创建漫射光和镜面光颜色向量并初始化为0，之后只有当光线和物体表面的角度小于90度时颜色值才不为零，这个要通过漫射光参数来检查（和在漫射光教程中说的一样）。
下一步要计算世界空间中从顶点位置到观察者位置的向量，这个通过观察者世界坐标和顶点的世界坐标相减计算得到，其中观察者的世界坐标是一个一致变量对于所有的像素点来说都一样。为了方便后面的点积操作这个向量要进行单位化。然后，使用内置的’reflect’函数就可以计算反射光向量了（当然也可以自行按照上面背景中介绍的手动计算）。’reflect’函数有两个参数：光线向量和物体表面法向量。注意这里使用的是最原始的射向物体表面的那个光源向量而不是用于漫射光参数计算的反向的光源向量（见上面图示）。然后计算镜面反射参数，也就是反射光和顶点到观察者那个向量的夹角余弦值（还是通过点积计算得到）。
镜面反射效果只有在那个夹角小于90度时才看得到，所以我们要先检查点积的结果是否大于0。最后一个镜面颜色值是通过将光源颜色和材料的镜面反射强度以及材料镜面反射参数相乘计算得到。我们将镜面颜色值添加到环境光和漫射光颜色中来制造光颜色的整体效果。最后和从纹理中取样的颜色相乘得到最终的像素颜色。
(tutorial19.cpp:134)

m_pEffect->SetEyeWorldPos(m_pGameCamera->GetPos());
m_pEffect->SetMatSpecularIntensity(1.0f);
m_pEffect->SetMatSpecularPower(32);

镜面反射光颜色的使用很简单。在渲染循环我们得到了camera的位置（在世界空间中已经维护好了）并将它传给了LightingTechnique类。这里还设置了镜面反射强度和镜面参数。剩下的就由着色器来处理了。
可以调整镜面反射的参数值以及光源的方向来看效果。当然为了找到可以看到镜面反射光效果的位置可能需要围着物体转一圈。 


