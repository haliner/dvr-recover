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

"""This module provides support for split files"""

class FileReader(object):
    """Handle multiple input streams as one big file"""
    __slots__ = ('parts', 'current_file', 'file')

    def __init__(self, filenames):
        """Initialize FileReader"""
        self.parts = []
        for filename in filenames:
            if filename[0:3] == r'\\.':
                raise FileReaderError("Direct access to Windows devices files "
                                      "is not supported currently.")
            part = {'filename': filename,
                    'size': os.stat(filename).st_size}
            self.parts.append(part)
        self.current_file = None
        self.file = None


    def get_size(self):
        """Return the total size of all input streams"""
        size = 0
        for part in self.parts:
            size += part['size']
        return size


    def get_index(self, offset):
        """Return the index of the file where offset is located"""
        index = 0
        start = 0
        for part in self.parts:
            end = start + part['size']
            if ((offset >= start) and
                (offset < end)):
                return index
            start = end
            index += 1
        return None


    def get_offset(self, index):
        """Return the starting offset of a specified file part"""
        i = 0
        offset = 0
        for part in self.parts:
            if i < index:
                offset += part['size']
            else:
                break
            i += 1
        return offset


    def open(self, index):
        """Open input stream with the specified index"""
        self.close()
        if (index >= 0) and (index < len(self.parts)):
            self.file = open(self.parts[index]['filename'], 'rb')
            self.current_file = index
        else:
            raise FileReaderError("Index out of range!")


    def close(self):
        """Close current input stream"""
        if self.file is not None:
            self.file.close()
        self.current_file = None
        self.file = None


    def seek(self, offset):
        """Seek to offset (open correct file, seek, ...)"""
        index = self.get_index(offset)
        delta = offset - self.get_offset(index)
        if self.current_file is None:
            self.open(index)
        else:
            if self.current_file != index:
                self.open(index)
        self.file.seek(delta)


    def is_eof(self):
        """Return true if eof of current file part is reached"""
        return (self.file.tell() == self.parts[self.current_file]['size'])


    def next_file(self):
        """Open next input file"""
        if self.current_file + 1 < len(self.parts):
            self.open(self.current_file + 1)
        else:
            self.close()


    def read(self, size):
        """Read data from stream, automatically switch stream if necessary"""
        if self.file is None:
            raise FileReaderError("No files are open!")
        buf = self.file.read(size)
        delta = size - len(buf)
        if delta != 0:
            if self.is_eof():
                self.next_file()
                buf += self.read(delta)
            else:
                raise FileReaderError("Incomplete filled buffer without "
                                      "reaching end of file!")
        return buf
