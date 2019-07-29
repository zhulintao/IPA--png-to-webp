//
//  UIImage+NamedUtils.m
//  WebpDemo
//
//  Created by lintao on 2019/7/17.
//  Copyright © 2019 lintao. All rights reserved.
//

#import "UIImage+NamedUtils.h"
#import "UIImage+WebP.h"
#import "NSBundle+AutoImgResourceScale.h"
#import <objc/message.h>

#define LBImageBundle_Name  @"LBImageBundle.bundle" //@"bundle路径"
#define LBImageBundle_Path [[[NSBundle mainBundle] resourcePath] stringByAppendingPathComponent:LBImageBundle_Name]
#define LBImageBundle [NSBundle bundleWithPath:LBImageBundle_Path]
@implementation UIImage (NamedUtils)

// 把类加载进内存的时候调用，只会调用一次
+ (void)load {
    // 交换方法:runtime
    
    // 获取imageNamed
    Method imageNameMethod = class_getClassMethod(self, @selector(imageNamed:));
    
    // 获取HiAR_imageNamed
    Method HiAR_imageNamedMethod = class_getClassMethod(self, @selector(HiAR_imageNamed:));
    
    method_exchangeImplementations(imageNameMethod, HiAR_imageNamedMethod);
}

// 以后想修改系统的方法，但是又不想重名字，可以在前面添加前缀
+ (UIImage *)HiAR_imageNamed:(NSString *)name {
    UIImage *image = [UIImage HiAR_imageNamed:name];
    
    if (image) {
//        NSLog(@"HiARImage--加载成功了");
    } else {
//        NSLog(@"HiARImage--加载失败了");
        NSData *imgData = [NSData dataWithContentsOfFile:[LBImageBundle pathForResource:name ofType:@"webp"]];
        image = [UIImage sd_imageWithWebPData:imgData];
    }
    
    return image;
}

@end
