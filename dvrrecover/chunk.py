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


block_start = 'block_start'
block_size  = 'block_size'
clock_start = 'clock_start'
clock_end   = 'clock_end'
concat      = 'concat'


class UnknownChunkKeyError(DvrRecoverError):
    """Invalid chunk key specified"""

    def __init__(self, key):
        DvrRecoverError.__init__(self,
            "Invalid chunk key specified: %s" % key)


class ChunkAlreadyAssociatedError(DvrRecoverError):
    """Chunk is already associated with database row"""

    def __init__(self):
        DvrRecoverError.__init__(self,
            "Chunk is already associated with database row")



class Chunk(object):
    """Object to save information about one chunk"""
    __slots__ = ('id', 'cache')

    def __init__(self, id=None):
        """Initalize Chunk object"""
        self.id = id
        if not self.is_associated():
            self.cache = {}


    def is_associated(self):
        return self.id is not None


    def is_valid_key(self, key, throw=False):
        """Return true if key is valid"""
        value = key in (block_start,
                        block_size,
                        clock_start,
                        clock_end,
                        concat)
        if not value and throw:
            raise UnknownChunkKeyError(key)


    def get(self, key):
        """Return value of chunk info specified by key"""
        self.is_valid_key(key, True)
        if self.is_associated():
            return instances.db.chunk_query(self.id, key)
        else:
            return self.cache[key]


    def set(self, key, value):
        """Change chunk info and update database"""
        self.is_valid_key(key, True)
        if self.is_associated():
            instances.db.chunk_update(self.id, key, value)
        else:
            self.cache[key] = value


    def save(self):
        """Inserts chunk info into database"""
        if self.is_associated():
            raise ChunkAlreadyAssociatedError()
        self.id = instances.db.chunk_insert()
        for k, v in self.cache.iteritems():
            self.set(k, v)
        del self.cache
