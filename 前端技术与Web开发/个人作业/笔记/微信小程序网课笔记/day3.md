小程序进阶一

## 1.事件处理

### 1.什么是事件

> 点击事件，长按事件，滚动事件，触摸事件 , 表单提交事件.....

- 事件是**视图层（wxml）到逻辑层(js)**的通讯方式。
- 事件可以将**用户的行为**反馈到**逻辑层**进行处理。
- 事件可以**绑定**在**组件**上，当达到触发事件，就会执行逻辑层中对应的**事件处理函数**。
- 事件对象event可以携带额外信息，如 id, dataset, touches。

### 2.事件的使用方式

#### 1.给组件添加点击Tap事件

> bindtap  :  bind ： 是绑定事件的意思， tap ： 是说绑定的事件是一个点击事件

1.绑定tap事件

```html
<view id="myView1" bindtap="onBindViewTap1" data-msg="xmg"> 
 1.给view绑定一个tap事件
</view>
```



2.处理点击事件, 并查看控制台的输出

> 注意： currentTarget   和  target  代表的实例
>
> currentTarget : 设计监听事件的目标
>
>  target ： 第一个发生事件的目标（事件源）

```json
这个是事件对象e :

{
"type":"tap",  // 事件类型
"timeStamp":895, //时间戳
"target": {    //发生点击事件的目标（事件源）
  "id": "myView1",   //组件的id
  "dataset":  {  
    "msg":"xmg"   //组件data-xxx绑定的数据
  }
},
"currentTarget":  {  //当前 设计了监听事件 的目标
  "id": "myview1",  //组件的id
  "dataset": {
    "msg":"xmg"   //组件data-xxx绑定的数据
  }
},
"detail": {   //点击的 x y 轴坐标
  "x":53,
  "y":14
},
"touches":[{   //点击的坐标
  "identifier":0,
  "pageX":53,
  "pageY":14,
  "clientX":53,
  "clientY":14
}],
"changedTouches":[{   //点击的坐标
  "identifier":0,
  "pageX":53,
  "pageY":14,
  "clientX":53,
  "clientY":14
}]
}
```

### 3.事件分类

事件分为冒泡( bubble )事件和非冒泡事件：

1. 冒泡事件：当一个组件上的事件被触发后，该事件会**向父节点传递**。
2. 非冒泡事件：当一个组件上的事件被触发后，该事件不会向父节点传递。

**WXML的冒泡事件列表**：

| 类型                 | 触发条件                                     | 最低版本                                     |
| ------------------ | ---------------------------------------- | ---------------------------------------- |
| touchstart         | 手指触摸动作开始                                 |                                          |
| touchmove          | 手指触摸后移动                                  |                                          |
| touchcancel        | 手指触摸动作被打断，如来电提醒，弹窗                       |                                          |
| touchend           | 手指触摸动作结束                                 |                                          |
| **tap**            | 手指触摸后马上离开                                |                                          |
| **longpress**      | 手指触摸后，超过350ms再离开，如果指定了事件回调函数并触发了这个事件，tap事件将不被触发 | [1.5.0](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/compatibility.html) |
| longtap            | 手指触摸后，超过350ms再离开（推荐使用longpress事件代替）      |                                          |
| transitionend      | 会在 WXSS transition 或 wx.createAnimation 动画结束后触发 |                                          |
| animationstart     | 会在一个 WXSS animation 动画开始时触发              |                                          |
| animationiteration | 会在一个 WXSS animation 一次迭代结束时触发            |                                          |
| animationend       | 会在一个 WXSS animation 动画完成时触发              |                                          |



**注：除上表之外的其他组件自定义事件如无特殊申明都是非冒泡事件，如的submit事件，的input事件，的scroll事件，(详见各个组件)**



### 4.冒泡事件-bind

> 注意：冒泡事件一般以bind开头, 例如：bindtap

#### 1.写布局

```
布局：
<view id="outer" bindtap="handleTap1">
  outer view
  <view id="middle" bindtap="handleTap2">
    middle view
    <view id="inner" bindtap="handleTap3">
      inner view
    </view>
  </view>
</view>

样式：
#outer{
  background: red;
  height: 400rpx;
  width: 100%;
}

#middle{
  background: green;
  width: 50%;
  height: 300rpx;
}

#inner{
  background: yellow;
  height: 100rpx;
  width: 30%;
}
```

#### 2.监听冒泡事件

冒泡事件：当一个组件上的事件被触发后，该事件会**向父节点传递**。



### 5.阻止冒泡事件-catch







## 2.WXS

###1.小程序脚本语言简介

WXS（WeiXin Script）是**小程序的一套脚本语言**，结合 `WXML`，可以构建出页面的结构。

注意：

1. wxs **不依赖**于运行时的基础库版本，可以在所有版本的小程序中运行。
2. wxs 与 javascript 是**不同**的语言，有自己的语法，并不和 javascript 一致。
3. wxs 的运行环境和其他 javascript 代码是**隔离**的，wxs 中不能调用其他 javascript 文件中定义的函数，也不能调用小程序提供的API。
4. wxs 函数不能作为组件的**事件回调**。
5. 由于运行环境的差异，在 iOS 设备上小程序内的 wxs 会比 javascript 代码**快 2 ~ 20 倍**。在 android 设备上二者运行效率无差异。

> 1.小程序脚本语言 主要是用来增强页面的表达能力
>
> 2.对es6的支持不友好。比如，const  let 箭头函数不支持。



小程序原理架构图：

微信小程序的框架包含两部分View视图层(可能存在多个)、App Service逻辑层(一个)，View层用来渲染页面结构，AppService层用来逻辑处理、数据请求、接口调用，它们在两个线程(webview)里运行。启动小程序默认至少有两个webview 。

一个视图层使用一个WebView渲染，逻辑层仅使用一个WebView并在其独立的 JS 引擎中运行。

视图层和逻辑层通过系统层的WeixinJsBridage进行通信，逻辑层把数据变化通知到视图层，触发视图层页面更新，视图层把触发的事件通知到逻辑层进行业务处理。



**讲一下wxs :**

**由于view 与 App Service**是不同线程,之前是传递数据。现在当遇到一些数据需要在view中处理时, 就可以用wxs来处理。



### 2.WXS 的简单示例

> 1.在wxml中定义wxs模版  <wxs module="msg" >  xxxxx  </wxs>
>
> 2.使用：<Text> {{  msg.xxx }} </Text>



```html

<!-- 1.在wxs中定义变量 -->
<wxs module="msg">

  var message1 = '我是在wxs中定义的变量message1';
  var message2 = '我是在wxs中定义的变量message2';


  //module.exports.message1=message1;
  //module.exports.message2=message2;

  <!-- 导出定义的变量 -->
  module.exports = {
    message1:message1, //这里不能简写
    message2:message2
  }

</wxs>

<!-- 2.使用data定义的变量 -->
<view>{{value}}</view>

<!-- 3.使用wxs中定义的变量 -->
<view>{{msg.message1}}</view>
<view>{{msg.message2}}</view>
```

#### 1.变量

- WXS 中的变量均为**值的引用**。
- **没有声明**的变量直接赋值使用，会被定义为**全局变量**。
- 如果只声明变量而不赋值，则默认值为 `undefined`。
- var表现与javascript一致，会有变量提升。

```js
var foo = 1
var bar = 'hello world'
var i // i === undefined
```

上面代码，分别声明了 `foo`、 `bar`、 `i` 三个变量。然后，`foo` 赋值为数值 `1` ，`bar` 赋值为字符串 `"hello world"`。



变量命名必须符合下面两个规则：

- 首字符必须是：字母（a-zA-Z），下划线（_）
- 剩余字符可以是：字母（a-zA-Z），下划线（_）， 数字（0-9）

#### 2.注释

WXS 主要有 3 种注释的方法。

**示例代码：**

```html
<!-- wxml -->
<wxs module="sample">

  // 方法一：单行注释 
  /* 方法二：多行注释 */ 
  
  /* 方法三：结尾注释。即从 /* 开始往后的所有 WXS 代码均被注释 var a = 1; var b = 2; var c = "fake";
  
</wxs>
```

上述例子中，所有 WXS 代码均被注释掉了。

> 方法三 和 方法二 的唯一区别是，没有 `*/` 结束符。



### 3.wxs数据处理-时间格式化

获取时间戳：https://tool.lu/timestamp

1545117587000   ----->   2018-12-18 15:19:47

下面的案例是将data中的时间戳 , 格式化后输出到界面

1.wxml  查看数据类型的api

Number

```html

<!-- 1.在wxs中定义变量 -->
<wxs module="msg">
  
  var formTime = function(time){
    //1.查看数据类型的api, 注意获取date不是通过new Date()
    var date=getDate(time) //只接受number类型
    var formTime = date.getFullYear() +'-'+ ( date.getMonth()+1 ) +'-'+date.getDate();
    return formTime;
  }

  module.exports = {
    formTime:formTime  //这里不能简写
  }

</wxs>

<!-- 3.使用wxs中定义的变量 -->
<view>{{ msg.formTime(time) }}</view>
```



2.js

```js
  /**
   * 页面的初始数据
   */
  data: {
    value:'我是在data定义的变量',
    time:1545117587000
  },
```





### 4.wxs工具类-价格格式

> 1.第一编写wxs文件，不用指定module
>
> 2.<wxs  src=""   module="tools" ></wxs>
>
> 3.使用：<Text> {{  tools.xxx }} </Text>

#### 1.在wxs文件中编写函数

String





```js
var message = '价格的格式化';

var formPrice = function(price){
  //1.把字符串转成int
  price = parseFloat(price);
  //2.保留2位小数点
  return price.toFixed(2);
}

module.exports= {
  message:message,  //不支持简写
  formPrice: formPrice
}
```



####2.导入编写好的工具函数

> <wxs src="../wxs/tools.wxs" module="tools"></wxs>





```html
<!-- 4.引用外部wxs定义的工具 -->
<wxs src="../wxs/tools.wxs" module="tools"></wxs>
<view>{{ tools.message}}:{{ tools.formPrice('112.242343') }}</view>
```



## 2.自定义组件

开发者可以将**页面内的功能模块**抽象成自定义组件，以便在不同的页面中重复使用；

也可以将**复杂的页面拆分成多个低耦合的模块**，有助于代码维护。

https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/

### 1.自定义组件的示例

#### 1.创建自定义组件

类似于页面，一个自定义组件由 `json` `wxml` `wxss` `js` 4个文件组成。要编写一个自定义组件，首先需要在 `json` 文件中进行自定义组件声明（将 `component` 字段设为 `true` 可这一组文件设为自定义组件）：

```json
{
  "component": true
}
```





####2.使用自定义组件

使用已注册的自定义组件前，首先要在**使用该组件页面的 `json` 文件中进行引用声明**。此时需要提供每个自定义组件的**标签名**和对应的自定义组件**文件路径**：

```json
{
    "usingComponents": {
      "my-view": "../../components/my-view/my-view"
    }
}
```



这样，在页面的 `wxml` 中就可以像使用基础组件一样使用自定义组件。节点名即自定义组件的标签名，节点属性即传递给组件的属性值。

> 开发者工具 1.02.1810190 及以上版本支持在 app.json 中声明 usingComponents 字段，在此处声明的自定义组件视为全局自定义组件，在小程序内的页面或自定义组件中可以直接使用而无需再声明。



#### 3.自定义组件的插槽

在组件的wxml中可以包含 `slot` 节点，用于承载组件使用者提供的wxml结构。

默认情况下，一个组件的wxml中只能有一个slot。需要使用多slot时，可以在组件js中声明启用。

##### 1.默认一个插槽

定义插槽 slot



使用插槽





##### 2.允许多个插槽

同时存在多个插槽的时候要给插槽起名称

1.定义多个插槽

```html
<view>
  <view>我是自定义my-view组件</view>
  <!-- 我是组件中的插槽 -->
  <slot name="content"></slot>
  <slot name="footer"></slot>

</view>
```



2.声明启用多个插槽



```js
options: {
    multipleSlots: true // 在组件定义时的选项中启用多slot支持
},
```



3.插槽的使用





#### 4.自定义组件的样式

组件可以指定它所在节点的默认样式，使用 `:host` 选择器（需要包含基础库 [1.7.2](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 或更高版本的开发者工具支持）。

##### 1.组件默认的样式-host

```css
/* components/my-view/my-view.wxss */
:host{
  /* 这些样式会被继承 */
  color: pink;
  font-size: 50rpx;
  line-height: 50rpx;

  /* 这个不会被继承 */
  background: red;
  
}
```



**CSS 哪些属性默认会继承, 哪些不会继承?**

**1）.不可继承的**：display、margin、border、padding、background、height、min-height、max-height、width、min-width、max-width、overflow、position、left、right、top、bottom、z-index、float、clear、table-layout、vertical-align、page-break-after、page-bread-before和unicode-bidi

**2）.所有元素可继承**：visibility和cursor

**3）.内联元素可继承**：letter-spacing、word-spacing、white-space、line-height、color、font、font-family、font-size、font-style、font-variant、font-weight、text-decoration、text-transform、direction。





##### 2.组件内部样式-class

组件对应 `wxss` 文件的样式，只对组件wxml内的节点生效。编写组件样式时，需要注意以下几点：

- 组件和引用组件的页面**不能使用id**选择器（`#a`）、**属性选择器**（`[a]`）和**标签名选择器**，请**改用class**选择器。
- 组件和引用组件的页面中使用**后代选择器**（`.a .b`）在一些极端情况下会有非预期的表现，如遇，请**避免**使用。
- 子元素选择器（`.a>.b`）只能用于 `view` 组件与其子节点之间，用于其他组件可能导致非预期的情况。
- **继承样式**，如 `font` 、 `color` ，会从组件外继承到组件内。
- 除继承样式外， `app.wxss` 中的样式、组件所在页面的的样式对自定义组件无效。

```css
#a {
} /* 在组件中不能使用 */

[a] {
} /* 在组件中不能使用 */

button {
} /* 在组件中不能使用 */

.a > .b {
} /* 除非 .a 是 view 组件节点，否则不一定会生效 */
```

除此以外，组件可以指定它所在节点的默认样式，使用 `:host` 选择器（需要包含基础库 [1.7.2](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 或更高版本的开发者工具支持）。

my-view.wxml不布局

```html
<view class="my-view">

  <view class="title">我是自定义my-view组件</view>
  <!-- 我是组件中的插槽 -->
  <slot name="content"></slot>
  <slot name="footer"></slot>

</view>
```

 



##### 3.组件外部样式-external

有时，组件希望接受外部传入的样式类（类似于 `view` 组件的 `hover-class` 属性）。此时可以在 `Component` 中用 `externalClasses` 定义段定义若干个外部样式类。这个特性从小程序基础库版本 [1.9.90](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 开始支持。

**注意：在同一个节点上使用普通样式类和外部样式类时，两个类的优先级是未定义的，因此最好避免这种情况。**



1.组件定义可接收外部的样式类

```js
  // 1.定义该组件可以接收的外部样式类
  externalClasses: ['my-view-class','my-view-active-class'],
```

> 注意样式的有级别问题，同一级别时内部样式可能会优先外部样式【 优先级是未定义的 】

 



2.组件使用定义的样式类

```html
<view class="my-view">
  <!-- 1.我是自定义组件 -->	
  <view class="title">我是自定义my-view组件</view>
  <!-- 2.我是组件中的插槽 -->
  <slot name="content"></slot>
  <slot name="footer"></slot>

  <!-- 3.我是组件中的样式 -->
  <view class="my-view-class">我使用的是外部传递进来的样式类</view>
  <view class="{{ true ? 'my-view-active-class' : '' }}">我使用的是外部传递进来的样式类</view>


</view>
```





 

3.外部传递样式类到组件内部



use-components.wxml布局：

```html
<!-- 使用自定义组件，这里将 my-view 类传递给my-view-class ; ... -->
<my-view my-view-class="my-view" my-view-active-class="my-view-active">
   
   <text slot="content">content布局\n</text>
   <text slot="footer">footer布局</text>
   

</my-view>
```

use-components.wxss 样式：

```css
/* pages/02-use-components/use-components.wxss */
.my-view{
  color: white;
  background: red;
}

.my-view-active{
  color: white;
  font-size: 50rpx;
  background: pink;
}
```



##### 4.内部class和external

当**一个组件同时**使用 **内部class** 和  **外部的class** 的时候，优先级别是没有定义的。建议避免这种情况，或者

两者应用不同的css属性



#### 5.组件接收外部数据

https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/component.html

##### 1.组件接收外部传的数据



```html
<!-- 使用自定义组件 -->
<my-view my-view-class="my-view" my-view-active-class="my-view-active"
  arrs-pramas = "{{ [1,2,3,4] }}"
  str-pramas = "liujun"
  num-pramas = "12"
>
   
   <text slot="content">content布局\n</text>
   <text slot="footer">footer布局</text>
   

</my-view>
```





##### 2.组件定义接收外部数据



```js
Component({ 
  
  /**
   * 组件的属性列表
   */
  properties: {
    
    arrsPramas:{
      type: Array, // 类型（必填），目前接受的类型包括：String, Number, Boolean, Object, Array, null（表示任意类型）
      value: [0,0,0,0], // 属性初始值（可选），如果未指定则会根据类型选择一个
      observer(newVal, oldVal, changedPath) {
        // 属性被改变时执行的函数（可选），也可以写成在methods段中定义的方法名字符串, 如：'_propertyChange'
        // 通常 newVal 就是新设置的数据， oldVal 是旧数据
        console.log(newVal,oldVal,changedPath) // [1,2,3,4] , [0,0,0,0] , ["arrsPramas"]
        // 通常这里也可以将数据备份到data中
        this.setData({
            as:newVal
        })
      }
    }
    
    strPramas: { // 属性名
      type: String, // 类型（必填），目前接受的类型包括：String, Number, Boolean, Object, Array, null（表示任意类型）
      value: '', // 属性初始值（可选），如果未指定则会根据类型选择一个
    },
    
    numPramas: Number // 简化的定义方式
    //...
  },
  
  
})
```



##### 3.组件使用接收到的数据

> properties 中定义的属性直接在模版中使用（ 不能通过this.data.xxx获取传进过来的数据 ）



```html
<view class="my-view">
  .....
  .....
  <view>===========接收外面的属性==============</view>
  
  <view wx:for="{{arrsPramas}}">
    {{item}}
  </view>
  <view>{{strPramas}}</view>
  <view>{{numPramas}}</view>

</view>
```



### 2.使用构造器构造页面-am

https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/component.html

事实上，**小程序的页面**也可以视为**自定义组件**。因而，页面也可以使用 `Component` 构造器构造，拥有与普通组件一样的定义段与实例方法。但此时要求对应 json 文件中包含 `usingComponents` 定义段。

此时，组件的属性可以用于接收页面的参数，如访问页面 `/pages/index/index?paramA=123&paramB=xyz` ，如果声明有属性 `paramA` 或 `paramB` ，则它们会被赋值为 `123` 或 `xyz` 。

页面的生命周期方法（即 `on` 开头的方法），应写在 `methods` 定义段中。

#### 1.构造器构造页面

home-page.json代码

```json
{
  "usingComponents": {}
}
```



####2.使用构造好的页面



```html
<!-- 点击跳转到组件页面 -->
<navigator url="../../components/home-page/home-page">
  <button>点击跳转到组件页面</button>
</navigator>
```



3.页面跳转时传递的参数



```html
<!-- 点击跳转到组件页面 -->
<navigator url="../../components/home-page/home-page?name=jack&age=13">
  <button>点击跳转到组件页面</button>
</navigator>
```



4.组件接收页面跳转时传递的参数

> 接收的参数可以在页面中使用，可以通过this.data.xxx获取



home-page.js

```js
// components/home-page/home-page.js
Component({
  /**
   * 组件的属性列表
   * 1.定义接收上一个页面传递过来的name/age参数
   * 
   * （ 可以直接拿到wxml中用 ）
   */
  properties: {
    name: String,
    age: Number,
  },
  /**
   * 组件的初始数据
   */
  data: {
   
  },
  /**
   * 组件的方法列表
   */
  methods: {
    
    onLoad(){
      //2.接收上一个页面传递过来的name/age参数 【 非页面组件(普通组件)不能这样接收外部传递的数据 】
      console.log(this.data.name);
      console.log(this.data.age);
    }
  }
})
```

home-page.wxml

```html
<!--components/home-page/home-page.wxml-->
<text>components/home-page/home-page.wxml</text>
<view>{{name}}-{{age}}</view>
```





**Bug & Tips:**

- 使用 `this.data` 可以**获取**内部数据和属性值，但不要直接修改它们，应使用 `setData` 修改。
- **生命周期函数**无法在组件方法中通过 `this` 访问到。
- **properties属性名**应避免以 data 开头，即不要命名成 `dataXyz` 这样的形式，因为在 WXML 中， `data-xyz=""` 会被作为节点 dataset 来处理，而不是组件属性。
- 在一个组件的定义和使用时，**组件的属性名和 data 字段相互间都不能冲突**（尽管它们位于不同的定义段中）。
- 从基础库 [2.0.9](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 开始，对象类型的属性和 data 字段中可以包含函数类型的子字段，即可以通过对象类型的属性字段来传递函数。低于这一版本的基础库不支持这一特性。
- `bug` : 对于 type 为 Object 或 Array 的属性，如果通过该组件自身的 this.setData 来改变属性值的一个子字段，则依旧会触发属性 observer ，且 observer 接收到的 `newVal` 是变化的那个子字段的值， `oldVal` 为空， `changedPath` 包含子字段的字段名相关信息。





### 3.组件的生命周期

**组件的主要生命周期**

组件的生命周期，指组件自身的一些函数，这些函数在特殊的时间点或遇到一些特殊的框架事件时被自动触发。

其中，最重要的生命周期是 `created` `attached` `detached` ，包含一个组件实例生命流程的最主要时间点。

- 组件实例刚刚被创建好时， `created` 生命周期被触发。此时，组件数据 `this.data` 就是在 `Component` 构造器中定义的数据 `data` 。 **此时还不能调用 setData 。** 通常情况下，这个生命周期只应该用于给组件 `this` **添加一些自定义属性字段**。
- 在**组件完全初始化完毕**、**进入页面节点树后**， `attached` 生命周期被触发。此时， `this.data` 已被初始化为组件的当前值。这个生命周期很有用，**绝大多数初始化工作可以在这个时机进行**。
- 在**组件离开页面节点树后**， `detached` 生命周期被触发。退出一个页面时，如果组件还在页面节点树中，则 `detached` 会被触发。



#### 1.组件的生命周期函数

| 生命周期         | 参数             | 描述                   | 最低版本                                     |
| ------------ | -------------- | -------------------- | ---------------------------------------- |
| **created**  | 无              | 在组件实例刚刚被创建时执行        | [1.6.3](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| **attached** | 无              | 在组件实例进入页面节点树时执行      | [1.6.3](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| ready        | 无              | 在组件在视图层布局完成后执行       | [1.6.3](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| moved        | 无              | 在组件实例被移动到节点树另一个位置时执行 | [1.6.3](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| **detached** | 无              | 在组件实例被从页面节点树移除时执行    | [1.6.3](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| error        | `Object Error` | 每当组件方法抛出错误时执行        | [2.4.1](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |

**代码示例：**

```js
Component({
  
  // 以下是旧式的定义方式，可以保持对 <2.2.3 版本基础库的兼容
  attached() {
    // 在组件实例进入页面节点树时执行
  },
  detached() {
    // 在组件实例被从页面节点树移除时执行
  },
  
  // ...
  
  /**
   * 组件的方法列表
  */
  methods: {
    
  },
  
})
```



#### 2.组件生命周期定义的位置

生命周期方法可以直接定义在 `Component` 构造器的**第一级参数**中。

自小程序基础库版本 [2.2.3](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 起，组件的的生命周期也可以在 `lifetimes` 字段内进行声明（这是推荐的方式，其优先级最高）。

**代码示例：**

```js
Component({
  
   /**
   * 组件的方法列表
   */
  methods: {
    
  },
  
  // 以下是新的定义方式，可以保持对 >=2.2.3 版本基础库的兼容
  lifetimes: {
    created() {
      //在组件实例刚刚被创建时执行
      console.log('1.在组件实例刚刚被创建时执行')
    },

    attached() {
      // 在组件实例进入页面节点树时执行
      console.log('2.在组件实例进入页面节点树时执行')
    },

    ready() {
      // 在组件在视图层布局完成后执行
      console.log('3.在组件在视图层布局完成后执行')
    },

    detached() {
      // 在组件实例被从页面节点树移除时执行
      console.log('4.在组件实例被从页面节点树移除时执行')
    },
    //....
  },
  
})
```



#### 3.组件所在页面的生命周期



还有一些特殊的生命周期，它们并非与组件有很强的关联，但有时组件需要获知，以便组件内部处理。

这样的生命周期称为“组件所在页面的生命周期”，在 `pageLifetimes` 定义段中定义。其中可用的生命周期包括：



| 生命周期   | 参数            | 描述                        | 最低版本                                     |
| ------ | ------------- | ------------------------- | ---------------------------------------- |
| show   | 无             | 组件所在的页面被展示时执行( **回到前台** ) | [2.2.3](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| hide   | 无             | 组件所在的页面被隐藏时执行( **回到后台** ) | [2.2.3](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |
| resize | `Object Size` | 组件所在的页面尺寸变化时执行            | [2.4.0](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) |



**代码示例：**

```js
// components/my-view/my-view.js
Component({

  options: {
    multipleSlots: true // 在组件定义时的选项中启用多slot支持
  },
  
  // 1.定义该组件可以接收的外部样式类
  externalClasses: ['my-view-class','my-view-active-class'],



  /**
   * 组件的属性列表
   */
  properties: {
    arrsPramas:{
      type:Array,
      value:[0,0,0,],
    },
    strPramas:{
      type:String,
      value:''
    },
    numPramas:Number
  },

  /**
   * 组件的初始数据
   */
  data: {

  },

  /**
   * 组件的方法列表
   */
  methods: {
    
  },

  lifetimes: {
    created() {
      //在组件实例刚刚被创建时执行
      console.log('1.在组件实例刚刚被创建时执行')
    },

    attached() {
      // 在组件实例进入页面节点树时执行
      console.log('2.在组件实例进入页面节点树时执行')
    },

    ready() {
      // 在组件在视图层布局完成后执行
      console.log('3.在组件在视图层布局完成后执行')
    },

    detached() {
      // 在组件实例被从页面节点树移除时执行
      console.log('4.在组件实例被从页面节点树移除时执行')
    },
    //....
  },

  
  //2.组件所在页面的生命周期
  pageLifetimes: {
    show() {
      // 页面被展示
      console.log('1.页面被展示')
    },
    hide() {
      // 页面被隐藏（ 例如切换到后台 ）
      console.log('2.页面被隐藏')
    },
    resize(size) {
      // 页面尺寸变化
      console.log('3.页面尺寸变化')
    }
  }


})
```





### 4.组件的事件-通讯

组件间的基本通信方式有以下几种。

- WXML 数据绑定( **传递参数** )：用于**父组件向子组件**的指定属性设置数据，仅能设置 JSON 兼容数据（自基础库版本 [2.0.9](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 开始，还可以在数据中包含函数）。具体在 [组件模板和样式](https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/wxml-wxss.html) 章节中介绍。
- 事件：用于**子组件向父组件**传递数据，可以传递任意数据。
- 如果以上两种方式不足以满足需要，**父组件还可以通过 `this.selectComponent` 方法获取子组件实例对象**，这样就可以直接访问组件的任意数据和方法。



#### 1.组件内部触发事件



my-view.wxml

```html
<view class="my-view">

  ....
  ....

  <view>========4.组件内部触发事件========</view>
  <button bindtap="onbindtap">组件内部触发事件</button>
  
</view>
```



组件内部触发事件



my-view.js

```js
  /**
   * 组件的方法列表
   */
  methods: {
    
    //1.监听组件内部的点击事件
    onbindtap(event){
      console.log('1.onbindtap')
      const myEventDetail = {des:'这个对象会赋值给detail对象'} // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      //2.组件内部触发事件，外部可以监听 bindbtnclick 事件
      this.triggerEvent('btnclick', myEventDetail, myEventOption)

    }

  },
```



#### 2.监听组件内部触发的事件

> 使用组件的地方 监听组件内部触发的事件

事件系统是组件间通信的主要方式之一。自定义组件可以触发任意的事件，引用组件的页面可以监听这些事件。关于事件的基本概念和用法，参见 [事件](https://developers.weixin.qq.com/miniprogram/dev/framework/view/wxml/event.html) 。

监听自定义组件事件的方法与监听基础组件事件的方法完全一致：





使用组件的地方监听组件内部触发的事件





#### 3.调用组件内部的方法

> 使用组件的地方  调用组件内部的方法

1.定义内部的方法

触发事件的选项myEventOption包括：

| 选项名          | 类型      | 是否必填 | 默认值   | 描述                                       |
| ------------ | ------- | ---- | ----- | ---------------------------------------- |
| bubbles      | Boolean | 否    | false | 事件是否冒泡                                   |
| composed     | Boolean | 否    | false | 事件是否可以穿越组件边界，为false时，事件将只能在引用组件的节点树上触发，不进入**其他任何组件内部** |
| capturePhase | Boolean | 否    | false | 事件是否拥有捕获阶段                               |

```js
  /**
   * 组件的方法列表
   */
  methods: {
    
    //1.监听组件内部的点击事件
    onbindtap(event){
      console.log('1.onbindtap')
      const myEventDetail = {des:'这个对象会赋值给detail对象'} // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      //2.组件内部触发事件，外部可以监听 bindbtnclick 事件
      this.triggerEvent('btnclick', myEventDetail, myEventOption)
      
	  //3.调用内部方法语法：this.showText('haha'); 
    },

    //2.在组件内部定义一个内部的方法共外部调用（ 只能在methods方法中定义 ）
    showText(value){
      console.log('value='+value)
    }

  },
```



2.外部调用组件内部定义的方法

**父组件还可以通过 `this.selectComponent` 方法获取子组件实例对象**，这样就可以直接访问组件的任意数据和方法。



```js
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 1.获取组件对象(只能获取自定义组件的对象)
    let myView = this.selectComponent('#my-view'); // myView 等于组件的 this
    myView.showText('haha')
    
    console.log(myView.data.name)
    console.log(myView)
  },
```



### 5.组件的behaviors

`behaviors` 是用于**组件间代码共享**的特性，类似于一些编程语言中的“**mixins**。

每个 `behavior` 可以包含一组**属性、数据、生命周期函数和方法**，组件引用它时，它的属性、数据和方法会被**合并**到组件中，生命周期函数也会在对应时机被调用。每个组件**可以引用多个** `behavior` 。 `behavior` 也可以引用其他 `behavior` 。

`behavior` 需要使用 `Behavior()` 构造器定义。



**字段的覆盖和组合规则**

组件和它引用的 `behavior` 中可以包含同名的字段，对这些字段的处理方法如下：

- 如果有同名的属性或方法，**组件本身的属性或方法会覆盖 `behavior` 中的属性或方法**，如果引用了多个 `behavior` ，在定义段中靠后 `behavior` 中的属性或方法会覆盖靠前的属性或方法；
- 如果有同名的数据字段，如果数据是对象类型，会进行**对象合并**，如果是非对象类型则会进行相互覆盖；
- **生命周期函数不会相互覆盖**，而是在对应触发时机被逐个调用。如果同一个 `behavior` 被一个组件多次引用，它定义的生命周期函数只会被执行一次。



#### 1.定义behaviors



```js
module.exports = Behavior({

  //1.引入外部的behavior
  behaviors: [],

  //2.定义属性，该属性将会合并到使用该behavior的组件中
  properties: {
    myBehaviorProperty: {
      type: String
    }
  },
  //2.定义data,该data将会合并到使用该behavior的组件中
  data: {
    myBehaviorData: {
      name:'XMG'
    }
  },

  //3.定义生命周期函数，当和组件的attached合并后，这个会比组件的attached先执行
  attached() {
    console.log('myBehaviorData -> attached')
  },

  // add  lifetimes
  lifetimes: {
    //定义生命周期函数，当和组件的attached合并后，这个会比组件的attached先执行
    ready() {
      console.log('myBehaviorData -> ready')
    },
  },


  //4.定义方法,该方法将会合并到使用该behavior的组件中
  methods: {
    myBehaviorMethod() { 
      console.log("---myBehaviorMethod---")
    }

  }

})
```



#### 2.使用behaviors



my-view.js

```js
// components/my-view/my-view.js
// 1.引入这个myBehavior
const myBehavior = require('../../behavior/my-behavior');

Component({

  behaviors: [myBehavior],  // 2.引入这个myBehavior, 它的属性、数据和方法会被合并到组件中
   
  ....
  ....
  ....
  
  lifetimes: {
    created() {
      //3.调用behavior合并过来的方法
      this.myBehaviorMethod();
    },
  },


})
```



my-view.wxml

```html
  <view>==5.使用behavior中的属性和数据===</view>
  <view>{{myBehaviorProperty}}--{{myBehaviorData.name}}</view>
```



## 3.自定义xmg-alert对话框



```html
<xmg-alert
  id="xmg-alert"
  xmg-title="授权提示"
  xmg-content="亲，你还有授权哦!"
  xmg-clear-text="取消"
  xmg-commit-text="确认"
           
  xmg-text-active-class="text-active"
           
  bindclear="onbindclear"
  bindcommit="onbindcommit"
>
</xmg-alert>
```



### 1.创建xmg-alert自定义组件

1.新建xmg-alert自定义组件





2.使用xmg-alert自定义组件

03-alert-test.json

```json
{
  "usingComponents": {
    "xmg-alert": "../../components/xmg-alert/xmg-alert"
  }
}
```



03-alert-test.wxml

```html
<!-- 1.在json文件中声明导入后，直接使用自定义组件 -->
<xmg-alert>

</xmg-alert>
```



### 2.编写对话框布局

#### 1.编写主体布局-500-350-20

> width:500  height:350  radius:20



xmg-alert.wxml

```html
<view class="xmg-alert">

  <view class="alert-content">
      
  </view>

</view>
```



xmg-alert.wxss

```css
page{
  height: 100%;
}

.xmg-alert{
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);/** 0.3 */

  position: fixed;
  top: 0;
  left: 0;
  
  display: flex;
  justify-content: center;
  align-items: center;
}

.alert-content{
  width: 500rpx;
  height: 350rpx;
  background: white;
  border-radius: 20rpx;
}
```



#### 2.编写内容布局-2:3:2

title-fs-45   desp-fs-40-gray



xmg-alert.wxml

```html
<view class="xmg-alert">

  <view class="alert-content">

      <view class="alert-title">title</view>  
      <view class="alert-desp">desp</view>

      <view class="alert-bar">
        <view class="alert-clear">clear</view>
        <view class="alert-commit">commit</view>
      </view>

  </view>

</view>
```



xmg-alert.wxss

```css
/* components/xmg-alert/xmg-alert.wxss */
page{
  height: 100%;
}

.xmg-alert{
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);

  display: flex;
  justify-content: center;
  align-items: center;
}

/* 内容布局 */
.alert-content{
  width: 500rpx;
  height: 350rpx;
  background: white;
  border-radius: 20rpx;

  display: flex;
  flex-direction: column;
}

/* 上 */
.alert-title{
  text-align: center;
  font-size: 45rpx;
  flex: 2;
  
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 中 */
.alert-desp{
  text-align: center;
  font-size: 40rpx;
  color: gray;

  flex: 3;
  background: skyblue;

  display: flex;
  justify-content: center;
  align-items: center;
}

/* 下 */
.alert-bar{
  flex: 2;
  display: flex;
  flex-direction: row;
}

.alert-clear,
.alert-commit{
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
```



### 3.修改文本

#### 1.传递数据给xmg-alert

03-alert-text.wxml

```html
<!-- 1.在json文件中声明导入后，直接使用自定义组件 -->
<xmg-alert
  id="xmg-alert"
  xmg-title="授权提示"
  xmg-content="亲，你还有授权哦!"
  xmg-clear-text="取消"
  xmg-commit-text="确认"
>

</xmg-alert>
```



#### 2.xmg-alert接收数据

xmg-alert.js

```js
// components/xmg-alert/xmg-alert.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

    xmgTitle:{
      type:String,
      value:'标题'
    },
    xmgContent: {
      type: String,
      value: '内容描述'
    },
    xmgClearText: {
      type: String,
      value: 'clear'
    },
    xmgCommitText: {
      type: String,
      value: 'ok'
    },
    
  },

  /**
   * 组件的初始数据
   */
  data: {

  },

  /**
   * 组件的方法列表
   */
  methods: {

  }
})
```



#### 3.展示接收的数据



xmg-alert.wxml

```html
<view class="xmg-alert">

  <view class="alert-content">

      <view class="alert-title">{{xmgTitle}}</view>  
      <view class="alert-desp">{{xmgContent}}</view>

      <view class="alert-bar">
        <view class="alert-clear">{{xmgClearText}}</view>
        <view class="alert-commit">{{xmgCommitText}}</view>
      </view>

  </view>

</view>
```



### 4.默认选中-确认文本



1.传递外部的class给组件

03-alert-text.wxml

```html
<!-- 1.在json文件中声明导入后，直接使用自定义组件 -->
<xmg-alert
  id="xmg-alert"
  xmg-title="授权提示"
  xmg-content="亲，你还有授权哦!"
  xmg-clear-text="取消"
  xmg-commit-text="确认"

  xmg-text-active-class="text-active"
>

</xmg-alert>
```



2.组件内部接收外部的class

xmg-alert.js

```js
// components/xmg-alert/xmg-alert.js
Component({

  // 1.定义该组件可以接收的外部样式类
  externalClasses: ['xmg-text-active-class'],

  /**
   * 组件的属性列表
   */
  properties: {

    .....

  },

  /**
   * 组件的初始数据
   */
  data: {

  },

  /**
   * 组件的方法列表
   */
  methods: {

  }
})

```



3.使用接收到的class样式

```html
<view class="xmg-alert">

  <view class="alert-content">

      <view class="alert-title">{{xmgTitle}}</view>  
      <view class="alert-desp">{{xmgContent}}</view>

      <view class="alert-bar">
        <view class="alert-clear">{{xmgClearText}}</view>
        <!-- 使用接收到外部的class -->
        <view class="alert-commit xmg-text-active-class">{{xmgCommitText}}</view>
      </view>

  </view>

</view>
```



### 5.处理点击事件

#### 1.监听xmg-alert点击事件

xmg-alert.wxml

```html
<view class="xmg-alert">

  <view class="alert-content">

      <view class="alert-title">{{xmgTitle}}</view>  
      <view class="alert-desp">{{xmgContent}}</view>

      <view class="alert-bar">
         <!-- 监听点击事件 -->
        <view bindtap="oncleartap" class="alert-clear">{{xmgClearText}}</view>
   
        <view bindtap="oncommittap" class="alert-commit xmg-text-active-class">{{xmgCommitText}}</view>
      </view>

  </view>

</view>
```



xmg-alert.js

```js
// components/xmg-alert/xmg-alert.js
Component({
  ...
  ...

  /**
   * 组件的方法列表
   */
  methods: {
    //1.取消
    oncleartap(){
      console.log('xmg-alert oncleartap')  
    },
    //确认
    oncommittap(){
      console.log('xmg-alert oncommittap')  
    }
  }
  
})
```



#### 2.触发点击事件

xmg-alert.js

> 注意函数都写在 methods 中

```js
// components/xmg-alert/xmg-alert.js
Component({

  ....
  ....

  /**
   * 组件的方法列表
   */
  methods: {
  
    //1.取消
    oncleartap(){
      console.log('xmg-alert oncleartap')  
      //2.触发点击事件
      this.dispatchTap('clear');

    },
    //确认
    oncommittap(){
      console.log('xmg-alert oncommittap')  
      //2.触发点击事件
      this.dispatchTap('commit');

    },
    
	//触发点击事件
    dispatchTap(value){
      const myEventDetail = { value: value } // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      //3.组件内部触发事件，外部可以监听 bindxxxx 事件
      this.triggerEvent(value, myEventDetail, myEventOption)
    }

  }
})
```



#### 3.外部监听点击事件



03-alert-test.wxml

```html
<!-- 1.在json文件中声明导入后，直接使用自定义组件 -->
<xmg-alert
  id="xmg-alert"
  xmg-title="授权提示"
  xmg-content="亲，你还有授权哦!"
  xmg-clear-text="取消"
  xmg-commit-text="确认"

  xmg-text-active-class="text-active"
  
  bindclear="onbindclear"
  bindcommit="onbindcommit"
>

</xmg-alert>
```



03-alert-test.js

```js
// pages/03-alert-test/03-alert-test.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  onbindclear:function(event){
    console.log(event.detail)
  },
  
  onbindcommit: function (event) {
    console.log(event.detail)
  },

 
})
```

### 6.控制显示和隐藏

xmg-alert.js

```js
// components/xmg-alert/xmg-alert.js
Component({

  ....
  ....

  /**
   * 1.组件的初始数据
   */
  data: {
    isShow:true,
  },

  /**
   * 组件的方法列表
   */
  methods: {
    ...
    ...

    //触发点击事件
    dispatchTap(value){
      const myEventDetail = { value: value } // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      //3.组件内部触发事件，外部可以监听 bindxxxx 事件
      this.triggerEvent(value, myEventDetail, myEventOption);
      
      
      //3.隐藏对话框
      this.hidden();
    },

    //2.显示对话框
    show(){
       this.setData({
         isShow:true,
       }) 
    },
    //2.隐藏对话框
    hidden(){
      this.setData({
        isShow: false,
      }) 
    }



  }
})
```

xmg-alert.wxml





### 7.给对话框添加动画

xmg-alert.wxml

```html
<view class="xmg-alert" wx:if="{{isShow}}">
   <!-- 添加动画类：alert-animated -->
  <view class="alert-content {{ isShow ? 'alert-animated':'' }}">

      <view class="alert-title">{{xmgTitle}}</view>  
      <view class="alert-desp">{{xmgContent}}</view>

      <view class="alert-bar">
        <view bindtap="oncleartap" class="alert-clear">{{xmgClearText}}</view>
        <view bindtap="oncommittap" class="alert-commit xmg-text-active-class">{{xmgCommitText}}</view>
      </view>

  </view>

</view>
```



xmg-alert.wxss

```css
.alert-animated{

  animation: alertAnimated 0.3s;

}

@keyframes alertAnimated{

  0%{
    transform: scale3d(0.5,0.5,0.5);
  }
  60%{
     transform: scale3d(1.2,1.2,1.2);
  }

  100%{
     transform: scale3d(1,1,1);
  }
}
```



## 4.自定组件VS自定义模版

Template vs Component 这两者之间的区别:   

1) template主要是展示，方法则需要在调用的页面中定义。

2) component组件则有自己的业务逻辑( 包含：js , wxml, wxss, json文件 )，也可以看做一个独立的page页面。

3) 简单来说，如果只是展示，使用template就足够了，如果涉及到的业务逻辑交互比较多，那就最好使用component组件了



## 5.构建 npm

从小程序基础库版本 [2.2.1](https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html) 或以上、及[开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) 1.02.18080 或以上开始，**支持使用 npm 安装第三方包**。

此文档要求开发者们对 npm 有一定的了解，因此不会再去介绍 npm 的基本功能。如若之前未接触过 npm，请翻阅[官方 npm 文档](https://docs.npmjs.com/getting-started/what-is-npm)进行学习。



**小程序第三方包：**https://github.com/wechat-miniprogram



### 1.安装第三方的 npm 包

1.在小程序**根目录**中执行命令安装 npm 包：

```js
npm install --save xxxxxxx    //安装生产的依赖
npm install --save-dev xxxxxxx  //安装开发的依赖

// or 根据package.json的依赖来安装
npm install --production  // 只会把 package.json 中 dependencies 依赖的模块下载到 node_modules 中
```

此处并没有强制要求 node_modules 必须在小程序根目录下（即 project.config.js 中的 `miniprogramRoot` 字段），也可以存在于小程序根目录下的各个子目录中。但是不允许 node_modules 在小程序根目录外。

> PS：此处请务必使用`--production`选项，可以减少安装一些业务无关的 npm 包，从而减少整个小程序包的大小。



国家密码算法，例如：https://github.com/wechat-miniprogram/sm-crypto

sm2椭圆曲线公钥密码: https://baike.baidu.com/item/SM2/15081831?fr=aladdin

sm3国产哈希算法  :https://baike.baidu.com/item/SM3/4421797

sm4分组密码算法( 对称密钥算法 ):  https://baike.baidu.com/item/SM4.0/3901780



```js
npm init -y;
npm install --save miniprogram-sm-crypto@0.0.5  //小程序 js 库。国家密码算法 sm2、sm3 和 sm4 的实现。
```

​	

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

    let publicKey = keypair.publicKey; // 获取公钥
    let privateKey = keypair.privateKey; // 获取私钥

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



## 6.使用slide-view第三方组件

https://github.com/wechat-miniprogram/slide-view

1.在小程序项目根目录安装 slide-view

```
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

1）left 节点用于承载静止时 slide-view 所展示的节点，此节点的宽高应与传入 slide-view 的宽高相同。

2）right 节点用于承载滑动时所展示的节点，其宽度应于传入 slide-view 的 slideWidth 相同。

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
  background-color: skyblue;/***/
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
  color: white; /***/
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
  width: 300rpx;  /***/
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









