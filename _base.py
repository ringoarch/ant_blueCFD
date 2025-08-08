#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@DATE: 2025-01-16 16:44:10
@Author: ringo
@Version: 0.1.0
@File: _base.py
@Software: vscode
@Description:
    1. 基础类
"""
from scriptcontext import sticky as st
from utility import print_time
import uuid
import rhinoscriptsyntax as rs


class _Base:
    """A base class for all geometry objects.

    Args:
        identifier: Text string for a unique object ID. Must be < 100 characters and
            not contain any spaces or special characters.

    Properties:
        * identifier
        * display_name
        * instances:

    """

    instances = []
    __slots__ = ("_identifier", "display_name")

    def __init__(self, display_name=None):
        """Initialize base object."""
        self._identifier = str(uuid.uuid4().int)[:6]
        self.__class__.instances.append(self)
        if display_name is None:
            self.display_name = self.identifier
        else:
            self.display_name = display_name

        # rc = rs.AddObjectToGroup(self, 'ant_objs')
        # print_time('Ant objs added to group {}'.format(str(rc)))

    @property
    def identifier(self):
        """Get or set a text string for the unique object identifier.

        This identifier remains constant as the object is mutated, copied, and
        serialized to different formats (eg. dict, idf, rad). As such, this
        property is used to reference the object across a Model.
        """
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value
        # self.identifier = valid_string(value, 'ant object identifier')

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def __copy__(self):
        new_obj = self.__class__(self.identifier)
        new_obj.display_name = self.display_name
        # new_obj._user_data = None if self.user_data is None else self.user_data.copy()
        return new_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "AT:{}".format(self.display_name)

    def __del__(self):
        try:
            rs.RemoveObjectFromGroup(self, "ant_objs")
            rs.SetDocumentUserText("id:{}".format(str(self.identifier)), None)
            st["AT_geometry"].remove(self)
            del self
        except:
            pass
        print_time("调用__del__() 销毁对象{}，释放其空间".format(self.display_name))

