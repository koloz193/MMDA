#include <stdio.h>
#include "bag.h"
#include "my_memory_checker_216.h"

/* (c) Larry Herman and Nelson Padua-Perez, 2015.  You are allowed to use
 * this code yourself, but not to provide it to anyone else.
 */

int main() {
  Bag bag;

  /***** Starting memory checking *****/
  start_memory_check();
  /***** Starting memory checking *****/

  init_bag(&bag);

  add_to_bag(&bag, "dog");
  add_to_bag(&bag, "cat");
  add_to_bag(&bag, "cat");
  add_to_bag(&bag, "goldfish");

  printf("Size of bag = %d.\n", (int) size(bag));

  clear_bag(&bag);

  /****** gathering memory checking info *****/
  stop_memory_check();
  /****** gathering memory checking info *****/

  return 0;
}
