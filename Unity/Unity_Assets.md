# Unity Manual 用户手册 
## [User Guide 用户指南](http://www.ceeger.com/Manual/index.html)
* Asset Import and Creation 资源导入与创建	
	* 基本介绍
		* 资源：纹理、模型、声音效果和行为脚本
		* Project:展示了项目资源文件夹中的文件组织架构
		* Hints 提示
			* 可以为资源添加标签，可在项目视图中利用搜索字段搜索到每个相关标签的资源
			* 备份项目文件夹时，会同时备份库和资源文件夹。库文件夹包含所有的元数据和对象之间的所有连接，如果库文件丢失，将丢失从场景到资源的参照。最简单的是备份包含资源和库文件夹的全部项目文件夹
			* 在项目视图中重命名和移动资源，不会破坏连接
			* 永远不要从Finder或其他程序重命名或移动任何东西，一切都会被破坏。
			* Unity为每个资源存储了大量的元数据，如果从Finder中移动一个文件，Unity将不再为移动的文件关联元数据。
	* Primitive Objects 基本对象
		* Unity可以运行由建模软件创建的任意3D模型。也有可以直接在Unity创建的基本的对象类型，如立方体、球体、胶囊、圆柱体、平面和四边形。可以用作占位符。
		* Cube 立方体：贴图会使图像在六个面上重复。
		* Sphere 球体：贴图使整个图像的顶部和底部的“夹持”在两极环绕一周。
		* Capsule 胶囊：圆柱体并在两端带有半球形盖。贴图使得图像夹在每个半球的顶点环绕一周。
		* Cylinder 圆柱：纹理是图像包围一周的桶状和两端的平面。
		* Plane 平面：可用于做地板和墙壁以及平整的表面。有时可以再GUI和特殊效果展示图像或电影。包含200个三角形。
		* Quad 正方形：包含两个三角形。可以实现简单的GUI和信息显示
	* Importing Assets 导入资源
		* Unity 自动检测添加到项目文件夹的资源文件夹中的文件。
		* ``Never move any assets or organize this folder from the Explorer or Finder. Always use the Project View``
		* Creating and Updating Assets 创建和更新资源
		* Asset Types 资源类型
			* 有少数基础的资源类型将进入你的游戏：
				* Mesh Files & Animations 网格文件&动画
					* 无论使用哪种3D软件，Unity将从每个文件导入网格和动画。
					* 网格将随UV和一些默认材质被导入
					* 可以给材质分配适当的纹理文件
				* Texture Files 纹理文件
					* 纹理被导入后，可以给材质添加纹理。
					* 材质可以应用到网格、粒子系统、GUI纹理。
					* 也可特殊设置为立方体贴图或法线贴图。
					* [纹理组件](http://www.ceeger.com/Components/class-Texture2D.html)
				* Sound Files 声音文件
					* 支持两种类型的音频:无压缩音频、Ogg Vorbis（有损的音频压缩技术）
					* OGG可以再相对较低的数据速率下实现比MP3更好的音质
					* .AIFF 转换为无压缩音频导入，最适合短音效果。可以在编辑器中按需求压缩。
					* .WAV 转换为无压缩音频导入，最适合短音效果。可以在编辑器中按需求压缩。
					* .MP3 转换成Ogg格式导入，最适合较长的音乐曲目。
					* .OGG 压缩音频格式，最适合较长的音乐曲目。  与iPhone设备不兼容，请使用MP3压缩格式代替。与某些Android设备不兼容，因此Unity不支持在Android平台使用这种格式。
					* [音频组件](http://www.ceeger.com/Components/class-AudioClip.html)
					* [音频源组件](http://www.ceeger.com/Components/class-AudioSource.html)
	* Models 模型