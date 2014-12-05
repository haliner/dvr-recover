/*
 * Copyright (C) 2010  Stefan Haller <haliner@googlemail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


#ifndef __MPEG__H__
#define __MPEG__H__

/*
 * This file doesn't provide full access to the mpeg file structure, it
 * doesn't even provide access to all the header fields. Only rudimentary
 * checks and access to timestamps are implemented.
 *
 *
 ******************************************************************************
 *             Partial Program Stream Pack header format
 *            *******************************************
 * Name                      |Number of bits| Description
 * --------------------------|--------------|----------------------------
 * sync bytes                | 32           | 0x000001BA
 * marker bits               | 2            | 01b
 * System clock_cur [32..30] | 3            | System Clock Reference
 *                           |              | (SCR) bits 32 to 30
 * marker bit                | 1            | Bit always set.
 * System clock_cur [29..15] | 15           | System clock_cur bits 29 to 15
 * marker bit                | 1            | Bit always set.
 * System clock_cur [14..0]  | 15           | System clock_cur bits 14 to 0
 * marker bit                | 1            | 1 Bit always set.
 *
 *
 *    [4]     [5]      [6]      [7]      [8]      = buffer[x]
 * 01000100|00000000|00000100|00000000|00000100   = marker bits
 *   ^^^ ^^ ^^^^^^^^ ^^^^^ ^^ ^^^^^^^^ ^^^^^      = SCR
 *
 * SCR -> 90 kHz Timer
 *
 * See http://en.wikipedia.org/wiki/MPEG_program_stream#Coding_structure
 */


/*
 * Type for storage of a mpeg timestamp. We mainly use a pointer to this
 * type with 5 elements. 4 bytes can hold 32 bits, but a mpeg timestamp
 * consists of 33 bits, so we need 5 bytes.
 */
typedef unsigned char mpeg_time;


/*
 * Type that stores information about mpeg fragment.
 */
struct mpeg_fragment {
	unsigned int block_start;
	unsigned int block_size;
	mpeg_time * time_start;
	mpeg_time * time_end;
};



/******************************************************************************
 * general
 ******************************************************************************/

/*
 * Checks whether buffer contains a valid mpeg header.
 */
char mpeg_is_valid(const char * buffer);



/******************************************************************************
 * mpeg_fragment
 ******************************************************************************/

/*
 * Memory allocation and deallocation.
 */
struct mpeg_fragment * mpeg_fragment_create();
void mpeg_fragment_destroy(struct mpeg_fragment * fragment);



/******************************************************************************
 * mpeg_time
 ******************************************************************************/

/*
 * Memory allocation and deallocation.
 */
mpeg_time * mpeg_timestamp_create();
void mpeg_timestamp_destroy(mpeg_time * t);
mpeg_time * mpeg_timestamp_copy(mpeg_time * t);

/*
 * Create mpeg timestamp from unsigned integer.
 */
mpeg_time * mpeg_timestamp_from_int(unsigned int value);

/*
 * Extracts the timestamp out of a mpeg stream.
 */
mpeg_time * mpeg_timestamp_extract(const char * buffer);

/*
 * Calculates the difference between two timestamps.
 */
mpeg_time * mpeg_timestamp_diff(const mpeg_time * t1, const mpeg_time * t2);

/*
 * Compares two timestamps. Results are the same like for memcmp.
 */
char mpeg_timestamp_cmp(const mpeg_time * t1, const mpeg_time * t2);

#endif
