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


input_filenames = 'input_filenames'
blocksize       = 'blocksize'
export_dir      = 'export_dir'
min_chunk_size  = 'min_chunk_size'
max_create_gap  = 'max_create_gap'
max_sort_gap    = 'max_sort_gap'


class UnknownConfigError(DvrRecoverError):
    """Invalid configuration item specified"""
    pass



class ConfigManager(object):
    """Manage program configuration"""
    __slots__ = ()


    defaults = {input_filenames: None,
                blocksize: 2048,
                export_dir: None,
                min_chunk_size: 2560,
                max_create_gap: 90000,
                max_sort_gap: 90000}


    def encode(self, key, value):
        """Prepare value for storage in database"""
        if value is None:
            return value
        elif key == input_filenames:
            if len(value) > 0:
                return buffer('\0'.join(value))
            else:
                return None
        else:
            return value


    def decode(self, key, value):
        """Convert value from database to a Python equivalent"""
        if key == input_filenames:
            if value is None:
                return []
            else:
                return str(value).split('\0')
        else:
            return value


    def is_valid_key(self, key):
        """Return true if key is valid"""
        return key in (input_filenames,
                       blocksize,
                       export_dir,
                       min_chunk_size,
                       max_create_gap,
                       max_sort_gap)


    def get(self, key):
        """Return value of config specified by key"""
        if not self.is_valid_key(key):
            raise UnknownConfigError("No valid configuration key: %s" %
                                        key)
        value = instances.db.setting_query(key)
        if value is None:
            value = self.defaults[key]
        return self.decode(key, value)


    def set(self, key, value):
        """Change setting and update database"""
        if not self.is_valid_key(key):
            raise UnknownConfigError("No valid configuration key: %s" %
                                        key)
        instances.db.setting_insert(key, self.encode(key, value))


    def reset(self):
        """Reset everything"""
        instances.db.setting_reset()
