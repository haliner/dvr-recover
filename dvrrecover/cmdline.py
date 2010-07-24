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


import sys

from dvrrecover import chunk
from dvrrecover import config
from dvrrecover import core
from dvrrecover import instances


class CmdInterface(object):
    """Commandline interface for dvr-recover."""
    __slots__ = ('argv', 'core')

    def __init__(self):
        """Initialize CmdInterface"""
        self.core = core.DvrRecover()


    def create(self):
        """Analyze input files"""
        self.core.create()


    def sort(self):
        pass


    def reset(self):
        pass


    def clear(self):
        pass


    def show(self):
        """Dump chunk list file in a human readable way"""
        header_lines = ''.join(['-'] * 5 + (['+'] + ['-'] * 14) * 5)
        header_captions = ''.join([' '] * 5 + ['| %12s '] * 5)[:-1] % \
                                ('Block Start',
                                 'Block Size',
                                 'Clock Start',
                                 'Clock End',
                                 'Concatenate')
        print header_lines
        print header_captions
        print header_lines

        def print_chunk(ch):
            fmt_str_list = []
            fmt_str_arg_list = []
            if ch.get(chunk.concat) is not None:
                fmt_str_list.append('%4s ')
                fmt_str_arg_list.append('#')
            else:
                fmt_str_list.append('%4i ')
                fmt_str_arg_list.append(index)
            fmt_str_list.extend(['| %12i '] * 4)
            fmt_str_list.extend(['| %10s'])
            fmt_str = ''.join(fmt_str_list)
            fmt_str_arg_list.extend([ch.get(chunk.block_start),
                                     ch.get(chunk.block_size),
                                     ch.get(chunk.clock_start),
                                     ch.get(chunk.clock_end),
                                     ch.get(chunk.concat) is not None])
            print fmt_str % tuple(fmt_str_arg_list)

        def process_concats(ch):
            ch2 = ch.get_concat()
            if ch2 is not None:
                print_chunk(ch2)
                process_concats(ch2)

        index = 1
        for chunk_id in instances.db.chunk_query_ids():
            ch = chunk.Chunk(chunk_id)
            if ch.get(chunk.concat) is not None:
                continue
            print_chunk(ch)
            process_concats(ch)
            index += 1


    def export(self):
        pass


    def setup(self):
        """Parse cmdline arguments and provide interface to configuration"""
        args = self.argv[1:]

        if len(args) == 0:
            args.append('show')

        if (args[0] == 'input') and (len(args) > 1):
            args[0:2] = (args[0] + ' '+ args[1],)

        parameters = {
                'show': 0,
                'reset': 0,
                'input': 1,
                'input add': 1,
                'input del': 1,
                'input clear': 0,
                config.blocksize: 1,
                config.min_export_size: 1,
                config.max_create_gap: 1,
                config.max_sort_gap: 1,
                config.export_dir: 1
            }

        if args[0] not in parameters:
            print "Unknown argument:", args[0]
            return

        if len(args) - 1 != parameters[args[0]]:
            print ("Invalid argument count -- parameter \"%s\" "
                   "expects %i argument(s).") % (args[0], parameters[args[0]])
            return

        if args[0] in (config.blocksize,
                       config.min_export_size,
                       config.max_create_gap,
                       config.max_sort_gap):
            instances.config.set(args[0], int(args[1]))
        elif args[0] == config.export_dir:
            instances.config.set(args[0], args[1])
        elif args[0] in 'input clear':
            instances.config.set(config.input_filenames, [])
        elif args[0] in ('input add', 'input del'):
            filenames = instances.config.get(config.input_filenames)
            if args[0] == 'input add':
                filenames.append(args[1])
            else:
                filenames.remove(args[1])
            instances.config.set(config.input_filenames, filenames)
        elif args[0] == 'show':
            filenames = instances.config.get(config.input_filenames)
            for filename in filenames:
                print "input_filename:", filename
            if len(filenames) == 0:
                print "No input files specified!"
            for key in (config.blocksize,
                        config.export_dir,
                        config.min_export_size,
                        config.max_create_gap,
                        config.max_sort_gap):
                print key + ":", instances.config.get(key)
        elif args[0] == 'reset':
            instances.config.reset()


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
                self.core.initialize()
                func = getattr(self, arg)
                func()
                self.core.finalize()
            else:
                self.usage()
        except KeyboardInterrupt:
            print "\nKeyboardInterrupt"
