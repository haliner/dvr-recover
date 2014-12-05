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
#include "dllist.h"

char check_list(dllistptr list, const int data[], const int data_len)
{
	int i;
	dlitemptr item = dllist_first(list);
	for (i = 0; i < data_len; i++, item = dllist_next(item))
		if ((const int)dllist_get_data(item) != data[i])
			return 0;

	if (item != NULL)
		return 0;
	
	return 1;
}


int main(int argc, char ** argv)
{
	const int data1_len = 5;
	const int data1[] = {0, 1, 2, 3, 4};
	
	const int data2_len = 9;
	const int data2[] = {6, 7, 5, 0, 1, 2, 3, 8, 9}; 
	
	int i;

	dlitemptr item;
	dllistptr list = dllist_create();

	/* Fill list. */
	for (i = 0; i < data1_len; i++)
		dllist_append(list, (void *)data1[i]);

	/* Check that list contains the right data. */
	assert(check_list(list, data1, data1_len));
	
	/* Modify list */
	item = dllist_prepend(list, (void *)5);
	item = dllist_insert_before(item, (void *)6);
	dllist_insert_after(item, (void *)7);
	item = dllist_append(list, (void *)8);
	dllist_insert_after(item, (void *)9);
	dllist_remove(dllist_prev(item));
	
	/* Compare list with expected results. */
	assert(check_list(list, data2, data2_len));
	
	/* Check that first and last items are set correctly. */
	assert((const int)dllist_get_data(dllist_first(list)) == 6);
	assert((const int)dllist_get_data(dllist_last(list)) == 9);

	dllist_destroy(list);

	return 0;
}
