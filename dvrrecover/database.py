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

from dvrrecover.exception import DvrRecoverError


class SqlManagerError(DvrRecoverError):
    pass



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
            "CREATE TABLE IF NOT EXISTS config("
                "key TEXT PRIMARY KEY ON CONFLICT REPLACE,"
                "value"
            ")")


    def chunk_check_column(self, column):
        """Check if column is a valid column in chunk table"""
        if column not in ('id',
                          'block_start',
                          'block_size',
                          'clock_start',
                          'clock_end',
                          'concat'):
            raise SqlManagerError("No valid column in chunk table: %s" %
                                  column)


    def chunk_count(self):
        """Return count of rows in chunk table"""
        return self.conn.execute("SELECT COUNT(*) FROM chunk").fetchone()[0]


    def chunk_delete_id(self, chunk_id):
        """Delete row from chunk table by id"""
        self.conn.execute("DELETE FROM chunk WHERE id = ?",
                          (chunk_id,))


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


    def chunk_query(self, id, column):
        """Return value for column and chunk id"""
        self.chunk_check_column(column)
        result = self.conn.execute(
            "SELECT %s FROM chunk "
            "WHERE id=?" % column,
            (id,)).fetchone()
        if result is None:
            return None
        return result[0]


    def chunk_query_concat(self, chunk):
        """Return chunk id which should be concatenated to the current one"""
        result = self.conn.execute(
            "SELECT id FROM chunk "
            "WHERE concat = ?",
            (chunk.id,)).fetchone()
        if result is None:
            return None
        if cur.fetchone() is not None:
            raise SqlManagerError("Multiple chunks are referencing the same "
                                  "chunk for concatenating!")
        return result[0]


    def chunk_insert(self):
        """Insert row into chunk table and return id"""
        cur = self.conn.execute(
            "INSERT INTO chunk (id) "
            "VALUES (null)")
        return cur.lastrowid


    def chunk_update(self, id, column, value):
        """Update column in chunk table"""
        self.chunk_check_column(column)
        self.conn.execute(
            "UPDATE chunk "
            "SET %s = ? "
            "WHERE id = ?" % column,
            (value, id))


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


    def config_reset(self):
        """Delete all entries of config table"""
        self.conn.execute("DELETE FROM config")


    def config_query(self, key):
        """Return value of config by key"""
        result = self.conn.execute(
            "SELECT value FROM config "
            "WHERE key = ?",
            (key,)).fetchone()
        if result is None:
            return None
        return result[0]


    def config_delete(self, key):
        """Delete entry in config table by key"""
        self.conn.execute(
            "DELETE from config "
            "WHERE key = ?",
            (key,))


    def config_insert(self, key, value):
        """Insert key/value pair into config table"""
        self.conn.execute(
            "INSERT INTO config "
            "VALUES (?, ?)",
            (key, value))
