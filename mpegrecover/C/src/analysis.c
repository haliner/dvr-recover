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
#include "analysis.h"
#include "mpeg.h"


dllistptr analyze_file(const char * filename,
                       unsigned int blocksize,
                       unsigned int gapsize)
{
	FILE * f = fopen(filename, "rb");
	if (f == NULL) {
		perror("fopen");
		return NULL;
	}

	dllistptr result = analyze_stream(f, blocksize, gapsize);

	fclose(f);

	return result;
}


dllistptr analyze_stream(FILE * stream,
                         unsigned int blocksize,
                         unsigned int gapsize)
{
	mpeg_time * max_gap = mpeg_timestamp_from_int(gapsize);
	if (max_gap == NULL) {
		perror("Error transforming gapsize");
		return NULL;
	}

	mpeg_time * time_current = NULL;
	mpeg_time * time_old     = NULL;
	struct mpeg_fragment * fragment  = NULL;

	dllistptr fragments = dllist_create();

	unsigned int block_current = 0;
	char * block = malloc(blocksize * sizeof(char));
	while (fread(block, sizeof(char), blocksize, stream) == blocksize) {
		time_current = mpeg_timestamp_extract(block);

		if (time_current != NULL) {
			/*
			 * The current block contains valid MPEG data and we got the
			 * timestamp. If the difference of the current and old timestamp
			 * is too high, we split the stream here into two fragments.
			 */

			/*
			 * If fragment == NULL, we always have to create a new fragment,
			 * because we found a fragment, but the last block contained no
			 * valid MPEG data.
			 */
			char cut = fragment == NULL;

			/*
			 * Otherwise we have to do a few checks.
			 */
			if (! cut) {
				if (mpeg_timestamp_cmp(time_current, time_old) < 0) {
					/*
					* The current timestamp is smaller then the older one.
					* Make a cut here...
					*/
					cut = 1;
				} else {
					/*
					* Calculate the difference. If the difference is greater
					* than max_gap, make a cut.
					*/
					mpeg_time * time_diff = mpeg_timestamp_diff(time_current,
					                                            time_old);
					cut = mpeg_timestamp_cmp(time_diff, max_gap) > 0;
					mpeg_timestamp_destroy(time_diff);
				}
			}

			/*
			 * We cut the stream into two peaces.
			 */
			if (cut) {
				/*
				 * End the current fragment and create a new fragment.
				 * But maybe fragment == NULL, in this case we only need to
				 * create a new fragment.
				 */
				if (fragment != NULL) {
					fragment->block_size = block_current -
						fragment->block_start;
					fragment->time_end = mpeg_timestamp_copy(time_old);
					dllist_append(fragments, fragment);
					fragment = NULL;
				}

				fragment = mpeg_fragment_create();
				fragment->block_start = block_current;
				fragment->time_start = mpeg_timestamp_copy(time_current);
			}
		} else {
			/*
			 * The current block contains no valid MPEG data. The current
			 * fragments ends here.
			 */
			if (fragment != NULL) {
				fragment->block_size = block_current - fragment->block_start;
				fragment->time_end = mpeg_timestamp_copy(time_old);
				dllist_append(fragments, fragment);
				fragment = NULL;
			}
		}

		mpeg_timestamp_destroy(time_old);
		time_old = time_current;
		block_current++;
	}

	/*
	 * Maybe there is an open fragment lying around after the loop above.
	 * End the fragment.
	 */
	if (fragment != NULL) {
		fragment->block_size = block_current - fragment->block_start;
		fragment->time_end = mpeg_timestamp_copy(time_old);
		dllist_append(fragments, fragment);
		fragment = NULL;
	}

	mpeg_timestamp_destroy(time_current);
	mpeg_timestamp_destroy(max_gap);
	free(block);

	/*
	 * Either the end of file was reached or an error occured.
	 */
	if (ferror(stream)) {
		perror("Error reading stream");

		/*
		 * We need to free each item in the list and addionally the list itself.
		 */
		dlitemptr item = dllist_first(fragments);
		while (fragment != NULL) {
			mpeg_fragment_destroy(dllist_get_data(item));
			item = dllist_next(item);
		}
		dllist_destroy(fragments);

		return NULL;
	}

	return fragments;
}


dllistptr merge_fragments(dllistptr original)
{
	/*
	 * This list contains a lists for every MPEG recording (which points
	 * to the single MPEG fragments in the right order).
	 */
	dllistptr result = dllist_create();

	/*
	 * We make a copy of the original list, because we need to modify it.
	 */
	dllistptr fragments = dllist_copy(original);

	/*
	 * Get first item of the list, remove it from list and insert it into
	 * new list which holds the whole recording the item belongs to.
	 * Do this until the list is empty.
	 *
	 * For each fragments search for other fragments, which could form
	 * together a recording and insert them at the right place into the
	 * list for the current recording.
	 *
	 * Each recording-list will be inserted into the result list, which
	 * contains all the recordings.
	 */
	dlitemptr item = dllist_first(fragments);
	while (item != NULL) {
		dllist_remove(item);
		item = dllist_first(fragments);
	}

	/*
	 * Free modified copy of fragment list. Freeing the fragments would be
	 * a very very bad idea... ;)
	 */
	dllist_destroy(fragments);

	return result;
}
