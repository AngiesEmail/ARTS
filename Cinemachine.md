##学习
* Virtual Camera 
	* 普通虚拟相机。
* FreeLook Camera
	* 自由查看相机。可以保证镜头内出现头和身体，以及相机的活动范围在目标周围圆柱（曲面）表面，常用于第三人称视角。
* State-driven Camera
	* 状态驱动相机。 

## 使用步骤
* 相机管理工具，可以制作电影和动画。
* 将Cinemachine导入工程中
* 导入一个人物
* 新建一个3d Plane。
* 给Camera增加一个Component ``Cinemachine Brain``
* 点击菜单栏中的Cinemachine，点击Create Virtual Camera 命名为A
* 选中创建好的Virtual Camera，然后把人物拖到面板中的Follow，再把相机调整到角色的前面，对准角色
* 再增加一个虚拟相机，命名为B
* 把角色的Body节点拖到B的Look At上，并调整相机位置
* 写一个脚本控制人物移动
* 用Timeline把 A B 这两个相机结合起来。
* 打开Timeline窗口
* 新建一个空物体，命名为Timeline
* 点击Timeline窗口中的create,然后点击保存，并删除默认的Timeline组件设置
* 点击Add，选择Animation Track ，然后把角色拖进选项框中。
* 右键点击拖进来的角色，选择Add From Animation Clip，并双击角色的行走动画。
* 拉长动画
* 把Main Camera拖进Timeline窗口的左边部分，出现菜单栏，选择Cinemachine Track。
* 右键Timeline中的Main Camera，选中Add Cinemachine Shot Clip.
* 点击出现的CinemachineShot，查看检视面板
* 把摄像机A拖到检视面板的Virtual Camera中
* 右键Timeline中的Main Camera，选中Add Cinemachine Shot Clip.
* 点击出现的CinemachineShot，查看检视面板
* 把摄像机B拖到检视面板的Virtual Camera中
* 运行查看效果

## 总结
* 需要两个虚拟的摄像机
* 需要角色
* 需要将角色绑定到虚拟的摄像机中
* 需要使用Timeline将两个虚拟摄像机结合起来