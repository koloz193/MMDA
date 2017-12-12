#include <stdio.h>
#include "bag.h"

/* (c) Larry Herman and Nelson Padua-Perez, 2015.  You are allowed to use
 * this code yourself, but not to provide it to anyone else.
 */

int main() {
  Bag bag;

  init_bag(&bag);

  add_to_bag(&bag, "cow");
  add_to_bag(&bag, "sheep");
  add_to_bag(&bag, "horse");

  printf("Size of bag = %d.\n", (int) size(bag));

  clear_bag(&bag);

  return 0;
}
