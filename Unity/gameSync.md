# 状态同步

* 属性同步
* 数据驱动表现
* 客户端需要将操作的属性发送给服务器，服务器将操作属性分发给对应客户端，客户端跟给定的属性，更新属性以及表现
* 状态同步，可以根据服务器下发的属性值，根据变化值比较，做lerp，如果差值较大，可以直接更改为对应的状态。
* 属性以服务器为准，作弊不容易

# 帧同步

* 操作同步
* 操作驱动表现以及属性
* 将操作同步对应客户端，根据操作，更改属性，对应驱动表现
* 帧同步：逻辑与表现分离开
* 更改后的数据与之前的数据做差值，平滑表现状态