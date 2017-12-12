/*
Name: Zachary Kolodny
UID: zkolodny
UID #: 112311827
Project 6
CMSC216 Section 0203
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "command.h"
#include "executor.h"

/*static void print_tree(struct tree *t);*/
int ambig_redirect_check(struct tree *t);
void redirect_io(struct tree *t);

/*
  Check for ambiguous redirect when called with a pipe. Sets type to 1 for
  input and 2 for output.
*/
int ambig_redirect_check(struct tree *t)
{
  if (t == NULL)
    return 0;
  else if (t->input != NULL)
    return 1;
  else if (t->output != NULL)
    return 2;
  else if (t->left == NULL && t->right == NULL)
    return 0;
  else
    return ambig_redirect_check(t->left) | ambig_redirect_check(t->right);
}

void redirect_io(struct tree *t)
{
  int fd_in, fd_out;

  if (t->input != NULL)
  {
    if ((fd_in = open(t->input, O_RDONLY)) == -1)
    {
      perror("open");
      return;
    }
    if (dup2(fd_in, STDIN_FILENO) == -1)
    {
      perror("dup2");
      return;
    }
  }

  if (t->output != NULL)
  {
    if ((fd_out = open(t->output, O_WRONLY | O_CREAT | O_TRUNC,
      0664)) == -1)
    {
      perror("open");
      return;
    }
    if (dup2(fd_out, STDOUT_FILENO) == -1)
    {
      perror("dup2");
      return;
    }
  }

  return;
}

int execute(struct tree *t)
{
  int cd_status, exec_status, status, ambig_check_left;
  int ambig_check_right, pipefd[2], status_two;
  pid_t pid, pid_two;
  char *path;

  /*
    If the conjunction is NONE then the shell determines if the command is a
    shell or UNIX command, handling shell commands internally and UNIX commands
    with execvp.
  */
  if (t->conjunction == NONE)
  {
    if (strcmp(t->argv[0], "cd") == 0)
    {
      if (t->argv[0] == NULL)
        cd_status = chdir(getenv("HOME"));
      else
        cd_status = chdir(t->argv[1]);

      if (cd_status == 0)
        return 1;
      else
      {
        perror("cd");
        return 0;
      }
    }
    else if(strcmp(t->argv[0], "exit") == 0)
    {
      exit(0);
    }
    else
    {
      pid = fork();
      if (pid == 0)
      {
        redirect_io(t);

        exec_status = execvp(t->argv[0], t->argv);

        if (exec_status == -1)
        {
          fprintf(stderr, "Failed to execute %s\n", t->argv[0]);
          exit(EXIT_FAILURE);
        }
      }
      else if (pid > 0)
      {
        waitpid(pid, &status, 0);
        return !status ? 1 : 0;
      }
      else if (pid == -1)
      {
        perror("fork");
        return 0;
      }
    }
  }
  /*
    If the conjuction is AND then the shell attempts to execute the left side
    of the command, and if that is successful moves on to the right side.
  */
  else if (t->conjunction == AND)
    return (execute(t->left) && execute(t->right));
  /*
    Connects the stdin of the right side to the std of then left side if there
    is no ambiguous redirection (output on left || input on right).

    Parent deals with read while child deals with write.
  */
  else if (t->conjunction == PIPE)
  {
    ambig_check_left = ambig_redirect_check(t->left);
    ambig_check_right = ambig_redirect_check(t->right);

    if (ambig_check_left == 2 || ambig_check_left == 3)
    {
      printf("Ambiguous output redirect.\n");
      return 0;
    }
    else if (ambig_check_right == 1 || ambig_check_right == 3)
    {
      printf("Ambiguous input redirect.\n");
      return 0;
    }

    pid = fork();

    /* Parent */
    if (pid > 0)
    {
      waitpid(pid, &status, 0);
      return !status ? 1 : 0;
    }
    /* Child */
    else if (pid == 0)
    {
      if (pipe(pipefd) == -1)
      {
        perror("pipe");
        return 0;
      }

      pid_two = fork();

      if (pid_two == 0)
      {
        dup2(pipefd[0], STDIN_FILENO);
        close(pipefd[1]);
        execute(t->right);
        close(pipefd[0]);
        return 1;
      }
      else if (pid_two > 0)
      {
        dup2(pipefd[1], STDOUT_FILENO);
        close(pipefd[0]);
        execute(t->left);
        close(pipefd[1]);
        return 1;
      }
      else
      {
        perror("fork");
        return 0;
      }
    }
    else
    {
      perror("fork");
      return 0;
    }
  }
  /*
    Commands run in subshell don't change the current environment
  */
  else if (t->conjunction == SUBSHELL)
  {
    pid_two = fork();

    if (pid_two > 0)
    {
      waitpid(pid_two, &status_two, 0);
      return !status_two ? 1 : 0;
    }
    else if (pid_two == 0)
    {
      path = getenv("PATH");

      redirect_io(t);

      execute(t->left);
      if ((strcmp(path, getenv("PATH")) != 0) && (chdir(path) == -1))
      {
        perror("cd");
        return 0;
      }
      /* if return is 0, passes 12, if 1 then fails 12 */
      return 1;
    }
  }

  return 0;
}

/*
static void print_tree(struct tree *t) {
   if (t != NULL) {
      print_tree(t->left);

      if (t->conjunction == NONE) {
         printf("NONE: %s, ", t->argv[0]);
      } else {
         printf("%s, ", conj[t->conjunction]);
      }
      printf("IR: %s, ", t->input);
      printf("OR: %s\n", t->output);

      print_tree(t->right);
   }
}
*/
