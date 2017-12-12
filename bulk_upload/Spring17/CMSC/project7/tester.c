/*
# Name: Zachary Kolodny
# UID #: 112311827
# UID: zkolodny
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bag.h"

# define SZ 4

static void test1(void);
static void test2(void);
static void test3(void);
static void test4(void);
static void test5(void);
static void test6(void);
static void test7(void);
static void test8(void);
static void test9(void);

static void test1(void) {
  Bag bag;

  init_bag(&bag);

  add_to_bag(&bag, "bitcoin");

  if (size(bag) != 1)
    exit(FOUND_BUG);
}

static void test2(void) {
  Bag bag;
  int i;

  init_bag(&bag);

  for (i= 1; i <= 10; i++)
    add_to_bag(&bag, "I love CMSC 216!");

  if (count(bag, "I love CMSC 216!") != 10) {
    printf("Buggy bag- count() is wrong!\n");
    exit(FOUND_BUG);
  }
}

static void test3(void) {
  Bag bag;
  int i;

  init_bag(&bag);

  for (i= 0; i < 10; i++)
    add_to_bag(&bag, "Anwar is the GOAT");

  for(i = 0; i < 9; i++) {
    remove_occurrence(&bag, "Anwar is the GOAT");
  }

  if (count(bag, "Anwar is the GOAT") != 1)
  {
    printf("BUG: remove_occurence when num > 1\n");
    exit(FOUND_BUG);
  }

  remove_occurrence(&bag, "Anwar is the GOAT");

  if (count(bag, "Anwar is the GOAT") != -1)
  {
    printf("BUG: remove_occurence when num == 1\n");
    exit(FOUND_BUG);
  }

}

static void test4(void) {
  Bag bag;

  init_bag(&bag);

  add_to_bag(&bag, "Jordan");
  add_to_bag(&bag, "Jordan");
  add_to_bag(&bag, "Ewing");
  add_to_bag(&bag, "Pippin");

  remove_from_bag(&bag, "Jordan");

  if (size(bag) != 2)
  {
    printf("BUG: removing entire start item from bag\n");
    exit(FOUND_BUG);
  }

  add_to_bag(&bag, NULL);

  if (size(bag) != 2)
  {
    printf("BUG: add to bag with NULL slipped through\n");
    exit(FOUND_BUG);
  }
}

static void test5(void) {
  Bag bag;

  init_bag(&bag);

  add_to_bag(&bag, "Ferrari");
  add_to_bag(&bag, "Lambo");
  add_to_bag(&bag, "Lambo");
  add_to_bag(&bag, "McLaren");

  remove_from_bag(&bag, "Lambo");

  if (count(bag, "Lambo") != -1)
  {
    printf("BUG: remove from middle of bag\n");
    exit(FOUND_BUG);
  }

}

static void test6(void) {
  Bag bag;


  init_bag(&bag);

  add_to_bag(&bag, "Seiko");
  add_to_bag(&bag, "Citizen");
  add_to_bag(&bag, "Breitling");
  add_to_bag(&bag, "Breitling");

  remove_from_bag(&bag, "Breitling");

  if (count(bag, "Breitling") != -1)
  {
    printf("BUG: remove from end of bag\n");
    exit(FOUND_BUG);
  }

}

static void test7(void) {
  Bag bag, bag2;

  init_bag(&bag);
  init_bag(&bag2);

  add_to_bag(&bag, "Dillon Francis");
  add_to_bag(&bag, "Odesza");
  add_to_bag(&bag, "Pretty Lights");

  add_to_bag(&bag2, "Dillon Francis");
  add_to_bag(&bag2, "Odesza");
  add_to_bag(&bag2, "Pretty Lights");
  add_to_bag(&bag2, "Gramatik");

  if (is_sub_bag(bag, bag2)!= 1)
  {
    printf("BUG: sub bag\n");
    exit(FOUND_BUG);
  }

  add_to_bag(&bag2, "Odesza");

  if (is_sub_bag(bag, bag2) != 1)
  {
    printf("BUG: sub bag - mult occurrences\n");
    exit(FOUND_BUG);
  }

  remove_from_bag(&bag2, "Dillon Francis");

  if (is_sub_bag(bag, bag2) != 0)
  {
    printf("BUG: sub bag should've failed\n");
    exit(FOUND_BUG);
  }
}

static void test8(void) {
  Bag bag, bag2, bag3;

  init_bag(&bag);
  init_bag(&bag2);

  add_to_bag(&bag, "Dillon Francis");
  add_to_bag(&bag, "Odesza");
  add_to_bag(&bag, "Pretty Lights");

  add_to_bag(&bag2, "Dillon Francis");
  add_to_bag(&bag2, "Odesza");
  add_to_bag(&bag2, "Pretty Lights");
  add_to_bag(&bag2, "Gramatik");

  bag3 = bag_union(bag, bag2);

  if (count(bag3, "Dillon Francis") != 2)
  {
    printf("BUG: bag union failed\n");
    exit(FOUND_BUG);
  }

  if (count(bag3, "Odesza") != 2)
  {
    printf("BUG: bag union failed\n");
    exit(FOUND_BUG);
  }

  if (count(bag3, "Pretty Lights") != 2)
  {
    printf("BUG: bag union failed\n");
    exit(FOUND_BUG);
  }

  if (count(bag3, "Gramatik") != 1)
  {
    printf("BUG: bag union failed\n");
    exit(FOUND_BUG);
  }
}

static void test9(void) {
  Bag bag, bag2;

  init_bag(&bag);
  init_bag(&bag2);

  add_to_bag(&bag, "Messi");
  add_to_bag(&bag, "Hazard");
  add_to_bag(&bag, "Hazard");
  add_to_bag(&bag, "Ibrahimovic");

  add_to_bag(&bag2, "Messi");
  add_to_bag(&bag2, "Hazard");
  add_to_bag(&bag2, "Ibrahimovic");
  add_to_bag(&bag2, "Rooney");

  if (is_sub_bag(bag, bag2) != 0)
  {
    printf("BUG: sub bag bag1 more occurrences\n");
    exit(FOUND_BUG);
  }

  remove_occurrence(&bag, "Hazard");

  if (is_sub_bag(bag, bag2) != 1)
  {
    printf("BUG: sub bag bags should be equal\n");
    exit(FOUND_BUG);
  }

  add_to_bag(&bag, "Ronaldinho");

  if (is_sub_bag(bag, bag2) != 0)
  {
    printf("BUG: sub bag bag1 more unique items\n");
    exit(FOUND_BUG);
  }
}

int main() {
  printf("Test1\n");
  test1();
  printf("Test2\n");
  test2();
  printf("Test3\n");
  test3();
  printf("Test4\n");
  test4();
  printf("Test5\n");
  test5();
  printf("Test6\n");
  test6();
  printf("Test7\n");
  test7();
  printf("Test8\n");
  test8();
  printf("Test9\n");
  test9();

  printf("No errors detected!\n");

  return CORRECT;
}
