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
#include <string.h>
#include <assert.h>
#include "analysis.h"
#include "dllist.h"
#include "endianness.h"
#include "mpeg.h"

int main(int argc, char ** argv)
{
	init_endianness();

	const unsigned int blocksize = 2048;
	const unsigned int gapsize   = 90000;

	const unsigned int size = 50;
	const unsigned int timestamps[] = {
		/* 1st MPEG fragment  --  5 bytes */
		5000, 5100, 5300, 6000, 7000,

		/* gap  --  5 bytes*/
		0, 0, 0, 0, 0,

		/* 2nd MPEG fragment  --  5 bytes */
		8000, 9000, 10000, 11000, 12000,

		/* 3rd MPEG fragment  --  20 bytes */
		500000, 500001, 500002, 500003, 500004,
		500005, 500006, 500007, 500008, 500009,
		500010, 500011, 500012, 500013, 500014,
		500015, 500016, 500017, 500018, 500019,

		/* gap  --  13 bytes */
		0, 0, 0, 0, 0,
		0, 0, 0, 0, 0,
		0, 0, 0,

		/* 4th MPEG fragment  --  2 bytes */
		1000000, 1090000
	};

	const unsigned int expected_len = 4;
	const unsigned int expected[][4] = {
		{0, 5, 5000, 7000},
		{10, 5, 8000, 12000},
		{15, 20, 500000, 500019},
		{48, 2, 1000000, 1090000}
	};

	FILE * f = tmpfile();
	freopen(NULL, "w+", f);

	/*
	 * Prepare temporary file.
	 */

	char * block = malloc(blocksize * sizeof(char));
	assert(block != NULL);

	unsigned int i;
	for (i = 0; i < size; i++) {
		memset(block, 0x00, blocksize);
		if (timestamps[i] != 0) {
			/*
			 * set magic characters
			 */
			block[0] = 0x00;
			block[1] = 0x00;
			block[2] = 0x01;
			block[3] = 0xBA;

			/*
			 * set marker bits
			 */
			block[4] = block[4] | (1 << 6);
			block[4] = block[4] | (1 << 2);
			block[6] = block[6] | (1 << 2);
			block[8] = block[8] | (1 << 2);

			
			mpeg_time * time = mpeg_timestamp_from_int(timestamps[i]);

			/*****************************************
			 * SOME PARTS ARE COPIED FROM MPEG.C !!! *
			 *****************************************/

			const mpeg_time locations[33][2] = {
				{8, 3}, {8, 4}, {8, 5}, {8, 6}, {8, 7},
				{7, 0}, {7, 1}, {7, 2}, {7, 3}, {7, 4}, {7, 5}, {7, 6}, {7, 7},
				{6, 0}, {6, 1}, {6, 3}, {6, 4}, {6, 5}, {6, 6}, {6, 7},
				{5, 0}, {5, 1}, {5, 2}, {5, 3}, {5, 4}, {5, 5}, {5, 6}, {5, 7},
				{4, 0}, {4, 1}, {4, 3}, {4, 4}, {4, 5}
			};

			unsigned int j;
			for (j = 0; j < 33; j++) {
				block[locations[j][0]] +=
					((time[4-j/8] >> (j%8)) & 1) << locations[j][1];
			}

			/*****************************************
			 *             END OF COPY               *
			 *****************************************/

			/* Check that generated MPEG timestamp is correct. */
			mpeg_time * check = mpeg_timestamp_extract(block);
			assert(mpeg_timestamp_cmp(time, check) == 0);
			mpeg_timestamp_destroy(check);
			
			mpeg_timestamp_destroy(time);
		}
		fwrite(block, sizeof(char), blocksize, f);
	}
	
	free(block);


	/*
	 * Analyze created temporary file.
	 */
	fseek(f, 0, SEEK_SET);
	dllistptr fragments = analyze_stream(f, blocksize, gapsize);
	fclose(f);

	dlitemptr item = dllist_first(fragments);
	for (i = 0; i < expected_len; i++, item = dllist_next(item)) {
		assert(item != NULL);

		mpeg_time * time;
		struct mpeg_fragment * fragment = dllist_get_data(item);
		assert(expected[i][0] == fragment->block_start);
		assert(expected[i][1] == fragment->block_size);

		time = mpeg_timestamp_from_int(expected[i][2]);
		assert(mpeg_timestamp_cmp(time, fragment->time_start) == 0);
		mpeg_timestamp_destroy(time);

		time = mpeg_timestamp_from_int(expected[i][3]);
		assert(mpeg_timestamp_cmp(time, fragment->time_end) == 0);
		mpeg_timestamp_destroy(time);
	}
	assert(item == NULL);


	/*
	 * Merge fragments of the same recording.
	 */

	dllistptr recordings = merge_fragments(fragments);
	dllist_destroy(recordings);

	
	/*
	 * Check passed. Freeing resources.
	 */

	item = dllist_first(fragments);
	while (item != NULL) {
		mpeg_fragment_destroy(dllist_get_data(item));
		item = dllist_next(item);
	}
	dllist_destroy(fragments);

	return 0;
}
