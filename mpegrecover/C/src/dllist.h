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


#ifndef __DLLIST__H__
#define __DLLIST__H__

/*
 * This interface provides support for double-linked-lists.
 */

struct dllist;
struct dlitem;

typedef struct dllist * dllistptr;
typedef struct dlitem * dlitemptr;

struct dllist {
	dlitemptr first;
	dlitemptr last;
};

struct dlitem {
	dlitemptr next;
	dlitemptr prev;
	dllistptr list;
	void * data;
};


/*
 * Memory allocation and deallocation.
 */
dllistptr dllist_create();
void dllist_destroy(dllistptr list);
dllistptr dllist_copy(dllistptr list);


/*
 * Get the first or last item of a list.
 */
dlitemptr dllist_first(dllistptr list);
dlitemptr dllist_last(dllistptr list);


/*
 * Get and set the data field of an item.
 */
void * dllist_get_data(dlitemptr item);
void dllist_set_data(dlitemptr item, void * data);


/*
 * Get the previous or next item of a list.
 */
dlitemptr dllist_next(dlitemptr item);
dlitemptr dllist_prev(dlitemptr item);


/*
 * Append and prepend
 */
dlitemptr dllist_append(dllistptr list, void * data);
dlitemptr dllist_prepend(dllistptr list, void * data);


/*
 * Insert item before or after existing item.
 */
dlitemptr dllist_insert_before(dlitemptr item, void * data);
dlitemptr dllist_insert_after(dlitemptr item, void * data);


/*
 * Remove item from list.
 */
void dllist_remove(dlitemptr item);


/*
 * Remove all items.
 */
void dllist_clear(dllistptr list);


#endif
