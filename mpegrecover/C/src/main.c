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
#include <unistd.h>

#include "analysis.h"
#include "buffer.h"
#include "dllist.h"
#include "endianness.h"
#include "mpeg.h"


char verbose = 0;
unsigned int blocksize   = 2048;
/* MPEG clock tickrate is 90,000 Hz. */
unsigned int gapsize     = 90000;     /* 1 second */
unsigned int discardsize = 27000000;  /* 5 minutes */

const char * input = NULL;
const char * output = NULL;


/*
 * Prints usage information to stdout.
 */
void usage()
{
	printf(
		"Syntax: mpegrecover [options] input-filename output-directory\n"
		"Options:\n"
		"  -b N        set block-size\n"
		"  -g N        set gap-size\n"
		"  -d N        set discard-size\n"
		"  -v          enable verbose mode\n"
		"  -h          display this message\n"
	);
}


int main(int argc, char ** argv)
{
	init_endianness();

	/*
	 * Parse commandline arguments.
	 */
	int opt;
	while ((opt = getopt(argc, argv, "b:g:d:vh")) != -1) {
		switch (opt) {
		case 'b':
			blocksize = atoi(optarg);
			break;
		case 'g':
			gapsize = atoi(optarg);
			break;
		case 'd':
			discardsize = atoi(optarg);
			break;
		case 'v':
			verbose = 1;
			break;
		default:
			usage();
			return 1;
		}
	}

	/*
	 * Need 2 additional parameters.
	 */
	if (argc - optind < 2) {
		usage();
		return 1;
	}
	input = argv[optind];
	output = argv[optind + 1];

	if (verbose) {
		printf("endianness:    %s\n"
		       "blocksize:     %u\n"
		       "gapsize:       %u\n"
		       "discardsize:   %u\n"
		       "input:         %s\n"
		       "output:        %s\n\n\n",
		       little_endian ? "little endian" : "big endian",
		       blocksize,
		       gapsize,
		       discardsize,
		       input,
		       output);
	}

	dllistptr fragments = analyze_file(input, blocksize, gapsize);
	if (fragments == NULL) {
		/* TODO: Errno */
		printf("Error analyzing file!\n");
		return 1;
	}

	if (verbose) {
		printf("All recoverable fragments:\n\n");
		dlitemptr item = dllist_first(fragments);
		while (item != NULL) {
			struct mpeg_fragment * fragment = dllist_get_data(item);
			printf("block start:  %u\n"
			       "block size:   %u\n"
			       "time start:   %02x %02x %02x %02x %02x\n"
			       "time end:     %02x %02x %02x %02x %02x\n\n",
			       fragment->block_start,
			       fragment->block_size,
			       fragment->time_start[4],
			       fragment->time_start[3],
			       fragment->time_start[2],
			       fragment->time_start[1],
			       fragment->time_start[0],
			       fragment->time_end[4],
			       fragment->time_end[3],
			       fragment->time_end[2],
			       fragment->time_end[1],
			       fragment->time_end[0]);
			item = dllist_next(item);
		}
		printf("\n");
	}

	dlitemptr item = dllist_first(fragments);
	while (item != NULL) {
		mpeg_fragment_destroy(dllist_get_data(item));
		item = dllist_next(item);
	}
	dllist_destroy(fragments);

	return 0;
}
