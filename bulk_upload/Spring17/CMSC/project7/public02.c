#include <stdio.h>
#include "bag.h"

/* (c) Larry Herman and Nelson Padua-Perez, 2015.  You are allowed to use
 * this code yourself, but not to provide it to anyone else.
 */

int main() {
  Bag bag;

  init_bag(&bag);

  add_to_bag(&bag, "gerbil");
  add_to_bag(&bag, "hamster");
  add_to_bag(&bag, "guinea pig");

  printf("Number of occurrences of \"hamster\" in the bag = %d.\n",
         count(bag, "hamster"));

  clear_bag(&bag);

  return 0;
}
