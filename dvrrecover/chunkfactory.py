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
from dvrrecover import chunk
from dvrrecover import config
from dvrrecover import state
from dvrrecover.chunk import Chunk
from dvrrecover.exception import DvrRecoverError
from dvrrecover.state import StateManager
from dvrrecover.utils import Timer


class ChunkFactoryError(DvrRecoverError):
    """ChunkFactoryError"""
    pass


class ChunkFactory(object):
    """Extract information about all chunks"""
    __slots__ = ('reader', 'timer', 'blocksize', 'max_gap', 'total_blocks',
                 'block_cur', 'clock_cur', 'clock_old', 'chunk', 'state')

    def __init__(self, reader):
        """Initialize ChunkFactory"""
        self.reader = reader
        self.timer = Timer()
        self.state = StateManager()

        self.chunk = None
        self.block_cur = None
        self.clock_cur = None
        self.clock_old = None

        self.blocksize = instances.config.get(config.blocksize)
        self.max_gap = instances.config.get(config.max_create_gap)

        self.total_blocks = int(self.reader.get_size() / self.blocksize)


    def save_state(self):
        """Save current state"""
        if self.chunk is None:
            block_start = None
            clock_start = None
        else:
            block_start = self.chunk.get(chunk.block_start)
            clock_start = self.chunk.get(chunk.clock_start)

        self.state.set(state.block_cur, self.block_cur)
        self.state.set(state.block_start, block_start)
        self.state.set(state.clock_start, clock_start)
        self.state.set(state.clock_old, self.clock_old)
        instances.db.commit()


    def load_state(self):
        """Load state"""
        block_cur = self.state.get(state.block_cur)
        block_start = self.state.get(state.block_start)
        clock_start = self.state.get(state.clock_start)
        clock_old = self.state.get(state.clock_old)

        self.block_cur = block_cur
        if (block_start is not None) and (clock_start is not None):
            self.chunk = Chunk()
            self.chunk.set(chunk.block_start, block_start)
            self.chunk.set(chunk.clock_start, clock_start)
        self.clock_old = clock_old


    def check_timer(self):
        """Save state every 30 seconds"""
        if self.timer.elapsed() > 30:
            self.save_state()
            self.timer.reset()


    def finished(self):
        """Reset state and commit changes"""
        self.state.reset()
        instances.db.commit()


    def mpeg_header(self, buf):
        """Check if buffer is mpeg header and return system clock_cur or None"""
        #            Partial Program Stream Pack header format
        #            =========================================
        #
        # Name                  |Number of bits| Description
        # ----------------------|--------------|----------------------------
        # sync bytes            | 32           | 0x000001BA
        # marker bits           | 2            | 01b
        # System clock_cur [32..30] | 3            | System Clock Reference
        #                       |              | (SCR) bits 32 to 30
        # marker bit            | 1            | Bit always set.
        # System clock_cur [29..15] | 15           | System clock_cur bits 29 to 15
        # marker bit            | 1            | Bit always set.
        # System clock_cur [14..0]  | 15           | System clock_cur bits 14 to 0
        # marker bit            | 1            | 1 Bit always set.
        #
        #
        #    [4]     [5]      [6]      [7]      [8]      = buffer[x]
        # 01000100|00000000|00000100|00000000|00000100   = marker bits
        #   ^^^ ^^ ^^^^^^^^ ^^^^^ ^^ ^^^^^^^^ ^^^^^      = SCR
        #
        # SCR -> 90 kHz Timer
        #
        # See http://en.wikipedia.org/wiki/MPEG_program_stream#Coding_structure
        if ((ord(buf[0]) != 0x00) or
            (ord(buf[1]) != 0x00) or
            (ord(buf[2]) != 0x01) or
            (ord(buf[3]) != 0xBA)):
            return None

        if (((ord(buf[4]) >> 6) & 3 != 1) or
            ((ord(buf[4]) >> 2) & 1 != 1) or
            ((ord(buf[6]) >> 2) & 1 != 1) or
            ((ord(buf[8]) >> 2) & 1 != 1)):
            return None

        clock_cur = 0
        i = 0
        for tup in ( tuple((0, i) for i in range(3, 8)) +
                     tuple((1, i) for i in range(0, 8)) +
                     tuple((2, i) for i in range(0, 2) + range(3, 8)) +
                     tuple((3, i) for i in range(0, 8)) +
                     tuple((4, i) for i in range(0, 2) + range(3, 5)) ):
            clock_cur += ((ord(buf[8 - tup[0]]) >> tup[1]) & 1) * 2**i
            i += 1
        return clock_cur


    def new_chunk(self):
        """Begin new chunk"""
        if self.chunk is not None:
            self.end_chunk(self)
        self.chunk = Chunk()
        self.chunk.set(chunk.block_start,
                       self.block_cur)
        self.chunk.set(chunk.clock_start,
                       self.clock_cur)


    def end_chunk(self):
        """End current chunk"""
        if self.chunk is not None:
            self.chunk.set(chunk.block_size,
                           self.block_cur - 1 -
                               self.chunk.get(chunk.block_start))
            self.chunk.set(chunk.clock_end,
                           self.clock_old)
            self.chunk.save()
            self.chunk = None


    def run(self):
        """Main function for this class"""
        self.load_state()
        if self.block_cur is None:
            if instances.db.chunk_count() != 0:
                raise ChunkFactoryError(
                          "No state information, but chunk count is not 0. "
                          "Probably the scan finished already. Abort process "
                          "to avoid loss of data. Use parameter clear to clear "
                          "database (you will lose all chunk information)."
                          )
            self.block_cur = 0
        self.state.reset()
        self.reader.seek(self.block_cur * self.blocksize)
        for self.block_cur in xrange(self.block_cur,
                                         self.total_blocks):
            self.check_timer()
            buf = self.reader.read(self.blocksize)
            if len(buf) != self.blocksize:
                raise ChunkFactoryError("len(buf) != self.blocksize")
            self.clock_cur = self.mpeg_header(buf)
            if self.clock_cur is None:
                self.end_chunk()
            else:
                if self.chunk is None:
                    self.new_chunk()
                else:
                    delta = self.clock_cur - self.clock_old
                    if (delta < 0) or (delta > self.max_gap):
                        self.end_chunk()
                self.clock_old = self.clock_cur
        self.end_chunk()
        self.finished()
