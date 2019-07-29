# encoding=utf-8

#  -s 最小要压缩图片大小（kb)
#  -i 要压缩的图片文件夹目录
#  -q 压缩图片质量  默认60

import commands
import os
import sys
import getopt
import shutil

input_file = "" 
quality = "60"

outputPath = input_file + "_webp"

compressSize = ""


def handle_sys_arguments():
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:q:s:")
    global quality
    global output_file
    global compressSize
    global input_file

    for op, value in opts:
        # print("op:" + op + "__" + value)
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_file = value
        elif op == "-h":
            print(" -s 最小要压缩图片大小 （kb)\n -i 要压缩的图片文件夹目录\n -q 压缩图片质量  默认60")
            exit()
        elif op == "-q":
            quality = value
        elif op == "-s":
            compressSize = value


def path_file(path):
    for i in os.listdir(path):
        print(i)
        new_path = os.path.join(path, i)
        if os.path.isfile(new_path):
            transform(new_path)
        else:
            path_file(new_path)


def transform(f):
    split_name = os.path.splitext(f)
    filePath = f

    print(split_name[0])

    if split_name[1] == ".webp" or (split_name[1] != ".jpg" and split_name[1] != ".png"):
        return

    if compressSize.strip() != "" and os.path.getsize(filePath) / 1024.0 > int(compressSize):
        command = "cwebp -q " + quality + " " + filePath + " -o " + \
                  split_name[0] + ".webp"
        commands.getstatusoutput(command)
        print("执行了:" + command)
    elif compressSize.strip() == "":
        command = "cwebp -q " + quality + " " + filePath + " -o " + \
                  split_name[0] + ".webp"
        commands.getstatusoutput(command)
        print("执行了:" + command)
    else:
        print("不压缩")


def check_args():
    if input_file.strip() == "":
        print("请输入要转换的文件夹路径")
        exit()


def copy_webp_files(sourceDir, targetDir):
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)

    print sourceDir
    print(targetDir)

    for file in os.listdir(sourceDir):
        new_source_path = os.path.join(sourceDir, file)
        new_target_path = targetDir
        if os.path.isdir(new_source_path):
            copy_webp_files(new_source_path, new_target_path)
        else:
            new_target_path = os.path.join(targetDir, file)
            splite_name = os.path.splitext(file)
            print("copyWebpFiles_split" + splite_name[1])

            if splite_name[1] != ".webp":  # 只复制webp
                print(splite_name[1])
                continue

            shutil.copy(new_source_path, new_target_path)
            os.remove(new_source_path)


if __name__ == '__main__':
    handle_sys_arguments()
    check_args()
    path_file(input_file)
    copy_webp_files(input_file, outputPath)
