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
#include <stdio.h>
#include <assert.h>
#include "endianness.h"
#include "mpeg.h"

int main(int argc, char ** argv)
{
	init_endianness();

	const char buffer1[9] =
		{0x00, 0x00, 0x01, 0xBA,
		 0x44, 0x06, 0x75, 0xFA, 0x9C};

	const char buffer2[9] =
		{0x00, 0x00, 0x01, 0xBA,
		 0x65, 0xC6, 0x04, 0x2F, 0x84};

	mpeg_time * stamp1 = mpeg_timestamp_extract(buffer1);
	mpeg_time * stamp2 = mpeg_timestamp_extract(buffer2);
	mpeg_time * diff1 = mpeg_timestamp_diff(stamp1, stamp2);
	mpeg_time * diff2 = mpeg_timestamp_diff(stamp2, stamp1);

	/*
	 * Check first timestamp.
	 */
	assert(stamp1[0] == 0x00);
	assert(stamp1[1] == 0x00);
	assert(stamp1[2] == 0x67);
	assert(stamp1[3] == 0x3F);
	assert(stamp1[4] == 0x53);

	/*
	 * Check second timestamp.
	 */
	assert(stamp2[0] == 0x01);
	assert(stamp2[1] == 0x1C);
	assert(stamp2[2] == 0x60);
	assert(stamp2[3] == 0x05);
	assert(stamp2[4] == 0xF0);

	/*
	 * Check comparision.
	 */
	assert(mpeg_timestamp_cmp(stamp1, stamp1) == 0);
	assert(mpeg_timestamp_cmp(stamp2, stamp2) == 0);
	assert(mpeg_timestamp_cmp(stamp1, stamp2) < 0);
	assert(mpeg_timestamp_cmp(stamp2, stamp1) > 0);

	/*
	 * Check differences.
	 */
	assert(mpeg_timestamp_cmp(diff1, diff2) == 0);
	assert(diff1[0] == 0x01);
	assert(diff1[1] == 0x1B);
	assert(diff1[2] == 0xF8);
	assert(diff1[3] == 0xC6);
	assert(diff1[4] == 0x9D);

	/*
	 * Check creation of timestamps from int.
	 */
	mpeg_time * stamp1_ = mpeg_timestamp_from_int((unsigned int)6766419);
	/* Values to large for 4-byte int. Set the the most significant byte
	   separately. */
	mpeg_time * stamp2_ = mpeg_timestamp_from_int((unsigned int)476055024);
	mpeg_time * diff1_ = mpeg_timestamp_from_int((unsigned int)469288605);
	stamp2_[0] = 1;
	diff1_[0] = 1;

	assert(mpeg_timestamp_cmp(stamp1, stamp1_) == 0);
	assert(mpeg_timestamp_cmp(stamp2, stamp2_) == 0);
	assert(mpeg_timestamp_cmp(diff1, diff1_) == 0);

	mpeg_timestamp_destroy(stamp1_);
	mpeg_timestamp_destroy(stamp2_);
	mpeg_timestamp_destroy(diff1_);

	mpeg_timestamp_destroy(stamp1);
	mpeg_timestamp_destroy(stamp2);
	mpeg_timestamp_destroy(diff1);
	mpeg_timestamp_destroy(diff2);



	stamp1 = mpeg_timestamp_from_int(117453876); /* 07 00 34 34 */
	stamp2 = mpeg_timestamp_from_int(83921032);  /* 05 00 88 88 */
	diff1 = mpeg_timestamp_from_int(33532844);   /* 01 FF AB AC */
	diff2 = mpeg_timestamp_diff(stamp1, stamp2);
	assert(mpeg_timestamp_cmp(diff1, diff2) == 0);

	mpeg_timestamp_destroy(stamp1);
	mpeg_timestamp_destroy(stamp2);
	mpeg_timestamp_destroy(diff1);
	mpeg_timestamp_destroy(diff2);

	return 0;
}
