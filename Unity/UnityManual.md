# Unity Manual 用户手册
## User Guide 用户指南
* Unity Basics
	* Learning the interface
		* Project Browser
		* Hierarchy
		* Toolbar
		* Scene View
		* Game View
		* Inspector
		* Other View
	* Customizing Your Workspace 自定义工作区
	* Asset Workflow 资源工作流程
		* 3D mesh ：3D 网格
		* 3D 建模软件：Maya、3ds max
		* 将资源放置到项目文件夹的资源文件夹中，打开unity时，资源会被检测并导入到项目中。
		* Unity会使用FBX输出模型组件将导入的模型转换为FBX格式。需要有这个输出组件或者可以使用建模软件将模型直接导出格式为fbx，导入到unity中。
		* Import Settings 导入设置
			* 选中导入的资源，在检视面板中，会显示导入的设置。注意：设置的选项是以资源的类型为基础的。（不同的资源有不同的导入设置）
		* Adding Asset to the Scene
			* 如果需要使用一个纹理或声音文件，必须将它添加到一个已存在于场景或项目中的游戏对象上。
		* Putting Different Assets Together 
			* A texture is spplied to a Material 纹理应用于材质
			* A Material is applied to a GameObject(With a Mesh Renderer Component) 材质应用于带有网格渲染组件的游戏对象
			* An Animation is aoolied to a GameObject(with an Animation Component)动画应用于带有动画组件的游戏对象
			* A Sound file is applied to a GameObject(with an Audio Source Component) 声音文件应用于带有音源组件的游戏对象
		* Creating a Prefab 
			* Prefab(预置)：就是一个游戏对象及其组件的集合。几个相同的对象可以通过一个单一的预置来创建，叫做实例化。
		* Updating Assets 更新资源
			* 选择需要更改的资源，在项目视图中双击，将会启动相应的程序，可以做任何更改。完成更改之后，点击保存。
		* Optional - Adding Labels to the Assets 给资源添加标签。	
			* 如果想让资源组织有序，可以为资源添加标签。通过标签，可以在项目视图中或对象选择器中与搜索字段相关的每个资源的标签。  
			* 添加标签：
				* 在项目视图中，选择想要增加标签的资源
				* 可以选择已有的标签，也可以增加新的标签
				* 一个资源可以有多个标签
				* 在输入标签名称时，空格或者回车，就可以分割或者创建标签。
	* Creating Scenes
		* Working with Cameras 使用相机
			* 相机是游戏的眼睛。玩家看到的一切都是通过一个或多个摄像机播放的。可以像其他游戏对象一样来设置摄像机的位置、旋转、及父节点。
			* 相机是附加了相机组件的游戏对象，因此可以做其他普通游戏对象可以做的事情，并且还有一些相机特有的功能。还有一些有用的摄像机脚本，是随着在标准资源包一起安装的。
			* Component->Camera-Control
		* Lights 光源
			* 定向光源
			* 点光源
			* 聚光
	* 编译发布 Publishing Builds
		* 每个场景都有不同的索引值。想要载入一个新的场景，在脚本中使用Application.LoadLevel()函数
		* Development Build
			* 将启用Profiler功能，也使Autoconnect Profiler和Script Debugging选项可用。
		* CanStreamedLevelBeLoaded()检查已完成数据流的关卡
		* GetStreamProgressForLevel() 获取关卡数据流的进展情况。
		* Offline webplayer deployment 离线部署网络播放器
			* UnityObject.js
		* Building standalone players 创建独立游戏
			* Intel、PowerPc、Universal mac系统使用的处理器
		* Inside the build process 内部生成过程
			* 在创建过程中，会把一个游戏程序的空白副本放到指定的地方。然后，通过使用发布设置中的场景列表，在编辑器中依次打开它们，对其进行优化，整合到程序包中。还将计算包括场景在内的所有资源数据，并存储到程序包里的一个单独文件中。
			* EditorOnly 标签的游戏对象，不会包含在发布的作品中。
			* DontDestoryOnLoad()
			* OnLevelWasLoaded()
			* Scripting Tutorial
				* 如果创建一个更好的游戏：主菜单、记分屏、当前关卡显示。
		* iOS
			* Inside the iOS build process iOS内部编译过程
				* XCode 工程被生成，并附带所有所需的库、预编译.NET代码以及已序列化的资源。
				* XCode 项目构建并在实际的设备上部署。
			* 第一步:在Build settings 对话框点Build
			* 第二步:点Build and Run
			* replace 替换-从目标文件夹所有文件被删除并生成新的内容。
			* append 追加-Data、Libraries和项目根文件夹被清空，并填充新生成的内容。XCode项目文件根据罪行的Unity项目变更进行更新。XCode项目Classes子文件夹被视为安全的地方，可放置自定义的本机代码，但建议定期备份。追加模式仅支持现有的XCode项目，带有有相同的Unity iOS版本生成。
			* CMD+B： 默认追加模式 
		* Android 
			* 生成所有需要的库和序列化资源的应用程序包（.apk文件）
			* 在实际设备上部署应用程序包
			* 当第一次尝试建立一个Android项目，Unity会询问查找Android SDK，这需要在设备上安装Android应用程序。可以以后再首选项中更改此设置。
			* 当编译应用到Android上，确保设备设置USB Debugging和Allow mock locations复选框被选中。
			* Texture Compression 纹理压缩
				* 在编译设置，还会发现纹理压缩选项。默认，Unity默认使用ETC1/RGBA16纹理格式。
				* 如果想生成一个应用程序包（.apk文件）针对一个特定的硬件架构，可以使用纹理压缩来覆盖默认的行为。任何纹理使用纹理格式覆盖将保留格式；仅纹理设置为自动压缩将使用纹理压缩选项中选择的格式。
				* 确保应用程序部署的设备支持选择的纹理压缩格式，unity将编辑AndroidManifest包含标签匹配所选的特定格式。这将启用Android Market filtering mechanism 过滤机制，仅用于带有相应图形硬件的设备启用应用程序。
		* Preloading 预加载
			* 发布的作品将在加载场景时自动预装场景中的所有资源。scene 0是例外，这是因为第一个场景通常是一个启动画面，你要尽可能快地显示它。
			* 要想确保所有内容完成预加载，可以创建一个空场景调用Application.LoadLevel(1)，在发布设置里让这个空场景的索引为0，这样所有后续关卡将会预加载。
	* Tutorials 教程
		* GUI Essentials
		* Scripting Essentials
	* Unity3D快捷键 Unity HotKeys
		* [UnityHotkeys](http://www.ceeger.com/Manual/UnityHotkeys.html)
		* shift Del 删除
		* F frame selected选择的帧
		* ctrl + p play
		* ctrl + shift + P pause
		* ctrl + alt + P step 停止
		* ctrl + shift + N 新建空游戏对象 
		* ctrl + alt + F Move to view 移动到视图
		* ctrl + shift + F Align with view 视图对齐
	* Preferences 首选项
		* 可以自定义编辑器的行为
		* General 
			* Auto Refresh 自动刷新
				* 当资源改变时，编辑器自动更新资源
			* Always Show Project Wizard
				* 启动时，是否显示项目向导
			* Compress Assets On Import
				* 导入时，资源是否自动被压缩
			* OSX Color Picker OSX 拾色器
				* 是否用本地OSX拾色器替代Unity
			* Editor Analytics 编辑器分析
				* 自动发送信息给Unity
			* Verify Saving Assets
				* 退出时，是否需要确认资源是否存储
			* Skin(Pro) 皮肤
		* External Tools 外部工具
			* External Script Editor
				* 选择使用哪个应用程序打开脚本文件
			* Editor Attaching 
				* 是否允许从外部脚本编辑器来调试控制
			* Image Application 
				* 使用哪个应用程序打开图片文件
			* Asset Server Diff Tool
				* 使用哪个应用程序比较资源服务器的文件异同
			* Android SDK Location
				* Android SDK 文件夹位置
			* iOS Xcode 4.x support 
				* 启用支持Xcode 4.x为iOS编译目标
		* Color 
		* Keys 快捷键
		* Cache Server 缓存服务器
			* Use Cache Server 是否启用缓存服务器
			* IP Address 启用时的，缓存服务器的地址
* Build Scenes
	* GameObject
		* The GameObject-Component Relationship
		* Using Components
			* 组件是每个游戏对象的功能零件
			* 一个游戏对象是许多不同组件的容器
			* 粒子系统：粒子发射器、粒子动画、粒子渲染器 创建一个运动粒子的群集。
			* 属性：赋值属性和引用属性
			* 组件的引用属性可以包含任何类型的组件、游戏对象、资源。
			* 在运行状态更改的属性，停止运行后，属性回归初始状态。
		* The Component-Script Relationship
			* 当创建了一个脚本，并将其附加到一个游戏对象上，脚本将出现在游戏对象的检视视图中。脚本也是一种组件。
			* 脚本中的属性可以显示在检视面板中，游戏对象会执行脚本的功能。
		* Deactivating GameObjects 停用游戏对象
			* 游戏对象名称前的复选框
			* 脚本调用activeSelf
			* Effect of deactivating a parent GameObject
				* 子节点会继承父节点的停用属性。
				* activeInHierarchy 属性，会基于父对象的状态获取
				* SetActiveRecursively 但是不会保存子节点的初始状态
	* Using the Inspector
	
		```
		检视面板用于查看和编辑不同类型的属性
		检视面板可以显示以及提供编辑游戏对象的属性和所有组件及材质
		检视面板也用于显示资源的导入选项：纹理、三维模型、选择字体。
		所有的设置管理器。
		检视面板中显示的任何属性都可以直接修改，两种主要类型的属性：赋值属性和参照（引用）属性
		```
		* Editing Value Properties 编辑赋值属性
		
			```
			值属性不能引用任何东西，可以直接编辑。
			数字、复选框、字符串、切换开关、字符串、选择弹出窗口、颜色、向量、曲线及其他类型。
			```
			* Color Picker 拾色器
				* 颜色类型的属性将打开拾色器。
			* Curve Editor 曲线编辑器
				* AnimationCurve(动画曲线)，将打开曲线编辑器。
				* 可以选择现有的曲线或者创建新的
				* 现有的曲线是保存在预置中的。
				* 可以在脚本运行时进行取值
				* Presets 可以使曲线设置为默认的形状
				* Preset Libraries 预设库
					* 预设库包含用户创建的数据和一段时间的留存。集成在拾色器、渐变编辑器和曲线编辑器。
					* 预设是如颜色、渐变或用户保存的动画曲线。
					* 预设库是保存到一个文件中的预设集合。
					* 预置库包含个人数据或项目数据。可以将他们保存在用户偏好文件夹或Assets文件夹中的"Editor"文件夹
					* 项目预设库可以被添加到版本控制
					* 项目预设库也可以添加到资源商店包。
					* [如何创建颜色预设](http://www.ceeger.com/Manual/PresetLibraries.html)
		* Assigning References 指定引用
			* 引用（参照）属性是这样一种属性，它可以引用其它对象如游戏对象、组件或资源。
			* 引用槽(输入框)会显示可以用于此位置的对象种类。
			* 可以通过拖放或者使用对象选取器两种方式给一个引用（参照）属性指定对象。
			* 在资源上使用标签，将能够使你在对象选取器中利用搜索字段更容易找到它们。
			* 如果你不想看到对象的描述，可以向下拖动预览窗口底部中间的滑块。
			* 如果想看到对象的详细预览，可以通过拖动在预览窗口底部中间的滑块来放大对象预览。	  
			
		* Multi-Object Editing 多重对象编辑
			* 可以在检视面板中同时选择和编辑多个类型相同的对象
			* 任何修改过的属性都会被应用到选中的对象上。
			* 在选择多个对象时，在检视面板上只有那些在所有被选中的对象上出现的组件才会被显示出来。
			* Property Values 属性值
				* 当多个对象被选中后，在检视面板上显示的每个属性都代表被选中对象的属性。如果所有对象上的属性值都相同，那么这个值会被正常显示，就好像在编辑单个对象一样。但如果属性值在被选中对象上都不同，那么没有值被显示而是用短划线之类取代显示来说明这些值是不同的。
				* 如果这些属性值不同从而被显示为短划线，仍然可以在属性标签上右击，从而弹出一个菜单悬浮框，可以选择从哪个对象上继承属性值。
			* Multi-Editing Prefab or Model Instances 多重编辑预设或者模型实例
				* 当编辑单个预设或模型的实例时，任何和预设或模型不同的属性都会以粗体显示，右击鼠标会有一个用来从预设或模型中恢复属性值的选项。
				* 游戏对象有选项可以用来应用或恢复所有的更改。
				* 在多重编辑时：属性不能被恢复或应用、和预设或模型不同的属性不会以粗体显示。
				* 检视面板会提示实例管理失效，然后恢复和应用按钮会出现。
			* Non-Supported Objects 不被支持的对象
				* 少数对象类型不支持多重编辑。当同时选择多个对象时，会提示：多重对象编辑不被支持
				* 如果使用编辑器编辑自己的脚本，如果不支持多重编辑，也会提示这个消息。
				* [编辑器类 查看如何支持多重编辑](http://www.ceeger.com/Script/Editor/Editor.html)
		* Inspector Options 检视面板选项
			* 检视锁定和检视调试模式是两个有用的选项，在工作流中很有帮助。
			* Lock 锁定选项
				* 锁定选项可以在选择其他游戏对象时，保持焦点在检视视图中的特殊的（明确的）游戏对象上。
				* 切换检视视图的锁定选项，在检视视图上面点击锁定/解锁图标，或打开标签菜单选择Lock 锁定
				* 可以同时打开多个检视视图
			* Debug调试模式
				* 调试模式可以在检视视图中查看组件的私有变量，通常它们不会显示。
				* 打开标签菜单，选择Debug
				* 调试模式可以检查脚本和其他组件的私有变量。
	* Using the Scene View 使用场景视图
		* Scene View Navigation 场景视图导航
			* 导航控制集
			* Arrow Movement 方向键移动
				* 上下->面对自己的向前向后方向
				* 左右->横向平移
				* shift 加速
			* Focusing 聚焦
				* 选择一个游戏对象，按住F键，场景视图将以所选对象为中心点（即框选）
			* Orbit、 Move、 Zoom 旋转、移动、缩放
				* Mouse 鼠标
					* Orbit:按住Alt键并拖动鼠标将绕当前轴点旋转镜头
					* Move:按住Alt键和鼠标滚轮并拖动进行镜头平移（实际使用中，无需按下Alt键也可实现效果）
					* Zoom：按住Alt键并拖动鼠标右键来缩放镜头
				* 对于两键鼠标或触控板，按住Alt-Control（Alt-Command）并左键将激活移动操作
				* mac中Control+Alt并左键将激活缩放操作
				* 鼠标滚轮可以用来缩放视图
				* Flythrough Mode 漫游模式
					* 按住鼠标右键；
					* WASD控制前后左右
					* QE控制上下移动
					* shift 加速
				* Scene Gizmo 场景手柄工具
					* 显示了场景视图当前视角方向，可以用其来快速修改视角。
					* 可以点击它的方向杆，更改场景成为该方向的正交模式。
					* 在正交模式中，可以鼠标右键拖动来旋转，也可Alt+鼠标左键拖动平移
					* 点击手柄中间的小方框，可退出正交模式
					* 可以按住shift并点击手柄中间的小方框来切换正交模式
					* 正交模式：对象不会因为距离远而变小
					* 透视模式：对象远近会影响大小
				* Mac 触控板
					* 可以两指拖拽来缩放视图
					* 三指来模拟gizmo效果：拖上、左右、下分别激活顶、右、前、透视图
		* Positioning GameObjects 定位游戏对象
			* Focusing 聚焦
				* 选中对象，点击F
			* Translate Rotate and Scale 移动、旋转、缩放
				* W 平移 E 旋转 R 缩放
			* Gizmo Display Toggles 显示切换器
				* 用来限定TransformGizmo的位置
				* Position 位置
					* Center 将在对象范围的中心位置提供Gizmo
					* Pivot 将在一个网格的实际轴点位置放置Gizmo
				* Rotation 旋转
					* Local 将相对于对象保持Gizmo的旋转
					* Global 将强制Gizmo为世界空间的方向
			* Unit Snapping 捕捉单位
				* 当你使用移动工具拖动Gizmo的方向轴时，可以按住Control键（Command），以捕捉在设置中定义的增量（拖动的限制，只能是设置的倍数，只在鼠标移动的情况下生效）
				* Edit->Snap Settings
			* Surface Snapping
				* 使用移动工具在中心拖拽时， 可以按住shift和ctrl（mac中的command）来让对象与任何碰撞体的交叉点对齐。可更精确的定位对象。
			* Look-At Rotation
				* 使用旋转工具时，可以按住shift和ctrl旋转对象朝向任何碰撞体表面的一个点。使得一个对象相对于另一对象的定向变得更简单。
			* Vertex Snapping 顶点捕捉
				* 可以将一个对象的顶点放置到选择的其他网格的顶点上
				* 选择想要操作的网格，激活变换工具
				* 按住V键激活顶点捕捉模式
				* 移动光标到想用作轴心的网格顶点上
				* 鼠标移到想要的顶点上，按住鼠标左键，拖动网格紧贴于另一网格的任意顶点。
				* 对结果满意时，松开鼠标按键和V键
				* shift-V 可以切换这个功能
				* 可以捕捉顶点到顶点，顶点到表面和轴心到顶点。
		* View Modes 视图模式
			* 场景视图控制条，可以查看场景的各种选项，可以控制灯光、音频。
			* Draw Mode 绘图模式
				* Textured 纹理：显示可见纹理表面
				* Wireframe 线框：用线框绘制网格
				* Tex-Wire 纹理-线框：显示网格纹理并有线框覆盖
				* Render Paths: 渲染路径：显示每个对象使用颜色代码的渲染路径：绿色代表延时光照，黄色表示正向渲染，红色表示顶点光照
				* Lightmap Resolution:光照贴图分辨率：在场景上覆盖棋盘格来显示光照贴图的分辨率。
			* Render Mode 渲染模式
				* RGB 渲染场景具有物体的正常颜色
				* Alpha 渲染颜色带有alpha
				* Overdraw 作为透明物体的“剪影”渲染物体。透明颜色累加，容易找出一个物体绘制到另一个物体上边
				* Mipmaps 使用颜色代码显示理想的纹理尺寸；红色表示纹理大于所需尺寸（在当前的距离和分辨率下），而蓝色表示纹理可以更大。理想的纹理尺寸依赖于游戏运行的分辨率，以及相机可以离特定表面的距离。
			* Scene Lighting , Game Overlay, and Audition Mode
				* 场景光照、游戏覆盖、试听模式 
				* 场景光照：使用默认光照方案、使用场景中的灯光
				* 游戏覆盖：控制天空盒和GUI元素是否在场景中渲染，以及显示和隐藏布局网格。
		* Gizmo and Icon Display Controls Gizmo和图标显示控制
			* Gizmos和Icon的选项，可以用来减少场景的混乱以及改善场景在开发过程中的视觉清晰度。
			* The Icon Selector 图标选择器
				* 可以在场景视图和检视面板中为游戏物体和脚本设置自定义图标
				* 标签图标是特殊种类的图标
				* 在场景视图中，会使用游戏物体的名字作为一个文本标签。
				* 图标为内置组件，不能被修改
			* Showing and Hiding Icons and Gizmos 显示隐藏图标和Gizmo
				* 单独的组件gizmos的可见度，取决于该组件在检视面板中是否被展开（折叠的组件是不可见的）
				* gizmos和图标，有助于减少视觉混乱
				* 可在Gizmos中设置图标以及gizmos的可见性
				* 脚本显示在Scripts区域，有一个自定义图标或者OnDrawGizmos()或OnDrawGizmosSelected()函数执行
				* 3D Gizmos 滑动条可以用来调节图标在场景显示的大小。图标会根据距屏幕的距离来缩放，当图标靠近屏幕一定近距离时会渐隐。取消勾选3D Gizmos，图标将前置并始终保持一定大小。
	* Searching 搜索
		* 点击搜索下拉菜单，可选择：All,Name,Type
		* Object Picker Search 对象选择器搜索
	* Prefabs 预制
		* 预制是资源类型：可重复使用的游戏对象。
		* 所有的预制实例都链接到原始预制
		* 更改预制，所有的实例都将生效
		* 预制实例的属性可以更改，更改后，变量名变为粗体，可被重写。所有的重写属性不会影响预制源的变化。
		* 点击Apply，根的位置和旋转将不被应用，会将所有的实例放在同一个位置
	* Lights 灯光
		* 光源决定3D环境的颜色和氛围
		* 场景中可使用多个光源
		* Component->Rendering->Light 可为选定的游戏对象添加光源组件。
		* 实时光源：在游戏运行的每一帧都要进行计算。
		* 如果某个地方的光照不改变，可以使用光照贴图，加快游戏运行速度
		* Rendering paths 渲染路径
			* unity支持不同的渲染路径。渲染路径主要影响光和影，可以根据游戏的需求选择正确的合适的渲染路径，来提高项目性能
	* Cameras 摄像机
		* 场景中至少需要有一个相机在场景中，也可以有多个
		* 多相机可营造双人分屏效果或创建高级的自定义效果
		* 可使用物理组件控制相机，让相机动起来
		* 相机是为玩家捕捉和显示世界的一种装置
		* Properties 属性
			* Clear Flags清除标记
				* 决定屏幕的那部分将被清除
			* Background 背景
				* 在镜头中的所有元素描绘完成且没有天空盒的情况下，将选中的颜色应用到剩余的屏幕。
			* Culling Mask 剔除遮罩
				* 控制选择由相机渲染包含或忽略对象的层
			* Projection 投射 ： 切换摄像机的模拟透视功能
				* Perspective 透视：相机用完全透视的方式来渲染对象
				* Orthographic 正交： 相机将用没有透视感的方式均匀地渲染对象
					* 主要用于等轴游戏或2D游戏
					* 雾在正交相机模式下渲染，并不会如预期般出现。
					* [渲染设置](http://www.ceeger.com/Script/RenderSettings/RenderSettings.html) 
					* 对象不会因距离而变小
			* Size 设置正交时摄像机的视口大小
			* Field of View 视野范围：相机的视角宽度以及纵向的角度尺寸
			* Clipping Planes 剪裁平面：相机从开始渲染和停止渲染之间的距离
				* Near 近点：开始描绘的相对于相机最近的点
				* Far 远点：开始描绘的相对于相机最远的点
			* Normalized View Port Rect 标准视口矩形
				* 用四个数值来表示这个相机的视图将绘制在屏幕的什么地方，使用屏幕坐标系（0-1）
				* X: 相机视图将进行绘制的水平位置的起点
				* Y: 相机视图将进行绘制的垂直位置的起点
				* W: 相机输出到屏幕上的宽度
				* H: 相机输出到屏幕上的高度
			* Depth 深度
				* 绘图顺序中的相机位置，具有较大值的相机将被绘制在具有较小值的相机的上面
			* Rendering Path 渲染路径-渲染方法
				* Use Player Settings 使用Player设置中的渲染路径
				* Vertex Lit 顶点光照 所有的对象作为顶点光照对象来渲染
				* Forward 快速渲染 所有的对象将按每种材质一个通道的方式来渲染
				* Deferred Lighting 延迟照明 所有对象将无照明绘制一次，然后所有对象的照明将一起在渲染队列的末尾被渲染。
			* Target Texture 目标纹理
				* 包含了相机视图的输出。这个属性将禁用相机渲染到屏幕的功能。
		* Details细节
			* 可以给不同的相机分配不同的深度。相机按深度从低到高来绘制的。
		* Render Path
			* Unity 支持不同的渲染路径。渲染路径的选取取决于游戏内容以及目标平台、硬件。
			* 不同的渲染路径具有不同的功能和性能特点，主要影响光源和阴影。
		* Clear Flags 清除标记
			* 每个相机在渲染时会存储颜色和深度信息。屏幕的未绘制部分是空的，默认情况下会显示天空盒。
			* 使用多个相机时，每一个相机都将自己的颜色和深度信息存储在缓冲区中，还将积累大量的每个相机的渲染数据。
			* 当场景中的任何特定相机进行渲染时，可以设定清除标记以清除缓冲区信息的不同集合。可通过以下4个选项来设置
				* Skybox  默认的设置（当前相机的天空盒）
					* 如果没有天空盒，会默认使用渲染设置（Edit->Render Settings）中选择的天空盒
				* Solid Color 屏幕空的部分显示当前相机的背景颜色
		* Depth Obly仅深度
		* Don't Clear 不清除
			* 该模式不清除任何颜色或深度缓存。
			* 效果是：每帧绘制在下一帧之上，造成涂片效果
			* 最好与自定义着色器一起使用
		* Clip Planes 剪裁平面
			* 近平面是开始渲染的最近位置
			* 远平面则是最远位置
			* 剪裁平面也决定深度缓存精度如何在场景上分布。一般来说，要得到更好的精度，应该移动Near平面尽可能的远。
			* Near和Far剪裁平面连同相机视野的轮廓平面一起构成的区域俗称相机锥（棱台）。Unity在渲染时，不会渲染锥形区域外的对象（即 可视性剪裁）
			* 无论是否使用遮挡剔除，可视性剪裁都将发生。
			* 出于性能原因，需要尽早剔除小物体。可将小物体放入一个隔离层并使用Camera.layerCullDistances脚本函数设置每一层的剔除距离
		* Culling Mask 剔除遮罩
			* 使用层来有选择地渲染一组对象
			* 可把用户界面放到不同的层，然后用一个独立相机单独渲染UI层
			* 为了使UI显示在其他相机视角的顶部，需要设置清除标记为Depth only，并确保UI相机的深度比其他相机高。
		* Render Texture 渲染纹理（Pro）
			* 将放置相机的视图到一个纹理上，该纹理可以被应用到另一个对象。
			* 可方便的创建体育场大屏幕、监控摄像机、倒影等效果
		* Hints 提示
			* 相机可以像其他对象一样被实例化、父子化、脚本化
			* 为提高赛车游戏的速度感，提高视野范围
			* 可给相机增加一个刚体组件（Rigidbody），可用于物体模拟
			* 相机的数量没有限制
			* 正交相机可以很好的用于制作3D用户界面
			* 如果遭遇深度问题（表面互相接近闪烁），可尝试设置Near Plane 尽可能大
			* 相机无法同时渲染到屏幕和渲染纹理，只能有一个
			* Unity中有相机脚本(Components->Camera Control)
	* [Terrain Engine Guide 地形引擎指南](http://www.ceeger.com/Manual/Terrains.html)
		* [Using Terrains 使用地形](http://www.ceeger.com/Components/terrain-UsingTerrains.html)
		* [光照贴图快速入门]() 
* Asset Import and Creation 资源导入与创建

## 常见问题
## 高级