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
#include "buffer.h"


/******************************************************************************
 * Internal stuff
 ******************************************************************************/

/*
 * Resize the buffer. This implies setting a new length and adjusting
 * the memory.
 */
void _buffer_resize(bufferptr buffer, unsigned int length)
{
	buffer->length = length;
	buffer->data = realloc(buffer->data, buffer->length);
}


/******************************************************************************
 * Public interface
 ******************************************************************************/

bufferptr buffer_create()
{
	/* TODO: Check return value */
	bufferptr buffer = malloc(sizeof(struct buffer));
	buffer->length = 0;
	buffer->data = NULL;
	return buffer;
}


void buffer_destroy(bufferptr buffer)
{
	/* TODO: Check return value */
	free(buffer->data);
	free(buffer);
}


bufferptr buffer_copy(bufferptr buffer)
{
	/* TODO: Check return value */
	bufferptr copy = buffer_create();
	copy->length = buffer->length;
	/* TODO: Check return value */
	copy->data = malloc(copy->length);
	memcpy(copy->data, buffer->data, buffer->length);
	return copy;
}


void buffer_append(bufferptr destination, bufferptr source)
{
	unsigned int offset = destination->length;
	/* TODO: Check return value */
	_buffer_resize(destination, destination->length + source->length);
	memcpy(destination->data + offset, source->data, source->length);
}


void buffer_append_str(bufferptr destination, const char * string)
{
	unsigned int offset = destination->length;
	unsigned int length = strlen(string);
	/* TODO: Check return value */
	_buffer_resize(destination, destination->length + length);
	memcpy(destination->data + offset, string, length);
}


void buffer_truncate(bufferptr buffer, unsigned int length)
{
	unsigned int i;
	unsigned int old_length = buffer->length;
	/* TODO: Check return value */
	_buffer_resize(buffer, length);
	for (i = old_length; i < buffer->length; i++) {
		buffer->data[i] = 0x00;
	}
}


bufferptr buffer_concat(bufferptr buffer1, bufferptr buffer2)
{
	/* TODO: Check return value */
	bufferptr result = buffer_copy(buffer1);
	buffer_append(result, buffer2);
	return result;
}


unsigned int buffer_get_length(bufferptr buffer)
{
	return buffer->length;
}


char * buffer_get_data(bufferptr buffer)
{
	return buffer->data;
}
