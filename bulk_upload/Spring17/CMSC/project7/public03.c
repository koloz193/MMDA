#include <stdio.h>
#include "bag.h"

/* (c) Larry Herman and Nelson Padua-Perez, 2015.  You are allowed to use
 * this code yourself, but not to provide it to anyone else.
 */

int main() {
  Bag bag;

  init_bag(&bag);

  add_to_bag(&bag, "dog");
  add_to_bag(&bag, "cat");
  add_to_bag(&bag, "cat");
  add_to_bag(&bag, "goldfish");

  printf("Number of occurrences of \"cat\" in the bag = %d.\n",
         count(bag, "cat"));

  clear_bag(&bag);

  return 0;
}
