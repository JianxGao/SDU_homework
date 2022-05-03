## 1.首页分类栏

### 1定义分类栏组件-h200

categorybar

> 1.定义一个categorybar组件( "component": true )   
>
> 2.使用组件 usingComponents

 



### 2.传递数据到组件



categorybar.js

```js
// components/catogorybar/catogorybar.js
Component({
  /**
   * 组件的属性列表
   * 
   * 这里面的属性可以直接拿到界面上使用
   */
  properties: {
    categoryItems:{
      type:Array,
      value:[]
    }
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

categorybar.wxss

```html
<view class="catogory-bar">
  
  <block wx:for="{{categoryItems}}" wx:key="{{index}}">

    {{index}}

  </block>

</view>
```

catogorybar.wxss

```css
/* components/catogorybar/catogorybar.wxss */
.catogory-bar{
  width: 100%;
  height: 200rpx;
  background: skyblue;
}
```



### 3.完善自定组件布局-86

> title-30-gray  image-w-100   image-h-86

布局

```html
<view class="catogory-bar">
  
  <block wx:for="{{categoryItems}}" wx:key="{{index}}">

    <view class="view-bar-item">
       <image src="{{item.inageurl}}" class="image-bar"></image>
       <text class="text-bar-item">{{item.name}}</text>
    </view>

  </block>

</view>
```



样式

```css
/* components/catogorybar/catogorybar.wxss */
.catogory-bar{
  height: 200rpx;
  width: 100%;
  background: white;

  display: flex;
  flex-direction: row;
  align-items: center;
}
/*每一个item  */
.view-bar-item{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
}
/*item里面的图片  */
.image-bar{
  width: 100rpx;
  		height: 86rpx;
  background: red;
}
/*item中的文字  */
.text-bar-item{
  color: gray;
  font-size: 30rpx;
}
```



### 4.处理组件的点击事件



categorybar.js

```js
// components/catogorybar/catogorybar.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    categoryItems:{
      type:Array,
      value:[]
    }
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
    // item 的点击事件
    itemclick(event){  
      // console.log(event)
      const myEventDetail = { index: event.currentTarget.dataset.index} // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      this.triggerEvent('itembarclick', myEventDetail, myEventOption)
    
    }

  }
})
```

categorybar.wxml

```html
<view class="catogory-bar">
  
  <block wx:for="{{categoryItems}}" wx:key="{{index}}">
    
	<!-- bindtap="itemclick" data-index="{{index}}" 绑定点击事件和索引 -->
    <view class="view-bar-item" bindtap="itemclick" data-index="{{index}}">
       <image src="{{item.inageurl}}" class="image-bar"></image>
       <text class="text-bar-item">{{item.name}}</text>
    </view>

  </block>

</view>
```





## 2.首页推荐栏

### 1.引入推荐栏自定组件-h320.

> padding:20rpx 0rpx

recommend.js

```js
// components/recommend/recommend.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    itemDatas:{
      type:Array,
      value:[],
    }
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
    itemclick(event){

      const myEventDetail = { index: event.currentTarget.dataset.index } // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      this.triggerEvent('itemclick', myEventDetail, myEventOption)

    }
  }
})
```

recommend.wxml

```html
<!--components/recommend/recommend.wxml-->
<view class="recommend">

  <block wx:for="{{itemDatas}}" wx:key="{{index}}">
        <view class="view-item" bindtap="itemclick" data-index="{{index}}">
            <image src="{{item}}" class="img"></image>
        </view>
  </block>

</view>
```

recommend.json

```json
{
  "component": true,
  "usingComponents": {}
}
```

recommend.wxss

```css
/* components/recommend/recommend.wxss */
/*第一个item 布局  */
.recommend{
  height: 320rpx;
  width: 100%;
  background: #dddddd;

  display: flex;
  flex-direction: row;
  justify-content: space-between;
  
  padding-top: 20rpx;
  padding-bottom: 20rpx;
}

/* 每一个item */
.view-item{
    flex: 1;
    background: red;
}
```



### 2.使用推荐栏组件



```html
<!-- 推荐栏recommend -->
<recommend itemDatas = "{{homeBean.firstItems}}" binditemclick="recommendItemClick"></recommend>
```



## 3.首页商品列表

### 1.列表基本布局



index.wxml

```html
<!-- 商品列表  -->
<view wx:for="{{homeBean.categorys}}">
    <!--title  -->
    <view>
      {{item.titleName}}
    </view>

    <!--九宫格列表  -->
    <view>
       list
    </view>

</view>
```

​	

### 2.列表的头部布局-vm-460





index.wxml

```html
    <!-- 商品分类列表 -->
    <view wx:for="{{homeBean.categorys}}" wx:key="{{index}}" class="gridview">
      <!--title  -->
      <view style="height: 460rpx;">
        <image src="{{item.titleImage}}" class='image-title'></image>
      </view>

      <!--九宫格列表  -->
      <view class="gridview-connent">
        list
      </view>

    </view>
```



index.wxss

```css
/* 商品列表 */
.gridview{
  width: 100%;
}

.image-title{
  width: 100%;
  height: 460rpx;
}
```



### 3.列表的内容布局-260

#### 1.内容布局





index.wxml

```html
    <!-- 商品分类列表 -->
    <view wx:for="{{homeBean.categorys}}" wx:key="{{index}}" class="gridview">
      <!--title  -->
      <view style="height: 460rpx;">
        <image src="{{item.titleImage}}" class='image-title'></image>
      </view>

      <!--九宫格列表  -->
      <view class="gridview-connent">
        
        <block wx:for="{{item.items}}" wx:for-item="goodData" wx:for-index="id" wx:key="{{id}}">
            <view class="gridview-item">
                {{id}}
            </view>
        </block>

      </view>

    </view>
```



index.wxss

```css
/* 列表item的样式 */
.gridview-item{
  width: 50%;
  height: 460rpx;
  background: skyblue;

  display: inline-block;
  border-top: 4rpx solid white;

  box-sizing: border-box;
}

.gridview-item:nth-of-type(odd){
  border-right: 4rpx solid white;
}
```



#### 2.布局的完善

> img-260     margin:0rpx 30rpx    fs-36-26-32 (  gray  )

1.添加图片

index.html

```html
      <!--九宫格列表  -->
      <view class="gridview-connent">
        
        <block wx:for="{{item.items}}" wx:for-item="goodData" wx:for-index="id" wx:key="{{id}}">
            <view class="gridview-item">
                <image src="{{goodData.imageurl}}"></image>

                <view>1</view>
            </view>
        </block>

      </view>
```



index.wxss

```css
.gridview-item image{
  width: 100%;
  height: 260rpx;
}

```



2.添加商品描述

index.html	

```html
  <!-- 商品分类列表 -->
    <view wx:for="{{homeBean.categorys}}" wx:key="{{index}}" class="gridview">
      <!--title  -->
      <view style="height: 460rpx;">
        <image src="{{item.titleImage}}" class='image-title'></image>
      </view>

      <!--九宫格列表  -->
      <view class="gridview-connent">
        
        <block wx:for="{{item.items}}" wx:for-item="goodData" wx:for-index="id" wx:key="{{id}}">
            <view class="gridview-item">
                <image src="{{goodData.imageurl}}"></image>

                <view class="goods-desp" style="margin:0rpx 30rpx;">
                    <view class="text-title">{{goodData.title}}</view>
                    <view class="text-desp">{{goodData.descp}}</view>
                    <view class="text-price">¥{{goodData.price}}</view>
                </view>
            </view>
        </block>

      </view>

    </view>
```



index.wxss

```css
.text-title{
  font-size: 36rpx;
}

.text-desp{
  font-size: 26rpx;
  color: gray;
  margin: 10rpx 0rpx;
}

.text-price{
  font-size: 32rpx;
  color: #FF6802;
}
```



### 4.点击商品跳转到详情页

/XiaoMiShop/detail?goodId=xxx



## 4.详情页面

> page-bg-#ddd

### 1.发起网络请求获取数据

detail.wxml

```js
// pages/detail/detail.js
const httpService = require('../../utils/service.js');
Page({

  /**
   * 页面的初始数据
   */
  data: {
    detailBean:null,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let _this = this;
    console.log(options)
    httpService.getGoodsDetail(options.goodId).then((result)=>{
      console.log(result.data)
      //把数据存在data中
      _this.setData({
        detailBean: result.data.data
      })

    }).catch((error)=>{
       console.log(error) 
    })

  },
  
})
```



services.js

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

//4.获取商品详情的数据
const getGoodsDetail = (goodId)=>{
  console.log(API.HOME)
  return fecth({ url: API.DETAIL +'?goodId='+goodId } )
}


module.exports = {
  getHomeBean: getHomeBean,
  getGoodsDetail: getGoodsDetail,
}
```



api.js

```js
// 定义基本的url
let baseurl = 'http://47.93.30.78:8080';


module.exports = {
  HOME: baseurl + '/XiaoMiShop/home',
  DETAIL: baseurl + '/XiaoMiShop/detail',
} 
```



### 2.加载进度提示



detail.wxml

```html
<!--pages/detail/detail.wxml-->
<!-- 导入加载模版 -->
<import src="../../templates/loading.wxml" ></import>

<!-- 1.如果有数据 -->
<block wx:if="{{detailBean}}">
  <view>
    detail
  </view>
</block>


<!-- 2.如果没有数据( 显示加载的进度 ) -->
<block wx:else>
    <template is="loading"></template>
</block>

```



### 3.*自定义AddCart组件-120

#### 1.基本布局-1-2-2

>  img-110   bg-ff6802        bg-e95f3a

add cart.wxml

```html
<!--components/addcart/addcart.wxml-->
<view class="addcart">

    <!-- 左 -->
    <view class="left">
      0
    </view>
    <!-- 中 -->
    <view class="center">
      0
    </view>
    <!-- 右 -->
    <view class="right">
      0
    </view>

</view>

```



addcart.wxss

```css
/* components/addcart/addcart.wxss */

.addcart {
  width: 100%;
  height: 120rpx;
  background: skyblue;
  display: flex;
  flex-direction: row;
}

.left {
  flex: 1;

  display: flex;
  justify-content: center;
  align-items: center;
}

.center {
  flex: 2;
  
  background: #ff6802;
  display: flex;
  justify-content: center;
  align-items: center;
}

.right {
  flex: 2;
  
  background: #e95f3a;
  display: flex;
  justify-content: center;
  align-items: center;
}
```



#### 2.完善布局-110

> 1.添加scrollview组件，隐藏scrollview的滚动条,  calc( 100%-120rpx )
>
> 2.addcart布局定位等  img-110     z-index =2 

addcart.wxml

```html
<!--components/addcart/addcart.wxml-->
<view class="addcart">

    <!-- 左 -->
    <view class="left">
      <image class="cart" src="../../image/cart.png"></image>
    </view>
    <!-- 中 -->
    <view class="center">
      加购物车
    </view>
    <!-- 右 -->
    <view class="right">
      立即购买
    </view>

</view>
```

addcart.wxss

```css
/* components/addcart/addcart.wxss */

.addcart {
  ....

  /* 定位 */
  position: fixed;
  bottom: 0rpx;
  left: 0rpx;
  z-index: 2;
  
  border-top: 2rpx solid #ddd;
}

.left {
  ....
}


.center {
  ....
  color: white;
}

.right {
  ...
  color: white;
}


.cart{
  width: 110rpx;
  height: 110rpx;
}
```

#### 3.隐藏scroll-view的滚动条

detail.wxss   

> 注意scroll-view的高度

```css
/* pages/detail/detail.wxss */
page{
  background: #dddddd;
}

/* scroll-view的高度 */
.detail-scroll{
  height: calc(100% - 120rpx);  
}

/* 隐藏scroll-view的滚动条 */
::-webkit-scrollbar{
  width: 0rpx;
  height: 0rpx;
  color: transparent;
}
```

#### 4.监听组件的点击事件

dispatch





addcart.wxml

```html
<!--components/addcart/addcart.wxml-->
<view class="addcart">

    <!-- 左   bindtap="clickCart" -->
    <view class="left" bindtap="clickCart">
      <image class="cart" src="../../image/cart.png"></image>
    </view>
    <!-- 中 bindtap="clickAddCart" -->
    <view class="center" bindtap="clickAddCart">
      加购物车
    </view>
    <!-- 右  bindtap="clickBuy" -->
    <view class="right" bindtap="clickBuy">
      立即购买
    </view>

</view>
```

addcart.wxss

```js
// components/addcart/addcart.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

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
    //1.点击购物车
    clickCart(event){
      const myEventDetail = { index: 0 } // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      this.triggerEvent('clickIndex', myEventDetail, myEventOption)

    },

    //2.点击加购物车
    clickAddCart(event) { 
      const myEventDetail = { index: 1 } // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      this.triggerEvent('clickIndex', myEventDetail, myEventOption)
      
    },

    //3.点击立即购买
    clickBuy(event) { 
      const myEventDetail = { index: 2 } // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项 bindclickIndex
      this.triggerEvent('clickIndex', myEventDetail, myEventOption)
      
    },
  }
})
```

detail.wxml

```html
  <!-- 底部的加购物车栏 -->
  <add-cart bindclickIndex = "cartClickIndex" ></add-cart>
```



detail.js

```js
  /**监听购物车组件的所有事件 */
  cartClickIndex:function(event){
    let index =event.detail.index;
    console.log(index);
    //1.点击购物车
    if(index == 0){

    //2.点击加购物车
    } else if (index == 1){


    //3.点击立即购买  
    }else{
		
    }  
  }
```





### 3.轮播图实现-800



detail.wxml

```html
  <!-- 可滚动的内容 -->
 
  <scroll-view scroll-y class="detail-scroll">

    <!-- 轮播图布局 -->
    <swiper class="detail-swiper"
      indicator-dots
      indicator-color="white"
      indicator-active-color="#FF6802"
    >
        <block wx:for="{{detailBean.banners}}" wx:key="{{index}}">
          <swiper-item>
            <image  src="{{item}}"></image>
          </swiper-item>
        </block>
    
    </swiper>
    
    <!--  -->

  </scroll-view>
```



detail.wxss

```css
/* 轮播图 */
.detail-swiper,
.detail-swiper image{
  width: 100%;
  height: 800rpx;
}
```



### 4.商品信息

#### 1.布局-padding:30

> padding:30     desp-24rpx-gray



#### 2.样式

```css
/* 商品信息 */
.good-info{
  padding: 30rpx;
  background: white;
}

.good-info view:nth-of-type(1){

}
.good-info view:nth-of-type(2){
  color: gray;
  font-size: 24rpx;
  margin: 10rpx 0rpx;
}
.good-info view:nth-of-type(3){
  color: #ff6802;
}
```



### 5.评论信息

assess

#### 1.评论标题-h100

>  title-34     desp-28-gray



detail.wxml

```html
  <!-- 可滚动的内容 -->
  <scroll-view scroll-y class="detail-scroll">
	
	....
	....

    <!-- 用户评价 -->
    <view class="user-assess">
      <text>用户评价({{detailBean.userAssess.number}})</text>
      <text>查看全部评价</text>
    </view>


  </scroll-view>
```

detail.wxss

```css

/* 用户评价 */
.user-assess{
  margin-top: 20rpx;

  height: 100rpx;
  width: 100%;
  background: white;
  border-bottom: 2rpx solid #dddddd;

  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;

}

.user-assess text:nth-of-type(1){
  font-size: 34rpx;
  margin-left: 20rpx;

}

.user-assess text:nth-of-type(2){
   font-size: 28rpx;
   color: gray;
   margin-right: 20rpx;
}
```



#### 2.评论内容

>  flex: 1    4        



detail.wxml

```html
    <!-- 用户评价详情 -->
    <view class="user-assess-info">
      <view class="left">
            <image src="{{detailBean.userAssess.users[0].headerImageUrl}}"></image>
      </view>
      <view class="right">
            1
      </view>
    </view>
```



detail.wxss

```css
/* 用户评价信息 */
.user-assess-info{
  display: flex;
  flex-direction: row;


}

.user-assess-info .left{
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  
}

.user-assess-info .right{
  flex: 4;
  background: red;
}

```



#### 3.内容的完善-100

> img-100    margin-top:30     desp-32     time-30-gray





detail.wxml

```html
    <!-- 用户评价详情 -->
    <view class="user-assess-info" wx:for="{{detailBean.userAssess.users}}" wx:key="{{index}}">
      <view class="left">
            <image src="{{item.headerImageUrl}}"></image>
      </view>
      <view class="right">
            <view>{{item.name}}</view>
            <view>{{item.msg}}</view>
            <view>{{item.timeTamp}}</view>
      </view>
    </view>
```



detail.wxss

```css
/* 用户评价信息 */
.user-assess-info{
  display: flex;
  flex-direction: row;
  background: white

}

.user-assess-info .left{
  flex: 1;
  display: flex;
  justify-content: center;
  
}

.user-assess-info .left image{
  width: 100rpx;
  height: 100rpx;
  margin-top: 50rpx;

}

.user-assess-info .right{
  flex: 4;
  margin-top: 50rpx;
}

.user-assess-info .right view:nth-of-type(2){
  margin:10rpx 0rpx;
  font-size: 32rpx;
}

.user-assess-info .right view:nth-of-type(3){
  font-size: 30rpx;
  color: gray;
  margin:10rpx 0rpx;
}
```

#### 4.时间戳的格式化

> 1.使用es5的语法编写wxs工具类   2.使用<wxs src=""  module="" ></wxs> 引用



tools.wxs

```js
//1.注意不能使用es6的语法
//2.导入的语法  <wxs src="" module="" />
var formatTime=function(strTimeTamp){

  //1.获取date
  var date = getDate(strTimeTamp);
  //2/格式化时间
  var time = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
  return time;

}

module.exports = {
  formatTime: formatTime,
}
```

detail.wxml

```html
<!-- 导入wxs工具类 -->
<wxs src="../../wxs/tools.wxs" module="tools" />

<view>{{  tools.formatTime(item.timeTamp) }}</view>
```



### 6.商品详情-AM

#### 1.*定义tabs组件

```html
    <!-- 使用tabs组件：tabs:['图文详情','参数详情'] -->
    <tabs 
      tabs="{{tabs}}"
      tabs-active-text-class="tabs-active-color"
      bindtabclick="tabclick"
    >
    </tabs>
```



##### 1.定义和使用tabs组件



tabs.js

```js
// components/tabs/tabs.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    tabs:{
      type:Array,
      value:[],
    }
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



tabs.wxml

```html
<view class="tabs">
    <block wx:for="{{tabs}}" wx:key="{{index}}">
      {{index}}
    </block>
</view>
```



##### 2.完善tabs布局-110

>  height-110    title-36-gray( wirte in parent )



tabs.wxml

```html
<view class="tabs">
    <block wx:for="{{tabs}}" wx:key="{{index}}">
      <view class="tabs-item">
          <text class="tabs-title">{{item}}</text>
      </view>
    </block>
</view>
```



tabs.wxss

```css
.tabs{
  height: 110rpx;
  background: white;
  display: flex;
  flex-direction: row;

  margin-top: 20rpx;

}

.tabs-item{
  flex: 1;
  /* background: pink; */
  display: flex;
  justify-content: center;
  align-items: center;
  
  /**字体的样式写在父亲这里*/
  font-size: 36rpx;
  color: gray;
}

.tabs-item:nth-of-type(1){
  border-right: 2rpx solid #ddd;
}


.tabs-title{
  display: inline-block;
  line-height: 110rpx;
  height: 100%;
  
  /* background: pink; */
}
```



##### 3.处理组件点击事件

> 1.bindtap="itemclick"  data-index="{{index}}"
>
> 2. event.currentTarget.dataset.index

tabs.wxml

```html
<view class="tabs">
    <block wx:for="{{tabs}}" wx:key="{{index}}">
      <view class="tabs-item" bindtap="itemclick" data-index="{{index}}">
          <text class="tabs-title">{{item}}</text>
      </view>
    </block>
</view>
```

tabs.js

```js
// components/tabs/tabs.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    tabs:{
      type:Array,
      value:[],
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
	//currentIndex:0,
  },

  /**
   * 组件的方法列表
   */
  methods: {
    itemclick:function(event){
      console.log(event)
      let index = event.currentTarget.dataset.index;
      //this.setData({
      //  currentIndex: index
      //})
      const myEventDetail = { index: index} // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项 bindtabclick
      this.triggerEvent('tabclick', myEventDetail, myEventOption)
    }
  }
})
```



detail.wxml

```html
   <!-- 使用tabs组件：tabs:['图文详情','参数详情'] -->
    <tabs 
      tabs="{{tabs}}"
      bindtabclick="tabclick"
    >
    </tabs>
```



detail.js

```js
  /**tabs 选项卡的点击事件 */
  tabclick:function(event){
    console.log(event.detail.index)
    //this.setData({
    //  tabIndex: event.detail.index,
    //})
  }
```



##### 4.处理选中状态

> 1.外部传递样式类
>
> 2.组件内接收外部的类：externalClasses:[]
>
> 3.监听currentIndex, 给当前选中的tabs添加外部的类
>
> 注意：外部修改text的样式时，最好组件内部不要**修改text的同样的样式**







detail.wxml

```html
    <!-- 使用tabs组件：tabs:['图文详情','参数详情'] -->
    <tabs 
      tabs="{{tabs}}"
      tabs-active-text-class="tabs-active-color"
      bindtabclick="tabclick"
      
    >
    </tabs>
```



detail.wxss

```css
/* tabs 选项卡选中的颜色 */
.tabs-active-color{
  color: #ff6802;
}
```



tabs.js

```js
// components/tabs/tabs.js
Component({
  
  //接收外部的类
  externalClasses: ['tabs-active-text-class'],
  
  ....
  ....
})  
```



tabs.wxml

```html
<view class="tabs">
    <block wx:for="{{tabs}}" wx:key="{{index}}">
      <view class="tabs-item" bindtap="itemclick" data-index="{{index}}">
          <text class="tabs-title {{ currentIndex == index ? 'tabs-active-text-class':'' }}">{{item}}</text>
      </view>
    </block>
</view>
```



#### 2.图文详情和产品参数

##### 1.基本布局





##### 2.内容布局-400

>  view-img-400

```html
    <!--图文详情  -->
    <view wx:if="{{ tabIndex == 0 }}">
       <block wx:for="{{detailBean.detailpics}}" wx:key="{{index}}">
          <view style="width:100%;height:400rpx;margin-top:10rpx;">
            <image style="width:100%;height:100%;" src="{{item}}"></image>
          </view>
       </block>
    </view>
    <!-- 参数详情 -->
    <view wx:if="{{ tabIndex == 1 }}">
      <block wx:for="{{detailBean.detailparams}}" wx:key="{{index}}">
          <view style="width:100%;height:400rpx;margin-top:10rpx;">
            <image style="width:100%;height:100%;" src="{{item}}"></image>
          </view>
       </block>
    </view>
```



## 5.购物车页面

### 1.空购物车界面模版.

>   bg-#eaeaea       v-200-rgba(0,0,0,0.1)       img-100      
>
>   desp-40-#4e4e4e          btn-100-36  



<template is="nullcart"  data="{{imgurl:'../../image/cart.png' , btnclick:'goToMiShop' }}" />



cart.wxml

```html
<!--pages/cart/cart.wxml-->
<import src="../../templates/nullcart" />

<!-- 如果有数据 -->
<block wx:if="{{cartList.lenght > 0 }}">
  <view>
      购物车界面
  </view>
</block>


<!-- 如果购物车没有数据 -->
<block wx:else>
     <template is="nullcart" data="{{imgurl:'../../image/cart.png',btnclick:'goToMiShop'}}"/>
</block>
```



nullcart.wxml 完整布局

```html
<template name="nullcart">
  <view class="nulcart">

      <view class="cart-logo">
        <image src="{{imgurl}}"></image>
      </view>

      <view class="cart-desp">购物车还是空的</view>

      <view class="cart-btn" bindtap="{{btnclick}}">到小米商城逛逛</view>
  </view>
</template>
```



nullcart.wxss 完整样式

```css
.nulcart{
  width: 100%;
  height: 100%;
  background: #eaeaea;

  display: flex;
  flex-direction: column;
  align-items: center;
}

.nulcart .cart-logo{
  width: 200rpx;
  height: 200rpx;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);

  margin: 100rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}

.nulcart .cart-logo image{
  width: 150rpx;
  height: 150rpx;

}

.nulcart .cart-desp{
  font-size: 40rpx;
  color: #4e4e4e;
} 

.nulcart .cart-btn{
  margin-top: 50rpx;
  width: 80%;
  height: 100rpx;
  background: #ff6803;
  color: white;

  font-size: 36rpx;
  display: flex;
  justify-content: center;
  align-items: center;

  border-radius: 10rpx;
  
}
```



### 2.*底部accountbar组件

```html
  <!-- 购物车底部accountbar组件 -->
  <account-bar 
      bindaccountclick="accountBarClick" 
      id="accountbar"
      summary="{{summary}}"
   >
  </account-bar>

 let accountbar = this.selectComponent('#accountbar')
 accountbar.isSelect(true);
```

#### 1.定义和使用accountbar

> height-120    flex: 1 1 1





accountbar.wxml

```html
<!--components/accountbar/accountbar.wxml-->
<view class="accountbar">

  <!-- 左 -->
  <view class="left">
      0
  </view>
  <!-- 中 -->
  <view class="center">
    1
  </view>
  <!-- 右 -->

  <view class="right">
    2
  </view>

</view>
```

accountbar.wxss

```css
.accountbar{
  height: 120rpx;
  width: 100%;
  background: white;

  position: fixed;
  bottom: 0rpx;
  left: 0rpx;
  z-index: 2rpx;
  border-top: 2rpx solid #dddddd;

  display: flex;
  flex-direction: row;

}

.left{
  flex:1;
  background: pink;
}

.center{
  flex:1;
}

.right{
  flex:1;
}
```



#### 2.完善accountbar组件布局

>  checkbox: scale(0.8, 0.8)     fs-34



accountbar.wxml

```html
<view class="accountbar">

  <!-- 左 -->
  <view class="left">
      <checkbox-group bindchange="bindSelectAll">
          <checkbox>全选</checkbox>
      </checkbox-group>
  </view>
  
  <!-- 中 -->
  <view class="center">
    <text>合计：</text>
    <text>500元</text>
  </view>

  <!-- 右 -->
  <view class="right" bindtap="bindAccount">
    <text>结算:( 500 )</text>
  </view>

</view>
```



accountbar.wxss

```css
/* components/accountbar/accountbar.wxss */
.accountbar{
  height: 120rpx;
  width: 100%;
  background: white;

  position: fixed;
  bottom: 0rpx;
  left: 0rpx;
  z-index: 2rpx;
  border-top: 2rpx solid #dddddd;

  display: flex;
  flex-direction: row;

}

.left{
  flex:1;
  /* background: pink; */

  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 34rpx;
}


.left checkbox{
  transform: scale(0.8,0.8);
}

.center{
  flex:1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 34rpx;
}

.center text:nth-of-type(2){
  color: #ff6802;
  font-size: 34rpx;
}

.right{
  flex:1;
  display: flex;
  justify-content: center;
  align-items: center;

  background: #ff6802;
  color: white;
  font-size: 34rpx;
}
```



accountbar.js

```js
// components/accountbar/accountbar.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

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
    /**1.点击全选 */
    bindSelectAll:function(event){
       console.log(event) 
       
    },

    /**2.点击结算*/
    bindAccount:function(event){
      console.log(event) 

    }  
  }
})
```



#### 3.处理组件中的事件

> 1.全选的点（记录选中还是没有选中）击  和  合计 的点击   
>
> 2.对外暴露一个方法修改选中状态

1.修改布局		

```html
<view class="accountbar">

  <!-- 左 -->
  <view class="left">
	 <!-- 1.监听选中和没有选中的事件 -->	    
      <checkbox-group bindchange="bindSelectAll">
        	<!--  value="selectAll" 点击的时候可以获取这个值;  checked:代码修改选中状态   -->	 
          <checkbox value="selectAll" checked="{{isChecked}}">全选</checkbox>
      </checkbox-group>
  </view>
  
  <!-- 中 -->
  <view class="center">
    <text>合计：</text>
    <text>{{summary}}元</text>
  </view>

  <!-- 右 -->
  <!-- 2.监听结算的点击事件 -->
  <view class="right" bindtap="bindAccount">
    <text>结算:( {{summary}} )</text>
  </view>

</view>
```



2.添加监听事件

```js
// components/accountbar/accountbar.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    summary:{
      type:Number,
      value:0
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    isChecked:false,
  },

  /**
   * 组件的方法列表
   */
  methods: {
    /**1.点击全选 */
    bindSelectAll:function(event){
      let value = event.detail.value[0];
      if (value == 'selectAll') {
        value = true;
      } else {
        value = false
      }
      // { index:1,checked:true }
      const myEventDetail = { index: 0, checked: value } // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      this.triggerEvent('accountclick', myEventDetail, myEventOption)
       
    },

    /**2.点击结算*/
    bindAccount:function(event){
      console.log(event)
      const myEventDetail = { index: 1} // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      this.triggerEvent('accountclick', myEventDetail, myEventOption)

    }, 

    /**3.选中或者取消选中checkbox（ 这个方法提供给外部调用来修改选中没选中 ） */
    isSelect: function (bool) {
      this.setData({
        isChecked: bool,
      })
    }

  },

 


})
```





### 3.购物车列表布局.

#### 1.基本布局

> height:140        flex: 1  5  2         scale(0.8, 0.8)     





cart.wxml

```html

  <scroll-view scroll-y class="cart-scroll">

     <view class="cart-item">
        <!-- 左 -->
        <view class="left">
           <checkbox></checkbox>
        </view>

        <!-- 中 -->
        <view class="center">
           <text>商品的tite</text>
        </view>

        <!-- 右 -->
        <view class="right">
            <text>2 x </text>
            <text> 200 元</text>
        </view>
     </view>
     
  </scroll-view>
      
```



cart.wxss

```css
/* pages/cart/cart.wxss */

/* 购物车滚动列表 */
.cart-scroll{
  height: calc(100% - 120rpx);
  background: skyblue;

}

.cart-item{
  height: 140rpx;
  display: flex;
  flex-direction: row;
  background: white;
  border-bottom: 2rpx solid #ddd;

}

.cart-item .left{
  flex:1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cart-item .left checkbox{
  transform: scale(0.8,0.8);
}

.cart-item .center{
  flex:5;
  background: red;
}

.cart-item .right{
  flex:2;
}

```



#### 2.完善布局

image-100    title-32





cart.wxml 完整布局

```html

  <scroll-view scroll-y class="cart-scroll">

     <view class="cart-item">
        <!-- 左 -->
        <view class="left">
           <checkbox></checkbox>
        </view>

        <!-- 中 -->
        <view class="center">
           <image src="../../image/user-head.png"></image>
           <text>商品的tite</text>
        </view>

        <!-- 右 -->
        <view class="right">
            <text>2 x </text>
            <text> 200 元</text>
        </view>
     </view>
     
  </scroll-view>
```



cart.wxss 完整样式

```css
/* pages/cart/cart.wxss */

/* 购物车滚动列表 */
.cart-scroll{
  height: calc(100% - 120rpx);
  background: skyblue;

}

.cart-item{
  height: 140rpx;
  display: flex;
  flex-direction: row;
  background: white;
  border-bottom: 2rpx solid #ddd;

}

.cart-item .left{
  flex:1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cart-item .left checkbox{
  transform: scale(0.8,0.8);
}

.cart-item .center{
  flex:5;
  /* background: red; */

  display: flex;
  flex-direction: row;
  align-items: center;
}

.cart-item .center image{
  width: 100rpx;
  height: 100rpx;
  margin: 20rpx;

}

.cart-item .right{
  flex:2;
  display: flex;
  align-items: center;
}


.cart-item .right text:nth-of-type(2){
    color: #ff6802;
    margin-left: 10rpx;
}
```



### 3.详情页面添加购物车

#### 1.先判断是否授权登陆

> 1.添加一个透明的button   
>
> 2.如果没有授权就显示透明的button  
>
> 3.授权并登陆  
>
> 4.在onload初始化 userInfo



```html
  <!-- 底部加购物车栏覆盖一个透明的button -->
  <button wx:if="{{userInfo==null}}" class="btn-transparent" open-type="getUserInfo" bindgetuserinfo="getUserInfo"></button>


/* 透明的button */
.btn-transparent{
  position: fixed;
  bottom: 0;
  left: 0;

  height: 120rpx;
  width: 100%;
  background: transparent;

  z-index: 2;
}
```



detail.js

```js
  /**
   * 页面的初始数据
   */
  data: {
    detailBean:null,
    tabs:['图文详情','参数详情'],
    tabIndex:0,
    userInfo: null,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      userInfo:app.globalData.userInfo
    })
    
    .....
    .....

  },
    
/**
   * 授权并登陆
   */
  getUserInfo:function(event){

      let _this = this;
      // console.log(event);
      //1.授权之后将数据存放在 app.js 和 data 中
      let userInfo = event.detail.userInfo;
      if (userInfo) {
        app.globalData.userInfo = userInfo;
        //2.刷新界面
        _this.setData({
          userInfo: userInfo,
        })
        console.log(app.globalData.userInfo, this.data.userInfo)
        
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
                //6.记录登陆状态在app.js中 ( isLogin  )
                app.globalData.isLogin = true;
                _this.setData({
                  isLogin: true,
                  
                })

              }
            })
          }
        })
      
      }//end if
  },//end getUserInfo
    
  ....
  ....
```

#### 2.编写购物车缓存工具类

```js
//1.定义一个Good类
class Good{
  constructor(goodId, title, counts, price, imgurl, isSelect){
    this.goodId = goodId || -1;
    this.title = title || '';
    this.counts = counts || 0;

    this.price = price || 0;
    this.imgurl = imgurl || '';
    this.isSelect = isSelect || false;
  }
}


//2.使用js 定义一个单例类
class CacheCart {
  constructor(data) {
    //1.在新建对象时，如果没有创建过就创建该类
    if (CacheCart.prototype.Instance === undefined) {
      this.data = data;
      CacheCart.prototype.Instance = this;
    }

    /**定义一个有两个商品的购物车
     * goods:
     * 
     * [
     *    { goodId:1000, title:'小米1', counts:2, price:799, imgurl:'htpp://xxx', isSelect:false },
     *    { goodId:2000, title:'小米2', counts:3, price:100, imgurl:'htpp://xxx', isSelect:ture },
     *    { goodId:3000, title:'小米3', counts:1, price:300, imgurl:'htpp://xxx', isSelect:true },
     *    { goodId:4000, title:'小米4', counts:2, price:899, imgurl:'htpp://xxx', isSelect:false },
     * ]
     *
     *  */
    this.cart={
      goods:[
        { goodId: 1000, title: "标题，例：红米Note 5A 高配版", counts: 1, price: 799, imgurl: "http://47.93.30.78:8080/XiaoMiShop/image/detail/1000/note5-1.jpg", isSelect:true },
        { goodId: 2000, title: "标题，例：红米Note 5A 高配版", counts: 3, price: 799, imgurl: "http://47.93.30.78:8080/XiaoMiShop/image/detail/2000/note5-1.jpg", isSelect: true },
      ],
    };

    //2.如果已经创建过就直接返回
    return CacheCart.prototype.Instance;
  }




  /**
   * 1.查找一个商品
   */
  findGood(goodId){
    let goods = this.cart.goods;
    for (let i = 0; i < this.cart.goods.length;i++){
      let good = goods[i];
      if (goodId == good.goodId) {
        return true;
      }
    }
    return false;
  }

  /**
   * 2.修改商品的数量
   */
  editGoodCounts(goodId,counts){

    let goods = this.cart.goods;
    for (let i = 0; i < this.cart.goods.length; i++) {
      let good = goods[i];
      //如果找到就修改商品数量
      if (goodId == good.goodId) {
        good.counts = good.counts + counts;
        console.log(this.cart.goods)
        return true;
      }
    }
    console.log(this.cart.goods)
    return false;
  }

  /**
   * 3.添加一个商品到购物车
   * { goodId:1000, title:'红米高配版', counts:2, price:799, imgurl: 'htpp://xxx', isSelect:false }
   */
  addGood(good) {
    let result = this.findGood(good.goodId);
    console.log(result,'===');
    if (result) {
      this.editGoodCounts(good.goodId, good.counts);
    } else {
      this.cart.goods.push(good);
    }
    console.log(this.cart.goods)
  }

  /**4.删除数据中指定的数据 */
  removeGood(index) {
    this.cart.goods.splice(index, 1);
  }

  /**5.获取购物车所有的商品 */
  getGoods(){
    return this.cart.goods;
  }

  /**
   * 6.统计选中商品的总价格
   */
  getAccount(){
    let sumPrice = 0; 
    this.cart.goods.forEach((value,index)=>{
      //已勾选的商品
      if (value.isSelect){
        //1.购买的数量
        let counts = value.counts;
        //2.商品的单价
        let price = value.price;
        sumPrice += (counts * price)
      }

    })
    return sumPrice;
  }

  /**
   * 7.选中所有的商品
   */
  selectAllGoods(isSelect){
    this.cart.goods.forEach((value, index) => {
      //已勾选的商品
      value.isSelect =isSelect;
    })
  }


  /**
 * 8.仅选中指定选中的商品: [ 1000, 2000 , 3000 ]
 */
  selectOnlySelect(goodIds) {

    //代表没有选中的商品
    if(goodIds.length == 0){
      this.selectAllGoods(false);
      console.log(this.cart.goods);
      return ;
    }

    //先取消所有的选中
    this.selectAllGoods(false);

    //在this.cart.goods找到了，就设为true
    goodIds.forEach((goodId, index) => {
      this.cart.goods.forEach((value, i) => {
        //仅仅比较goodId的值
        if (value.goodId == goodId) {
          //已勾选的商品
          value.isSelect = true;
        }
      })
    })
    console.log(this.cart.goods);
  }

  /**
   * 9.判断是否全选
   */
  isAllSelect(){
    let goods = this.cart.goods;
    for (let i = 0; i < this.cart.goods.length; i++) {
      let good = goods[i];
      //如果存在一个没有选中的，就返回false
      if (!good.isSelect) {
        return false;
      }
    }
    return true;
  }



}

module.exports = { 
  CacheCart: CacheCart,
  Good: Good,
};

// 使用案例：
/**
 * let CacheCart = require('../../CacheCart').CacheCart;
 * 
 * let c1 = new CacheCart();
 * let c1 = new CacheCart();
 * 
 */
```



#### 3.添加购物车

> 1.创建一个商品   2.把商品添加到购物车的工具类  3.界面跳转
>
> let good = new Good(xx);
>
> cacheCart.addGood(good);
>
> wx.switchTab

detail.js

```js
....
....

const CacheCart = require('../../utils/cachecart.js').CacheCart;
const Good = require('../../utils/cachecart.js').Good;
var app =getApp();
let cacheCart = new CacheCart();


Page({

  ....
  ....
  
  
  
  /**监听购物车组件的所有事件 */
  cartClickIndex:function(event){

    
    let userInfo = app.globalData.userInfo;
    let isLogin = app.globalData.isLogin;

    //判断用户受否授权和登陆
    if ( userInfo!=null && isLogin ){
      let index = event.detail.index;
      console.log(index);
      //1.点击购物车
      if (index == 0) {
        wx.switchTab({
          url: '../../cart/cart',
        })       
        //2.点击加购物车
      } else if (index == 1) {

        //1.1获取商品信息
        let detailBean = this.data.detailBean;
        let good = new Good(detailBean.goodsid, detailBean.title, 1,detailBean.price, detailBean.banners[0], true);
        cacheCart.addGood(good);//加购物车
        wx.showToast({
          title: '加入成功',
          success:function(){
            wx.switchTab({
              url: '../cart/cart',
            })
          }
        })
       
        //3.点击立即购买  
      } else {

      }  
    }



  },
	
  ....
  ....
})
```

### 4.购物车展示商品

> 1.在onLoad 和 onShow函数中初始化数据   2.展示数据
>
> this.initData()  // 初始化数据和刷新界面

cart.wxml

```html
  <checkbox-group bindchange="cartSelectChange">
          <block wx:for="{{cartList}}" wx:key="{{index}}">
          
                  <view class="cart-item">
                    <!-- 左 -->
                    <view class="left">
                      <checkbox value="{{item.goodId}}" checked="{{item.isSelect}}"></checkbox>
                    </view>

                    <!-- 中 -->
                    <view class="center">
                      <image src="{{item.imgurl}}"></image>
                      <text>{{item.title}}</text>
                    </view>

                    <!-- 右 -->
                    <view class="right">
                        <text>{{item.counts}} x </text>
                        <text> {{item.price}} 元</text>
                    </view>
                  </view>
            
          </block>
      </checkbox-group>
```



cart.js

```js
// pages/cart/cart.js
const CacheCart = require('../../utils/cachecart.js').CacheCart;
const Good = require('../../utils/cachecart.js').Good;
var app = getApp();
let cacheCart = new CacheCart();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    cartList:[],
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    //初始化数据
    this.initData();

  },

  //初始化数据
  initData:function(){
    let goods = cacheCart.getGoods();
    console.log(goods);
    this.setData({
      cartList:goods,
    })
  },
  
  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    //初始化数据
    this.initData();
  },

  /**
   * 选中的商品
   */
  cartSelectChange:function(event){
    console.log(event);

  }

})
```



### 5.item点击事件-选中或取消

> 1.每次点击item, 到购物车工具类中 选中仅被选中的商品
>
> cacheCart.selectOnlySelect(  event.detail.value  );  //参数是选中的商品，最好要刷新界面



cart.js

```js
  /**
   * 选中的商品
   */
  cartSelectChange:function(event){
    console.log(event.detail.value);
    //1.修改购物车中的商品(选中／ 取消选中)
    cacheCart.selectOnlySelect(event.detail.value);

  }
```



### 4.全选商品

> 1.点击全选按钮需要全选  2.点击item如果都选中需要全选钩上   3.记住要刷新界面
>
> cacheCart.selectAllGoods(selectAll);
>
> this.selectComponent("#accountbar").isSelect( bool )
>
> this.initData()  // 记住要刷新界面



cart.js

```js
 /**
   * 选中的商品
   */
  cartSelectChange:function(event){
    console.log(event.detail.value);
    cacheCart.selectOnlySelect(event.detail.value);

    //1.获取到accountbar组件
    let accountbar = this.selectComponent("#accountbar")
    //2.判断是否全选
    if (cacheCart.isAllSelect()){
      //3.全选
      accountbar.isSelect(true);
    }else{
      //4.取消全选
      accountbar.isSelect(false);
    }

  },
  //account-bar组件的回调事件
  accountBarClick:function(event){
    let index = event.detail.index;
    
    //1.点击全选
    if(index == 0){

      let selectAll = event.detail.checked;
      cacheCart.selectAllGoods(selectAll);// 全选获取取消全选
      //刷新界面
      this.initData();

    //1.点击结算
    }else{

    }
  }
```

account bar.js

```js
// components/accountbar/accountbar.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    isChecked:false,
  },

  /**
   * 组件的方法列表
   */
  methods: {
    /**1.点击全选 */
    bindSelectAll:function(event){
      let value = event.detail.value[0];
      if (value == 'selectAll') {
        value = true;
      } else {
        value = false
      }
      // { index:1,checked:true }
      const myEventDetail = { index: 0, checked: value } // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      this.triggerEvent('accountclick', myEventDetail, myEventOption)
       
    },

    /**2.点击结算*/
    bindAccount:function(event){
      console.log(event)
      const myEventDetail = { index: 1} // detail对象，提供给事件监听函数
      const myEventOption = {} // 触发事件的选项
      this.triggerEvent('accountclick', myEventDetail, myEventOption)

    }, 

    /**选中获取取消选中checkbox */
    isSelect: function (bool) {
      this.setData({
        isChecked: bool,
      })
    }

  },



})

```



### 5.统计summary合计

> 1.界面初始化时要合计   2.点击选择全部用合计  3.点击item选中和取消需要合计； 
>
> this.initData()  // 统计合计 并 刷新界面

cart.wxml



cart.js

```js
// pages/cart/cart.js
....
....

Page({

  /**
   * 1.页面的初始数据
   */
  data: {
    cartList:[],
    summary:0,
  },
  
  ....
  ....

  //2.初始化数据
  initData:function(){
    let goods = cacheCart.getGoods();
    let sum = cacheCart.getAccount();
    console.log(goods);
    this.setData({
      cartList:goods,
      summary: sum,
    })
  },
    

  /**
   * 选中的商品
   */
  cartSelectChange:function(event){
    console.log(event.detail.value);
    ....
    ....
    
    
    //3.刷新界面
    this.initData();

  },

})
```



accountbar.js

```js
// components/accountbar/accountbar.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    summary:{
      type:Number,
      value:0
    }
  },
  
  ....
  ....
  
})
```



accountbar.wxml

```html
<!--components/accountbar/accountbar.wxml-->
<view class="accountbar">

  <!-- 左 -->
  <view class="left">
      <checkbox-group bindchange="bindSelectAll">
          <checkbox value="selectAll" checked="{{isChecked}}">全选</checkbox>
      </checkbox-group>
  </view>
  
  <!-- 中 -->
  <view class="center">
    <text>合计：</text>
    <text>{{summary}}元</text>
  </view>

  <!-- 右 -->
  <view class="right" bindtap="bindAccount">
    <text>结算:( {{summary}} )</text>
  </view>

</view>
```





