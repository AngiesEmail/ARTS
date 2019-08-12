# 教程 21 聚光灯光源

原文： http://ogldev.atspace.co.uk/www/tutorial21/tutorial21.html

CSDN完整版专栏： http://blog.csdn.net/column/details/13062.html

## 背景
聚光灯光源是目前这里要介绍的第三种也是最后一种光源类型了，它比平行光和点光源要复杂，但聚光灯光源其实是具有平行光和点光源核心特征的一种特殊光源。聚光灯光源也会随着距离衰减，但它不是像点光源照向四面八方的而是像平行光那样有一个聚光方向（相当于取点光源的一个锥形的一小部分），聚光灯光源呈锥形，因此有一个新的属性，就是离光源越远，照亮的圆形区域会越大（光源位于锥形体的尖端）。聚光灯光源，顾名思义，对应于现实中的聚光灯，例如：手电筒。在游戏中，聚光灯主要用于某些场景，例如：主角拿着手电筒在黑暗的地道里探索或者逃离监狱。

我们已经知道了创建聚光灯光源的所有技术，这里最后还要另外学一下如何实现这个光源类型的锥形效果。如下图：

图中垂直指向地面的黑色尖头指的是光源方向，这里想实现让光源只照亮两条红线夹角之间的区域，这里仍然可以使用点积来实现。我们可以定义光锥为光线方向L和红线之间的那个夹角（两条红线之间夹角的一半）。计算那个夹角的余弦值‘C’（点积计算得到）以及L和V夹角的余弦，其中V指的是光源到某个像素的向量，如果后者的值大于余弦值‘C’（夹角越小余弦越大），说明L和V之间的夹角偏小，该像素就位于被照亮的区域内。反之，像素位于区域外就不会被该光源照亮。
如果我们紧紧按照上面说的在照亮区域内就点亮像素，否则就不点亮，那样就会看上去非常假，因为照亮区域和未照亮区域之间的边界边缘会非常明显（没有一个自然的过渡），看上去会是一个清晰的圆形画在一个黑色区域（如果没有其他光源的话）。一个真实的聚光灯光源会从照亮区域的中心向圆形边缘慢慢衰减。这里我们可以利用上面计算得到的那些点积作为一个衰减的参数。首先我们知道，当L和V两个向量相等重合时，点积为‘1’。但是用余弦来做衰减参数会有问题，因为聚光灯光源的夹角不能太大，否则范围太广就失去了聚光灯的效果，但是在夹角从0到一个比较小的角度范围内，cos值得变化是很缓慢的，导致衰减不明显。例如:让聚光灯的夹角为20度，余弦值就为0.939，[0.939,1.0]这个变化范围就不好作为衰减参数了，在这个范围内进行插值的空间不足，造成的衰减程度不足以让眼睛察觉到。要想衰减效果明显这个参数范围应该是[0,1]。解决方法是将这个参数的小范围映射到[0,1]的范围，方法如下：

原理很简单：计算大的范围和小的范围的比例，然后根据那个比例对小范围进行映射扩张即可。

## 源代码详解

```
(lighting_technique.h:68)
struct SpotLight : public PointLight
{
    Vector3f Direction;
    float Cutoff;

    SpotLight()
    {
        Direction = Vector3f(0.0f, 0.0f, 0.0f);
        Cutoff = 0.0f;
    }
};
```
聚光灯光源的结构体继承自点光源的结构体，并添加了两个属性和点光源区别开：一个是光源的方向向量，另一个是截断光源照亮范围的一个阈值。阈值代表的是光源方向向量和光源到可照亮像素之间的最大夹角。比这个阈值夹角大的像素是不会被该光源照亮的。这里还在LightingTechnique类中为shader添加了一个位置数组，用来获取shader中的聚光灯光源数组。

```
(lighting.fs:39)
struct SpotLight
{
    struct PointLight Base;
    vec3 Direction;
    float Cutoff;
};
...
uniform int gNumSpotLights;
...
uniform SpotLight gSpotLights[MAX_SPOT_LIGHTS];
```
在GLSL中有一个聚光灯光源类型的类似的结构体。由于这里我们不能够在C++代码中进行继承，所以这里将一个点光源结构体对象作为一个成员对象变量，并在后面添加新的属性。有一个不一样的地方是在C++代码中那个阈值是夹角本身，而在shader中这个阈值是那个夹角的余弦值。shader着色器只关心夹角的余弦值，因此计算一次并存储比为每一个像素都重新计算余弦值要高效得多。这里还定义了一个聚关灯光源的数组，并使用一个叫做’gNumSpotLights’的计数器来限制允许应用去创建使用的聚光灯光源的数量。

```
(lighting.fs:85)
vec4 CalcPointLight(struct PointLight l, vec3 Normal)
{
    vec3 LightDirection = WorldPos0 - l.Position;
    float Distance = length(LightDirection);
    LightDirection = normalize(LightDirection);

    vec4 Color = CalcLightInternal(l.Base, LightDirection, Normal);
    float Attenuation = l.Atten.Constant +
        l.Atten.Linear * Distance +
        l.Atten.Exp * Distance * Distance;

    return Color / Attenuation;
}
```
点光源的函数有了轻微的改动：将一个点光源的结构体作为一个参数，而不是直接获取全局数组。这样更容易将它分享给聚光灯光源对象使用。其他的这里没有做改动。

```
(lighting.cpp:fs)
vec4 CalcSpotLight(struct SpotLight l, vec3 Normal)
{
    vec3 LightToPixel = normalize(WorldPos0 - l.Base.Position);
    float SpotFactor = dot(LightToPixel, l.Direction);

    if (SpotFactor > l.Cutoff) {
        vec4 Color = CalcPointLight(l.Base, Normal);
        return Color * (1.0 - (1.0 - SpotFactor) * 1.0/(1.0 - l.Cutoff));
    }
    else {
        return vec4(0,0,0,0);
    }
}
```
这里这个函数是我们计算聚光灯光源效果的地方。首先得到光源到某个像素的向量，将向量单位化方便点积运算，然后和单位化了的光源方向向量进行点积运算得到他们之间夹角的余弦值。将得到的余弦值和光源的阈值（定义光源范围的最大夹角的余弦值）进行比较，如果余弦值比阈值小，说明夹角太大像素在照亮圆区域的外面，这样像素就不会被该光源点亮。这样那个阈值就可以将聚光灯光源的照亮范围限制在一个大的或者小的圆圈内。反之如果像素在照亮区域内，我们就先像点光源那样计算光源的基础颜色。然后将那个点积计算得到的参数’SpotFactor’放到上面的公式中，将这个参数线性插值到0到1的范围，最后和点光源颜色相乘计算得到最终的聚光灯颜色值。

```
(lighting.fs:122)
...
for (int i = 0 ; i < gNumSpotLights ; i++) {
    TotalLight += CalcSpotLight(gSpotLights[i], Normal);
}
...
```
和点光源的计算模式一样我们在主函数通过循环遍历累加所有聚光灯光源的效果得到对应像素的最终颜色值。

```
(lighting_technique.cpp:367)
void LightingTechnique::SetSpotLights(unsigned int NumLights, const SpotLight* pLights)
{
    glUniform1i(m_numSpotLightsLocation, NumLights);

    for (unsigned int i = 0 ; i < NumLights ; i++) {
        glUniform3f(m_spotLightsLocation[i].Color, pLights[i].Color.x, pLights[i].Color.y, pLights[i].Color.z);
        glUniform1f(m_spotLightsLocation[i].AmbientIntensity, pLights[i].AmbientIntensity);
        glUniform1f(m_spotLightsLocation[i].DiffuseIntensity, pLights[i].DiffuseIntensity);
        glUniform3f(m_spotLightsLocation[i].Position, pLights[i].Position.x, pLights[i].Position.y, pLights[i].Position.z);
        Vector3f Direction = pLights[i].Direction;
        Direction.Normalize();
        glUniform3f(m_spotLightsLocation[i].Direction, Direction.x, Direction.y, Direction.z);
        glUniform1f(m_spotLightsLocation[i].Cutoff, cosf(ToRadian(pLights[i].Cutoff)));
        glUniform1f(m_spotLightsLocation[i].Atten.Constant, pLights[i].Attenuation.Constant);
        glUniform1f(m_spotLightsLocation[i].Atten.Linear, pLights[i].Attenuation.Linear);
        glUniform1f(m_spotLightsLocation[i].Atten.Exp, pLights[i].Attenuation.Exp);
    }
}
```
这个函数根据聚光灯光源的结构体数组来继续更新着色器程序，基本上和点光源中对应的这个函数一样，除了额外又添加了两个参数，光的方向单位化后也传给了shader，另外那个阈值夹角装换成它的余弦值之后也传给了shader（方便shader直接用它和点积运算的结果进行比较）。注意库函数cosf()使用的是弧度值参数，是先用ToRadian宏将角度转换成的弧度值。 


