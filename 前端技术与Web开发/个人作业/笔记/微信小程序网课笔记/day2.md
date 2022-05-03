## 02-小程序基础二

## 1.scroll-view水平滚动案例

**第一步：**给scroll-view添加**scroll-x="{{true}}"**属性

**第二步：**给scroll-view设计高度,  并给scroll-view添加 **white-space=‘ nowrap ’**  来强制scroll-view内容要在一行（默认内容抵达边界会换行）

**第三步：**指定scroll-view里面的组件的类型为**行内块级标签：display: inline-block**（块级标签默认会换行）

### 1.引入本地的json

```json
[
  {	"imgUrl":"https://img14.360buyimg.com/n1/s150x150_jfs/t30814/9/944457966/151730/b9082df7/5c01fcbbNa3869e29.jpg.dpg",
 "price":"1699",
 "outPrice":"1899"  
  },
  {	"imgUrl":"https://img14.360buyimg.com/n1/s150x150_jfs/t30409/283/889241385/203388/d44ae817/5c00d21aNcfbb2aa7.jpg.dpg",
 "price":"38.7",
 "outPrice":"60"  
  },
  {	"imgUrl":"https://img14.360buyimg.com/n1/s150x150_jfs/t1/17561/2/174/181822/5c078d55E6b3dd312/001c59776d959381.jpg.dpg",
 "price":"1899",
 "outPrice":"2899"  
  },
  {	"imgUrl":"https://img14.360buyimg.com/n1/s150x150_jfs/t26470/12/2593089004/174952/e153816b/5c0633c1N80aff116.jpg.dpg",
 "price":"28.5",
 "outPrice":"35.9"  
  },
  {	"imgUrl":"https://img14.360buyimg.com/n1/s150x150_jfs/t1411/245/746207504/132419/981fb579/55a8d386N2cbd7ba1.jpg.dpg",
 "price":"5399",
 "outPrice":"6799"  
  }
]
```

### 2.基本布局-300

> height:300   with:250  

代码：

```css
scroll-view{
  height: 300rpx;
  width: 100%;
  background: skyblue;
  /**让scroll-view内容不换行*/
  white-space: nowrap;
}

.item{
  width: 250rpx;
  height: 100%;
  border: 1rpx solid #dddddd;
  /**让view不换行*/
  display: inline-block;
}
```

### 3.item布局-200

> image-h200   fs-red-36   price-28-gray   line-through

```css
scroll-view{
  .....
}

.item{
  .....
  text-align: center;
}

.item image{
  width: 90%;
  height: 200rpx;
}

/**弹性布局*/
.item view{
  display: flex;
  flex-direction: column;
}

.item view text:nth-of-type(1){
  color: red;
  font-size: 36rpx;
}

.item view text:nth-of-type(2){
  color: gray;
  font-size: 28rpx;
  text-decoration: line-through;
}
```

### 4.其它属性

```html
<scroll-view scroll-x
             
  bindscroll='onbindscroll'
  bindscrolltoupper="onbindscrolltoupper"
  scroll-into-view="item2"
>

  <block wx:for="{{itemsdata}}" wx:key="{{index}}">
      <view class='item' id="item{{index}}">
          <image src="{{item.imgUrl}}"></image>
          <view>
              <text>¥{{item.price}}</text>
              <text>¥{{item.outPrice}}</text>
          </view>
      </view>
  </block>

</scroll-view>
```

> 1.scroll-into-view="item2"    —>    id="item2"   ( 默认显示第二个item )
>
> 2.bindscrolltoupper   滚动到顶部／左边



## 2.模板

Template vs Component 这两者之间的区别:   

1) template主要是展示，方法则需要在调用的页面中定义。

2) component组件则有自己的业务逻辑( 包含：js , wxml, wxss, json文件 )，也可以看做一个独立的page页面。

3) 简单来说，如果只是展示，使用template就足够了，如果涉及到的业务逻辑交互比较多，那就最好使用component组件了



### 1.定义模板和使用

> 1.在wxml页面中定义模版  <template name="abc"> xxxx <template>
>
> 2.使用模版 <template is="abc"   data="{{   }}"> <template>

```html
<!-- 1.定义模板 -->
<template name="tempName">
  <view> 
      <text>我是一个模板</text>
  </view>
</template>

<!-- 2.使用模板 -->
<template is="tempName"/>
```

### 2.动态渲染模板

> <template is="{{2>4?'tempName1':'tempName2'}}"/>

```html
<!-- 1.定义模板 -->
<template name="tempName1">
  <view> 
      <text>我是第1个模板</text>
  </view>
</template>

<template name="tempName2">
  <view> 
      <text>我是第2个模板</text>
  </view>
</template>

<!-- 2.使用模板 -->
<template is="{{2>4?'tempName1':'tempName2'}}"/>
```

### 3.模板接收参数

布局代码

```html
<!-- 1.定义模板 -->
<template name="tempName1">
  <view> 
      <text>我是第1个模板\n</text>
      <!-- 3.接收参数  -->
      <text>{{msg}}-->{{time}}</text>
  </view>
</template>

<template name="tempName2">
  <view> 
      <text>我是第2个模板\n</text>
    	<!-- 3.接收参数  -->
      <text>{{msg}}-->{{time}}</text>
  </view>
</template>

<!-- 2.使用模板 data传递参数  -->
<template is="{{2>4?'tempName1':'tempName2'}}" data="{{...item}}"/>
```

js代码：

```js
 /**
   * 页面的初始数据
   * 可以在item中定义一个事件的名称传递到模版中 
   */
  data: {
    item: {
      msg: 'this is a template',
      time: '2018-12-16'
    }
  },
```

### 4.模板的抽取

> 1.定义外部模版<template name=""> xxxx </template>
>
> 2.导入外部模版 <import src="" ></import>
>
> 3.使用模版：<template is=""  data="{{}}"></template>

1.定义外部的模板



> 模板中的样式一般写在app.wxss文件中或者直接写在组件上（ 也可以写在使用模板的页面上，例如：template.wxss上）

**2.引用外部的模板**

https://developers.weixin.qq.com/miniprogram/dev/framework/view/wxml/import.html

```html
<!-- 3.使用外部的模板 -->
<import src="../temp/message.wxml" />
<template is="tempName3" data="{{...item}}"/>
```

### 5.import VS include

**import 有作用域的概念**，即只会 import 目标文件中定义的 template，而不会 import 目标文件 import 的 template。

**如：B import A，C import B，在C中可以使用B定义的template，在B中可以使用A定义的template，但是C不能使用A定义的template**。

```html
<!-- A.wxml -->
<template name="A">
  <text> A template </text>
</template>

<!-- B.wxml -->
<import src="a.wxml" /> <!-- B import A -->
<template is="A" /><!-- B可以使用A中的模板 -->
<template name="B">
  <text> B template </text>
</template>

<!-- C.wxml -->
<import src="b.wxml" />
<template is="A" />  <!-- C import B, C 可用B中的模板,而不能用A中的模板。这种是错误的-->
<template is="B" />  <!-- 这种是对的 -->
```



**include** 可以将目标文件**除了**  < template/>   < wxs /> 外的整个代码引入，相当于是拷贝到 `include` 位置，

如下面案例：

```html
<!-- header.wxml -->
<view> header </view>

<!-- footer.wxml -->
<view> footer </view>
```

```html
<!-- index.wxml -->
<include src="header.wxml" /> 
<view> body </view> 
<include src="footer.wxml" />
```

代码演示

```html
<!-- 4.在template.wxml中include外部的文件 -->
<include src="../temp/message.wxml" />
```



### 6.自定义加载进度模板-h100

#### 1.定义模板

```html
<template name='loading'>
  <view style='background:#F5FCFF;text-align:center;height:100rpx;line-height: 100rpx'>
    <view class='weui-loading'></view>
    <text style="font-size:30rpx">加载中...</text>
  </view>
</template>
```

weui-loading样式写在app.wxss中：

```css
/**下面这个样式是给view添加一个背景图片, 并使用css3旋转该组件*/
.weui-loading {
  margin: 0 5px;
  width: 20px;
  height: 20px;
  display: inline-block;
  vertical-align: middle;
  -webkit-animation: weuiLoading 1s steps(12, end) infinite;
          animation: weuiLoading 1s steps(12, end) infinite;
  background: transparent url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiB2aWV3Qm94PSIwIDAgMTAwIDEwMCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgxMDB2MTAwSDB6Ii8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjRTlFOUU5IiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgLTMwKSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iIzk4OTY5NyIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgzMCAxMDUuOTggNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjOUI5OTlBIiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKDYwIDc1Ljk4IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0EzQTFBMiIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSg5MCA2NSA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNBQkE5QUEiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoMTIwIDU4LjY2IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0IyQjJCMiIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgxNTAgNTQuMDIgNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjQkFCOEI5IiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKDE4MCA1MCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNDMkMwQzEiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTE1MCA0NS45OCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNDQkNCQ0IiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTEyMCA0MS4zNCA2NSkiLz48cmVjdCB3aWR0aD0iNyIgaGVpZ2h0PSIyMCIgeD0iNDYuNSIgeT0iNDAiIGZpbGw9IiNEMkQyRDIiIHJ4PSI1IiByeT0iNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTkwIDM1IDY1KSIvPjxyZWN0IHdpZHRoPSI3IiBoZWlnaHQ9IjIwIiB4PSI0Ni41IiB5PSI0MCIgZmlsbD0iI0RBREFEQSIgcng9IjUiIHJ5PSI1IiB0cmFuc2Zvcm09InJvdGF0ZSgtNjAgMjQuMDIgNjUpIi8+PHJlY3Qgd2lkdGg9IjciIGhlaWdodD0iMjAiIHg9IjQ2LjUiIHk9IjQwIiBmaWxsPSIjRTJFMkUyIiByeD0iNSIgcnk9IjUiIHRyYW5zZm9ybT0icm90YXRlKC0zMCAtNS45OCA2NSkiLz48L3N2Zz4=) no-repeat;
  background-size: 100%;
}
@-webkit-keyframes weuiLoading {
  0% {
    -webkit-transform: rotate3d(0, 0, 1, 0deg);
            transform: rotate3d(0, 0, 1, 0deg);
  }
  100% {
    -webkit-transform: rotate3d(0, 0, 1, 360deg);
            transform: rotate3d(0, 0, 1, 360deg);
  }
}
@keyframes weuiLoading {
  0% {
    -webkit-transform: rotate3d(0, 0, 1, 0deg);
            transform: rotate3d(0, 0, 1, 0deg);
  }
  100% {
    -webkit-transform: rotate3d(0, 0, 1, 360deg);
            transform: rotate3d(0, 0, 1, 360deg);
  }
}
```

#### 2.使用模板

```html
<!-- 1.导入一个加载中的模板 -->
<import src='../temp/loading.wxml' />
<!-- 2.使用模板 -->
<template is="loading" />
```



## 3.rich-text组件

https://developers.weixin.qq.com/miniprogram/dev/component/rich-text.html

> 1.可以渲染字符串模版    
>
> 2.可以渲染节点
>
> 3.适合展示html模版，不适合有业务逻辑的交互(  建议使用webview  )

### 1.使用html字符渲染

```json
/**定义一个html字符串模板: ( 样式写在使用的页面中 )  */
const htmlSnip =
  `<div class="div-class">
  <h1>Title</h1>
  <p class="p">
    Life is&nbsp;<i>like</i>&nbsp;a box of
    <b>&nbsp;chocolates</b>.
  </p>
  <img class="img" src="https://www.baidu.com/img/bd_logo1.png?where=super"/>
  <a href="https://www.baidu.com">A Link</a>
</div>
`
```

> 1.模版的样式支持class和style属性，**不支持id属性**。 2.只支持部分标签

对应的rich-text.wxml布局：

```html
<view>1.渲染html字符串</view>

<rich-text nodes="{{htmlSnip}}"></rich-text>
```

对应的rich-text.wxss样式：

```css
.div-class{
  background: skyblue;
}

.p{
  color: green;
}

/* 选择器不能使用 img */
.img{
  width: 200rpx;
  height: 100rpx;
}
```



### 2.使用节点渲染

**type = node**

```json
nodes: [{
      name: 'div',
      attrs: {
        class: 'div-class',
        style: 'line-height: 60px; color: #1AAD19;'
      },
      children: [
        {
        	type: 'text',
        	text: 'You never know what you\'re gonna get.'
      	}
      ]
    }]
```

> 上面的代码相当于：
>
> <div class="div-class"  style="xx">  You never know what you\'re gonna get.   </div>   这个布局

**1.定义节点**



1）如果是标签节点有下面属性（默认）：

**type = node**

| 属性       | 说明    | 类型     | 必填   | 备注                     |
| -------- | ----- | ------ | ---- | ---------------------- |
| name     | 标签名   | String | 是    | 支持部分受信任的HTML节点         |
| attrs    | 属性    | Object | 否    | 支持部分受信任的属性，遵循Pascal命名法 |
| children | 子节点列表 | Array  | 否    | 结构和nodes一致             |

```json
{
      name: 'div',
      attrs: {
      },
      children: [
      ]
}
```

2）如果是文本节点有下面一个给属性：

**type = text**

| 属性   | 说明   | 类型     | 必填   | 备注         |
| ---- | ---- | ------ | ---- | ---------- |
| text | 文本   | String | 是    | 支持entities |

```json
{
    type: 'text',
    text: 'You never know what you\'re gonna get.'
}
```

**2.渲染节点：**

```html
<view>1.渲染html字符串</view>
<rich-text nodes="{{htmlSnip}}"></rich-text>

<view>2.使用节点渲染</view>
<rich-text nodes="{{nodes}}"></rich-text>
```

## 4.webview组件-am

> 基础库 1.6.4 开始支持，低版本需做[兼容处理](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html)。

web-view 组件是一个可以用来承载网页的容器，**会自动铺满整个小程序页面**。**个人类型与海外类型的小程序暂不支持使用。**

> 客户端 6.7.2 版本开始，[`navigationStyle: custom`](https://developers.weixin.qq.com/miniprogram/dev/framework/config.html#window) 对 webview 组件无效

| 属性名         | 类型           | 默认值  | 说明                                       |
| ----------- | ------------ | ---- | ---------------------------------------- |
| src         | String       |      | webview 指向网页的链接。可打开关联的公众号的文章，其它网页需登录[小程序管理后台](https://mp.weixin.qq.com/)配置业务域名。 |
| bindmessage | EventHandler |      | 网页向小程序 postMessage 时，会在特定时机（小程序后退、组件销毁、分享）触发并收到消息。e.detail = { data } |
| bindload    | EventHandler |      | 网页加载成功时候触发此事件。e.detail = { src }         |
| binderror   | EventHandler |      | 网页加载失败的时候触发此事件。e.detail = { src }        |

```html
<web-view src="https://m.jd.com/"></web-view>
```



1）网页可以使用[JSSDK 1.3.2](https://res.wx.qq.com/open/js/jweixin-1.3.2.js)提供的接口实现：1.返回小程序页面  2.向小程序发送消息 等等

2）web-view中的bindmessage属性可以接受小程序发送消息。



## 5.open-data组件



> 基础库 1.4.0 开始支持，低版本需做[兼容处理](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html)。

用于展示微信**开放的数据**(  不需要授权也可以获取部分的用户数据  )

| 属性名      | 类型     | 默认值  | 说明                                       |
| -------- | ------ | ---- | ---------------------------------------- |
| type     | String |      | 开放数据类型                                   |
| open-gid | String |      | 当 type="groupName" 时生效,  获取 群的 id        |
| lang     | String | en   | 当 type="user*" 时生效，以哪种语言展示 userInfo，有效值有：en, zh_CN, zh_TW |

```html
<open-data type="userNickName"></open-data>
<view style='width:200rpx;height:200rpx;'>
    <open-data type="userAvatarUrl"></open-data>
</view>
<open-data type="userNickName" lang="en"></open-data>
```

> 注意：open-data组件圆头像如何实现？ overflow : hidde  ;  display:block

## 6.checkbox

多选项目。

| 属性名         | 类型      | 默认值   | 说明                                       |
| ----------- | ------- | ----- | ---------------------------------------- |
| **value**   | String  |       | [checkbox]()标识，选中时触发checkbox的 change 事件，并携带checkbox的 value |
| disabled    | Boolean | false | 是否禁用                                     |
| **checked** | Boolean | false | 当前是否选中，可用来设置默认选中(  适合使用js代码控制选中与否  )     |
| color       | Color   |       | checkbox的颜色，同css的color (  **勾的颜色**  )    |



1.引用checkbox

```html
<checkbox checked="{{false}}" color="red">play</checkbox>
```



2.监听checkbox的选择

> 1.添加 checkbox-group 监听。   2.checkbox 需要value属性

wxml代码：

```html
<checkbox-group bindchange="onbindchange">
  <checkbox value="玩游戏" checked="{{false}}" color="red">玩游戏</checkbox>
  <checkbox value="看电影" checked="{{false}}" color="red">看电影</checkbox>
</checkbox-group>
```

js代码：

```js
   /**
   * 页面的初始数据
   */
  data: {

  },

  onbindchange:function(event){

    console.log(event.detail)

  },
```



## 7.label

用来改进表单组件的可用性。

1.使用lable标签包裹表单等组件，当点击非表单组件时，就会触发对应的表单组件。

2.使用`for`属性找到对应的`id` ； 

> `for`优先级高于内部控件，内部有多个控件的时候默认触发第一个控件。

目前for可以**绑定**的控件有：button   checkbox   radio  switch

| 属性名  | 类型     | 说明           |
| ---- | ------ | ------------ |
| for  | String | **绑定**控件的 id |

**1.wxml布局**

```html
<checkbox-group bindchange="onbindchange">
  <checkbox value="玩游戏" checked="{{false}}" color="red"></checkbox> <text>玩游戏</text>
  <checkbox value="看电影" checked="{{false}}" color="red"></checkbox> <text>看电影</text>
</checkbox-group>
```

当点击 `玩游戏 和 看电影`  字体是不会选中checkbox , 只能点击选框才能选中。想要点击文本也能选中可以使用label 改进表单组件的可用性



**2.改进wxml布局:   使用label包裹每一个checkbox**

```html
<checkbox-group bindchange="onbindchange">
  <label>
      <checkbox value="玩游戏" checked="{{false}}" color="red"></checkbox> <text>玩游戏</text>
  </label>
  
  <label>
      <checkbox value="看电影" checked="{{false}}" color="red"></checkbox> <text>看电影</text>
  </label>
</checkbox-group>
```



**3.改进wxml布局：使用`for`属性**



```html
<checkbox-group bindchange="onbindchange">
  
  <checkbox id='check1' value="玩游戏" checked="{{false}}" color="red"></checkbox>
  <label for='check1'><text>玩游戏</text></label>

  <checkbox value="看电影" checked="{{false}}" color="red"></checkbox>
  <label for='check1'><text>看电影</text></label>

</checkbox-group>
```



**4.`for`优先级高于内部控件，label内部有多个控件的时候默认触发第一个控件**

```html
<view>3.label内部有多个控件也没有指定for属性的时候，默认选中第一个</view>

<view>
 <!--label内部有多个控件也没有指定for属性的时候，默认选中第一个-->	
  <label>
      <checkbox value="玩游戏" checked="{{false}}" color="red"></checkbox><text>玩游戏</text>
      <checkbox value="看电影" checked="{{false}}" color="red"></checkbox><text>看电影</text>
      <checkbox value="看电影" checked="{{false}}" color="red"></checkbox><text>看书</text>
  </label>

</view>

<view>

  <!--label内部有多个控件有指定for属性的时候，默认选中指定那个-->	
  <label for='check2'>
      <checkbox value="玩游戏" checked="{{false}}" color="red"></checkbox><text>玩游戏</text>
      <checkbox id='check2' value="看电影" checked="{{false}}" color="red"></checkbox><text>看电影</text>
      <checkbox value="看电影" checked="{{false}}" color="red"></checkbox><text>看书</text>
  </label>

</view>
```



## 8.radio

单选项目

| 属性名         | 类型      | 默认值   | 说明                                       |
| ----------- | ------- | ----- | ---------------------------------------- |
| **value**   | String  |       | radio 标识。当该 radio 选中时，radio-group 的 change 事件会携带radio 的value |
| **checked** | Boolean | false | 当前是否选中                                   |
| disabled    | Boolean | false | 是否禁用                                     |
| color       | Color   |       | radio的颜色，同css的color                      |

1.wxml

```html
<!-- radio 和 radio-group 要一起用才会有效果 -->	
<radio-group bindchange="radioChange">
  
   <radio value='男'>男</radio>
   <radio value='女' checked="{{checked}}">女</radio>
  
</radio-group>
```



2.js

```js
  /**
   * 页面的初始数据
   */
  data: {
    checked:true
  },

  radioChange:function(event){
    console.log(event.detail)
  },
```



## 9.picker

从**底部弹起**的滚动选择器，现支持五种选择器，通过mode来区分，分别是普通选择器，多列选择器，时间选择器，日期选择器，省市区选择器，默认是普通选择器。

### 1.普通选择器-selector

> array: ['美国', '中国', '巴西', '日本','韩国','巴西','印度','泰国'],

| 属性名            | 类型                   | 默认值   | 说明                                       | 最低版本 |
| -------------- | -------------------- | ----- | ---------------------------------------- | ---- |
| **range**      | Array / Object Array | []    | mode为 selector 或 multiSelector 时，range 有效 |      |
|                |                      |       |                                          |      |
| **value**      | Number               | 0     | value 的值表示选择了 range 中的第几个（下标从 0 开始）      |      |
| **bindchange** | EventHandle          |       | value 改变时触发 change 事件，event.detail = {value: value} |      |
| disabled       | Boolean              | false | 是否禁用                                     |      |
| bindcancel     | EventHandle          |       | 取消选择或点遮罩层收起 picker 时触发                   |      |



1.wxml

```html
<picker
  mode="selector"
  range="{{array}}"
  value='1'
  bindchange="onbindchange"
>
    <button size='mini' type='primary'>1.普通选择器</button>
</picker>
```



2.js

```js
  /**
   * 页面的初始数据
   */
  data: {
    array: ['美国', '中国', '巴西', '日本','韩国','巴西','印度','泰国'],
  },
    
  /**点击确认时回调 */
  onbindchange:function(event){
     console.log(event.detail)

  },
  
```



### 2.多列选择器-multiSelector

| 属性名                  | 类型                       | 默认值   | 说明                                       | 最低版本                                     |
| -------------------- | ------------------------ | ----- | ---------------------------------------- | ---------------------------------------- |
| **range**            | 二维Array / 二维Object Array | []    | mode为 selector 或 multiSelector 时，range 有效。二维数组，长度表示多少列，数组的每项表示每列的数据，如`[["a","b"], ["c","d"]]` |                                          |
| range-key            | String                   |       | 当 range 是一个 二维Object Array 时，通过 range-key 来指定 Object 中 key 的值作为选择器显示内容 |                                          |
| **value**            | Array                    | []    | value 每一项的值表示选择了 range 对应项中的第几个（下标从 0 开始）。[0,0] |                                          |
| **bindchange**       | EventHandle              |       | value 改变时触发 change 事件，event.detail = {value: value} |                                          |
| **bindcolumnchange** | EventHandle              |       | 某一列的值改变时触发 columnchange 事件，event.detail = {column: column, value: value}，column 的值表示改变了第几列（下标从0开始），value 的值表示变更值的下标 |                                          |
| bindcancel           | EventHandle              |       | 取消选择时触发                                  | [1.9.90](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| disabled             | Boolean                  | false | 是否禁用                                     |                                          |





1.wxml

```html
<picker
  mode="multiSelector"
  range="{{multiArray}}"
  value='{{multiIndex}}' 
  bindcolumnchange="onbindcolumnchange"
  bindchange="onbindchange"
>
    <button size='mini' type='primary'>2.多列选择器</button>
</picker>
```

2.js

```js
  /**
   * 页面的初始数据
   */
  data: {
    array: ['美国', '中国', '巴西', '日本','韩国','巴西','印度','泰国'],

    multiArray: [
        ['无脊柱动物', '脊柱动物'], 
        ['扁性动物', '线形动物', '环节动物', '软体动物', '节肢动物'], 
        ['猪肉绦虫', '吸血虫']
    ],
    multiIndex: [1, 0, 1], 
      
  },


  /**点击确认时回调 */
  onbindchange:function(event){
     console.log(event.detail)

  },

  /** 当滚动的时候会回调*/
  onbindcolumnchange:function(event){
    console.log(event.detail) // {column:0,value:0}  代表是滚动第0列的第0个值
  },
```



### 3.时间选择器-time

| 属性名            | 类型          | 默认值   | 说明                                       | 最低版本                                     |
| -------------- | ----------- | ----- | ---------------------------------------- | ---------------------------------------- |
| **value**      | String      |       | 表示**选中**的时间，格式为"hh:mm"                   |                                          |
| **start**      | String      |       | 表示**有效时间范围**的开始，字符串格式为"hh:mm"            |                                          |
| **end**        | String      |       | 表示**有效时间范围**的结束，字符串格式为"hh:mm"            |                                          |
| **bindchange** | EventHandle |       | value 改变时触发 change 事件，event.detail = {value: value} |                                          |
| bindcancel     | EventHandle |       | 取消选择时触发                                  | [1.9.90](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| disabled       | Boolean     | false | 是否禁用                                     |                                          |



1.wxml

```html
<picker
    mode="time"
    value="{{time}}"
    start="09:00"
    end="21:00"
    bindchange="bindTimeChange"
  >
    <button size='mini' type='primary'>2.时间选择器</button>
</picker>
```



2.js

```js
  /**
   * 页面的初始数据
   */
  data: {
    ....
    ....

    time: '12:01',

  },

  bindTimeChange:function(event){
    console.log(event.detail)
  },

```





### 4.日期选择器-date



1.wxml

```html

<picker
    mode="date"
    value="{{date}}"
    start="2015-09-01"
    end="2017-09-01"
    bindchange="bindDateChange"
  >
    <button size='mini' type='primary'>4.日期选择器</button>
</picker>
```



2.js

```js
 data: {
    ....
    date:'2016-01-01'

  },
  
  bindDateChange:function(event){
    console.log(event.detail)
  },
  
```



### 5.省市区选择器-region

region  [ˈri:dʒən]  区域





1.wxml

```html
<picker
    mode="region"
    bindchange="bindRegionChange"
    value="{{region}}"
    custom-item="{{customItem}}"
  >
    <button size='mini' type='primary'>5.省市区选择器</button>
</picker>
```



2.js

```js
  /**
   * 页面的初始数据
   */
  data: {
    ....
    
    region: ['广东省', '广州市', '海珠区'],
    customItem: '全部'

  },

  bindRegionChange: function (event) {
    console.log(event.detail)
  },
```

> 注意：很多属性不是必须的



## 10.picker-view

嵌入页面的滚动选择器, 而不是从底部弹出的选择器

> 注意：其中只可放置`<picker-view-column/>`组件，其他节点不会显示。

| value               | NumberArray | 数组中的数字依次表示 picker-view 内的 picker-view-column 选择的第几项（下标从 0 开始），数字大于 picker-view-column 可选项长度时，选择最后一项。 | [0,0,0]                                  |
| ------------------- | ----------- | ---------------------------------------- | ---------------------------------------- |
| **indicator-style** | String      | 设置选择器**中间**选中框的**样式**                    |                                          |
| indicator-class     | String      | 设置选择器**中间**选中框的**类名**                    | [1.1.0](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| mask-style          | String      | 设置蒙层的样式                                  | [1.5.0](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| mask-class          | String      | 设置蒙层的类名                                  | [1.5.0](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| **bindchange**      | EventHandle | 当滚动选择，value 改变时触发 change 事件，event.detail = {value: value}；value为数组，表示 picker-view 内的 picker-view-column 当前选择的是第几项（下标从 0 开始） |                                          |
| bindpickstart       | EventHandle | 当滚动选择开始时候触发事件                            | [2.3.1](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| bindpickend         | EventHandle | 当滚动选择结束时候触发事件                            |                                          |



**picker-view-column**

仅可放置于 picker-view中，其孩子节点的高度会自动设置成与picker-view的选中框的高度一致





1.wxml

```html
<picker-view
    indicator-style="height: 50px;"
    value="{{value}}"
    style="width: 100%; height: 300px;background:orange;"
    bindchange="bindChange"
  >
    <picker-view-column>
      <view wx:for="{{years}}" style="line-height: 50px;text-align:center">{{item}}年</view>
    </picker-view-column>
    <picker-view-column>
      <view wx:for="{{months}}" style="line-height: 50px;text-align:center">{{item}}月</view>
    </picker-view-column>
    <picker-view-column>
        <view wx:for="{{days}}" style="line-height: 50px;text-align:center">{{item}}月</view>
    </picker-view-column>

    <picker-view-column>
        <view style="line-height: 50px;text-align:center">上午</view>
        <view style="line-height: 50px;text-align:center">下午</view>
    </picker-view-column>

</picker-view>
```



2.js

```js

const date = new Date()
const years = []
const months = []
const days = []

for (let i = 2000; i <= date.getFullYear(); i++) {
  years.push(i)
}

for (let i = 1; i <= 12; i++) {
  months.push(i)
}

for (let i = 1; i <= 31; i++) {
  days.push(i)
}


Page({

  /**
   * 页面的初始数据
   * years [2000,2001,...]
   * months [1, 2,...]
   * days [1, 2,...]
   * value [1,1,1]
   */
  data: {
    years,
    months,
    days,
    value: [1, 0, 1],
  },

  bindChange(event) {
    console.log(event.detail.value)
  }

})
```





## 11.swiper-400

swiper是一个**滑块视图容器**。即: **轮播图**组件或者**焦点图**组件。swiper这个组件封装的已经比较完善，使用起来非常方便。

### 2.swiper组件常用属性

https://mp.weixin.qq.com/debug/wxadoc/dev/component/swiper.html

| 属性名                    | 类型          | 默认值               | 说明                                       | 最低版本                                     |
| ---------------------- | ----------- | ----------------- | ---------------------------------------- | ---------------------------------------- |
| indicator-dots         | Boolean     | false             | 是否显示面板指示点                                |                                          |
| indicator-color        | Color       | rgba(0, 0, 0, .3) | 指示点颜色                                    | [1.1.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| indicator-active-color | Color       | #000000           | 当前选中的指示点颜色                               | [1.1.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| autoplay               | Boolean     | false             | 是否自动切换                                   |                                          |
| current                | Number      | 0                 | 当前所在页面的 index。  ['kʌr(ə)nt]              |                                          |
| interval               | Number      | 5000              | 自动切换每一页时间的间隔                             |                                          |
| duration               | Number      | 500               | 滑动一页时的动画时长                               |                                          |
| circular               | Boolean     | false             | ['sɜːkjʊlə] 是否采用衔接滑动（ loop ）             |                                          |
| vertical               | Boolean     | false             | 滑动方向是否为纵向                                |                                          |
| bindchange             | EventHandle |                   | current 改变时会触发 change 事件，event.detail = {current: current, source: source} |                                          |

### 4.swiper组件的使用

> **注意**：swiper只中可放置swiper-item组件，否则会导致未定义的行为。swiper-item的宽度自定设计为100%。

#### 1.引入准备数据

```
 banners:[
      'http://img02.tooopen.com/images/20150928/tooopen_sy_143912755726.jpg',
      'http://img06.tooopen.com/images/20160818/tooopen_sy_175866434296.jpg',
      'http://img06.tooopen.com/images/20160818/tooopen_sy_175833047715.jpg'
    ],
  
```



#### 2.引入swiper组件-400



#### 3.添加分页器-点-indicator

1.添加点



2.修改点的颜色

#### 4.自动轮播-auto-intervel

自动轮播和自定轮播切换的时间



#### 5.循环轮播-circular



#### 6.纵向轮播-vertical



> current-item-id  vs   item-id    ===  current

## 12.video组件

### 1.video组件的简介

视频组件，用来播放本地和网络上的视频

### 2.video组件的常用属性

| 属性名                  | 类型           | 默认值     | 说明                                       | 最低版本                                     |
| -------------------- | ------------ | ------- | ---------------------------------------- | ---------------------------------------- |
| src                  | String       |         | 要播放视频的资源地址                               |                                          |
| initial-time         | Number       |         | 指定视频初始播放位置: initial-time='100' 或 initial-time='{{60}}' | [1.6.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| duration             | Number       |         | **仅**指定视频时长: duration='60'               | [1.1.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| controls             | Boolean      | true    | 是否显示默认播放控件（播放/暂停按钮、播放进度、时间）controls="{{true}}" |                                          |
| **danmu-list**       | Object Array |         | 弹幕列表:danmu-list="{{ arr }}"              |                                          |
| **danmu-btn**        | Boolean      | false   | 是否显示弹幕按钮，只在初始化时有效，不能动态变更                 |                                          |
| **enable-danmu**     | Boolean      | false   | 是否展示弹幕，只在初始化时有效，不能动态变更                   |                                          |
| autoplay             | Boolean      | false   | 是否自动播放                                   |                                          |
| loop                 | Boolean      | false   | 是否循环播放                                   | [1.4.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| muted                | Boolean      | false   | 是否静音播放                                   | [1.4.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| page-gesture         | Boolean      | false   | 在非全屏模式下，是否开启亮度与音量调节手势                    | [1.6.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| bindplay             | EventHandle  |         | 当开始/继续播放时触发play事件                        |                                          |
| bindpause            | EventHandle  |         | 当暂停播放时触发 pause 事件                        |                                          |
| bindended            | EventHandle  |         | 当播放到末尾时触发 ended 事件                       |                                          |
| bindtimeupdate       | EventHandle  |         | 播放进度变化时触发，event.detail = {currentTime: '当前播放时间'} 。触发频率应该在 250ms 一次 |                                          |
| bindfullscreenchange | EventHandle  |         | 当视频进入和退出全屏是触发，event.detail = {fullScreen: '当前全屏状态'} | [1.4.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| objectFit            | String       | contain | 当视频大小与 video 容器大小不一致时，视频的表现形式。contain：包含，fill：填充，cover：覆盖 |                                          |
| poster               | String       |         | 默认控件上的音频封面的图片资源地址，如果 controls 属性值为 false 则设置 poster 无效 |                                          |

### 3.video组件的使用

#### 1.引入本地数据

```son
 urls:[
       "http://baobab.kaiyanapp.com/api/v1/playUrl?vid=56841&editionType=default&source=qcloud",
       
       "http://baobab.kaiyanapp.com/api/v1/playUrl?vid=56499&editionType=default&source=qcloud",
       
       "http://baobab.kaiyanapp.com/api/v1/playUrl?vid=19111&editionType=default&source=qcloud",
       
       "http://baobab.kaiyanapp.com/api/v1/playUrl?vid=22963&editionType=high&source=qcloud",
       
     ],
```



#### 2.引入video组件-400



> 如何video播放出现这个错误，是开发工具的问题：net::ERR_INSUFFICIENT_RESOURCES 

#### 3.其它的属性使用

```html
<view>

<block wx:for="{{urls}}">
      <video src="{{item}}" 
      style="width:100%;height:400rpx;" 
      initial-time="100" //指定视频初始播放位置 1.6.0

      muted="{{true}}"
	  loop="{{true}}"
	  autoplay="{{true}}"

      
      bindplay="onBindplay"
      bindpause="onBindpause"
      > 
      </video>
</block>

</view>
```

#### 4.弹幕使用

##### 1.准备弹幕的数据-text-color-time

```son
danmuList:
     [
       {	
        text: '第 1s 出现的弹幕',
        color: '#ff0000',
        time: 1
       },
       {
        text: '第 3s 出现的弹幕',
        color: '#ff00ff',
        time: 3
       }
     ],
```

##### 2.开始弹幕功能



##### 5.发送弹幕

**原理：调用video对象中sendDanmu( {  } ) 函数**

1.写发送弹幕布局



2.获取input输入框的内容

> this.inputValue=e.detail.value ;  //将获取的内容存到this的inputValue变量中 



3.监听点击发送弹幕-onReady

> 注意：wx.createVideoContext('myVideo',this) 中的myVideo是video组件中的id名称

```js
//随机获取颜色值, 返回的结果例如: #AE0B08
function getRandomColor() {
  const rgb = []
  for (let i = 0; i < 3; ++i) {
    let color = Math.floor(Math.random() * 256).toString(16)   // AE 、  B  、8
    color = color.length == 1 ? '0' + color : color  //AE   、 0B   、08
    rgb.push(color)
  }
  return '#' + rgb.join('') //AE0B08
}
```







