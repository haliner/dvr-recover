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
#include "dllist.h"

/******************************************************************************
 * Internal stuff
 ******************************************************************************/

/*
 * Allocate memory for empty list item, set data and associate item with list.
 */
dlitemptr _dlitem_create(dllistptr list, void * data)
{
	/* TODO: Check return value */
	/* TODO: Errno */
	dlitemptr result = malloc(sizeof(struct dlitem));
	result->next = NULL;
	result->prev = NULL;
	result->data = data;
	result->list = list;
	return result;
}


/*
 * Free memory allocated for list item.
 */
void _dlitem_destroy(dlitemptr item)
{
	free(item);
}


/******************************************************************************
 * Public interface
 ******************************************************************************/

dllistptr dllist_create()
{
	/* TODO: Check return value */
	/* TODO: Errno */
	dllistptr result = malloc(sizeof(struct dllist));
	result->first = NULL;
	result->last = NULL;
	return result;
}


void dllist_destroy(dllistptr list)
{
	dllist_clear(list);
	free(list);
}


dllistptr dllist_copy(dllistptr list)
{
	dllistptr result = dllist_create();

	dlitemptr item = dllist_first(list);
	while (item != NULL) {
		dllist_append(result, dllist_get_data(item));
		item = dllist_next(item);
	}
	
	return result;
}


dlitemptr dllist_first(dllistptr list)
{
	return list->first;
}


dlitemptr dllist_last(dllistptr list)
{
	return list->last;
}


void * dllist_get_data(dlitemptr item)
{
	return item->data;
}


void dllist_set_data(dlitemptr item, void * data)
{
	item->data = data;
}


dlitemptr dllist_next(dlitemptr item)
{
	return item->next;
}


dlitemptr dllist_prev(dlitemptr item)
{
	return item->prev;
}


dlitemptr dllist_append(dllistptr list, void * data)
{
	dlitemptr item = _dlitem_create(list, data);
	if (list->last == NULL) {
		/*
		 * The list is empty. The new item will be the first and last one in
		 * the list.
		 */
		 list->first = item;
		 list->last = item;
	} else {
		/*
		 * Link new item with the last item and set the new last item.
		 */
		list->last->next = item;
		item->prev = list->last;
		list->last = item;
	}
	
	/* Return the new item */
	return item;
}


dlitemptr dllist_prepend(dllistptr list, void * data)
{
	dlitemptr item = _dlitem_create(list, data);
	if (list->first == NULL) {
		/* List is empty. */
		list->first = item;
		list->last = item;
	} else {
		list->first->prev = item;
		item->next = list->first;
		list->first = item;
	}
	
	return item;
}


dlitemptr dllist_insert_before(dlitemptr item, void * data)
{
	if (item->prev == NULL) {
		/*
		 * The item is the first one in the list.
		 */
		return dllist_prepend(item->list, data);
	}
	
	dlitemptr new = _dlitem_create(item->list, data);
	new->next = item;
	new->prev = item->prev;
	new->next->prev = new;
	new->prev->next = new;
	
	return new;
}


dlitemptr dllist_insert_after(dlitemptr item, void * data)
{
	if (item->next == NULL) {
		/*
		 * The item is the last one in the list.
		 */
		 return dllist_append(item->list, data);
	}
	
	dlitemptr new = _dlitem_create(item->list, data);
	new->prev = item;
	new->next = item->next;
	new->prev->next = new;
	new->next->prev = new;
	
	return new;
}


void dllist_remove(dlitemptr item)
{
	if (item->next == NULL)
		item->list->last = item->prev;
	else
		item->next->prev = item->prev;
	
	if (item->prev == NULL)
		item->list->first = item->next;
	else
		item->prev->next = item->next;
	
	_dlitem_destroy(item);
}


void dllist_clear(dllistptr list)
{
	dlitemptr item = list->first;
	while (item != NULL) {
		dlitemptr next = item->next;
		_dlitem_destroy(item);
		item = next;
	}
	list->first = NULL;
	list->last = NULL;
}
