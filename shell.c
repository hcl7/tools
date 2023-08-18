#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <dirent.h>
#include <stdbool.h>
#include <readline/readline.h>
#include <readline/history.h>

#define WHITE "\033[1;37m"
#define GREY "\033[0;37m"
#define PURPLE "\033[0;35m"
#define RED_LIGHT "\033[1;31m"
#define GREEN "\033[1;32m"
#define YELLOW "\033[1;33m"
#define CYAN "\033[0;36m"
#define CAFE "\033[0;33m"
#define BLUE "\033[1;34m"
#define DEFAULT "\033[0m"
#define RED "\033[00;31m"

#define MAX_ARGS 64
#define MAX_DIR_ENTRIES 256

int background = 0;
DIR *dp;

void logo() {
    system("clear");
    usleep(100000); printf("%s", BLUE);
    usleep(100000); printf("   ___  _____   _____ _ __  \n");
    usleep(100000); printf("  / __|/ _ \\ \\ / / _ \\ |_ \\ \n");
    usleep(100000); printf("  \\__ \\  __/\\ V /  __/ | | |\n");
    usleep(100000); printf("  |___/\\___| \\_/ \\___|_| |_|\n");
    usleep(100000); printf("%s\n", DEFAULT);
    printf("\n\n");
}

void handle_signal(int signo) {
    if (signo == SIGCHLD) {
        while (waitpid(-1, NULL, WNOHANG) > 0);
    }
}

char *tab_complete_generator(const char *text, int state) {
    static int list_index, len;
    struct dirent *entry;

    if (!state) {
        list_index = 0;
        len = strlen(text);
    }

    while ((entry = readdir(dp)) != NULL) {
        if (strncmp(entry->d_name, text, len) == 0) {
            list_index++;
            return strdup(entry->d_name);
        }
    }

    closedir(dp);
    return NULL;
}

char **tab_complete(const char *text, int start, int end) {
    rl_attempted_completion_over = 1;

    char *buf = rl_line_buffer;
    char *dir = strrchr(buf, ' ');
    if (dir) {
        dir++;
        char *partial = buf + start;

        dp = opendir(".");
        if (dp) {
            return rl_completion_matches(text, tab_complete_generator);
        }
    }

    return NULL;
}

void parse_command(char *command, char **args) {
    int i = 0;
    char *token = strtok(command, " ");
    while (token != NULL) {
        args[i++] = token;
        token = strtok(NULL, " ");
    }
    args[i] = NULL;
}

int execute_command(char **args) {
    pid_t pid = fork();
    if (pid == 0) {
        if (execvp(args[0], args) == -1) {
            perror(RED_LIGHT "[*] limited shell" DEFAULT);
            exit(EXIT_FAILURE);
        }
    } else if (pid > 0) {
        if (!background) {
            waitpid(pid, NULL, 0);
        }
    } else {
        perror(RED_LIGHT "[*] limited shell" DEFAULT);
        return -1;
    }
    return 0;
}

int main() {
    logo();
    char *prompt;
    char *command;
    char *args[MAX_ARGS];

    char *username = getenv("USER");
    if (username == NULL) {
        perror("getenv");
        exit(EXIT_FAILURE);
    }

    if (getuid() == 0) {
        size_t prompt_len = strlen(username) + strlen(RED_LIGHT) + strlen("# ") + strlen(DEFAULT) + 1;
        prompt = (char *)malloc(prompt_len);
        snprintf(prompt, prompt_len, "%s%s# %s", RED_LIGHT, username, DEFAULT);
    } else {
        size_t prompt_len = strlen(username) + strlen(BLUE) + strlen("$ ") + strlen(DEFAULT) + 1;
        prompt = (char *)malloc(prompt_len);
        snprintf(prompt, prompt_len, "%s%s$ %s", BLUE, username, DEFAULT);
    }

    signal(SIGCHLD, handle_signal);

    rl_attempted_completion_function = tab_complete;

    while ((command = readline(prompt)) != NULL) {
        if (strcmp(command, "exit") == 0) {
            printf(RED_LIGHT"[+] Exiting the shell!... " DEFAULT "\n");
            free(command);
            break;
        } else if (strlen(command) > 0) {
            add_history(command);

            if (strncmp(command, "cd", 2) == 0) {
                parse_command(command, args);
                if (args[1]) {
                    chdir(args[1]);
                }
            } else {
                parse_command(command, args);
                execute_command(args);
            }
        }

        free(command);
    }

    return 0;
}
