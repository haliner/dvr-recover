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


from dvrrecover import instances
from dvrrecover.exception import DvrRecoverError


block_start = 'black_start'
block_size  = 'block_size'
clock_start = 'clock_start'
clock_end   = 'clock_end'
concat      = 'concat'


class UnknownChunkKeyError(DvrRecoverError):
    """Invalid chunk key specified"""
    pass



class Chunk(object):
    """Object to save information about one chunk"""
    __slots__ = ('id',)
    
    def __init__(self, id=None):
        """Initalize Chunk object"""
        self.id = id


    def is_valid_key(self, key):
        """Return true if key is valid"""
        return key in (block_start,
                       block_size,
                       clock_start,
                       clock_end,
                       concat)


    def get(self, key):
        """Return value of chunk info specified by key"""
        if not self.is_valid_key(key):
            raise UnknownChunkKeyError("No valid chunk key: %s" %
                                        key)
        return instances.db.chunk_query(key)


    def set(self, key, value):
        """Change chunk info and update database"""
        if not self.is_valid_key(key):
            raise UnknownChunkKeyError("No valid chunk key: %s" %
                                        key)
        instances.db.chunk_insert(key, value)
