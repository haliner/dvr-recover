# -*- coding: utf-8 -*-
# This file is part of the dvr-recover project.
#
# Copyright (C) 2010 Stefan Haller <haliner@googlemail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Chunk(object):
    """Object to save information about one chunk"""
    __slots__ = ('id',
                 'block_start',
                 'block_size',
                 'clock_start',
                 'clock_end',
                 'concat',
                 'new')

    def __init__(self, new = True):
        for i in self.__slots__:
            setattr(self, i, None)
        self.new = new
