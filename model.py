# -*- coding:UTF-8 -*-
import platform
import os
import ghpythonlib.components as gh
import Rhino.Geometry as rg  # type: ignore
import scriptcontext as sc
from utility import (
    print_time,
    mkdir,
    round_custom,
    item_to_list,
    inter_brep,
    split_brep,
    breps_to_meshs,
    srf_on_door,
    breps_to_mesh,
)
from blue_cfd import BlueDoor, BlueModel, BlueRoom


def brep_to_blueModel(
    room_blocks,
    door_blocks=None,
    _windows=None,
    _inlets=None,
    _outlets=None,
    _sources=None,
    _fans=None,
):
    blue_model = BlueModel()

    if door_blocks is not None:
        print_time("Split doors")
        name = "_doors_"
        door_srfs = inter_brep(room_blocks, door_blocks, name)
        _doors = srf_on_door(door_srfs, door_blocks)

        blue_doors = []
        for index, door_block in enumerate(door_blocks):
            split_connect = split_brep(door_block, door_srfs, "Connects")
            # door_srfs = inter_brep(room_blocks, door_block, name)
            # _doors = srf_on_door(door_srfs, door_block)
            # connect = split_connect[0]
            blue_door = BlueDoor()
            blue_door.display_name = "door_" + blue_door.identifier
            blue_door.connect = breps_to_meshs(split_connect[0])
            blue_door.door_srfs = split_connect[1]
            blue_door.door_meshes = breps_to_meshs(blue_door.door_srfs)
            blue_doors.append(blue_door)
            blue_model.doors.append(blue_door)

    room_blocks = item_to_list(room_blocks)
    rooms = []
    for index, room_block in enumerate(room_blocks):
        room = BlueRoom()
        room.display_name = "Room-" + room.identifier
        room.geometry = room_block
        room_srfs = room_block

        inter_doors = []
        _doors = []
        # inter_doors = [i for i in blue_doors if srf_on_door(i.door_srfs, room_srfs)]
        if blue_doors:
            for blue_door in blue_doors:
                door_srf = srf_on_door(blue_door.door_srfs, room_srfs)
                if len(door_srf) > 0:
                    blue_door.rooms.append(room)
                    # inter_doors.append(blue_door)
                    room.blue_doors.append(blue_door)
                    # for inter_door in inter_doors:
                    _doors += blue_door.door_srfs
        if _doors:
            split = split_brep(room_srfs, _doors, "Doors")
            room_srfs = split[0]
            # doors = split[1]
            # room.doors = breps_to_meshs(doors)
            # for inter_door in inter_doors:
            #     inter_door.parents.append(room)
        if _windows:
            split = split_brep(room_srfs, _windows, "Windows")
            room_srfs = split[0]
            windows = split[1]
            room.windows = breps_to_meshs(windows)
        if _inlets:
            split = split_brep(room_srfs, _inlets, "Inlets")
            room_srfs = split[0]
            inlets = split[1]
            room.inlets = breps_to_meshs(inlets)
        if _outlets:
            split = split_brep(room_srfs, _outlets, "Outlets")
            room_srfs = split[0]
            outlets = split[1]
            room.outlets = breps_to_meshs(outlets)
        if _sources:
            split = split_brep(room_srfs, _sources, "Sources")
            room_srfs = split[0]
            sources = split[1]
            room.sources = breps_to_meshs(sources)
        if _fans:
            split = split_brep(room_srfs, _fans, "Fans")
            room_srfs = split[0]
            fans = split[1]
            room.fans = breps_to_meshs(fans)

        walls = []
        roofs = []
        floors = []
        room_srfs = item_to_list(room_srfs)

        for face in room_srfs[0].Faces:
            room_srf = face.DuplicateFace(True)
            # normal = rs.SurfaceNormal(room_srf, [0.5, 0.5])
            normal = face.NormalAt(0.5, 0.5)
            z = normal[2]
            if z >= -0.5 and z <= 0.5:
                walls.append(room_srf)
            elif z < -0.5:
                floors.append(room_srf)
            elif z > 0.5:
                roofs.append(room_srf)
        array = rg.Brep.JoinBreps(walls, 0.01)
        wall = []
        print_time(room.display_name)

        if array:
            for a in array:
                wall.append(a)
        else:
            print_time(room.display_name + " geometry is None")
            continue

        room.roof = breps_to_meshs(roofs)
        room.floor = breps_to_meshs(floors)
        room.wall = breps_to_mesh(wall)
        # if index == 0:
        #     room.connects = breps_to_meshs(connects)
        rooms.append(room)

    # room.connects = breps_to_meshs(connects)
    blue_model.rooms = rooms
    return blue_model


def blueModel_to_stl(blue_model, file_name=None, path=None):
    if file_name is None:
        file_name = "blueCFD air model"
    rooms = blue_model.rooms
    doors = blue_model.doors
    # 初始化path
    if path is None:
        USER_PATH = os.path.expanduser("~")
        PLATFORM = platform.system()
        if PLATFORM == "Windows":
            mkdir(USER_PATH + "\\ant_tools")
            file_path = USER_PATH + "\\ant_tools\\" + file_name + ".stl"
        elif PLATFORM == "Darwin":
            mkdir(USER_PATH + "/ant_tools")
            file_path = USER_PATH + "/ant_tools/" + file_name + ".stl"
        # file_path = "C:/" + file_name + ".stl"
    else:
        path = path.replace("\\", "/")
        file_path = path + "/" + file_name + ".stl"
    file_path_w = file_path.replace("/", "\\")

    # 初始化字段
    str_rooms = ""
    str_roof = ""
    str_floor = ""
    str_connects = ""
    str_doors = ""
    str_windows = ""
    str_inlets = ""
    str_outlets = ""
    str_sources = ""
    str_fans = ""

    for room in rooms:
        name = room.display_name
        str_rooms += mesh_to_string(room.wall, "room", name)
        str_roof += mesh_to_string(room.roof, "roof", name)
        str_floor += mesh_to_string(room.floor, "floor", name)
        # str_doors += mesh_to_string(room.doors, 'door', name)
        str_windows += mesh_to_string(room.windows, "window", name)
        str_inlets += mesh_to_string(room.inlets, "inlet", name)
        str_outlets += mesh_to_string(room.outlets, "outlet", name)
        str_sources += mesh_to_string(room.sources, "source", name)
        str_fans += mesh_to_string(room.fans, "fan", name)
        # if len(room.blue_doors) > 0:
        #     str_doors += mesh_to_string(room.blue_doors, "door", name, room.blue_doors)
        #     str_connects += mesh_to_string(room.connects, "connect", name)
    for door in doors:
        name = door.display_name
        str_doors += mesh_to_string(door.door_meshes, "door", name, blueDoor=door)
        str_connects += mesh_to_string(door.connect, "connect", name, blueDoor=door)

    with open(file_path, "w") as f:
        stl = (
            str_rooms
            + str_doors
            + str_roof
            + str_floor
            + str_windows
            + str_inlets
            + str_outlets
            + str_sources
            + str_fans
            + str_connects
        )
        f.write(stl)
        f.close()
        stl_path = file_path_w
    return stl_path


def mesh_to_string(mesh, type, name=None, no=None, blueDoor=None):
    string = ""
    sum = 0  # 计数
    if no is None:
        no = 0
    if mesh:
        if not isinstance(mesh[0], rg.Mesh):
            mesh = [i.door_meshes for i in mesh]
        mesh = item_to_list(mesh)
        # print_time(name + " mesh to string start")
        for index, m in enumerate(mesh):
            if m:
                if m is None:
                    continue
                sum += 1

                normals = [
                    m.NormalAt(i, 0, 0, 0, 0) for i in range(m.Faces.Count)
                ]  # rs.MeshFaceNormals(m)
                faceVerts = [(i.A, i.B, i.C, i.D) for i in m.Faces]

                # normals = rs.MeshFaceNormals(m)
                # if index == 0:
                #     print normals
                verts = [i for i in m.Vertices]  # rs.MeshVertices(m)

                f_string = ""
                if faceVerts:
                    if type == "room":
                        f_name = name
                    elif type == "connect":
                        f_name = " <" + name + "> "
                    elif type == "door":
                        room_name = blueDoor.rooms[index].display_name
                        # f_name = name + " < " + str(type) + " " + str(index)
                        f_name = room_name + " < " + blueDoor.display_name
                    else:
                        f_name = name + " < " + str(type) + "-" + str(no) + str(index)
                    if type == "room":
                        f_string = "solid |" + f_name + "\n"
                    else:
                        f_string = "solid " + f_name + "\n"
                    for count, face in enumerate(faceVerts):
                        line = "facet normal " + str(normals[count]) + "\n"
                        line = str.replace(line, ",", " ")
                        line2 = "outer loop" + "\n"
                        f_string += line + line2
                        if face[2] == face[3]:
                            i_t = 3
                        else:
                            i_t = 4
                        for i in range(0, i_t):
                            line = "vertex " + str(verts[face[i]]) + "\n"
                            line = str.replace(line, ",", " ")
                            f_string += line
                        line = "endloop" + "\n"
                        line2 = "endfacet" + "\n"
                        f_string += line + line2
                    f_string = f_string + "endsolid " + f_name + "\n"
                string += f_string
        if sum != 0:
            if type == "connect":
                print_time("[" + str(type) + "]-" + str(sum))
            else:
                print_time("[" + name + "." + str(type) + "]-" + str(sum))
        print_time(name + " mesh to string end")
    return string


def string_to_mesh(string):
    # Initialize "mesh" variable as a blank mesh object to hold each face.
    mesh = rg.Mesh()
    # Initialize "MESH" variable as a blank mesh object to accumulate faces.
    MESH = rg.Mesh()

    for line in string.splitlines():
        if "vertex" in line:
            q = line.replace("vertex ", "")
            q = q.replace("\n", "")
            q = [float(x) for x in q.split()]
            len_q = len(q)
            # print_time(len_q)
            # Fill mesh with three vertex lines in a row.
            mesh.Vertices.Add(q[0], q[1], q[2])
        # File itself tells us we are done with three vertices for one face.
        if "endloop" in line:
            mesh.Faces.AddFace(0, 1, 2)  # Create a single face mesh.
            # Magically build a real multi-face mesh while removing redundant vertices.
            MESH.Append(mesh)
            # Reinitialize empty mesh object for each mesh face.
            mesh = rg.Mesh()

    # Gives nice mesh and preview but makes the script take longer.
    MESH.Normals.ComputeNormals()
    return MESH


def stl_reader(stl_path):
    # list_brep =[]
    meshs = []
    names = []
    objs = []
    temp_string = ""
    temp_mesh = rg.Mesh()
    brep = []
    inlets = []
    walls = []
    # connects = []
    doors = []
    windows = []
    outlets = []
    sources = []
    fans = []
    room_names = []
    window_names = []
    inlet_names = []
    outlet_names = []
    # connect_names =[]
    source_names = []
    fan_names = []
    faces = []

    with open(stl_path) as f:
        for line in f:
            if "endsolid" in line:
                line = line.replace("\n", "")
                temp_string += line
                line = line.replace("endsolid ", "")
                if "-" in line:
                    line = gh.TextSplit(line, "<")[1]
                    line = line.replace(" ", "")
                # line = line.replace(" <", "-")
                names.append(line)
                temp_mesh = string_to_mesh(temp_string)
                obj = sc.doc.Objects.AddMesh(temp_mesh)
                meshs.append(obj)
                temp_string = ""
                temp_mesh = rg.Mesh()
            else:
                temp_string += line
        print_time("读取成功，共读取" + str(len(meshs)) + "个物体")

    for index, m in enumerate(meshs):
        if m:
            # b = rs.MeshToNurb(m)
            # b = rs.coercebrep(b)
            b = rg.Brep.CreateFromMesh(m, True)
            b.MergeCoplanarFaces(0.001)
            if "< door" in names[index]:
                print_time("跳过" + names[index])
            else:
                faces.append(b)
            # sc.doc.Objects.AddBrep(b)  # bake the brep object
            # sc.doc.Objects.Delete(obj, True)  # delete the Rhino brep
            # sc.doc.Views.Redraw()
            # brep.append(b)
            if "window" in names[index]:
                windows.append(b)
                window_names.append(names[index])
            elif "inlet" in names[index]:
                inlets.append(b)
                inlet_names.append(names[index])
            elif "outlet" in names[index]:
                outlets.append(b)
                outlet_names.append(names[index])
            elif "source" in names[index]:
                sources.append(b)
                source_names.append(names[index])
            elif "< door" in names[index]:
                doors.append(b)
            elif "fan" in names[index]:
                fans.append(b)
                fan_names.append(names[index])
            # elif ">" in names[index]:
            #    connects.append(b)
            #   connect_names.append(names[index])
            else:
                walls.append(b)
                room_names.append(names[index])
    # box = rs.JoinSurfaces(faces)
    # box = faces


def cull_curves(curves):
    cull_curves = []
    list_n = []
    for index, c in enumerate(curves):
        len = gh.Length(c)
        if index == 0:
            i_len = len
            cull_curves.append(c)
            n = 0
        bool = gh.Similarity(i_len, len, 0.5)[0]
        if bool:
            n += 1
            continue
        else:
            cull_curves.append(c)
            i_len = len
            list_n.append(n)
            n = 1
    list_n.append(n)
    return cull_curves, list_n
