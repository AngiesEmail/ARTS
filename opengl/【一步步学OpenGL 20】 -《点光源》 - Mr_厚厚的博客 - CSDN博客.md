# 教程 20 点光源

原文： http://ogldev.atspace.co.uk/www/tutorial20/tutorial20.html

CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

## 背景
之前已经学习了三个基本的光照模型（环境光，漫射光和镜面反射光），这三种模型都是基于平行光的。平行光只是通过一个向量来表示，没有光源起点，因此它不会随着距离的增大而衰减（实际上没有起点根本无法定义光源和某个物体的距离）。现在我们再来看点光源类型，它有光源起点而且有衰减效果，距离光源越远光线越弱。点光源的经典例子是灯泡，灯泡在屋子里可能效果不明显，但是拿到室外就会明显看出它的衰减效果了。注意之前平行光的方向是恒定的，但点光源光线的方向是变化的，四处扩散。点光源想各个方向均匀照射，因此点光源的方向要通过计算物体到点光源之间的向量得到，这就是为什么要定义点光源的起点而不是它的方向。

点光源光线慢慢变淡的的想象叫做‘衰减’。真实光线的衰减是按照平方反比定律的，也就是说光线的强度和离光源的距离的平方成反比。数学原理如下图中的公式：

但3D图形中这个公式计算的结果看上去效果并不好。例如：当距离很近时，光的强度接近无穷大了。另外，开发者除了通过设置光的起始强度外无法控制点光源的亮度，这样就太受限制了，因此我们添加了几个新的因素到公式中使对其的控制更加灵活：

我们在分母上添加了三个光衰减的参数因子，一个常量参数，一个线性参数和一个指数参数。当将常量参数和线性参数设置为零且指数参数设置为1时，就和实际的物理公式是对应的了，也就是这个特殊情况下在物理上是准确的。当设置常量因子参数为1时，调节另外两个参数整体上就有比较好的衰减变化效果了。常量参数的设置是要保证当距离为0时光照强度达到最大（这个要在程序内进行配置），然后随着距离的增大光照强度要慢慢减弱，因分母在慢慢变大。控制好线性参数因子和指数参数因子的变化，就可以实现想要的衰减效果，线性参数主要用于实现缓慢的衰减效果而指数因子可以控制光强度的迅速衰减。

现在总结计算点光源需要的步骤：

计算和平行光一样的环境光；

计算一个从像素点（世界空间中的）到点光源的向量作为光线的方向。利用这个光线方向就可以计算和平行光一样的漫射光以及镜面反射光了；

计算像素点到点光源的距离用来计算最终的光线强度衰减值；

将三种光叠加在一起，计算得到最终的点光源颜色，通过点光源的衰减性三种光看上去也可以被分离开了。

## 源代码详解

```
(lighting_technique.h:24)

struct BaseLight
{
    Vector3f Color;
    float AmbientIntensity;
    float DiffuseIntensity;
};
.
.
.
struct PointLight : public BaseLight
{
    Vector3f Position;

    struct
    {
        float Constant;
        float Linear;
        float Exp;
    } Attenuation;
}
```
平行光虽然和点光源不一样，但它们仍然有很多共同之处，它们共同的部分都放到了BaseLight结构体中，而点光源和平行光的结构体则继承自BaseLight。平行光额外添加了方向属性到它的类中，而点光源则添加了世界坐标系中的位置变量和那三个衰减参数因子。

```
(lighting_technique.h:81)
void SetPointLights(unsigned int NumLights, const PointLight* pLights);
```
这个教程除了展示如何实现点光源，还展示怎样使用多光源。通常只存在一个平行光光源，也就是太阳光，另外可能还会有一些点光源（屋子里的灯泡，地牢里的火把等等）。这个函数参数有一个点光源数据结构的数组和数组的长度，使用结构体的值来更新shader。

```
(lighting_technique.h:103)
struct {
    GLuint Color;
    GLuint AmbientIntensity;
    GLuint DiffuseIntensity;
    GLuint Position;
    struct
    {
        GLuint Constant;
        GLuint Linear;
        GLuint Exp;
    } Atten;
} m_pointLightsLocation[MAX_POINT_LIGHTS];
```
为了支持多个点光源，shader需要包含一个和点光源结构体（只在GLSL中）内容一样的结构体数组。主要有两种方法来更新shader中的结构体数组：

可以获取每个数组元素中每个结构字段的位置（例如，一个数组如果有五个结构体，每个结构体四个字段，那就需要20个‘位置一致变量’），然后单独设置每个元素中每个字段的值。

也可以只获取数组第一个元素每个字段的位置，然后用一个GL函数来保存元素中每个字段的属性类型。例如，数组元素也就是一个结构体的第一个字段是一个float变量，第二个是一个integer变量，就可以在一次回调中使用一个float数组遍历设置数组中每个结构体第一个字段的值，然后在第二次回调中使用一个int数组来设置每个结构体的第二个值。

第一种方法由于要维护大量的位置一致变量因此很浪费资源，但是会更加灵活，因为你可以通过位置一致变量访问更新数组中的任何一个元素，不需要像第二种方法那样先要转换输入的数据。

第二种方法不需要管理那么多的位置一致变量，但是如果想要同时更新数组中的几个元素的话，同时用户传入的又是一个结果体数组（像SetPointLights()），你就要先将这个结构体数组转换成多个字段的数组结构，因为结构体中每个位置的字段数据都要使用一个同类型的数组来更新。当使用结构体数组时，在数组中两个连续元素（结构体）中的同一个字段之间存在内存间隔（被其他字段间隔开了，我们是想要同一个字段的连续字段数组），需要将它们收集到它们自己的同类型数组中。本教程中，我们将使用第一种方法。最好两个都实现一下，看你觉得哪一个方法更好用。

MAX_POINT_LIGHTS是一个常量，用于限制可以使用的点光源的最大数量，并且必须和着色器中的相应值同步一致。默认值为2，当你增加应用中光的数量，随着光源的增加会发现性能越来越差。这个问题可以使用一种称为“延迟着色”的技术来优化解决，这个后面再探讨。

```
(lighting.fs:46)
vec4 CalcLightInternal(BaseLight Light, vec3 LightDirection, vec3 Normal)
{
    vec4 AmbientColor = vec4(Light.Color, 1.0f) * Light.AmbientIntensity;
    float DiffuseFactor = dot(Normal, -LightDirection);

    vec4 DiffuseColor = vec4(0, 0, 0, 0);
    vec4 SpecularColor = vec4(0, 0, 0, 0);

    if (DiffuseFactor > 0) {
        DiffuseColor = vec4(Light.Color * Light.DiffuseIntensity * DiffuseFactor, 1.0f);
        vec3 VertexToEye = normalize(gEyeWorldPos - WorldPos0);
        vec3 LightReflect = normalize(reflect(LightDirection, Normal));
        float SpecularFactor = dot(VertexToEye, LightReflect);
        if (SpecularFactor > 0) {
            SpecularFactor = pow(SpecularFactor, gSpecularPower);
            SpecularColor = vec4(Light.Color * gMatSpecularIntensity * SpecularFactor, 1.0f);
        }
    }

    return (AmbientColor + DiffuseColor + SpecularColor);
}
```
这里在平行光和点光源之间实现很多着色器代码的共享就不算什么新技术了。大多数算法是相同的。不同的是，我们只需要考虑点光源的衰减因素。 此外，针对平行光，光的方向是由应用提供的，而对点光源，需要计算每个像素的光的方向。
上面的函数封装了两种光类型之间的共用部分。 BaseLight结构体包含光强度和颜色。LightDirection是额外单独提供的，原因上面刚刚已经提到。 另外还提供了顶点法线，因为我们在进入片段着色器时要对其进行一次单位化处理，然后在每次调用此函数时使用它。

```
(lighting.fs:70)
vec4 CalcDirectionalLight(vec3 Normal)
{
    return CalcLightInternal(gDirectionalLight.Base, gDirectionalLight.Direction, Normal);
}
```
有了公共的封装函数，定义函数简单的包装调用一下就可以计算出平行光了，参数多数来自全局变量。

```
(lighting.fs:75)
vec4 CalcPointLight(int Index, vec3 Normal)
{
    vec3 LightDirection = WorldPos0 - gPointLights[Index].Position;
    float Distance = length(LightDirection);
    LightDirection = normalize(LightDirection);

    vec4 Color = CalcLightInternal(gPointLights[Index].Base, LightDirection, Normal);
    float Attenuation = gPointLights[Index].Atten.Constant +
                        gPointLights[Index].Atten.Linear * Distance +
                        gPointLights[Index].Atten.Exp * Distance * Distance;

    return Color / Attenuation;
}
```
计算点光比定向光要复杂一点。每个点光源的配置都要调用这个函数，因此它将光的索引作为参数，在全局点光源数组中找到对应的点光源。它根据光源位置（由应用程序在世界空间中提供）和由顶点着色器传递过来的顶点世界空间位置来计算光源方向向量。使用内置函数length（）计算从点光源到每个像素的距离。 一旦我们有了这个距离，就可以对光的方向向量进行单位化处理。注意，CalcLightInternal（）是需要一个单位化的光方向向量的，平行光的单位化由LightingTechnique类来负责。 我们使用CalcInternalLight（）函数获得颜色值，并使用我们之前得到的距离来计算光的衰减。最终点光源的颜色是通过将颜色和衰减值相除计算得到的。

```
(lighting.fs:89)
void main()
{
    vec3 Normal = normalize(Normal0);
    vec4 TotalLight = CalcDirectionalLight(Normal);

    for (int i = 0 ; i < gNumPointLights ; i++) {
        TotalLight += CalcPointLight(i, Normal);
    }

    FragColor = texture2D(gSampler, TexCoord0.xy) * TotalLight;
}
```
有了前面的基础，片段着色器方面就变得非常简单了。简单地将顶点法线单位化，然后将所有类型光的效果叠加在一起，结果再乘以采样的颜色，就得到最终的像素颜色了。

```
(lighting_technique.cpp:279)
void LightingTechnique::SetPointLights(unsigned int NumLights, const PointLight* pLights)
{
    glUniform1i(m_numPointLightsLocation, NumLights);

    for (unsigned int i = 0 ; i < NumLights ; i++) {
        glUniform3f(m_pointLightsLocation[i].Color, pLights[i].Color.x, pLights[i].Color.y, pLights[i].Color.z);
        glUniform1f(m_pointLightsLocation[i].AmbientIntensity, pLights[i].AmbientIntensity);
        glUniform1f(m_pointLightsLocation[i].DiffuseIntensity, pLights[i].DiffuseIntensity);
        glUniform3f(m_pointLightsLocation[i].Position, pLights[i].Position.x, pLights[i].Position.y, pLights[i].Position.z);
        glUniform1f(m_pointLightsLocation[i].Atten.Constant, pLights[i].Attenuation.Constant);
        glUniform1f(m_pointLightsLocation[i].Atten.Linear, pLights[i].Attenuation.Linear);
        glUniform1f(m_pointLightsLocation[i].Atten.Exp, pLights[i].Attenuation.Exp);
    }
}
```
此函数通过迭代遍历数组元素并依次传递每个元素的属性值，然后使用点光源的值更新着色器。 这是前面所说的“方法1”。

本教程的Demo显示两个点光源在一个场景区域中互相追逐。一个光源基于余弦函数，而另一个光源基于正弦函数。该场景区域是由两个三角形组成的非常简单的四边形平面，法线是一个垂直的向量。 


