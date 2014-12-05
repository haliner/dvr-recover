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


#ifndef __ANALYSIS__H__
#define __ANALYSIS__H__

#include <stdio.h>
#include "dllist.h"

/*
 * Handles file analysis. Reads data from files and streams and
 * looks for MPEG fragments. All fragments are stored in a double-linked-lists
 * for easy access.
 */

/*
 * Open file and analyze its stream content.
 */
dllistptr analyze_file(const char * filename,
                       unsigned int blocksize,
                       unsigned int gapsize);

/*
 * Read stream content into buffer and analyze it.
 */
dllistptr analyze_stream(FILE * stream,
                         unsigned int blocksize,
                         unsigned int gapsize);


/*
 * Tries to merge fragments which are belonging together.
 */
dllistptr merge_fragments(dllistptr original);

#endif
