# encoding: utf-8
'''
@Author: liteng
@File: rename
@Time: 2019/1/2 15:04
'''


# 文件夹里边的文件太乱怎么办
# 统一处理
# import os
#
# fileFolder = '/Users/liteng/Desktop/Demo1'
#
# list = os.listdir(fileFolder)
#
# for index,filename in enumerate(list):
#
#     print('修改前:'+filename)
#     # param1: 修改前的文件路径 param2: 修改后的文件路径
#     os.rename(fileFolder+filename,fileFolder+(str(int(index)+1))+'.'+filename.split('.')[1])
#

for i in [1,2,3,4]:
    print(i)
    for j in [5,6,7,8]:
        print(j)