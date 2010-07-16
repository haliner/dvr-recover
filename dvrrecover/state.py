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


current_block = 'current_block'
block_start   = 'block_start'
clock_start   = 'clock_start'
old_clock     = 'old_clock'
time_elapsed  = 'time_elapsed'


class UnknownStateError(DvrRecoverError):
    """Invalid state item specified"""
    pass



class StateManager(object):
    """Manage state info for analyze"""
    __slots__ = ()


    def is_valid_key(self, key):
        """Return true if key is valid"""
        return key in (current_block,
                       block_start,
                       clock_start,
                       old_clock,
                       time_elapsed)


    def get(self, key):
        """Return value of state specified by key"""
        if not self.is_valid_key(key):
            raise UnknownStateError("No valid state key: %s" %
                                        key)
        return self.db.state_query(key)


    def set(self, key, value):
        """Change state and update database"""
        if not self.is_valid_key(key):
            raise UnknownStateError("No valid state key: %s" %
                                        key)
        self.db.state_insert(key, value)
