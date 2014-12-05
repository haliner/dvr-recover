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


#ifndef __BUFFER__H__
#define __BUFFER__H__

/*
 * This file provides a buffer datatype.
 *
 * A buffer is a piece of memory of arbitrary length.
 * The interface allows manipulating the buffer in various ways.
 */


/*
 * We need only to know the length and the starting point of the buffer.
 */
struct buffer {
	unsigned int length;
	char * data;
};

/*
 * Simple access to buffer struct. The struct mustn't be accessed directly
 * from outside of this interface. All functions should process this datatype.
 */
typedef struct buffer * bufferptr;

/******************************************************************************
 * Create / Free buffer
 ******************************************************************************/

/*
 * Allocate and initialize memory for the buffer struct.
 */
bufferptr buffer_create();

/*
 * Frees the memory allocated for the buffer struct.
 */
void buffer_destroy(bufferptr buffer);

/*
 * Return a copy of the buffer.
 */
bufferptr buffer_copy(bufferptr buffer);



/******************************************************************************
 * Append something to the buffer
 ******************************************************************************/

/*
 * Copy the content of the source buffer to the end of the destination buffer
 * and adjust the length properly.
 */
void buffer_append(bufferptr destination, bufferptr source);

/*
 * Copy the content of the string to the end of the buffer and adjust the
 * length.
 */
void buffer_append_str(bufferptr destination, const char * string);



/******************************************************************************
 * Truncate buffer
 ******************************************************************************/

/*
 *
 */
void buffer_truncate(bufferptr buffer, unsigned int length);




/******************************************************************************
 * Concatenation
 ******************************************************************************/

/*
 * Return a new buffer with the data from both source buffers.
 */
bufferptr buffer_concat(bufferptr buffer1, bufferptr buffer2);


/******************************************************************************
 * Accessing properties
 ******************************************************************************/

/*
 * Return the length of the buffer.
 */
unsigned int buffer_get_length(bufferptr buffer);

/*
 * Return the data of the buffer.
 */
char * buffer_get_data(bufferptr buffer);

#endif 
