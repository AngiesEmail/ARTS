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

## 常见问题
## 高级