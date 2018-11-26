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

## 常见问题
## 高级