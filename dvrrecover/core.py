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
from dvrrecover import config
from dvrrecover.chunkfactory import ChunkFactory
from dvrrecover.config import ConfigManager
from dvrrecover.database import DatabaseManager
from dvrrecover.filereader import FileReader


class DvrRecover(object):
    """Core class"""
    __slots__ = ('config',)

    def __init__(self):
        """Initialize DvrRecover"""
        instances.core = self
        instances.db = DatabaseManager()
        instances.config = ConfigManager()


    def initialize(self):
        """Initialization -- must be undone with finalize()"""
        instances.db.open('dvr-recover.sqlite')


    def finalize(self):
        """Deinitialization"""
        instances.db.close()


    def create(self):
        """Analyze input files and insert chunk list into database"""
        reader = FileReader(instances.config.get(config.input_filenames))
        cf = ChunkFactory(reader)
        cf.run()
        reader.close()


    def sort(self):
        """Sort chunks and try to concatenate parts of the same recording"""
        pass


    def reset(self):
        """Reset concat attribute of every chunk"""
        instances.db.chunk_reset_concat()


    def clear(self):
        """Delete all chunks and reset state table"""
        instances.db.chunk_reset()
        instances.db.state_reset()
