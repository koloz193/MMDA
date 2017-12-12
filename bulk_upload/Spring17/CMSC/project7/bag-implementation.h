/*
# Name: Zachary Kolodny
# UID #: 112311827
# UID: zkolodny
*/
#ifndef BAG_IMPLEMENTATION_H
  #define BAG_IMPLEMENTATION_H

  typedef struct item {
    int num;
    char *name;
    struct item *next;
    struct item *prev;
  } Item;

  typedef struct bag {
    int num_items;
    int unique_items;
    Item *items;
  } Bag;

#endif
