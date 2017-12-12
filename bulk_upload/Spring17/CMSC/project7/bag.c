/*
# Name: Zachary Kolodny
# UID #: 112311827
# UID: zkolodny
*/
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "bag.h"

static Item *find_item(Bag *bag, const char *name);

static Item *find_item(Bag *bag, const char *name)
{
  Item *iter;

  if (bag->unique_items == 0)
    return NULL;

  for (iter = bag->items; iter != NULL; iter = iter->next)
    if (strcmp(iter->name, name) == 0)
      return iter;

  return NULL;
}

void init_bag(Bag *bag)
{
  if (bag == NULL)
    return;

  bag->num_items = 0;
  bag->unique_items = 0;
  bag->items = NULL;

  return;
}

void add_to_bag(Bag *bag, const char *element)
{
  Item *new;

  if (bag == NULL || element == NULL)
    return;

  if (bag->num_items == 0)
  {
    bag->items = calloc(1, sizeof(Item));

    if (bag->items == NULL)
      return;

    new = bag->items;

    new->name = malloc(strlen(element) + 1);

    if (new->name == NULL)
    {
      free(new);
      return;
    }

    strcpy(new->name, element);
    new->num = 1;
    new->next = NULL;
    new->prev = NULL;

    bag->num_items = 1;
    bag->unique_items = 1;

    return;
  }
  else
  {
    new = find_item(bag, element);

    if (new == NULL)
    {
      for (new = bag->items; new->next != NULL; new = new->next);

      new->next = calloc(1, sizeof(Item));

      if (new->next == NULL)
        return;

      new->next->prev = new;

      new->next->name = malloc(strlen(element) + 1);

      if (new->next->name == NULL)
      {
        free(new);
        return;
      }

      strcpy(new->next->name, element);
      new->next->num = 1;
      new->next->next = NULL;

      bag->num_items++;
      bag->unique_items++;

      return;
    }
    else
    {
      new->num++;
      bag->num_items++;
      return;
    }
  }
}

size_t size(Bag bag)
{
  return bag.unique_items;
}

int count(Bag bag, const char *element)
{
  Item *item;

  if (element == NULL)
    return -1;

  item = find_item(&bag, element);

  return item != NULL ? item->num : -1;
}

int remove_occurrence(Bag *bag, const char *element)
{
  Item *item;

  if (bag == NULL || element == NULL)
    return -1;

  item = find_item(bag, element);

  if (item == NULL)
    return -1;

  if (item->num > 1)
  {
    item->num--;
    bag->num_items--;
    return item->num;
  }
  else
  {
    if (item->prev == NULL && item->next == NULL)
    {
      free(item->name);
      free(item);
      bag->items = NULL;
    }
    else if (item->prev == NULL)
    {
      free(item->name);
      bag->items = item->next;
      item = item->next;
      free(item->prev);
      item->prev = NULL;
    }
    else if (item->next == NULL)
    {
      free(item->name);
      item = item->prev;
      free(item->next);
      item->next = NULL;
    }
    else
    {
      item->next->prev = item->prev;
      item->prev->next = item->next;
    }

    bag->num_items--;
    bag->unique_items--;
    return -1;
  }
}

int remove_from_bag(Bag *bag, const char *element)
{
  Item *item;
  int i, n;

  if (bag == NULL || element == NULL)
    return -1;

  item = find_item(bag, element);

  if (item == NULL)
    return -1;
  else
  {
    n = item->num;

    for (i = 0; i < n; i++)
      remove_occurrence(bag, element);

    return 0;
  }
}

Bag bag_union(Bag bag1, Bag bag2)
{
  Bag new;
  Item *item;

  init_bag(&new);

  for (item = bag1.items; item != NULL; item = item->next)
    add_to_bag(&new, item->name);

  for (item = bag2.items; item != NULL; item = item->next)
    add_to_bag(&new, item->name);

  return new;
}

int is_sub_bag(Bag bag1, Bag bag2)
{
  Item *item, *item_two;

  if (bag1.num_items == 0)
    return 1;

  if (bag1.unique_items > bag2.unique_items)
    return 0;

  for (item = bag1.items; item != NULL; item = item->next)
  {
    if ((item_two = find_item(&bag2, item->name)) == NULL)
      return 0;
    else
      if (item->num > item_two->num)
        return 0;
  }

  return 1;
}

void clear_bag(Bag *bag)
{
  Item *item;

  if (bag == NULL || bag->num_items == 0 || bag->items == 0)
    return;

  item = bag->items;

  while (item->next != NULL)
  {
    item = item->next;
    remove_from_bag(bag, item->prev->name);
  }

  remove_from_bag(bag, item->name);

  return;
}
