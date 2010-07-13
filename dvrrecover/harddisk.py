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


class ChunkFactory(object):
    """Extract information of all chunks"""
    __slots__ = ('current_block', 'clock', 'old_clock', 'timer', 'timer_all',
                 'timer_blocks', 'blocksize', 'min_chunk_size', 'max_gap',
                 'db_manager', 'reader', 'input_blocks', 'chunk')

    def __init__(self, main, reader):
        self.current_block = 0
        self.clock = 0
        self.old_clock = 0
        self.chunk = None
        self.timer = Timer()
        self.timer_all = Timer()
        self.timer_blocks = 0

        self.blocksize = main.blocksize
        self.min_chunk_size = main.min_chunk_size
        self.max_gap = main.max_create_gap
        self.db_manager = main.db_manager

        self.reader = reader
        self.input_blocks = int(self.reader.get_size() / self.blocksize)


    def save_state(self):
        if self.chunk is None:
            block_start = None
            clock_start = None
        else:
            block_start = self.chunk.block_start
            clock_start = self.chunk.clock_start
        self.db_manager.state_insert(
            'current_block',
            self.current_block)
        self.db_manager.state_insert(
            'block_start',
            block_start)
        self.db_manager.state_insert(
            'clock_start',
            clock_start)
        self.db_manager.state_insert(
            'old_clock',
            self.old_clock)
        self.db_manager.state_insert(
            'time_elapsed',
            self.timer_all.elapsed())
        self.db_manager.commit()


    def load_state(self):
        current_block = self.db_manager.state_query('current_block')
        block_start = self.db_manager.state_query('block_start')
        clock_start = self.db_manager.state_query('clock_start')
        old_clock = self.db_manager.state_query('old_clock')
        time_elapsed = self.db_manager.state_query('time_elapsed')

        self.current_block = current_block
        if (block_start is not None) and (clock_start is not None):
            self.chunk = Chunk()
            self.chunk.block_start = block_start
            self.chunk.clock_start = clock_start
        self.old_clock = old_clock
        if time_elapsed is not None:
            self.timer_all.timecode -= time_elapsed


    def check_timer(self):
        """Print statistics and save state if timer elapses"""
        delta = self.timer.elapsed()
        if delta > 30:
            self.timer.reset()

            self.save_state()

            chunk_count = self.db_manager.chunk_count()
            speed = float(self.current_block - self.timer_blocks) \
                        / float(delta)
            print "[%5.1f%%] %i/%i blocks (%.1f bl/s; " \
                  "%.1f MiB/s): %i chunks" % \
                  (
                    float(self.current_block) /
                        float(self.input_blocks) * 100.0,
                    self.current_block,
                    self.input_blocks,
                    speed,
                    float(speed * self.blocksize) / float(1024**2),
                    chunk_count
                  )
            self.timer_blocks = self.current_block


    def finished(self):
        """Print statistics and commit changes after finishing"""
        self.db_manager.state_reset()
        self.db_manager.commit()

        delta = self.timer_all.elapsed()
        chunk_count = self.db_manager.chunk_count()
        speed = float(self.current_block + 1) / float(delta)
        print
        print "Finished."
        print "Read %i of %i blocks." % (self.current_block + 1,
                                         self.input_blocks)
        print "Found %i chunks." % chunk_count
        print "Took %.2f seconds." % delta
        print "Average speed was %.1f blocks/s (%.1f MiB/s)." % \
              (speed, float(speed * self.blocksize) / float(1024**2))


    def mpeg_header(self, buf):
        """Check if buffer is mpeg header and return system clock or None"""
        #            Partial Program Stream Pack header format
        #            =========================================
        #
        # Name                  |Number of bits| Description
        # ----------------------|--------------|----------------------------
        # sync bytes            | 32           | 0x000001BA
        # marker bits           | 2            | 01b
        # System clock [32..30] | 3            | System Clock Reference
        #                       |              | (SCR) bits 32 to 30
        # marker bit            | 1            | Bit always set.
        # System clock [29..15] | 15           | System clock bits 29 to 15
        # marker bit            | 1            | Bit always set.
        # System clock [14..0]  | 15           | System clock bits 14 to 0
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

        marker_bit_1 = ord(buf[4] >> 6) & 3
        marker_bit_2 = ord(buf[4] >> 2) & 1
        marker_bit_3 = ord(buf[6] >> 2) & 1
        marker_bit_4 = ord(buf[8] >> 2) & 1

        if ((marker_bit_1 != 1) or
            (marker_bit_2 != 1) or
            (marker_bit_3 != 1) or
            (marker_bit_4 != 1)):
            return None

        clock_bits = [None] * 33

        clock_bits[32] = ord(buf[4] >> 5) & 1;
        clock_bits[31] = ord(buf[4] >> 4) & 1;
        clock_bits[30] = ord(buf[4] >> 3) & 1;
        clock_bits[29] = ord(buf[4] >> 1) & 1;
        clock_bits[28] = ord(buf[4] >> 0) & 1;
        clock_bits[27] = ord(buf[5] >> 7) & 1;
        clock_bits[26] = ord(buf[5] >> 6) & 1;
        clock_bits[25] = ord(buf[5] >> 5) & 1;
        clock_bits[24] = ord(buf[5] >> 4) & 1;
        clock_bits[23] = ord(buf[5] >> 3) & 1;
        clock_bits[22] = ord(buf[5] >> 2) & 1;
        clock_bits[21] = ord(buf[5] >> 1) & 1;
        clock_bits[20] = ord(buf[5] >> 0) & 1;
        clock_bits[19] = ord(buf[6] >> 7) & 1;
        clock_bits[18] = ord(buf[6] >> 6) & 1;
        clock_bits[17] = ord(buf[6] >> 5) & 1;
        clock_bits[16] = ord(buf[6] >> 4) & 1;
        clock_bits[15] = ord(buf[6] >> 3) & 1;
        clock_bits[14] = ord(buf[6] >> 1) & 1;
        clock_bits[13] = ord(buf[6] >> 0) & 1;
        clock_bits[12] = ord(buf[7] >> 7) & 1;
        clock_bits[11] = ord(buf[7] >> 6) & 1;
        clock_bits[10] = ord(buf[7] >> 5) & 1;
        clock_bits[ 9] = ord(buf[7] >> 4) & 1;
        clock_bits[ 8] = ord(buf[7] >> 3) & 1;
        clock_bits[ 7] = ord(buf[7] >> 2) & 1;
        clock_bits[ 6] = ord(buf[7] >> 1) & 1;
        clock_bits[ 5] = ord(buf[7] >> 0) & 1;
        clock_bits[ 4] = ord(buf[8] >> 7) & 1;
        clock_bits[ 3] = ord(buf[8] >> 6) & 1;
        clock_bits[ 2] = ord(buf[8] >> 5) & 1;
        clock_bits[ 1] = ord(buf[8] >> 4) & 1;
        clock_bits[ 0] = ord(buf[8] >> 3) & 1;

        clock = 0
        for i in range(0,33):
            clock += clock_bits[i] * 2**i
        return clock


    def split(self):
        """End current chunk and start a new one"""
        if self.chunk is not None:
            self.chunk.block_size = self.current_block - 1 - \
                                    self.chunk.block_start
            self.chunk.clock_end = self.old_clock

            if (self.chunk.block_size >= self.min_chunk_size):
                self.db_manager.chunk_save(self.chunk)
            self.chunk = None


    def run(self):
        """Main function for this class"""
        self.load_state()
        if self.current_block is None:
            if self.db_manager.chunk_count() != 0:
                raise CreateError("No state information, but chunk "
                                  "count is not 0. Probably the scan "
                                  "finished already. Abort process to "
                                  "avoid loss of data. Use parameter "
                                  "clear to clear database (you will "
                                  "lose all chunk information).")
            self.current_block = 0
        self.db_manager.state_reset()
        self.timer_blocks = self.current_block
        self.reader.seek(self.current_block * self.blocksize)
        for self.current_block in xrange(self.current_block,
                                         self.input_blocks):
            self.check_timer()
            buf = self.reader.read(self.blocksize)
            if len(buf) != self.blocksize:
                raise UnexpectedResultError("len(buf) != "
                                            "self.blocksize")
            self.clock = self.mpeg_header(buf)
            if self.clock is None:
                self.split()
            else:
                if self.chunk is None:
                    self.chunk = Chunk()
                    self.chunk.block_start = self.current_block
                    self.chunk.clock_start = self.clock
                else:
                    delta = self.clock - self.old_clock
                    if (delta < 0) or (delta > self.max_gap):
                        self.split()
                self.old_clock = self.clock
        self.split()
        self.finished()
