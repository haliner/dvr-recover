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

"""This module contains a commandline interface for dvr-recover."""


import sys

from dvrrecover.core import DvrRecover


class CmdInterface(object):
    """Commandline interface for dvr-recover."""

    def __init__(self):
        self.core = DvrRecover()


    def create(self):
        self.core.create


    def sort(self):
        self.core.sort()


    def reset(self):
        self.core.reset()


    def clear(self):
        self.core.clear()


    def show(self):
        self.core.show()


    def export(self):
        self.core.export()


    def setup(self):
        pass


    def usage(self):
        pass


    def run(self, argv=None):
        """Main function, runs the the commandline processor."""
        try:
            if argv is None:
                self.argv = sys.argv[1:]
            else:
                self.argv = argv

            if len(self.argv) > 0:
                arg = self.argv[0]
            else:
                arg = None

            if arg in ('create', 'sort', 'reset', 'clear', 'show', 'export',
                       'setup'):
                func = getattr(self, arg)
                func()
            else:
                self.usage()
        except KeyboardInterrupt:
            print "\nKeyboardInterrupt"
