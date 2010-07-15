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

input_filenames = 'input_filenames'
blocksize       = 'blocksize'
export_dir      = 'export_dir'
min_chunk_size  = 'min_chunk_size'
max_create_gap  = 'max_create_gap'
max_sort_gap    = 'max_sort_gap'


class ConfigManager(object):
    """Manage program configuration"""
    __slots__ = ('db', 'configs')


    defaults = {input_filenames: [],
                blocksize: 2048,
                export_dir: None,
                min_chunk_size: 2560,
                max_create_gap: 90000,
                max_sort_gap: 90000}


    def __init__(self, db):
        """Initialize ConfigManager"""
        self.db = db
        self.configs = {input_filenames: None,
                        blocksize: None,
                        export_dir: None,
                        min_chunk_size: None,
                        max_create_gap: None,
                        max_sort_gap: None}


    def encode(self, key):
        """Prepare value for storage in database"""
        value = self.configs[key]
        if value is None:
            return none
        elif key == input_filenames:
            return buffer('\0'.join(value))
        else:
            return value


    def decode(self, key, value):
        """Convert value from database to a Python equivalent"""
        if value is None:
            return None
        elif key == input_filenames:
            return str(value).split('\0')
        else:
            return value


    def load(self):
        """Load settings from database"""
        for key in self.configs.iterkeys():
            self.configs[key] = self.decode(key,
                                            self.db.setting_query(key))


    def get(self, key):
        """Return value of config specified by key"""
        value = self.configs[key]
        if value is None:
            value = self.defaults[key]
            if type(value) is list:
                value = [i for i in value]
        return value


    def set(self, key, value):
        """Change setting and update database"""
        self.configs[key] = value
        self.db.settings_insert(key, value)
