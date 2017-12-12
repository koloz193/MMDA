import os

for x in range(1,6):
    print('-' * 80)
    print("PUBLIC TEST: " + str(x))
    os.system("gcc public0" + str(x) + ".c my_memory_checker_216.c calendar.c -0 a.out")
    os.system("./a.out | diff -u - public0" + str(x) + ".output")
print('-' * 80)
