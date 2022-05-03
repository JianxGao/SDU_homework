##   小程序进阶二

## 1.构建 npm

从小程序基础库版本 [2.2.1](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 或以上、及[开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) 1.02.18080 或以上开始，**支持使用 npm 安装第三方包**。

此文档要求开发者们对 npm 有一定的了解，因此不会再去介绍 npm 的基本功能。如若之前未接触过 npm，请翻阅[官方 npm 文档](https://docs.npmjs.com/getting-started/what-is-npm)进行学习。



**小程序第三方包：**https://github.com/wechat-miniprogram

### 1.安装第三方的 npm 包

1.在小程序**根目录**中执行命令安装 npm 包：

```js
npm install --save xxxxxxx       //安装生产的依赖
npm install --save-dev xxxxxxx   //安装开发的依赖

// or 通过package.json文件安装
npm install --production  // 只会把 package.json 中 dependencies 依赖的模块下载到 node_modules 中
```

此处并没有强制要求 node_modules 必须在小程序根目录下（即 project.config.js 中的 `miniprogramRoot` 字段），也可以存在于小程序根目录下的各个子目录中。但是不允许 node_modules 在小程序根目录外。

> PS：此处请务必使用`--production`选项，可以减少安装一些业务无关的 npm 包，从而减少整个小程序包的大小。



国家密码算法，例如：https://github.com/wechat-miniprogram/sm-crypto

sm2椭圆曲线公钥密码: https://baike.baidu.com/item/SM2/15081831?fr=aladdin

sm3国产哈希算法  :https://baike.baidu.com/item/SM3/4421797

sm4分组（以16个字节为一组）密码算法( 对称密钥算法 ):  https://baike.baidu.com/item/SM4.0/3901780



安装sm-crypto ：['krɪptoʊ]

```js
npm init -y;
npm install --save miniprogram-sm-crypto@0.0.5  //小程序 js 库。国家密码算法 sm2、sm3 和 sm4 的实现。
```



### 2.构建 npm并勾选使用 npm

1.点击开发者工具中的菜单栏：工具 --> 构建 npm 

2.勾选“使用 npm 模块”选项： 

### 3.使用第三方 npm 包



```js
// pages/04-test-sm/04-test-sm.js
const sm2 = require('miniprogram-sm-crypto').sm2;

Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let keypair = sm2.generateKeyPairHex();

    let publicKey = keypair.publicKey; // 获取公钥( 加密 )
    let privateKey = keypair.privateKey; // 获取私钥（ 解密 ）

    console.log(publicKey);
    console.log(publicKey);
    console.log(privateKey);
    console.log(privateKey);

    console.log('======================')

    const cipherMode = 1; // 1 - C1C3C2，0 - C1C2C3，默认为1 (密码模式)))
    let msgString ='我是要加密的数据';
    let encryptData = sm2.doEncrypt(msgString, publicKey, cipherMode); // 加密结果
    console.log(encryptData);  //密文:3f4eb070c0689a8cdaf1665xxxxxxxxxxxxxxxxx
    let decryptData = sm2.doDecrypt(encryptData, privateKey, cipherMode); // 解密结果
    console.log(decryptData); // 我是要加密的数据

  },
  
})
```



## 2.使用slide-view第三方组件

https://github.com/wechat-miniprogram/slide-view

1.在小程序项目根目录安装  slide-view

```json
npm install --save miniprogram-slide-view@0.0.4
```



2.重新构建npm



3.在需要使用 slide-view 的页面 的xxx.json 中添加 slide-view 自定义组件配置

```json
{
  "usingComponents": {
    "slide-view": "miniprogram-slide-view"
  }
}
```



3.WXML界面引入slide-view组件

每一个 slide-view 提供两个`<slot>`节点，用于承载组件引用时提供的子节点。

1）left 节点用于承载静止时 slide-view 所展示的节点，此节点的宽高应与传入 slide-view 的**宽高**相同。

2）right 节点用于承载滑动时所展示的节点，其宽度应于传入 slide-view 的 **slideWidth**属性相同。

demo: https://github.com/wechat-miniprogram/slide-view/tree/master/tools/demo/pages/index

04-test-sm.wxml

```html
<view  class='slide'>
  <!-- width="750" height="110" slide-width="500" 必须项，不需要单位 -->
  <slide-view width="750" height="110" slide-width="500" id="slider-view">

      <view slot="left" class="l">
        <image src="/pages/image/file_transfer.jpg" class="img"></image>
        <view class='text'>
          <view class='title'>文件传输助手</view>
          <view class='time'>7:00 PM</view>
        </view>
      </view>

      <view slot="right" class="r">
        <view class='read' bindtap="readclick">标为已读</view>
        <view class='delete'>删除</view>
      </view>

</slide-view>

</view>
```



04-test-sm.wxss

```css
.slide{
  border-bottom:1px solid #DEDEDE;
}

.l {
  background-color: skyblue;/* white */
  height: 110rpx;
  width: 750rpx;
  display: flex;
  flex-direction: row;
}

.img {
  width: 90rpx;
  height: 90rpx;
  border-radius:10rpx;
  margin: 10rpx 15rpx;
}

.time {
  margin-top: 15rpx;
  color: white; /* #ccc */
  font-size: 25rpx;
  margin-left: 330rpx;
}

.r {
  height: 110rpx;
  display: flex;
  direction: row;
  text-align: center;
  vertical-align: middle;
  line-height: 110rpx;
}
.read {
  background-color: #ccc;
  color: #fff;
  width: 300rpx; /* 350 */
}
.delete {
  background-color: red;
  color: #fff;
  width: 150rpx; 
}

.text {
  display: flex;
  flex-direction: row;
}
.title {
  margin-top: 15rpx;
  font-size: 33rpx;
}
```



4.监听点击事件

```js
  readclick:function(event){
    let sliderview = this.selectComponent('#slider-view');
    //滚回默认状态
    sliderview.setData({
      x:0
    })
  },
```





## 3.网络请求

> 注意：
>
> 1.正式版有appid的小程序要在`小程序管理平台`配置允许访问的`域名` ;  
>
> ​		小程序管理平台入口：https://mp.weixin.qq.com/
>
> 2.正式版有appid小程序网络请求必须使用`https`协议 ;

注意事项：https://developers.weixin.qq.com/miniprogram/dev/framework/ability/network.html

### 1.简单的使用

https://mp.weixin.qq.com/debug/wxadoc/dev/api/network-request.html



**wx.request(OBJECT)**

```js
    // 1.发起网络请求POST ：http://47.93.30.78:8080/MeiTuan/login
    wx.request({
       url: 'http://47.93.30.78:8080/MeiTuan/login',
       method:'POST',
       data:'username=xiaomage&password=123456',
       header:{
         'content-type': 'application/x-www-form-urlencoded' // 添加的参数为表单
       },
      //2.拿到请求的结果
      success: function (result){
        console.log(result.data);//获取返回的数据
        console.log(result.statusCode);//获取返回的状态码
      },
      //3.处理请求失败
      fail:function(error){
        console.log(error);
      }
    })
```





### 2.发起请求失败情况

1.开发工具配置了代理

​	解决：设计 -- > 代理设计 --->  勾选不使用任何代理 

2.接口异常 ， 或者网络异常

​	解决：

3.可能启动了域名的校验

​	解决：项目 --> 详情 --> 勾选不进行域名的校验



## 4.开眼分类页案例-openeye

```
http://baobab.kaiyanapp.com/api/v2/categories?udid=26868b32e808498db32fd51fb422d00175e179df&vc=83
```

### 1.发起网路请求获取数据-onLoad





```json
[
  {
    "id": 24,
    "name": "时尚",
    "alias": null,
    "description": "优雅地行走在潮流尖端",
    "bgPicture": "http://img.kaiyanapp.com/22192a40de238fe853b992ed57f1f098.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/c9b19c2f0a2a40f4c45564dd8ea766d3.png"
  },
  {
    "id": 18,
    "name": "运动",
    "alias": null,
    "description": "冲浪、滑板、跑酷、骑行，生命停不下来",
    "bgPicture": "http://img.kaiyanapp.com/c746d56db089909b1cdd933fa7c98ef8.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/d51a3cce9d53805e4473d94e71b90e20.png"
  },
  {
    "id": 2,
    "name": "创意",
    "alias": null,
    "description": "技术与审美结合，探索视觉的无限可能",
    "bgPicture": "http://img.kaiyanapp.com/f4a9aba1c6857ee0cefcdc5aee0a1fc9.png?imageMogr2/quality/60/format/jpg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/78452493130483ad6416c191b6be4cb6.png"
  },
  {
    "id": 14,
    "name": "广告",
    "alias": null,
    "description": "为广告人的精彩创意点赞",
    "bgPicture": "http://img.kaiyanapp.com/98beab66d3885a139b54f21e91817c4f.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/fc228d16638214b9803f46aabb4f75e0.png"
  },
  {
    "id": 20,
    "name": "音乐",
    "alias": null,
    "description": "全球最酷、最炫、最有态度的音乐集合",
    "bgPicture": "http://img.kaiyanapp.com/9279c17b4da5ba5e7e4f21afb5bb0a74.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/8c1e48b68c2fd63f49c3c49d732c5af6.png"
  },
  {
    "id": 6,
    "name": "旅行",
    "alias": null,
    "description": "发现世界的奇妙和辽阔",
    "bgPicture": "http://img.kaiyanapp.com/75bc791c5f6cc239d6056e0a52d077fd.jpeg?imageMogr2/quality/60/format/jpg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/e4b9d20b3835fd9630ae25274f8e5659.png"
  },
  {
    "id": 36,
    "name": "生活",
    "alias": null,
    "description": "匠心、健康、生活感悟",
    "bgPicture": "http://img.kaiyanapp.com/924ebc6780d59925c8a346a5dafc90bb.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/a1a1bf7ed3ac906ee4e8925218dd9fbe.png"
  },
  {
    "id": 22,
    "name": "记录",
    "alias": null,
    "description": "告诉他们为什么与众不同",
    "bgPicture": "http://img.kaiyanapp.com/a2fc6d32ac0b4f2842fb3d545d06f09b.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/8857d51d0222ae6d0b142b1f40f11f2d.png"
  },
  {
    "id": 4,
    "name": "开胃",
    "alias": null,
    "description": "眼球和味蕾，一个都不放过",
    "bgPicture": "http://img.kaiyanapp.com/5817f1bfdce61130204a24268160b619.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/085dca86b0eddab9903c82f42e132203.png"
  },
  {
    "id": 30,
    "name": "游戏",
    "alias": null,
    "description": "欢迎来到惊险刺激的新世界",
    "bgPicture": "http://img.kaiyanapp.com/2b7ac9d21ca06df7e39e80a3799a3fb6.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/2993249829996b85fcb3f37051607724.png"
  },
  {
    "id": 26,
    "name": "萌宠",
    "alias": null,
    "description": "来自汪星、喵星、蠢萌星的你",
    "bgPicture": "http://img.kaiyanapp.com/ac6971c1b9fc942c7547d25fc6c60ad2.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/44d902292741e4d385f39df832446a48.png"
  },
  {
    "id": 10,
    "name": "动画",
    "alias": null,
    "description": "有趣的人永远不缺童心",
    "bgPicture": "http://img.kaiyanapp.com/482c741c06644f5566c7218096dbaf26.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/41015e6fe963cf58866ad0d061c073f1.png"
  },
  {
    "id": 32,
    "name": "科普",
    "alias": null,
    "description": "每天获得新知识",
    "bgPicture": "http://img.kaiyanapp.com/0117b9108c7cff43700db8af5e24f2bf.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/000d96c25e74024a64a04b596af3b7e4.png"
  },
  {
    "id": 12,
    "name": "剧情",
    "alias": null,
    "description": "用一个好故事，描绘生活的不可思议",
    "bgPicture": "http://img.kaiyanapp.com/8581b06aa17c7dbe8970e4c27bbdbd98.png?imageMogr2/quality/60/format/jpg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/30954626dd53df5747f18b782a13adbb.png"
  },
  {
    "id": 28,
    "name": "搞笑",
    "alias": null,
    "description": "哈哈哈哈哈哈哈哈",
    "bgPicture": "http://img.kaiyanapp.com/cd74ae49d45ab6999bcd55dbae6d550f.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/ff9ff562a9be8f7dd621c0f526915d1d.png"
  },
  {
    "id": 8,
    "name": "预告",
    "alias": null,
    "description": "电影、剧集、戏剧抢先看",
    "bgPicture": "http://img.kaiyanapp.com/003829087e85ce7310b2210d9575ce67.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/448bcc5e39bfaa7fa31aa1409cbd3247.png"
  },
  {
    "id": 38,
    "name": "综艺",
    "alias": null,
    "description": "全球网红在表演什么",
    "bgPicture": "http://img.kaiyanapp.com/9f4c1559d54d4274e5463fba4262b284.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/54147e3a179fd46ab1e3166c4d993d58.png"
  },
  {
    "id": 34,
    "name": "集锦",
    "alias": null,
    "description": "最好的部分 + 有化学反应的混剪",
    "bgPicture": "http://img.kaiyanapp.com/d7186edff72b6a6ddd03eff166ee4cd8.jpeg",
    "bgColor": "",
    "headerImage": "http://img.kaiyanapp.com/58a511d09016272f3288ebedac13a77e.png"
  }
]
```



### 2.*将数据保存在data中

> 拷贝当前的上下文  :  var _this=this ;



对应的代码

```js
/**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    //1.拷贝this对象
    var _this=this;
    wx.request({
      url:this.data.url,
      method:'GET',
      success:function(result){
        //2.使用this对象
        _this.setData({
          // 3.将数据保存在data中
          categorys:result.data,
        })
      },
      fail:function(error){
        console.log(error);
      }
    });
  },
```

### 3.开始写布局

#### 1.基本布局



对应的样式：

```
/*页面的根元素  */
page{
    width: 100%;
    height: 100%;
}

/*第一个view  */
.view-body{
  width: 100%;
  height: 100%;
  background: green;
}
```

#### 2.添加scroll-view

布局



对应的样式：



#### 3.item布局-h-360

item布局 ,  注意要修改view标签类型



样式：



#### 4.实现item中的内容-f-50

item布局



item样式



 

## 5.下载文件

### 1.下载文件

wx.downloadFile(Object)

> wx.downloadFile()  可以下载 mp4  mp4  png  pdf ppt …….

| 属性       | 类型       | 默认值  | 必填   | 说明                                   | 最低版本                                     |
| -------- | -------- | ---- | ---- | ------------------------------------ | ---------------------------------------- |
| url      | string   |      | 是    | 下载资源的 url                            |                                          |
| header   | Object   |      | 否    | HTTP 请求的 Header，Header 中不能设置 Referer |                                          |
| filePath | string   |      | 否    | 指定文件下载后存储的路径                         | [1.8.0](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| success  | function |      | 否    | 接口调用成功的回调函数                          |                                          |
| fail     | function |      | 否    | 接口调用失败的回调函数                          |                                          |
| complete | function |      | 否    | 接口调用结束的回调函数（调用成功、失败都会执行）             |                                          |





01-download-file.js

```js
// pages/01-download-file/01-download-file.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    tempFilePath:'',
    imgTempFilePath:''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let _this=this;
    //1.下载mp4视频( 31.4 M )
    wx.downloadFile({
      url:'http://baobab.kaiyanapp.com/api/v1/playUrl?vid=56499&editionType=default&source=qcloud',
      success:function(res){
        console.log(res.tempFilePath) 
        //下载好后开始播放
        _this.setData({
          tempFilePath: res.tempFilePath
        })
      },
      fail:function(error){
        console.log(error) 
      }
    })
    
    //2.下载img图片
    wx.downloadFile({
      url: 'https://www.baidu.com/img/bd_logo1.png?where=super',
      success: function (res) {
        console.log(res.tempFilePath)
        //下载后开始播放
        _this.setData({
          imgTempFilePath: res.tempFilePath
        })
      },
      fail: function (error) {
        console.log(error)
      }
    })
  },

})
```



01-download-file.wxml

```html
<video src="{{tempFilePath}}"></video>
<image src='{{imgTempFilePath}}'></image>
```



### 2.本地临时文件

本地临时文件产生后，仅在当前生命周期内有效，重启之后即不可用。

因此，**不可把本地临时文件路径存储起来下次使用**。如果需要下次在使用，可通过 [FileSystemManager.saveFile()](https://developers.weixin.qq.com/miniprogram/dev/api/FileSystemManager.saveFile.html) 或 [FileSystemManager.copyFile()](https://developers.weixin.qq.com/miniprogram/dev/api/FileSystemManager.copyFile.html) 接口把**本地临时文件**转换成**本地缓存文件**或**本地用户文件**。



## 6.文件操作-10M

https://developers.weixin.qq.com/miniprogram/dev/framework/ability/file-system.html

其中本地文件又分为三种：

1. 本地临时文件：临时产生，随时会被回收的文件。不限制存储大小。
2. **本地缓存文件**：小程序通过接口把本地临时文件缓存后产生的文件，**不能自定义目录和文件名**。除非用户主动删除小程序，否则不会被删除。跟本地用户文件共计，**普通小程序最多可存储 10MB**，游戏类目的小程序最多可存储 **50MB**。  < 1.7.0
3. **本地用户文件**：小程序通过接口把本地临时文件缓存后产生的文件，**允许自定义目录和文件名**。除非用户主动删除小程序，否则不会被删除。跟本地用户文件共计，**普通小程序最多可存储 10MB**，游戏类目的小程序最多可存储 **50MB**。 > 1.7.0

### 1.本地缓存文件<1.7.0

本地缓存文件只能通过调用特定接口产生，不能直接写入内容。本地缓存文件产生后，重启之后仍可用。本地缓存文件只能通过 [FileSystemManager.saveFile()](https://developers.weixin.qq.com/miniprogram/dev/api/FileSystemManager.saveFile.html) 接口将本地临时文件保存获得。

示例

```js
fs.saveFile({
  tempFilePath: '', // 传入一个本地临时文件路径
  success(res) {
    console.log(res.savedFilePath) // res.savedFilePath 为一个本地缓存文件路径
  }
})
```

**注意：本地缓存文件是最初的设计，1.7.0 版本开始，提供了功能更完整的本地用户文件，可以完全覆盖本地缓存文件的功能，如果不需要兼容低于1.7.0 版本，可以不使用本地缓存文件。**



#### 1.保存文件-wx.saveFile

保存文件( 如果是同一张图片保存时不会覆盖 )



```js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    
  },

  /**
   * 保存文件
   */
  savefile:function(event){
     //1.下载一个文件
     wx.downloadFile({
       url:'https://www.baidu.com/img/bd_logo1.png?where=super',
       success:function(result){
          // console.log(result)
          //2.保存文件( 如果是同一张图片保存时不会覆盖 )
          wx.saveFile({
            tempFilePath: result.tempFilePath,
            success:function(res){
              console.log(res)
            }
          })
       },
       fail:function(error){
         console.log(error)
       }
     }) 
  },

})
```



#### 2.获取文件列表-wx.getSavedFileList

保存文件( 如果是同一张图片保存时不会覆盖 )



```js
 wx.getSavedFileList({
      success: function (results) {
        console.log(results)
      }
    })
```



#### 3.打开pdf文件-wx.openDocument

> 真机测试要切换到debug模式

https://jtzl.gzjt.gov.cn/

网络上的pdf :  https://jtzl.gzjt.gov.cn/attachment/20181026/1540524854107.pdf



```js
  /**
   * 下载并打开pdf文件
   */
  openpdf:function(){
    wx.downloadFile({
      url:'https://jtzl.gzjt.gov.cn/attachment/20181026/1540524854107.pdf',
      success:function(result){
        //1.在android手机上会默认打开浏览器查看pdf ( 可选择其它的应用查看 )
        //2.在 macbook 和 window 会默认使用打开pdf的软件打开
        wx.openDocument({
          filePath: result.tempFilePath,
          fileType:'pdf',
          success:function(res){
              console.log('pdf打开成功')
          },
          fail:function(err){
             console.log('pdf打开失败')
          }
        })  
      },
      fail:function(error){
		
      }

    })
  },
```



### 2.本地用户文件>1.7.0

本地用户文件是从 `1.7.0` 版本开始新增的概念。我们提供了一个**用户文件目录**给开发者，开发者对**这个目录**有完全自由的读写权限。

**通过 `wx.env.USER_DATA_PATH` 可以获取到这个本地文件根目录的路径**。

示例

```js
// 在本地用户文件目录下创建一个文件 hello.txt，写入内容 "hello, world"
const fs = wx.getFileSystemManager()  // 获取全局唯一的文件管理器
fs.writeFileSync(`${wx.env.USER_DATA_PATH}/hello.txt`, 'hello, world', 'utf8')
```



#### 1.创建一个文件夹-mkdir

 let fileManager = wx.getFileSystemManager();

```js
  /**
   * 创建一个文件夹
   */
  createDir:function(event){
    let fileManager = wx.getFileSystemManager();
    //1.在本地创建一个文件夹（ 注意dirPath的值是一个字符串模版 ）
    // ${wx.env.USER_DATA_PATH} 是获取本地的目录
    // `${wx.env.USER_DATA_PATH}/liujun` 意思是在本地目录下新建一个liujun的文件夹
    fileManager.mkdir({
      dirPath: `${wx.env.USER_DATA_PATH}/liujun`,
      recursive:false, //不会递归创建，仅创建对应的文件夹
      success:function(result){
        console.log(result)
      }
    });
   
  },
```



#### 2.查看创建文件夹-readdir





#### 3.写一个文件-writeFileSync

```js
 /**
   * 同步的写一个json文件
   */
  wirteJson:function(event){
    let fileManager = wx.getFileSystemManager();
    //参数一：写的路径 ； 参数二：内容 ； 参数三：指定的编码
    fileManager.writeFileSync(`${wx.env.USER_DATA_PATH}/liujun/home.json`,'{"name":"jack","age":"12"}','utf-8');

  },
```

> 1)   writeFileSync   是把数据写到指定的文件
>
> 2）saveFileSync   是把一个存在的文件存到指定的目录中

#### 4.读一个文件-readFileSync





```js
  /**
   * 读取本地的json文件
   */
  readJson:function(event){
    //参数一：读取文件的路径 ； 参数二：指定编码
    let dataString=fileManager.readFileSync(`${wx.env.USER_DATA_PATH}/liujun/home.json`,'utf-8');
    console.log(dataString)
 
  },
```



## 7.选择和预览图片

真机测试要切换到debug模式

https://mp.weixin.qq.com/debug/wxadoc/dev/api/media-picture.html#wxchooseimageobject

### 1.选择图片-chooseImage



1.新建一个有AppId的项目，**有APPID的项目就可以在手机上测试**



```js
// pages/03-picture/03-picture.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    imgUrl:''
  },
  
  // 1.打开图库	
  openPicture:function(event){

    //复制一个下上下文
    var _this = this;
    wx.chooseImage({
      count: 1, // 默认最多一次选中9张
      sizeType: ['original', 'compressed'], // 可以指定是需要的是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定是打开相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        var tempFilePaths = res.tempFilePaths; //["http://tmp/touristappid.o6DE.eafe.png"]
        console.log(tempFilePaths);
        _this.setData({
          imgUrl: tempFilePaths[0],
        })
      }
    })

  },

  
  //2.打开相机 
  openCamera:function(event){
    //复制一个下上下文
    var _this = this;
    wx.chooseImage({
      count: 1, // 默认最多一次选中9张
      sizeType: ['compressed'], // 指定是需要的是压缩图
      sourceType: ['camera'], // 指定是打开相机
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        var tempFilePaths = res.tempFilePaths; //["http://tmp/touristappid.o6DE.eafe.png"]
        console.log(tempFilePaths);
        _this.setData({
          imgUrl: tempFilePaths[0],
        })
      }
    })
  },

})
```



### 2.预览图片-previewImage

> https://m.360buyimg.com/mobilecms/s750x366_jfs/t1/25068/8/2121/139183/5c19dcc7E41eab98d/6db9ce38bbaf07d8.jpg!cr_1125x549_0_72!q70.jpg.dpg
>
> https://m.360buyimg.com/mobilecms/s750x366_jfs/t1/11048/15/3135/179599/5c1b3531E9bcd557b/3867b51fc90825a0.jpg!cr_1125x549_0_72!q70.jpg.dpg



```js
  /**预览图片 */
  previewPicture:function(event){
    let _this=this;

    wx.previewImage({
      urls: [_this.data.imgUrl, 'https://m.360buyimg.com/mobilecms/s750x366_jfs/t1/25068/8/2121/139183/5c19dcc7E41eab98d/6db9ce38bbaf07d8.jpg!cr_1125x549_0_72!q70.jpg.dpg','https://m.360buyimg.com/mobilecms/s750x366_jfs/t1/11048/15/3135/179599/5c1b3531E9bcd557b/3867b51fc90825a0.jpg!cr_1125x549_0_72!q70.jpg.dpg'],
      success:function(res){
         console.log(res) 
      }
    })
  },
```





## 8.数据缓存-am



https://mp.weixin.qq.com/debug/wxadoc/dev/api/data.html#wxsetstorageobject

> 本地数据存储的大小限制为 **10MB**

### 1.保存数据到本地-3

**wx.setStorage(OBJECT)**

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

1.新建一个项目

2.将数据保存在本地

```js
  //1.保存数据到本地
  onBindTap1:function(){
    //1.保存普通的字符串
     wx.setStorage({
       key: 'username',
       data: 'xiaomage',
     }) 
    //2.保存json字符窜
     wx.setStorage({
       key: 'userInfo',
       data: '{"name":"xmg","age":"3"}',
     }) 
     //3.保存一个json对象
     var objs={
       name:'lulu',
       sex:'男'
     }
     wx.setStorage({
       key: 'userObj',
       data: objs,
     }) 
  },
```



### 2.获取本地数据

#### 1.获取指定key的数据

```js
  //2.获取指定key的本地的数据
  onBindTap2: function () { 
     //1.获取普通字符串
      wx.getStorage({
        key: 'username',
        success: function(res) {
          console.log(res.data);
        },
      })
      //2.获取json字符串
      wx.getStorage({
        key: 'userInfo',
        success: function (res) {
          //JSON.parse ： 将一个json字符串解析成json对象
          console.log(JSON.parse(res.data).name);
        },
      })
      //3.获取json对象
      wx.getStorage({
        key: 'userObj',
        success: function (res) {
          console.log(res.data.sex);
        },
      })
  },
```

#### 2.获取所有的数据

wx.getStorageInfo(OBJECT)    //获取所有的keys

### 3.删除本地数据

#### 1.删除指定key的数据

#### 2.删除所有的数据



## 9.导航栏API

### 1.NavigationBar

这些api仅仅对调用的那个页面起作用，不会作用于其它页面

setNavigationBarTitle   setNavigationBarColor   showNavigationBarLoading

```js
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    //1.修改导航栏的标题
    wx.setNavigationBarTitle({
      title: "导航栏",
    })
    
    //2.修改导航栏的背景颜色( 仅支持 #ffffff 和 #000000 )
    wx.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: '#FF6802',
    })
    
    //3.显示加载的进度
    wx.showNavigationBarLoading();
  },
```



## 10.操作反馈小工具



界面-交互反馈工具：Toast 吐司    、Modal弹窗 、   ActionSheet操作菜单

https://mp.weixin.qq.com/debug/wxadoc/dev/api/api-react.html#wxshowtoastobject

### 1.Toast

#### 1.显示Toast

1.显示加载中图标

> icon :  success  loading



2.显示自定图标



#### 2.隐藏Toast

> mask 属性是给布局添加了透明的蒙层

### 2.odal

#### 1.显示Modal

### 3.ActionSheet

#### 1.显示ActionSheet



#### 2.监听点击的item



或者如下：

items 是在data中定义的变量

```js
  onBindTap7: function () {
   var  _this=this;
    wx.showActionSheet({
      itemList: this.data.items,
      success: function (res){
        wx.showToast({
          title: _this.data.items[0],
        })
      }
    })
  },
```





## 11.需要授权的API

https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/authorize.html

**部分接口需要经过用户授权同意才能调用**。

authorize  

**scope 列表**

| scope                  | 对应接口                                     | 描述         |
| ---------------------- | ---------------------------------------- | ---------- |
| scope.userInfo         | [wx.getUserInfo](https://developers.weixin.qq.com/miniprogram/dev/api/wx.getUserInfo.html) | **用户信息**   |
| scope.userLocation     | [wx.getLocation](https://developers.weixin.qq.com/miniprogram/dev/api/wx.getLocation.html), [wx.chooseLocation](https://developers.weixin.qq.com/miniprogram/dev/api/wx.chooseLocation.html) | 地理位置       |
| scope.address          | [wx.chooseAddress](https://developers.weixin.qq.com/miniprogram/dev/api/wx.chooseAddress.html) | **通讯地址**   |
| scope.invoiceTitle     | [wx.chooseInvoiceTitle](https://developers.weixin.qq.com/miniprogram/dev/api/wx.chooseInvoiceTitle.html) | 发票抬头       |
| scope.invoice          | [wx.chooseInvoice](https://developers.weixin.qq.com/miniprogram/dev/api/wx.chooseInvoice.html) | 获取发票       |
| scope.werun            | [wx.getWeRunData](https://developers.weixin.qq.com/miniprogram/dev/api/wx.getWeRunData.html) | **微信运动步数** |
| scope.record           | [wx.startRecord](https://developers.weixin.qq.com/miniprogram/dev/api/wx.startRecord.html) | 录音功能       |
| scope.writePhotosAlbum | [wx.saveImageToPhotosAlbum](https://developers.weixin.qq.com/miniprogram/dev/api/wx.saveImageToPhotosAlbum.html), [wx.saveVideoToPhotosAlbum](https://developers.weixin.qq.com/miniprogram/dev/api/wx.saveVideoToPhotosAlbum.html) | 保存到相册      |
| scope.camera           | 《camera》 组件                              | 摄像头        |

### 1.使用button授权

```html
<button open-type='getUserInfo'>授权</button>
```

### 2.打开设置界管理授权

```js
wx.openSetting(); // 好处是可以管理授权 ，例如：当取消授权后, 还可以重新进入这个页面授权等
```

### 3.授权接口调用案例

> 1.获取用户信息   2.获取送货地址   3.获取微信步数

```js
// pages/05-authorize/05-authorize.js
Page({

  /**
   * 1.需要授权后才能调用 wx.getUserInfo（ 不会弹出授权窗口 ）
   */
  getUserInfo:function(event){
    wx.getUserInfo({
      success:function(res){
        console.log(res)
      }
    })
  },

  /**2.打开授权页面（ 可以管理授权信息  ） */
  openSetting:function(event){
    wx.openSetting();
  },

  /**3.如果没有授权 会自定弹出授权窗口，如果授权过了就不会弹出授权窗口（ 仅授权该接口 ） */
  changeAddress:function(event){
    wx.chooseAddress({
      success:function(result){
        console.log(result)
      }
    })
  },

  /**
   * 4.需要授权后才能调用（ 会弹出授权窗口, 仅授权该接口 ）
   */
  getWeRunData:function(event){
    wx.getWeRunData({
      success:function(res){
        console.log(res)
      }
    })  
  },


})
```



## 12.小程序登陆

小程序可以通过**微信官方提供的登录能力**方便地获取微信提供的用户身份标识，快速建立小程序内的用户体系。

### 1.登录流程时序

> **1.调用wx.login()   2.拿到wx.login()返回的code  3.把code提交给后端 (  不是微信后端  )**  
>
> 4.后端程序猿拿着code等信息请求微信后台  5.拿到微信返回的openid等信息，然后返回 token 给前端
>
> **6.前端拿到token后记录用户的登录状态 ，实现登陆成功**





### 2.授权并登陆案例

http://47.93.30.78:8080/MeiTuan/login

username=xiaomage&password=123456



js代码

```js
 /**
   * 1.获取授权结果
   */
  getUserInfo:function(event){
    
    app.globalData.userInfo = event.detail.userInfo
    console.log(app.globalData.userInfo)
    //2.实现登陆功能( 获取code, 调用这个login api不需要授权都可以 )
    wx.login({
      success: function (result) {
        console.log(result.code);
        //3.将code提交给后台
        wx.request({
          url: 'http://47.93.30.78:8080/MeiTuan/login',
          method:'POST',
          data: 'username=xiaomage&password=123456&code='+result.code,
          header: {
            'content-type': 'application/x-www-form-urlencoded' // 添加的参数为表单
          },
          success:function(res){
            console.log(res);
            //4.记录登陆状态和后端返回的token
            // app.globalData.accessToken = res.data.accessToken;
            
            app.globalData.isLogin = true;
            console.log('isLogin=' + app.globalData.isLogin);
          },
          fail:function(error){
            console.log(error)
          }
        })

      }
    })

    
  },
```



布局代码：

```html

<open-data type="userAvatarUrl"></open-data>

<button open-type="getUserInfo" bindgetuserinfo="getUserInfo">授权并登陆</button>
```



## 13.转发分享小程序



监听用户点击页面内转发按钮   1) button 组件的`open-type="share"`   2)右上角菜单“转发”按钮的行为， 3)自定义转发内容。

**转发回调函数：onShareAppMessage(Object)  ； Object 接收的参数说明：**

| 参数         | 类型     | 说明                                       | 最低版本                                     |
| ---------- | ------ | ---------------------------------------- | ---------------------------------------- |
| from       | String | 转发事件来源。`button`：页面内转发按钮；`menu`：右上角转发菜单   | [1.2.4](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| target     | Object | 如果 `from` 值是 `button`，则 `target` 是触发这次转发事件的 `button`，否则为 `undefined` | [1.2.4](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| webViewUrl | String | 页面中包含web-view组件时，返回当前web-view的url        | [1.6.4](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |



此 onShareAppMessage(Object) 函数需要 **return 一个 Object**，用于自定义转发内容，返回内容如下：

**自定义转发内容**

| 字段       | 说明                                       | 默认值        | 最低版本                                     |
| -------- | ---------------------------------------- | ---------- | ---------------------------------------- |
| title    | 转发标题( title:"xmg" )                      | 当前小程序名称    |                                          |
| path     | 转发路径, 一般是当前页面路径:path:"pages/index/index" | 转发路径path   |                                          |
| imageUrl | 自定义图片路径，可以是本地文件路径、代码包文件路径或者网络图片路径。支持PNG及JPG。显示图片长宽比是 5:4。 | 使用**默认截图** | [1.5.0](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |

### 1.点击菜单转发

1.点右上角菜单转发



```js
  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function (event) {
    console.log(event)

    return {
      title:'liujun',
      path:'pages/07-showshare/07-showshare',
      imageUrl:'https://www.baidu.com/img/bd_logo1.png?where=super'
    }
  }
```

控制台输出：

```json
{ from: "menu", target: undefined }
```



### 2.点击按钮转发

> 如果同时给了button 添加了点击事件，那么 onShareAppMessage 和 按钮的监听事件都会触发

布局

```html
<button open-type="share" type="primary" size="mini" id="btn">转发</button>
```

js代码：

```js
  /**
   * 用户点击右上角分享
   * path:'pages/07-showshare/07-showshare?id=123' 指定用户打开小程序进入的页面，
   *	  可以在该07-showshare页面获取参数id
   */
  onShareAppMessage: function (event) {
    console.log(event)

    return {
      title:'liujun',
      path:'pages/07-showshare/07-showshare?id=123',
      imageUrl:'https://www.baidu.com/img/bd_logo1.png?where=super'
    }
  }
```

控制台输出：

```json
{  
   from: "button" , 
   target: { id: "btn", dataset: {…}, offsetTop: 0, offsetLeft: 0}
}   
```

## 14.判断小程序API的兼容

判断小程序的API 、回调函数 、参数 、 组件等在当前**微信软件中的小程序基础库的版本**是否可用。

> 例如, 你手机微信软件小程序库是2.2.0 , 我们开发时却用了2.4.2最新的版本

参数

string schema  模式  ['skiːmə]

使用 `${API}.${method}.${param}.${options}` 或者 `${component}.${attribute}.${option}` 方式来调用

返回值

boolean

当前版本是否可用

参数说明

- `${API}` 代表 API 名字

- `${method}` 代表调用方式，有效值为return, **success, object**, callback

- `${param}` 代表参数或者返回值

- `${options}` 代表参数的可选值

  

- `${component}` 代表组件名字

- `${attribute}` 代表组件属性

- `${option}` 代表组件属性的可选值



### 1.使用语法：

```js
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
      //1.判断小程序的API是否在当前版本可用
    //${API}.${method}.${param}
    console.log(wx.canIUse('request.object.responseType'))   //判断这个属性在当前版本是否可用
    //${API}.${method}.${param}.$(options)
    console.log(wx.canIUse('request.object.method.POST'))  // 判断这个属性里的POST在当前版本是否可用
    //${API}.${method}.${param}
    console.log(wx.canIUse('request.success.header'))   //判断这个方法里的属性在当前版本是否可用

    //2.判断小程序组件是否在当前版本可用
    console.log('====================')
    //${component}.${attribute}.${option}
    console.log(wx.canIUse('button.open-type.share'))
    //${component}.${attribute}.${option}
    console.log(wx.canIUse('button.open-type.getUserInfo'))
    //${component}.${attribute}.${option}
    console.log(wx.canIUse('button.open-type.launchApp'))
    
  },
```



### 2.使用案例

该上面分享的案例的布局(  添加监听事件 )

```html
<button open-type="share" type="primary" size="mini" id="btn" bindtap="shareClick">转发</button>
```



js代码

```js
// pages/07-showshare/07-showshare.js

Page({
  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function (event) {
    console.log(event)

    return {
      title:'liujun',
      path:'pages/07-showshare/07-showshare',
      imageUrl:'https://www.baidu.com/img/bd_logo1.png?where=super'
    }
  },

  shareClick:function(event){
    console.log('shareClick', wx.canIUse('button.open-type.share'))
    
    //判断该版本是否支持分享功能
    if(!wx.canIUse('button.open-type.share')){
      wx.showModal({
        title: '当前版本不支持转发按钮',
        content: '请升级至最新版本微信客户端',
        showCancel: false
      })
      
    }
   
  },

})
```


