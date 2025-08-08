#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@DATE: 2024-07-29 15:08:36
@Author: ringo
@Version: 1.0
@File: utility.py
@Software: vscode
@Description:工具函数
        
"""

import os
from datetime import datetime
import Rhino
import Rhino.Geometry as rg
import ghpythonlib.components as gh

doc = Rhino.RhinoDoc.ActiveDoc


def mkdir(path):
    """
    如果目录不存在,则创建目录
    """
    if not os.path.exists(path):
        os.makedirs(path)


def item_to_list(item):
    """
    将输入的item转换为列表形式,如果item本身就是列表,则将其展开
    """
    new_list = []
    if hasattr(item, "__len__"):
        for i in item:
            if isinstance(i, list):
                new_list += i
            else:
                new_list.append(i)
    else:
        new_list.append(item)
    return new_list


def print_time(text=None):
    ticks = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(ticks + " " + str(text))


def round_custom(float, times=2):
    a = float * times
    a_roundup = int(a + 0.5)
    return a_roundup


def find_BCA_exe_file():
    """
    查找指定目录及其子目录下的blueCFD-AIR.exe文件
    """
    target = "blueCFD-AIR.exe"
    dir_paths = get_common_program_files()
    for dir_path in dir_paths:
        for root, _dirs, files in os.walk(dir_path):
            for filename in files:
                if filename.lower() == target.lower():
                    return os.path.join(root, filename)
    raise ValueError("No exe file found in the folder.")


def get_common_program_files():
    """
    Find the common Program Files directories.
    :return: A list of common Program Files directories.
    """
    return [os.environ["ProgramFiles"], os.environ["ProgramFiles(x86)"]]


def find_exe_files(software="ParaView"):
    """
    查找指定目录及其子目录下的.exe文件
    """

    target_map = {"blueCFD-AIR": "blueCFD-AIR.exe", "ParaView": "paraview.exe"}
    if software not in target_map:
        raise ValueError(f"Unsupported software: {software}")
    target = target_map[software]
    dir_paths = get_common_program_files()
    for dir_path in dir_paths:
        for root, _dirs, files in os.walk(dir_path):
            if target in files:
                return os.path.join(root, target)
    raise ValueError("No exe file found in the folder.")


def inter_brep(brep1, brep2, name):
    """
    Intersect two breps and return the surfaces
    :param brep1: brep1
    :param brep2: brep2
    :param name: name
    :return: list_surfaces, list_breps
    """
    print_time(name + "inter brep start")
    list_surfaces = []
    for b in brep1:
        # print_timei
        curve = gh.BrepXBrep(b, brep2)[0]
        if curve:
            # print_timecurve
            if gh.Planar(curve)[0]:
                surfaces = []
                surfaces.append(gh.BoundarySurfaces(curve))
                list_surfaces += surfaces
    print_time("{} inter brep success, total {}".format(name, len(list_surfaces)))

    return list_surfaces


def id_srf(srf):
    """
    indentify the surface
    :param srf: surface
    :return: id_srf_list
    """
    srf = item_to_list(srf)
    id_srf_list = []

    for s in srf:
        if s:
            id_s = gh.EvaluateBox(s, 0.5, 0.5, 0.5)
            xyz = "{}_{}_{}".format(
                round_custom(id_s[1][0], 1000),
                round_custom(id_s[1][1], 1000),
                round_custom(id_s[1][2], 100),
            )
            id_srf_list.append(xyz)

    return id_srf_list


def split_brep(breps, surfaces, name):
    print_time(name + " split brep start___________________")
    walls = []
    tree_faces = []
    # 判断面是不是一个列表，如果不是
    breps = item_to_list(breps)

    surfaces = item_to_list(surfaces)
    # s_id_srf = id_srf(surfaces)
    # breps循环
    for b in breps:
        s_breps = gh.SplitBrepMultiple(b, surfaces)
        b_center = id_srf(b)
        # print_time(s_breps)
        # 判断是不是切出一个面
        s_breps = item_to_list(s_breps)
        for s_b in s_breps:
            s_b_center = id_srf(s_b)
            if s_b_center == b_center:
                walls.append(s_b)
                s_breps.remove(s_b)
                tree_faces += s_breps

    print_time(
        "{} split brep success, total {}___________________".format(
            name, len(tree_faces)
        )
    )

    return walls, tree_faces


def breps_to_mesh(breps):
    print_time(" breps to mesh start")
    meshs = breps_to_meshs(breps)
    if meshs:
        mesh = [gh.MeshJoin(meshs)]
    else:
        print_time("Breps to mesh Failed")
    return mesh


def breps_to_meshs(breps):
    print_time(" breps to meshs start___________________")
    breps = item_to_list(breps)
    try:
        meshs = [rg.Mesh.CreateFromBrep(i) for i in breps]
        meshs = [gh.Triangulate(gh.MeshJoin(i))[0] for i in meshs]
        print_time(" Breps to meshs End, total {}".format(len(meshs)))
    except:
        print_time("Breps to meshs Failed")
    return meshs


def srf_on_door(doors, door_blocks):
    list_door = [
        i for i in doors if gh.PointInBreps(door_blocks, gh.Area(i)[1], False)[0]
    ]
    return list_door
