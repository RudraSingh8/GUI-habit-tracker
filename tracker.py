#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_HABITS 5
#define STR_LEN 100

// Blueprint structure grouping related habit attributes
struct Habit {
    char name[STR_LEN];
    int streak;
    int last_status;            // 1 = Success, 0 = Failed
    char last_trigger[STR_LEN]; // Reason for failure
    char last_date[12];         // DD-MM-YYYY format
};

// Function prototypes
int loadData(struct Habit habits[]);
void saveData(struct Habit habits[], int count);
void updateStreak(struct Habit *h, int status, const char *trigger, const char *date);
void getTodayDate(char *date_str);
void deleteHabit(struct Habit habits[], int *count, int del_idx);

int main() {
    struct Habit habits[MAX_HABITS];
    int habit_count = loadData(habits);
    int choice;

    // Main program loop
    do {
        printf("\n==================================\n");
        printf("    DISCIPLINE & HABIT TRACKER    \n");
        printf("==================================\n");
        printf("1. View Active Habits & Streaks\n");
        printf("2. Add a New Habit (Max %d)\n", MAX_HABITS);
        printf("3. Log Daily Status (Success/Failure)\n");
        printf("4. Delete a Habit\n");
        printf("5. Save & Exit\n");

        // Defensive validation loop for menu selection
        do {
            printf("Enter your choice (1-5): ");
            if (scanf("%d", &choice) != 1) {
                while (getchar() != '\n'); // Clear buffer on invalid keystroke
                printf("Mistake: Letters are not allowed. Please type a number from 1 to 5.\n\n");
                choice = 0;
            } else if (choice < 1 || choice > 5) {
                printf("Mistake: %d is not an option. Please choose between 1 and 5.\n\n", choice);
            }
        } while (choice < 1 || choice > 5);

        switch (choice) {
            case 1: {
                if (habit_count == 0) {
                    printf("\nNo habits tracked yet. Choose Option 2 to add one first!\n");
                } else {
                    printf("\n--- CURRENT STREAKS ---\n");
                    for (int i = 0; i < habit_count; i++) {
                        printf("[%d] %s | Streak: %d days | Last Logged: %s\n", 
                               i + 1, habits[i].name, habits[i].streak, habits[i].last_date);
                        if (habits[i].last_status == 0 && strcmp(habits[i].last_trigger, "None") != 0) {
                            printf("    Last Relapse Trigger: %s\n", habits[i].last_trigger);
                        }
                    }
                }
                break;
            }

            case 2: {
                if (habit_count >= MAX_HABITS) {
                    printf("\nLimit reached! Focus on mastering your 5 core habits.\n");
                } else {
                    printf("\nEnter habit name (use_underscores, e.g., Study_C): ");
                    scanf("%s", habits[habit_count].name);
                    habits[habit_count].streak = 0;
                    habits[habit_count].last_status = 1;
                    strcpy(habits[habit_count].last_trigger, "None");
                    strcpy(habits[habit_count].last_date, "Not_Started");
                    habit_count++;
                    printf("Habit registered successfully!\n");
                }
                break;
            }

            case 3: {
                if (habit_count == 0) {
                    printf("\nNo habits available to log. Add one in Option 2 first.\n");
                    break;
                }
                printf("\nSelect habit to log:\n");
                for (int i = 0; i < habit_count; i++) {
                    printf("%d. %s\n", i + 1, habits[i].name);
                }

                int idx;
                do {
                    printf("Select habit number (1-%d): ", habit_count);
                    if (scanf("%d", &idx) != 1) {
                        while (getchar() != '\n');
                        printf("Mistake: Please type a number, not a letter.\n");
                        idx = 0;
                    } else if (idx < 1 || idx > habit_count) {
                        printf("Mistake: Please pick a number between 1 and %d.\n", habit_count);
                    }
                } while (idx < 1 || idx > habit_count);

                int status;
                char date[12];
                char trigger[STR_LEN] = "None";

                // Automatically fetch date from system clock
                getTodayDate(date);

                if (strcmp(habits[idx - 1].last_date, date) == 0) {
                    printf("\nNotice: You already logged '%s' today (%s). Updating today's entry...\n", 
                           habits[idx - 1].name, date);
                }

                do {
                    printf("Did you succeed today [%s]? (1 = Yes, 0 = No): ", date);
                    if (scanf("%d", &status) != 1) {
                        while (getchar() != '\n');
                        printf("Mistake: Type 1 for Yes or 0 for No.\n");
                        status = -1;
                    } else if (status != 0 && status != 1) {
                        printf("Mistake: Only 1 (Yes) or 0 (No) is allowed.\n");
                    }
                } while (status != 0 && status != 1);

                if (status == 0) {
                    printf("What was the trigger/distraction? (use_underscores): ");
                    scanf("%s", trigger);
                }

                // Pass memory address directly using pointers
                updateStreak(&habits[idx - 1], status, trigger, date);
                printf("Status updated automatically for %s!\n", date);
                break;
            }

            case 4: {
                if (habit_count == 0) {
                    printf("\nNo habits available to delete.\n");
                    break;
                }
                printf("\nSelect habit to delete:\n");
                for (int i = 0; i < habit_count; i++) {
                    printf("%d. %s\n", i + 1, habits[i].name);
                }

                int del_idx;
                do {
                    printf("Select habit number to remove (1-%d): ", habit_count);
                    if (scanf("%d", &del_idx) != 1) {
                        while (getchar() != '\n');
                        printf("Mistake: Please type a valid number.\n");
                        del_idx = 0;
                    } else if (del_idx < 1 || del_idx > habit_count) {
                        printf("Mistake: Pick a number between 1 and %d.\n", habit_count);
                    }
                } while (del_idx < 1 || del_idx > habit_count);

                deleteHabit(habits, &habit_count, del_idx);
                break;
            }

            case 5:
                saveData(habits, habit_count);
                printf("\nProgress saved to habits_data.txt. Stay disciplined!\n");
                break;
        }
    } while (choice != 5);

    return 0;
}

// Grabs system date from phone OS
void getTodayDate(char *date_str) {
    time_t t = time(NULL);
    struct tm *tm_info = localtime(&t);
    strftime(date_str, 12, "%d-%m-%Y", tm_info);
}

// Loads persistent data from text file
int loadData(struct Habit habits[]) {
    FILE *fp = fopen("habits_data.txt", "r");
    if (fp == NULL) {
        return 0; // File doesn't exist on first run
    }
    int count = 0;
    while (count < MAX_HABITS && fscanf(fp, "%s %d %d %s %s", 
           habits[count].name, 
           &habits[count].streak, 
           &habits[count].last_status, 
           habits[count].last_trigger, 
           habits[count].last_date) == 5) {
        count++;
    }
    fclose(fp);
    return count;
}

// Saves data array to phone storage file
void saveData(struct Habit habits[], int count) {
    FILE *fp = fopen("habits_data.txt", "w");
    if (fp == NULL) {
        printf("Error opening file for saving.\n");
        return;
    }
    for (int i = 0; i < count; i++) {
        fprintf(fp, "%s %d %d %s %s\n", 
                habits[i].name, 
                habits[i].streak, 
                habits[i].last_status, 
                habits[i].last_trigger, 
                habits[i].last_date);
    }
    fclose(fp);
}

// Modifies streak and values using pointer referencing
void updateStreak(struct Habit *h, int status, const char *trigger, const char *date) {
    if (status == 1) {
        if (strcmp(h->last_date, date) != 0) {
            h->streak += 1;
        }
    } else {
        h->streak = 0; // Reset streak on relapse
    }
    h->last_status = status;
    strcpy(h->last_trigger, trigger);
    strcpy(h->last_date, date);
}

// Shifts array elements forward to delete a habit
void deleteHabit(struct Habit habits[], int *count, int del_idx) {
    int target = del_idx - 1;
    for (int i = target; i < (*count) - 1; i++) {
        habits[i] = habits[i + 1];
    }
    (*count)--;
    printf("\nHabit successfully deleted and memory re-indexed!\n");
}
