## 小程序项目一

## 1.小程序的配置

### 1.app.json全局配置

`app.json`文件用来对微信小程序进行**全局配置**，决定**页面的路径、窗口表现、设置网络超时时间、设置多 tab** 等。

> 注意：
>
> 1.配置文件所有的路劲前面不要写：./  ../
>
> 2.pages最后面的一个不能有 , 逗号 ;  其它类同 
>
> 3.配置文件都是以key : value 的字符窜形式

**app.json文件：**

```json
{
  //1.页面的路径
  "pages": [ 
    "pages/index/index",  //代表小程序的初始页面
    "pages/logs/index"
  ],
  //2.窗口表现
  "window": {
    "navigationBarTitleText": "Demo"
  },
  //3.设置多个 底部的tab
  "tabBar": {
    "list": [{
      "pagePath": "pages/index/index",
      "text": "首页"
    }, {
      "pagePath": "pages/logs/logs",
      "text": "日志"
    }]
  },
  //4.设置网络超时时间
  "networkTimeout": {
    "request": 10000,
    "downloadFile": 10000
  },
  //5.debug开发模式
  "debug": true
}
```

#### 1.pages 属性

接受一个数组，每一项都是字符串，来**指定小程序由哪些页面组成**。每一项代表对应页面的【路径+文件名】信息，**数组的第一项代表小程序的初始页面。小程序中新增/减少页面，都需要对 pages 数组进行修改。**

**文件名不需要写文件后缀**，因为框架会自动去寻找路径下 `.json`, `.js`, `.wxml`, `.wxss` 四个文件进行整合。

```json
 "pages": [ 
    "pages/index/index",  //代表小程序的初始页面 , 文件名不需要写文件后缀
    "pages/logs/index"
  ],
```

#### 2.*window 属性

用于设置小程序的状态栏、导航条、标题、窗口背景色。

```json
 "window":{
    "navigationBarBackgroundColor": "#06C1AE",  // 状态栏的背景
    "navigationBarTitleText": "首页",    // 状态栏中的文本
    "navigationBarTextStyle":"white",  //状态栏中的文本样式（仅支持 black/white）
    "navigationStyle":"custom",  //沉浸式导航栏
   
    "enablePullDownRefresh":"true",  //允许所有页面的下拉刷新，允许回调 onPullDownRefresh 这个函数
    "backgroundColor":"green",      //窗口的背景
    "backgroundTextStyle":"dark",  //下拉背景字体、loading 图的样式，仅支持 dark/light
    
    "onReachBottomDistance":"200rpx"  //距离内容的底部200rpx的时候回调onReachBotto这个函数
  }
```

 

#### 3.tabBar 属性

如果小程序是一个多 tab 应用（客户端窗口的底部或顶部有 tab 栏可以切换页面），可以通过 tabBar 配置项指定 tab 栏的表现，以及 tab 切换时显示的对应页面。

**Tip：**

1. 当设置 position 为 top 时，将不会显示 icon
2. tabBar 中的 list 是一个数组，**只能配置最少2个、最多5个 tab**，tab 按数组的顺序排序。

```json
  "tabBar": {
  	"color":"#989898",
    "selectedColor":"#FF6802",
    "list":[
      {
        "pagePath":"pages/index/index",
        "text":"首页",
        "iconPath": "pages/image/find_icon_nor.png",
        "selectedIconPath": "pages/image/find_icon_press.png"
      },
      {
        "pagePath": "pages/logs/logs",
        "text": "日志",
        "iconPath": "pages/image/find_icon_nor.png",
        "selectedIconPath": "pages/image/find_icon_press.png"
      }
    ]

  }
```

 

#### 4.networkTimeout 属性

> 默认超时时间为60 000

```json
 "networkTimeout":{
    "request":50000,
    "connectSocket":50000,
    "uploadFile":50000,
    "downloadFile":50000
  },
```

#### 5.debug 属性

可以在开发者工具中开启 debug 模式，在开发者工具的控制台面板，**调试信息**以 info 的形式给出，其信息有`Page的注册`，`页面路由`，`数据更新`，`事件触发` 。 可以帮助开发者快速定位一些常见的问题。

```
"debug":true
```



## 2.小程序的生命周期

> index   log    home

### 1. 页面的五个生命周期函数

1.当打开一个页面的时，执行下面的生命周期函数：

`onLoad  -->  onShow  -- > onReady`

2.当小程序切换到后台（例如：按下home建），执行：

`onHide`

3.当小程序切换到前台的时候，执行：

`onShow`

4.当页面被销毁的时候，执行：

`onUnload`



5.1当A页面**切换tabbar**到B页面的生命周期

```
A: onLoad  -->  onShow  -- > onReady  -->  onHide
B: onLoad  -->  onShow  -- > onReady
```

5.2.当B页面**切换tabbar**到A页面的生命周期

```
B: onHide   ***隐藏***
A: onShow 
```



6.1.当A页面**跳转**到B页面的生命周期(  以5.1一样 )

```json
A: onLoad  -->  onShow  -- > onReady  --> onHide
B: onLoad  -->  onShow  -- > onReady
```

6.2.当B页面**返回**到A页面的生命周期

```
B: onUnload  ***销毁***
A: onShow
```



```js
Page({
  /**
   * 1.生命周期函数--监听页面加载
   *  options ： 可以获取到上一个页面传递过来的参数
   */
  onLoad: function (options) {
    //一般在这里执行网络请求
    console.log('onLoad');
  },

  /**
   * 2.生命周期函数--监听页面显示
   */
  onShow: function () {
    console.log('onShow');
  },
  
  /**
   * 3.生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    //界面渲染完成后可以获取组件对象
    console.log('onReady');
  },

  /**
   * 4.生命周期函数--监听页面隐藏
   */
  onHide: function () {
    console.log('onHide');
  },

  /**
   * 5.生命周期函数--监听页面卸载
   */
  onUnload: function () {
    console.log('onUnload');
  },

})
```



### 2.App的生命周期函数

```js
App({
  onLaunch: function(options) {
    // Do something initial when launch.
    // options :包含打开小程序的路径，打开小程序的场景值 ...
  },
  onShow: function(options) {
      // Do something when show.
      // options :包含打开小程序的路径，打开小程序的场景值 ...
  },
  onHide: function() {
      // Do something when hide.
  },
})
```



## 3.界面的跳转

> index  log   home

navigator : 页面链接（**跳转**）。

> 注意：该组件默认**不能跳转到tabBar**上的界面 , 除非设置了 open-type='switchTab'

### 1.navigator 组件

| 属性名                                      | 类型     | 默认值             | 说明                                       | 最低版本       |
| ---------------------------------------- | ------ | --------------- | ---------------------------------------- | ---------- |
| **url**                                  | String |                 | 应用内的跳转链接 , **相对路径**                      |            |
| **open-type**                            | String | navigate        | 跳转方式：**类似 a 标签中的: target**。 如果是`navigate`，表示在`新的`窗口打开界面；如果是`redirect`，表示在`当前`的窗口打开界面；如果是`switchTab`，表示在打开tabbar上的界面； | read  rect |
| delta                                    | Number | 1               | 当 open-type 为 'navigate' 时有效，表示回退(**返回界面**)的层数。 |            |
| 可通过 [`getCurrentPages()`](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/app-service/page.html#getCurrentPages()) 获取当前的页面栈，决定需要返回几层 | String | navigator-hover | 指定点击时的样式类，当`hover-class="none"`时，没有点击态效果 |            |

#### 1.新建一个项目

####  2.点击跳转到home页面

1.跳转到home页(在新的窗口打开) ,  这个是默认的页面跳转。

   原理是**在新的窗口**打开**新的页面** ， 新的页面有**返回的按钮**

 

#### 3.指定跳转的方式

**open-type 有效值：**

| 值                | 说明                                       | 最低版本                                     |
| ---------------- | ---------------------------------------- | ---------------------------------------- |
| **navigate**     | (**默认**)对应 `wx.navigateTo` 的功能，表示在`新的窗口`打开界面； |                                          |
| **redirect**     | 对应 `wx.redirectTo` 的功能，表示在`当前的窗口`打开界面；   |                                          |
| **switchTab**    | 对应 `wx.switchTab` 的功能，表示在打开tabbar上的界面；   |                                          |
| reLaunch         | 对应 `wx.reLaunch` 的功能 , **关闭所有页面**跳转到非tabBar页面 | [1.1.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| **navigateBack** | 对应 `wx.navigateBack` 的功能，**返回上一个页面**，和wx.navigateTo结合使用。 |                                          |

##### 1.open-type : redirect

#####  2.open-type  :  switchTab

```json
 //app.json
 
 "tabBar": {
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页"
      },
      {
        "pagePath": "pages/logs/logs",
        "text": "日志"
      }
    ]
  }
```

###  2.navigator API

https://mp.weixin.qq.com/debug/wxadoc/dev/api/ui-navigate.html#wxnavigatetoobject

> 注意： **wx.navigateTo** 和 **wx.redirectTo** 不允许跳转到 **tabbar** 页面，只能用 **wx.switchTab** 跳转到 **tabbar** 页面

#### 1.点击跳转到home页面

1.布局

 

2.处理点击跳转到home界面

####  2.home页面点击回退上一个页面

1.布局实现

 

2.点击回退上一个页面

####  3.指定页面跳转的方式

1.布局页面

 

2.以wx.redirectTo方式跳转界面

 



### 3.页面之间数据的传输

1.通过在**跳转、重定向**等**切换页面**时候，可以直接**通过url**来传送数据

2.**全局变量**之中传递参数数据

3.使用本地缓存的方法保存全局变量

....

http://www.jianshu.com/p/dae1bac5fc75

#### 1.通过url传递数据-onLoad

1.传递数据

```js
//界面跳转时传递数据:?id=4&userName=xmg
    wx.navigateTo({
      url: '../home/home?id=4&userName=xmg',
    })
   
或者：

//界面跳转时传递数据:?id=1&userName=xiaomage
   <navigator 
    url="../home/home?id=1&userName=xiaomage"
   >
      <text >1.点击跳转到home页面（新的窗口打开）</text>
   </navigator>
```

 

2.获取数据

 

#### 2.数据的逆向传递

var pages=getCurrentPages();   // 获取当前跳转页面的个数

 

#### 3.通过全局变量传递数据

1.定义全局变量

在app.js文件中定义全局变量。可以在自定一个函数data／userInfo函数中定义

 

2.获取全局变量

可以在**任意一个js文件**中获取全局变量的值

 

3.修改全局变量的值

可以在**任意一个js文件**中修改全局变量的值

 



## 4.小米商城项目

### 1.项目搭建

appid :  wx15f83890a7cb7f85

#### 1.顶部导航栏配置

```json
 "window":{
    "navigationBarBackgroundColor": "#FF6802",
    "navigationBarTitleText": "小码哥小米商城",
    "navigationBarTextStyle":"white",
    
    "backgroundTextStyle":"light"
  },

 "networkTimeout":{
    "request":60000,
    "connectSocket":60000,
    "uploadFile":60000,
    "downloadFile":60000
  },
```



#### 2.底部导航栏配置

```json
 "pages": [
    "pages/index/index",
    "pages/category/category",
    "pages/find/find",
    "pages/cart/cart",
    "pages/mine/mine",
    "pages/detail/detail",
    "pages/logs/index"
 ],
"tabBar": {
    "color":"#989898",
    "selectedColor":"#FF6802",
    "list": [
      {
      "pagePath": "pages/index/index",
      "text": "首页",
      "iconPath": "image/home_icon_nor.png",
      "selectedIconPath": "image/home_icon_press.png"
      },
      {
        "pagePath": "pages/category/category",
        "text": "分类",
        "iconPath": "image/cate_icon_nor.png",
        "selectedIconPath": "image/cate_icon_press.png"
      },
      {
        "pagePath": "pages/find/find",
        "text": "发现",
        "iconPath": "image/find_icon_nor.png",
        "selectedIconPath": "image/find_icon_press.png"
      },
      {
        "pagePath": "pages/cart/cart",
        "text": "购物车",
        "iconPath":"image/car_icon_nor.png",
        "selectedIconPath":"image/car_icon_press.png"
      },
      {
        "pagePath": "pages/mine/mine",
        "text": "我的",
        "iconPath": "image/mine_icon_nor.png",
        "selectedIconPath": "image/mine_icon_press.png"
      }
    ]
  }
```



#### 3.项目结构搭建

 



### 2.我的页面-am

#### 1.搭建授权页面-200

authorize  英[ˈɔ:θəraɪz]

> bg-#eaebea    img-200       line-2       title-32-#4e4e4e      desp-26-#9d9d9d   btn-90-36

 



##### 1.编写布局

```html
<view class="authorize">

  <!-- 头像: 将益处的部分隐藏(实现圆头像) -->
  <open-data class="header" type="userAvatarUrl" mode="aspectFit"></open-data>

  <!-- 分界线 -->
  <view class="line"></view>

  <view class="content">该小程序有小米商城开发，请提供以下授权，即可继续操作</view>

  <view class="desp">
    <!-- 点 -->
    <text class="dot"></text>
    <text >获取你的公开信息(昵称、头像等)</text> 
  </view>

  <button class="btn" hover-class="hover-class-style">确认授权</button>


</view> 
```





##### 2.编写样式

```css
/* pages/mine/mine.wxss */

/* 授权页面 */
.authorize{
  width: 100%;
  height: 100%;
  background: #eaebea;

  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 头像 */
.header{
 
  width: 200rpx;
  height: 200rpx;
  border-radius: 50%;

  background: red;
  /* 将益处的部分隐藏(实现圆头像) */
  display:block;
  overflow: hidden;

  margin:100rpx 0rpx; 
}

/* 分界线 */ 
.line{
  height: 2rpx;
  width: 80%;
  background: #cccccc;
}

.content{
  width: 80%;
  margin-top: 50rpx;
 
  color: #4e4e4e;
  font-size: 32rpx;

}

.desp{
  width: 80%;
  color: #9d9d9d;
  font-size: 26rpx;

  margin: 20rpx 0rpx;
  /* background: pink; */
  position: relative;

}
/* 点的样式( 定位 ) */
.dot{
  position: absolute;
  top: 20rpx;
  left: 20rpx;

  width: 5rpx;
  height: 5rpx;
  border-radius: 50%;
  background: #9d9d9d;
}

/* 字体样式 */
.desp text:nth-of-type(2){
  margin-left: 40rpx;
}

/* 确认授权按钮 */
.btn{
  width: 80%;
  height: 90rpx;
  font-size: 36rpx;
  background: #ff6802;
  color: white;
  margin: 50rpx;
}

.hover-class-style{
  opacity: 0.9
}
```

 

##### 3.抽取成模版页面-3

> 1.<template name="">  布局  </template>  样式写在全局样式
>
> 2.<import  src="../../xxxx.wxml" />   or   <import  src="../../xxxx.wxml" ></import>  
>
> 3.<template is=""  data="{{ key:value }}"></template>



 

authorize.wxml

```html
<template name="authorize">

  <view class="authorize">

   
    <open-data class="header" type="userAvatarUrl" mode="aspectFit"></open-data>

   
    <view class="line"></view>

    <view class="content">该小程序有小米商城开发，请提供以下授权，即可继续操作</view>

    <view class="desp">
    
      <text class="dot"></text>
      <text >获取你的公开信息(昵称、头像等)</text> 
    </view>
	 <!-- 绑定点击事件 bindtap="{{btnClick}}" -->
    <button bindtap="{{btnClick}}" class="btn" hover-class="hover-class-style">确认授权</button>


  </view> 

</template>
```

mine.wxml

```html
<!-- 导入授权也买呢 -->
<import src="../../templates/authorize.wxml"></import>

<!-- 使用授权页面 -->
<template is="authorize" data="{{btnClick: 'authorizeClick'}}" />
```

mine.js

```js
// pages/mine/mine.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },
  /**
   * 监听授权的点击事件
   */
  authorizeClick:function(event){
    console.log(event);
  },
  
})
```



authorize.wxss

```css

/* 授权页面 */
.authorize{
  width: 100%;
  height: 100%;
  background: #eaebea;

  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 头像 */
.authorize .header{
  width: 200rpx;
  height: 200rpx;
  border-radius: 50%;

  background: red;
  /* 将益处的部分隐藏(实现圆头像) */
  overflow: hidden;
  margin:100rpx 0rpx; 
}

/* 分界线 */ 
.authorize .line{
  height: 2rpx;
  width: 80%;
  background: #cccccc;
}

.authorize .content{
  width: 80%;
  margin-top: 50rpx;
  color: #4e4e4e;
  font-size: 32rpx;
}
.authorize .desp{
  width: 80%;
  color: #9d9d9d;
  font-size: 26rpx;
  margin: 20rpx 0rpx;
  /* background: pink; */
  position: relative;
}
/* 点的样式( 定位 ) */
.authorize .dot{
  position: absolute;
  top: 20rpx;
  left: 20rpx;

  width: 5rpx;
  height: 5rpx;
  border-radius: 50%;
  background: #9d9d9d;
}

/* 字体样式 */
.authorize .desp text:nth-of-type(2){
  margin-left: 40rpx;
}

/* 确认授权按钮 */
.authorize .btn{
  width: 80%;
  height: 90rpx;
  font-size: 36rpx;
  background: #ff6802;
  color: white;
  margin: 50rpx;
}

.authorize .hover-class-style{
  opacity: 0.9
}
```



app.wxss

```css
page{
  height: 100%;
}

/* 导入授权页面的样式 */
@import "style/authorize.wxss"
```



#### 2.实现授权功能

> 1. open-type="getUserInfo"    bindgetuserinfo="{{btnClick}}"
> 2. 将用户的信息存起来( data.userInfo / app.globalData.userInfo )
> 3. 授权成功后隐藏授权页面

1.修改模板:authorize.wxml

```html
<template name="authorize">

  <view class="authorize">

   ....
   ....

    <button open-type="getUserInfo" bindgetuserinfo="{{btnClick}}" class="btn" hover-class="hover-class-style">确认授权</button>


  </view> 

</template>
```



2.接收用户信息

 

mine.js

```js
// pages/mine/mine.js
let app = getApp();

Page({

   /**
   * 页面的初始数据
   */
  data: {
    //userInfo:null,
    userInfo:app.globalData.userInfo,
  },
  
  /**
   * 监听授权的点击事件
   */
  authorizeClick:function(event){
    console.log(event);
    //1.授权之后将数据存放在 app.js 和 data 中
    let userInfo = event.detail.userInfo;
    if (userInfo){
      app.globalData.userInfo = userInfo;
      this.setData({
        userInfo: userInfo,
      })
      console.log(app.globalData.userInfo,this.data.userInfo)
    }
    
  },
  
})
```

app.js

```js
  App({
    
   /**
    * 定义全局数据
    */
    globalData: {
      userInfo: null,
      isLogin:false,

    },
  
  })
```



3.授权成功后隐藏授权页面

```html
<!-- 导入授权也买呢 -->
<import src="../../templates/authorize.wxml"></import>

<block wx:if="{{userInfo}}">
  <view>
      mine
  </view>
</block>

<block wx:else>
  <!-- 使用授权页面 -->
  <template is="authorize" data="{{btnClick: 'authorizeClick'}}" />
</block>
```



#### 3.*实现登陆

> 1.授权成功后实现登陆
>
> 2.登陆成功后保存登陆状态到app.js中和用户信息到data中

http://47.93.30.78:8080/XiaoMiShop/mine

 

mine.js

```js
// pages/mine/mine.js
let app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: app.globalData.userInfo,
    minebean:null,
    isLogin: app.globalData.isLogin,
  },

  /**
   * 监听授权的点击事件
   */
  authorizeClick:function(event){
    let _this=this;
    // console.log(event);
    //1.授权之后将数据存放在app.js中
    let userInfo = event.detail.userInfo;
    if (userInfo){
      app.globalData.userInfo = userInfo;
      //2.刷新界面
      _this.setData({
        userInfo: userInfo,
      })
      // console.log(app.globalData.userInfo,this.data.userInfo)
      
      
      
      //3.实现登陆功能
      wx.login({
        success:function(result){
          //4.拿到code
          // console.log(result.code);
          //5.(模拟)把code提交给后台，获取后台返回的token
          wx.request({
            url: 'http://47.93.30.78:8080/XiaoMiShop/mine?code=' + result.code,
            success:function(res){
              console.log(res.data)
              //6.记录登陆状态( isLogin  )
              app.globalData.isLogin=true;
              _this.setData({
                isLogin: true,
                minebean: res.data.data,
              })
            }
          })
        }
      })
      
      
    }
  
  },
  
  
  
})
```



mine.wxml

```html
<!-- 导入授权模版 -->
<import src="../../templates/authorize.wxml"></import>

<block wx:if="{{userInfo}}">
  <!-- 显示我的界面的布局 -->
  <view wx:if="{{minebean}}">
      
  </view>

  <!-- 显示加载中的模版 -->
  <view wx:else>
      加载中。。。
  </view>

</block>

<block wx:else>
  <!-- 使用授权页面 -->
  <template is="authorize" data="{{btnClick: 'authorizeClick'}}" />
</block>
```

#### 4.*实现加载中ui布局

> 1.如果minebean个人中心数据为空时显示加载进度

 



> 注意：要在app.wxss中引入weui框架

https://github.com/Tencent/weui-wxss

[WeUI](https://github.com/weui/weui) 是一套同微信原生视觉体验一致的基础样式库（小程序UI框架），由微信官方设计团队为微信内网页和微信小程序量身设计，令用户的使用感知更加统一。包含`button`、`cell`、`dialog`、 `progress`、 `toast`、`article`、`actionsheet`、`icon`等各式元素

```html
<!-- 导入授权也买呢 -->
<import src="../../templates/authorize.wxml"></import>

<block wx:if="{{userInfo}}">
  <!-- 显示我的界面的布局 -->
  <view wx:if="{{minebean}}">
      
  </view>

  <!-- 显示加载中的模版（ 使用weiui框架中的 加载中... 样式 ） -->
  <view wx:else class="weui-loadmore">
     <view class="weui-loading"></view>
     <view class="weui-loadmore__tips">正在加载</view>
  </view>

</block>

<block wx:else>
  <!-- 使用授权页面 -->
  <template is="authorize" data="{{btnClick: 'authorizeClick'}}" />
</block>
```

 



#### 5.抽取加载中的布局为模版

> 1.<template name="">  布局  </template>  样式写在全局样式
>
> 2.<import  src="../../xxxx.wxml" />   or   <import  src="../../xxxx.wxml" ></import>  
>
> 3.<template is=""  data="{{ key:value }}"></template>



 

```html
<!-- 1.导入授权模版 -->
<import src="../../templates/authorize.wxml"></import>
<!-- 2.加载中模版 -->
<import src="../../templates/loading.wxml"></import>

<block wx:if="{{userInfo}}">
  <!-- 显示我的界面的布局 -->
  <view wx:if="{{minebean}}">
      
  </view>

  <!-- 显示加载中的模版 -->
  <view wx:else>
     <template is="loading"/>
  </view>

</block>

<block wx:else>
  <!-- 使用授权页面 -->
  <template is="authorize" data="{{btnClick: 'authorizeClick'}}" />
</block>


```

loading.wxml

```html
<template name="loading">

  <view class="weui-loadmore">
     <view class="weui-loading"></view>
     <view class="weui-loadmore__tips">正在加载</view>
  </view>

</template>
```



#### 6.我的界面头部布局-m120

##### 1.左边的布局

> flex : 1  , 3  , 1       img-120-20      desp-26-#9d9d9d      img-60

 

mine.wxml

```html
<!-- 1.导入授权模版 -->
<import src="../../templates/authorize.wxml"></import>
<!-- 2.加载中模版 -->
<import src="../../templates/loading.wxml"></import>

<block wx:if="{{userInfo}}">
  <!-- 1.显示我的界面的布局 -->
  <view wx:if="{{minebean}}">
    
    <!-- 3.头部布局 -->
    <view class="mine-header">
    	 <!--左  -->
     	<view class="left">
        	<image src="{{userInfo.avatarUrl}}"></image>
     	</view>
     	<!-- 中 -->
     	<view class="center">
       		d 
     	</view>
     	<!-- 右 -->
     	<view class="right">
      		0
     	</view>
    </view> 
     

  </view>

  <!-- 2.显示加载中的模版 -->
  <view wx:else>
     <template is="loading"/>
  </view>

</block>

<block wx:else>
  <!-- 使用授权页面 -->
  <template is="authorize" data="{{btnClick: 'authorizeClick'}}" />
</block>
```



mine.wxss

```css
/* pages/mine/mine.wxss */
/* 我的头部样式 */
.mine-header{
  background: pink;

  display: flex;
  flex-direction: row;
}

.left{
  flex:1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.left image{
  width: 120rpx; /**头像的宽和高*/
  height: 120rpx;
  margin: 20rpx;
}

.center{
  flex:3;
  background: purple;
}

.right{
  flex:1;
}
```



##### 2.中间的布局

> desp-26-#9d9d9d      img-60

  

mine.wxml

```html
<!-- 1.导入授权模版 -->
<import src="../../templates/authorize.wxml"></import>
<!-- 2.加载中模版 -->
<import src="../../templates/loading.wxml"></import>

<block wx:if="{{userInfo}}">
  <!-- 显示我的界面的布局 -->
  <view wx:if="{{minebean}}" >
  
    <!-- 头部布局 -->
    <view class="mine-header">
      <!--左  -->
      <view class="left">
          <image src="{{userInfo.avatarUrl}}"></image>
      </view>
      <!-- 中 -->
      <view class="center">
        <view>{{userInfo.nickName}}</view>
        <view>小米账号：23412343434</view>
      </view>
      <!-- 右 -->
      <view class="right">
          <image src="../../image/z-code.png"></image>
      </view>
    </view>



     
  </view>

  <!-- 显示加载中的模版 -->
  <view wx:else>
     <template is="loading"/>
  </view>

</block>

<block wx:else>
  <!-- 使用授权页面 -->
  <template is="authorize" data="{{btnClick: 'authorizeClick'}}" />
</block>
```



mine.wxss

```css
/* pages/mine/mine.wxss */
page{
  background: #eaebea;
}
/* 我的头部样式 */
.mine-header{
  /* background: pink; */

  display: flex;
  flex-direction: row;

  background: white;
  margin: 20rpx 0rpx;
}

...
...
...

.center{
  flex:3;

  display: flex;
  flex-direction: column;
  justify-content: center;


}
.center view:nth-of-type(1){
  margin-bottom: 10rpx;
}
.center view:nth-of-type(2){
  font-size: 26rpx;
  color: #9d9d9d;
}

.right{
  flex:1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.right image{
  width: 60rpx;
  height: 60rpx;
}
```



#### 7.我的界面item布局-30

> 1.直接拷贝weui框架list的模版
>
> 2.img-30  title-34

 



mine.wxml

```html
<!-- 1.导入授权模版 -->
<import src="../../templates/authorize.wxml"></import>
<!-- 2.加载中模版 -->
<import src="../../templates/loading.wxml"></import>

<block wx:if="{{userInfo}}">
  <!-- 显示我的界面的布局 -->
  <view wx:if="{{minebean}}" >

    <!-- 头部布局 -->
    .....
    .....

    <!-- item布局 -->
    <view class="mine-items">
        <!-- 下面是拷贝weui框架的布局 -->
        <view class="weui-cells weui-cells_after-title">

          
            <block wx:for="{{minebean.settings}}" wx:key="{{index}}">
              <view class="weui-cell">
                <view class="weui-cell__hd">
                    <image src="{{item.imageUrl}}" style="margin-right: 5px;vertical-align: middle;width:30px; height: 30px;"></image>
                </view>
                <view class="weui-cell__bd" style="font-size:34rpx;">{{item.name}}</view>
                <!-- <view class="weui-cell__ft">说明文字</view> -->
            </view>
            </block> 
          
             
        </view>

    </view>
     
  </view>

  <!-- 显示加载中的模版 -->
  ....
  ....

</block>

<block wx:else>
  <!-- 使用授权页面 -->
  <template is="authorize" data="{{btnClick: 'authorizeClick'}}" />
</block>
```



#### 8.实现界面的跳转

```html
    <!-- item布局 -->
    <view class="mine-items">
        
        <view class="weui-cells weui-cells_after-title">
			
            <block wx:for="{{minebean.settings}}" wx:key="{{index}}">
               <!-- 实现界面跳转 -->
              <navigator class="weui-cell" url="../order/order">
                <view class="weui-cell__hd">
                    <image src="{{item.imageUrl}}" style="margin-right: 5px;vertical-align: middle;width:30px; height: 30px;"></image>
                </view>
                <view class="weui-cell__bd" style="font-size:34rpx;">{{item.name}}</view>
                <!-- <view class="weui-cell__ft">说明文字</view> -->
            </navigator>
            </block> 

        </view>

    </view>
```



### 3.首页布局

http://47.93.30.78:8080/XiaoMiShop/home

#### 1.获取首页数据

 



index.js

```js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    homeBean:null,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let _this=this;
    //1.获取首页数据
    wx.request({
      url: 'http://47.93.30.78:8080/XiaoMiShop/home',
      success:function(result){
        console.log(result.data)
        _this.setData({
          homeBean: result.data,
        })
      }
    })
  },

})
```



#### 2.显示加载进度

index.wxml

```html
<!--index.wxml-->
<import src="../../templates/loading"></import>

<!-- 有数据 -->
<block wx:if="{{homeBean}}">
  <view style="width:100%;height:100%;" class="home-content">
    


  </view>
</block>


<!-- 没有数据 -->
<block wx:else>
  <!-- 显示加载进度... -->
  <template is="loading"></template>
</block>
```



#### 3.封装网络请求工具

##### 1.编写fetch.js工具类

fetch.js

```js
// 封装了一个fetch函数
let fetch=(options)=>{

  return new Promise(function(resolve,reject){
    wx.request({
      url: options.url || '',
      method: options.method || 'GET',
      data:options.data || '',
      header:options.header || {'content-type':'application/json'}, //指定提交的数据类型
      dataType:options.dataType || 'json', //指定返回的数据类型
      success:function(res){
        //1.相当与调用外部传递进来的then函数
        resolve(res);
      },
      fail:function(error){
        //2.相当与调用外部传递进来的catch函数
        reject(error);  
      }
    })
  })
}

module.exports = {
  fetch: fetch
}
```

使用工具

 



##### 2.编写api.js工具类

 

```js
// 定义基本的url
let baseurl = 'http://47.93.30.78:8080';


module.exports = {
  HOME: baseurl + '/XiaoMiShop/home',
} 
```



##### 3.编写service.js工具类

 



```js
// 1.引入发起网络请求的函数
const fecth = require('./fetch.js').fetch;
//2.引入API接口文件
const API = require('./api.js');


// 3.获取首页的数据（ 以后可以在这里扩展，方便后期维护 ）
const getHomeBean = ()=>{
  console.log(API.HOME)
  //4.发起网络请求
  return fecth( {url:API.HOME} );
  
}


module.exports = {
  getHomeBean: getHomeBean,
}
```



##### 4.service.js获取首页数据

 



```js
let httpService = require('../../utils/service.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    homeBean:null,
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let _this=this;
    //1.获取首页数据
    // fetch({
    //   url:'http://47.93.30.78:8080/XiaoMiShop/home',
    // }).then((result)=>{
    //   console.log(result.data)
    //     _this.setData({
    //       homeBean: result.data,
    //     })
    // }).catch((error)=>{
    //   console.log(error)
    // })

    //1.发起网络请求
    httpService.getHomeBean().then((result)=>{
        console.log(result.data)
        _this.setData({
          homeBean: result.data.data
        })
    }).catch((error)=>{
      console.log(error)
    })


  },
  .....
  .....
})  
  
```



#### 4.授权提示

##### 1.授权提示布局-h120

> bg-#f4f4f4   height-120     icon-info-size-40     title-28-gray

 

index.wxml

```html
<!--index.wxml-->
<import src="../../templates/loading"></import>

<!-- 有数据 -->
<block wx:if="{{homeBean}}">
  <view style="width:100%;height:100%;" class="home-content">

    <!-- 显示授权的布局 -->
   <view wx:if="{{ userInfo == null }}">
       <view style="background:#f4f4f4;height:120rpx;display: flex;flex-direction: row;align-items: center;">
          <icon style="margin:0rpx 20rpx;" type="info" size="40rpx"/>
          <text style="color:gray;font-size:28rpx">请授权头像等信息，以便为您提供更好的服务</text>
        </view>
   </view>


  </view>
</block>


<!-- 没有数据 -->
<block wx:else>
  <!-- 显示加载进度... -->
  <template is="loading"></template>
</block>
```



index.js

```js
// 导入httpService
let httpService = require('../../utils/service.js');
//导入App对象
let app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    homeBean:null,
    userInfo: null,
  },
  
  onLoad(){
    let _this = this;
    ////当页面加载时的时候，重新赋值userInfo，如果不为空代表已经授权过了
    let userInfo = app.globalData.userInfo;
    _this.setData({
      userInfo: userInfo,
    })
    ....
    ....
  }

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    //当页面再次显示的时候，重新赋值userInfo，如果不为空代表已经授权过了
    this.setData({
      userInfo: app.globalData.userInfo
    })
  },


})
```



##### 2.抽取授权提示布局

> 1. <button style="margin:0rpx;padding:0"></button>
> 2. open-type="getUserInfo" bindgetuserinfo="bindgetuserinfo"

 



index.wxml

```html
<!--index.wxml-->
<import src="../../templates/loading"></import>
<import src="../../templates/authorize-view.wxml"></import>

<!-- 有数据 -->
<block wx:if="{{homeBean}}">
  <view style="width:100%;height:100%;" class="home-content">

    <!-- 显示授权的布局 -->
   <button style="margin:0rpx;padding:0" wx:if="{{ userInfo == null }}" open-type="getUserInfo" bindgetuserinfo="bindgetuserinfo">
    
        <template is="authorize-view"></template>
   </button>

    

  </view>
</block>


<!-- 没有数据 -->
<block wx:else>
  <!-- 显示加载进度... -->
  <template is="loading"></template>
</block>
```

##### 3.点击授权并登陆

index.js  授权并登陆

```js

  /**
   * 获取用户信息
   */
  bindgetuserinfo:function(event){
    console.log(event)
    //1.授权成功保存用户信息到app.js
    app.globalData.userInfo = event.detail.userInfo;
    //2.授权成功保存用户信息到page.js
    this.setData({
      userInfo: event.detail.userInfo
    })
    
     //3.登陆
    wx.login({
      success: function (result) {
        //4.拿到code
        // console.log(result.code);
        //5.(模拟)把code提交给后台，获取后台返回的token
        wx.request({
          url: 'http://47.93.30.78:8080/XiaoMiShop/mine?code=' + result.code,
          success: function (res) {
            console.log(res.data)
            //6.记录登陆状态( isLogin  )
            app.globalData.isLogin = true;
            _this.setData({
              isLogin: true,
            })

          }
        })
      }
    })
  },
```



#### 5.处理Mine页面授权的bug

mine.js

```js
// pages/mine/mine.js
let app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: app.globalData.userInfo,
    minebean:null,
    isLogin: app.globalData.isLogin,
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    //1.当页面显示时，重新赋值useinfo到page中的data中
    this.setData({
      userInfo: app.globalData.userInfo
    })

    //2.代表已经授权过
    if (app.globalData.userInfo!=null){  
      //3..直接登陆即可
      this.login();
    }
  },

  /**
   * 实现登陆的代码
   */
  login(){
    let _this=this;

    wx.login({
      success: function (result) {
        //4.拿到code
        // console.log(result.code);
        //5.(模拟)把code提交给后台，获取后台返回的token
        wx.request({
          url: 'http://47.93.30.78:8080/XiaoMiShop/mine?code=' + result.code,
          success: function (res) {
            console.log(res.data)
            //6.记录登陆状态( isLogin  )
            app.globalData.isLogin = true;
            _this.setData({
              isLogin: true,
              minebean: res.data.data,
            })
          }
        })
      }
    })

  },

})
```



### 4.首页搜索布局

#### 1.搜索布局-80-6-4-3-gray

 

index.wxml

```html
    <navigator class="view-search"
      url="../search/search"
    >
      <view class="view-search-bg">
         <image src="../../image/search_icon.png" class="image-search"></image>
         <text class="text-title">搜索商品</text>   
      </view>
    </navigator> 
```





index.wxss

```css
/*search 布局  */
.view-search{
  width: 100%;
  height: 80rpx;
  background: #FF6902;

  display: flex;
  justify-content: center;
  align-content: center;
}

.view-search .view-search-bg{
  width: 80%;
  height: 60rpx;
  background: white;
  border-radius: 30rpx;
  margin-top: 10rpx;

  display: flex;
  justify-content: center;
  align-content: center;
}

/*搜索的图片  */
.view-search .image-search{
  width: 40rpx;
  height: 40rpx;
  margin-top: 10rpx;
}
/*占位符  */
.view-search .text-title{
  color: gray;
  font-size: 30rpx;
  margin-top: 10rpx;
  margin-left: 10rpx;
}
```



#### 2.*抽取成模版

> 1.<template is=""  data="{{  LinkTo:"相对于当前页面",  imageurl:"相对于当前页面"  }}" ></template>

 



search-view.wxml

```html
<template name="search-view">

    <navigator class="view-search"
      url="{{LinkTo}}"
    >
      <view class="view-search-bg">
         <image src="../../image/search_icon.png" class="image-search"></image>
         <text class="text-title">搜索商品</text>   
      </view>
    </navigator> 

</template>
```

search-wxss

```css
/*search 布局  */
.view-search{
  width: 100%;
  height: 80rpx;
  background: #FF6902;

  display: flex;
  justify-content: center;
  align-content: center;
}

.view-search .view-search-bg{
  width: 80%;
  height: 60rpx;
  background: white;
  border-radius: 30rpx;
  margin-top: 10rpx;

  display: flex;
  justify-content: center;
  align-content: center;
}

/*搜索的图片  */
.view-search .image-search{
  width: 40rpx;
  height: 40rpx;
  margin-top: 10rpx;
}
/*占位符  */
.view-search .text-title{
  color: gray;
  font-size: 30rpx;
  margin-top: 10rpx;
  margin-left: 10rpx;
}
```



app.wxss

```css
/* 导入weui框架 */
@import "style/weui.wxss";

page{
  height: 100%;
}

/* 导入授权页面的样式 */
@import "style/authorize.wxss";
/* 导入搜索页面的样式 */
@import "style/search-view.wxss"
```



### 5.首页轮播图-sm-400

 

布局

```html
  <!--banner 布局 -->
  <swiper class="view-banner" indicator-dots="true"
    indicator-color="white" indicator-active-color="#FF6802"
  >
    <block wx:for="{{homeBean.banners}}" wx:key="{{index}}">
      <swiper-item>
          <image src="{{item}}" class="image-banner"></image>
      </swiper-item>
    </block>

  </swiper>
```



样式

```css
/*banner  */
.view-banner,
.image-banner{
  width: 100%;
  height: 400rpx;
}
```





















