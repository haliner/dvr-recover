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

import sqlite3


"""This module contains functionality for handling database connections."""


class DatabaseManager(object):
    """Interface to access data via SQL queries"""
    __slots__ = ('conn',)

    def __init__(self):
        """Initialize SqlManager"""
        self.conn = None


    def open(self, filename):
        """Open Sqlite3 database"""
        self.conn = sqlite3.connect(filename)
        self.init_db()


    def close(self, commit=True):
        """Close database connection after optional commit"""
        if commit:
            self.commit()
        self.conn.close()


    def commit(self):
        """Commit all changes"""
        self.conn.commit()


    def init_db(self):
        """Create structure of database"""
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS chunk("
                "id INTEGER PRIMARY KEY,"
                "block_start INTEGER,"
                "block_size INTEGER,"
                "clock_start INTEGER,"
                "clock_end INTEGER,"
                "concat INTEGER"
            ")")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS state("
                "key TEXT PRIMARY KEY ON CONFLICT REPLACE,"
                "value"
            ")")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS setting("
                "key TEXT PRIMARY KEY ON CONFLICT REPLACE,"
                "value"
            ")")


    def chunk_count(self):
        """Return count of rows in chunk table"""
        return self.conn.execute("SELECT COUNT(*) FROM chunk").fetchone()[0]


    def chunk_load(self, chunk_id):
        """Return chunk object by chunk_id"""
        result = self.conn.execute(
            "SELECT * FROM chunk "
            "WHERE id = ?",
            (chunk_id,)).fetchone()
        if result is None:
            return None
        chunk = Chunk(False)
        (chunk.id,
         chunk.block_start,
         chunk.block_size,
         chunk.clock_start,
         chunk.clock_end,
         chunk.concat) = result
        return chunk


    def chunk_save(self, chunk):
        """Insert or update info in chunk table"""
        if chunk.new:
            cur = self.conn.execute(
                "INSERT INTO chunk "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (chunk.id,
                 chunk.block_start,
                 chunk.block_size,
                 chunk.clock_start,
                 chunk.clock_end,
                 chunk.concat))

            chunk.id = cur.lastrowid
            chunk.new = False
        else:
            self.conn.execute(
                "UPDATE chunk "
                "SET block_start = ?,"
                    "block_size = ?,"
                    "clock_start = ?,"
                    "clock_end = ?,"
                    "concat = ? "
                "WHERE id = ?",
                (chunk.block_start,
                 chunk.block_size,
                 chunk.clock_start,
                 chunk.clock_end,
                 chunk.concat,
                 chunk.id))


    def chunk_delete_id(self, chunk_id):
        """Delete row from chunk table by id"""
        self.conn.execute("DELETE FROM chunk WHERE id = ?",
                          (chunk_id,))


    def chunk_delete(self, chunk):
        """Delete row from chunk table by chunk object"""
        self.chunk_delete_id(chunk.id)


    def chunk_reset(self):
        """Delete all rows from chunk table"""
        self.conn.execute("DELETE FROM chunk")


    def chunk_reset_concat(self):
        """Set concat to null for all rows in chunk table"""
        self.conn.execute(
            "UPDATE chunk "
            "SET concat = null")


    def chunk_query_ids(self):
        """Return iterator for all chunk ids"""
        for result in self.conn.execute(
            "SELECT id FROM chunk "
            "ORDER BY clock_start"):
            yield result[0]


    def chunk_query(self):
        """Return iterator for all chunk objects"""
        for chunk_id in self.chunk_query_ids():
            yield self.chunk_load(chunk_id)


    def chunk_query_concat(self, chunk):
        """Return chunk which should be concatenated to the current one"""
        cur = self.conn.execute(
            "SELECT id FROM chunk "
            "WHERE concat = ?",
            (chunk.id,))
        result = cur.fetchone()
        if result is None:
            return None
        if cur.fetchone() is not None:
            raise SqlManagerError("Multiple chunks are referencing the same "
                                  "chunk for concatenating!")
        return self.chunk_load(result[0])


    def chunk_fix_multiple_concats(self):
        """Fix multiple chunks referencing the same chunk in concat field"""
        self.conn.execute(
            "UPDATE chunk "
            "SET concat = null "
            "WHERE id IN "
             "("
              "SELECT a.id FROM chunk a "
              "INNER JOIN chunk b ON a.id != b.id AND a.concat = b.concat"
             ")")


    def state_reset(self):
        """Delete all entries of state table"""
        self.conn.execute("DELETE FROM state")


    def state_query(self, key):
        """Return value of state by key"""
        result = self.conn.execute(
            "SELECT value FROM state "
            "WHERE key = ?",
            (key,)).fetchone()
        if result is None:
            return None
        return result[0]


    def state_delete(self, key):
        """Delete entry in state table by key"""
        self.conn.execute(
            "DELETE from state "
            "WHERE key = ?",
            (key,))


    def state_insert(self, key, value):
        """Insert key/value pair into state table"""
        self.conn.execute(
            "INSERT INTO state "
            "VALUES (?, ?)",
            (key, value))


    def setting_reset(self):
        """Delete all entries of setting table"""
        self.conn.execute("DELETE FROM setting")


    def setting_query(self, key):
        """Return value of setting by key"""
        result = self.conn.execute(
            "SELECT value FROM setting "
            "WHERE key = ?",
            (key,)).fetchone()
        if result is None:
            return None
        return result[0]


    def setting_delete(self, key):
        """Delete entry in setting table by key"""
        self.conn.execute(
            "DELETE from setting "
            "WHERE key = ?",
            (key,))


    def setting_insert(self, key, value):
        """Insert key/value pair into setting table"""
        self.conn.execute(
            "INSERT INTO setting "
            "VALUES (?, ?)",
            (key, value))