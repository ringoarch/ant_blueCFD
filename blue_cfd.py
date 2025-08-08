#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@DATE: 2025-02-27 15:11:07
@Author: ringo
@Version: 0.1.0
@File: CFD.py
@Software: vscode
@Description:
        
"""
import Rhino.Geometry as rg
from utility import print_time, item_to_list
from _base import _Base
from utility import inter_brep, split_brep, srf_on_door


class BlueDoor(_Base):
    """
    Properties:
        * identifier
        * display_name
        * geometry
        * door_srf_1
        * door_srf_2
        * connect
    """

    __slots__ = (
        "geometry",
        "parents",
        "door_srfs",
        "name",
        "connect",
        "door_meshes",
        "door_names",
    )

    def __init__(self):
        _Base.__init__(self)  # process the identifier
        self.door_srfs = []
        self.parents = []
        self.connect = ""
        self.door_meshes = []
        self.door_names = ""
        self.rooms = []
        self.name = "_doors_"

    @property
    def geometry(self):
        return self.geometry

    @geometry.setter
    def geometry(self, value):
        if self.is_solid(value):
            self.geometry = value
        else:
            print_time("geo is not solid")

    def is_solid(self, brep):
        if not isinstance(brep, rg.Brep):
            raise ValueError("Input must be solid")
        else:
            return True

    def add_door_srfs(self, rooms):
        rooms = item_to_list(rooms)
        room_blocks = [i.geometry for i in rooms]
        name = "_doors_"
        # print (self.display_name)
        # door_srfs = inter_brep(room_blocks, self.geometry, name)
        # if door_srfs:
        #    self.door_srfs.append(door_srfs)

    @classmethod
    def from_blocks(self, blocks):
        blocks = item_to_list(blocks)
        doors = []
        for index, block in enumerate(blocks):
            if block is not None:
                door = BlueDoor()
                try:
                    door.geometry = block
                    doors.append(door)
                except:
                    pass
        return doors


class BlueModel(_Base):
    __slots__ = (
        "rooms",
        "doors",
        "windows",
        "inlets",
        "outlets",
        "sources",
    )

    def __init__(self):
        _Base.__init__(self)  # process the identifier
        self.rooms = []
        self.doors = []
        self.windows = None
        self.inlets = None
        self.outlets = None
        self.sources = None


class BlueRoom(_Base):
    """
    Args:
    identifier: Text string for a unique object ID. Must be < 100 characters and
        not contain any spaces or special characters.

    Properties:
        * identifier
        * display_name
        * geometry
        * wall
        * floor
        * roof
        * doors
        * windows
        * inlets
        * outlets
        * sources
        * fans
        * connects
    """

    # 限制实例的属性
    __slots__ = (
        "geometry",
        "wall",
        "roof",
        "floor",
        "doors",
        "windows",
        "inlets",
        "outlets",
        "sources",
        "fans",
        "connects",
        "blue_doors",
    )

    def __init__(self):
        _Base.__init__(self)  # process the identifier
        self.wall = []
        self.roof = []
        self.doors = []
        self.windows = []
        self.inlets = []
        self.outlets = []
        self.sources = []
        self.fans = []
        self.connects = []
        self.blue_doors = []

    @property
    def geometry(self):
        return self.geometry

    @geometry.setter
    def geometry(self, value):
        if self.is_solid(value):
            self.geometry = value

    @property
    def wall(self):
        return self.wall

    @wall.setter
    def wall(self, value):
        if self.is_mesh(value):
            self.wall = item_to_list(value)

    @property
    def roof(self):
        return self.roof

    @roof.setter
    def roof(self, value):
        if self.is_mesh(value):
            self.roof = item_to_list(value)

    @property
    def floor(self):
        return self.floor

    @floor.setter
    def floor(self, value):
        if self.is_mesh(value):
            self.floor = item_to_list(value)

    @property
    def doors(self):
        return self.doors

    @doors.setter
    def doors(self, value):
        if self.is_mesh(value):
            self.doors = item_to_list(value)

    @property
    def windows(self):
        return self.windows

    @windows.setter
    def windows(self, value):
        if self.is_mesh(value):
            self.windows = item_to_list(value)

    @property
    def inlets(self):
        return self.inlets

    @inlets.setter
    def inlets(self, value):
        if self.is_mesh(value):
            self.inlets = item_to_list(value)

    @property
    def outlets(self):
        return self.outlets

    @outlets.setter
    def outlets(self, value):
        if self.is_mesh(value):
            self.outlets = item_to_list(value)

    @property
    def sources(self):
        return self.sources

    @sources.setter
    def sources(self, value):
        if self.is_mesh(value):
            self.sources = item_to_list(value)

    @property
    def fans(self):
        return self.fans

    @fans.setter
    def fans(self, value):
        if self.is_mesh(value):
            self.fans = item_to_list(value)

    @property
    def connects(self):
        return self.connects

    @connects.setter
    def connects(self, value):
        if self.is_mesh(value):
            self.connects = item_to_list(value)

    def is_solid(self, brep):
        # print(rg.Brep.IsSolid(brep))
        if not isinstance(brep, rg.Brep):
            raise ValueError("Input must be solid")
        else:
            return True

    def is_mesh(self, mesh):
        if mesh is None:
            raise ValueError("Input must be something, got {}.", mesh)
        elif not isinstance(mesh, rg.Mesh):
            raise ValueError("Input must be a mesh, got {}.", type(mesh))
        else:
            return True

    def find_door(self, blue_doors):
        for blue_door in blue_doors:
            if blue_door is not None:
                print_time("Split doors")
                name = "_doors_"
                door_srfs = inter_brep(self.geometry, blue_door, name)
                self.doors += srf_on_door(door_srfs, blue_door)
                connects = split_brep(blue_door, door_srfs, "Connects")[0]

    @classmethod
    def from_blocks(self, blocks):
        blocks = item_to_list(blocks)
        rooms = []
        for index, block in enumerate(blocks):
            if block is not None:
                room = BlueRoom()
                try:
                    room.geometry = block
                    rooms.append(room)
                except:
                    pass
        return rooms
