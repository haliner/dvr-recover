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


#include <stdlib.h>
#include <string.h>
#include "endianness.h"
#include "mpeg.h"


/******************************************************************************
 * general
 ******************************************************************************/

char mpeg_is_valid(const char * buffer)
{
	/*
	 * Check magic bytes
	 */
	if (memcmp(buffer, "\x00\x00\x01\xBA", 4) != 0) {
		return 0;
	}

	/*
	 * Check marker bits
	 */
	if ((((buffer[4] >> 6) & 3) != 1) ||
	    (((buffer[4] >> 2) & 1) != 1) ||
	    (((buffer[6] >> 2) & 1) != 1) ||
	    (((buffer[8] >> 2) & 1) != 1)) {
		return 0;
	}

	/*
	 * All checks passend -- probably valid mpeg header
	 */
	return 1;
}


/******************************************************************************
 * mpeg_fragment
 ******************************************************************************/

struct mpeg_fragment * mpeg_fragment_create()
{
	/* TODO: Check return value */
	/* TODO: Errno */
	struct mpeg_fragment * fragment = malloc(sizeof(struct mpeg_fragment));
	fragment->block_start = 0;
	fragment->block_size  = 0;
	fragment->time_start  = NULL;
	fragment->time_end    = NULL;
	return fragment;
}


void mpeg_fragment_destroy(struct mpeg_fragment * fragment)
{
	mpeg_timestamp_destroy(fragment->time_start);
	mpeg_timestamp_destroy(fragment->time_end);
	free(fragment);
}


/******************************************************************************
 * mpeg_time
 ******************************************************************************/

mpeg_time * mpeg_timestamp_create()
{
	/* TODO: Check result value */
	/* TODO: Errno */
	mpeg_time * result = malloc(5 * sizeof(char));
	memset(result, 0x00, 5 * sizeof(char));
	return result;
}


void mpeg_timestamp_destroy(mpeg_time * t)
{
	free(t);
}


mpeg_time * mpeg_timestamp_copy(mpeg_time * t)
{
	/* TODO: Check return value */
	mpeg_time * result = mpeg_timestamp_create();
	memcpy(result, t, 5);
	return result;
}


mpeg_time * mpeg_timestamp_from_int(unsigned int value)
{
	/*
	 * BUG: Only copies 4 bytes, but no huge problem, because on LP64 platform
	 * the width of int are also 4 bytes.
	 */
	mpeg_time * time = mpeg_timestamp_create();
	unsigned char * p = (unsigned char *) &value;

	unsigned int i;
	for (i = 1; i < 5; i++)
		time[i] = p[little_endian ? 4 - i : i - 1];

	return time;
}


mpeg_time * mpeg_timestamp_extract(const char * buffer)
{
	if (! mpeg_is_valid(buffer)) {
		return NULL;
	}

	/*
	 * This constant arrays contains the location of all bits.
	 * locations[0] -- least significant bit
	 */
	const mpeg_time locations[33][2] = {
		{8, 3}, {8, 4}, {8, 5}, {8, 6}, {8, 7},
		{7, 0}, {7, 1}, {7, 2}, {7, 3}, {7, 4}, {7, 5}, {7, 6}, {7, 7},
		{6, 0}, {6, 1}, {6, 3}, {6, 4}, {6, 5}, {6, 6}, {6, 7},
		{5, 0}, {5, 1}, {5, 2}, {5, 3}, {5, 4}, {5, 5}, {5, 6}, {5, 7},
		{4, 0}, {4, 1}, {4, 3}, {4, 4}, {4, 5}
	};

	mpeg_time * result = mpeg_timestamp_create();

	/*
	 * Transform single bits to 5 bytes in Big-Endian format. (Only one bit
	 * is used in the most significant byte, because a mpeg timestamp uses
	 * exactly 33 bits.)
	 */
	unsigned int i;
	for (i = 0; i < 33; i++) {
		result[4-i/8] +=
			((buffer[locations[i][0]] >> locations[i][1]) & 1) << (i%8);
	}
	
	return result;
}


mpeg_time * mpeg_timestamp_diff(const mpeg_time * t1, const mpeg_time * t2)
{
	/*
	 * Which timestamp is the bigger one? We subtract the smaller from
	 * the bigger one.
	 */
	const mpeg_time * big, * small;
	if (mpeg_timestamp_cmp(t1, t2) > 0) {
		big = t1;
		small = t2;
	} else {
		big = t2;
		small = t1;
	}

	mpeg_time * result = mpeg_timestamp_create();

	int i;
	for (i = 4; i >= 0; i--) {
		/*
		 * Calculate the difference of each positions separately.
		 */
		result[i] += big[i] - small[i];
		if (big[i] < small[i]) {
			/*
			 * If the difference is negative, decrement the next position
			 * (the one with the higher significance). We use unsigned
			 * chars, so for a negative difference a arithmetic overflow
			 * occurs -- exactly what's needed.
			 *
			 * If the next position in big contains 0, the decrementation
			 * will overflow, too. For a correct result, we must decrement
			 * the next position again and so on.
			 */
			int j;
			for (j = i-1; j >= 0; j--) {
				result[j]--;
				if (big[j] != 0)
					break;
			}
		}
	}

	return result;
}


char mpeg_timestamp_cmp(const mpeg_time * t1, const mpeg_time * t2)
{
	return memcmp(t1, t2, 5);
}
