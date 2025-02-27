# Ant blueCFD

[English](README_EN.md)

## 简介

本项目是基于Grasshopper软件开发的用于blueCFD AIR软件的建模插件。
![截图](./resources/01.png)

## 功能

- 将Grasshopper的几何模型转化为blueCFD的几何模型
- 模型可视化，不同构件的颜色不同
- 调用blueCFD AIR软件进行仿真，需要在本地安装blueCFD AIR软件
- 对模拟结果进行解压缩，用于进一步后处理，例如利用Paraview进行可视化。

## 使用方法

- 安装blueCFD AIR软件；
- 安装blueCFD Core；
- 安装Rhino 7；
- 下载本项目，并保存到Rhino 7的`c:\Users\<用户名>\AppData\Roaming\McNeel\Rhinoceros\7.0\scripts\`，其中用户名是你的计算机用户名；
- 将项目中的`UserObjects`文件夹复制到Rhino 7的`UserObjects`文件夹中；
- 打开项目中的`Templates`文件夹中的`01_BlueCFD_Air_Modelling.gh`进行建模。

由于没在其他电脑上测试过，可能不同环境下，会有一些bug，欢迎大家捉虫，具体操作方法见B站视频。