# IPA--png-to-webp
png转webp本地图片优化实践
## 本地图片资源png转webp

在最近一个项目中，遇到这么个情况，同一个移动端APP产品，iOS版本的安装包大小约170M，几乎是Android版本（约60M）的3倍；检查发现iOS打包时引用了不少的本地测试资源，经过移除本地测试资源link、编译配置选项优化等操作后，仍有130M，解压IPA文件发现图片资源Assets.car竟有80多M，而这个文件在打包时是不会被压缩的，我们工程中image.assets文件总大小才55M左右，说明我们也进了苹果PNG编译优化的坑，越优化越大了。
我们都知道，webp格式图片时目前淘宝、美团、Google等用于网络图片优化的主流格式，它拥有更小的图片体积，而且拥有肉眼识别无差异的图像质量。我测试将image.assets文件下的图片全部转化为webp格式后，总大小变为5.1M，这让我很是兴奋，但是原生的oc代码并不支持webp的加载，而且APPicon、launchImage、xib、storyboard等都不能直接加载webp文件，Google调研一番并没有前辈们把webp用到本地图片优化的案例，倒是有很多网络图片资源的webp优化实践，借鉴网络图片webp格式优化的加载方式，测试确认可以正常加载bundle的webp文件。这让我对继续png转webp的优化方式有了信心，下面记录一下我的实践过程。

### 1、转化2倍图大于30k的图片资源并copy
利用[脚本](https://github.com/zhulintao/IPA--png-to-webp/blob/master/webp_converter.py)将2倍图大于30k的图片转化为webp格式并拷贝到指定目录下

```
lintaozhudeMacBook-Pro-3:~ lintao$ python /Users/lintao/Desktop/webp调试/webp_converter.py -i /Users/lintao/Desktop/webp调试/Assets.xcassets -o /Users/lintao/Desktop/webp调试/webpImage -s 30

// python 脚本文件路径 -i 待转化的图片文件（夹）路径 -o webp文件输出路径 -s 转化图片的最小大小（默认为60kb）
```


### 2、将转化后的webp图片资源打包到bundle
bundle文件是静态的，也就是说，我们包含到包中的资源文件作为一个资源包是不参加项目编译的。这在webp文件本地处理编译选项不明的情况下，无疑是很好的选择。
bundle文件的制作过程参考[iOS 如何把图片资源或者xib文本文件,打包成bundle文件及遇到的坑（详解）](https://blog.csdn.net/Z1591090/article/details/88356461)

### 3、移除image.assets下被转化的图片资源
除APPicon、launchImage等不支持加载webp文件对应的图片资源，以及小于30k的icon资源外，其他图片资源全部删除，另外，移除所有一倍图，剩余image.assets约3.5M。

### 4、接入装有webp格式图片文件的bundle
**接入webp格式的图片文件分三步：** 
<1>、安装webp支持文件SDWebImage/WebP，需依赖libwebp，pod安装SDWebImage/WebP时可能会安装失败。原因是SDWebImage的配置文件中，libwebp的源是国外的镜像。翻墙后仍可能失败，比较保险的办法是替换libwebp 的 .podspec pod配置文件中的源地址为国内的源。具体可参考【[pod 'libwebp'失败的解决办法](https://www.jianshu.com/p/eacd3cee51ac)】；
<2>、以最小的代价完成bundle下webp格式图片对image.assets下png图片的替换使用，我使用的方法交换方式，修改了系统的 **-imageNamed:** 方法，在它获取不到PNG格式图片的情况下，获取一次bundle下的webp文件。具体见代码【[UIImage+NamedUtils](https://github.com/zhulintao/IPA--png-to-webp/blob/master/UIImage%2BNamedUtils.m)】；
<3>、让第<2>步能读取到正确倍数的webp文件，详见代码【[NSBundle+AutoImgResourceScale.h](https://github.com/zhulintao/IPA--png-to-webp/blob/master/NSBundle%2BAutoImgResourceScale.m)】
### 5、处理xib&storyboard下默认的图片配置
前面有说道APPicon、launchImage、xib、storyboard等不支持webp格式文件的加载，虽然APPicon、launchImage对应的图片资源为做转化，但是xib、storyboard对应的图片资源仍应使用代码的方式重新配置。
### 6、检查&测试
最后一步，查缺补漏，首先检查xib、storyboard下是否还有图片配置未更新；然后运行工程，检查是否有图片缺失的情况；最后检查性能情况，由于webp格式图片的解码需要比png解码更多的时间，所以也需要看是否会影响到用户体验。


