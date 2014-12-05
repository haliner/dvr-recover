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
#include "buffer.h"

int main(int argc, char ** argv)
{
	const char * str1 = "dummy string";
	unsigned int str1_len = 12;

	const char * str2 = "dummy";
	unsigned int str2_len = 5;

	const char * str3 = "dummy\0\0\0\0\0\0\0";
	unsigned int str3_len = 12;

	const char * str4 = "dummy\0\0\0\0\0\0\0dummy\0\0\0\0\0\0\0";
	unsigned int str4_len = 24;


	unsigned int i;


	bufferptr buffer1 = buffer_create();
	assert(buffer1->length == 0);
	assert(buffer_get_length(buffer1) == 0);
	assert(buffer1->data == NULL);
	assert(buffer_get_data(buffer1) == NULL);

	buffer_append_str(buffer1, str1);
	assert(memcmp(str1, buffer_get_data(buffer1), str1_len) == 0);

	buffer_truncate(buffer1, str2_len);
	assert(buffer_get_length(buffer1) == str2_len);
	assert(memcmp(str2, buffer_get_data(buffer1), str2_len) == 0);

	buffer_truncate(buffer1, str3_len);
	assert(buffer_get_length(buffer1) == str3_len);
	assert(memcmp(str3, buffer_get_data(buffer1), str3_len) == 0);

	bufferptr buffer2 = buffer_copy(buffer1);
	assert(buffer_get_length(buffer2) == str3_len);
	assert(memcmp(str3, buffer_get_data(buffer2), str3_len) == 0);

	bufferptr buffer3 = buffer_concat(buffer1, buffer2);
	assert(buffer_get_length(buffer3) == str4_len);
	assert(memcmp(str4, buffer_get_data(buffer3), str4_len) == 0);

	buffer_truncate(buffer3, 0);
	buffer_truncate(buffer3, 1024);
	for (i = 0; i < buffer_get_length(buffer3); i++) {
		assert(buffer_get_data(buffer3)[i] == 0x00);
	}

	buffer_destroy(buffer1);
	buffer_destroy(buffer2);
	buffer_destroy(buffer3);

	return 0;
}
