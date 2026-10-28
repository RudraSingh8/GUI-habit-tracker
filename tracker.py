import os
import time
import tkinter as tk
from tkinter import messagebox, simpledialog

# Constants matching #define in C
MAX_HABITS = 5
STR_LEN = 100


# 1. Exact equivalent of: struct Habit
class Habit:

  def __init__(
      self,
      name="",
      streak=0,
      last_status=1,
      last_trigger="None",
      last_date="Not_Started",
  ):
    self.name = name[:STR_LEN]
    self.streak = int(streak)
    self.last_status = int(last_status)  # 1 = Success, 0 = Failed
    self.last_trigger = last_trigger[:STR_LEN]  # Reason for failure
    self.last_date = last_date[:12]  # DD-MM-YYYY


# 2. Exact equivalent of: void getTodayDate(char *date_str)
def getTodayDate():
  return time.strftime("%d-%m-%Y", time.localtime())


# 3. Exact equivalent of: int loadData(struct Habit habits[])
def loadData(habits):
  if not os.path.exists("habits_data.txt"):
    return 0  # File does not exist yet on initial run

  count = 0
  try:
    with open("habits_data.txt", "r") as fp:
      for line in fp:
        if count >= MAX_HABITS:
          break
        parts = line.strip().split()
        # Matches fscanf(fp, "%s %d %d %s %s", ...) == 5
        if len(parts) == 5:
          habits[count] = Habit(
              name=parts[0],
              streak=int(parts[1]),
              last_status=int(parts[2]),
              last_trigger=parts[3],
              last_date=parts[4],
          )
          count += 1
  except Exception:
    return 0

  return count


# 4. Exact equivalent of: void saveData(struct Habit habits[], int count)
def saveData(habits, count):
  try:
    with open("habits_data.txt", "w") as fp:
      for i in range(count):
        # Matches fprintf(fp, "%s %d %d %s %s\n", ...)
        fp.write(
            f"{habits[i].name} {habits[i].streak} {habits[i].last_status}"
            f" {habits[i].last_trigger} {habits[i].last_date}\n"
        )
  except Exception:
    messagebox.showerror("Error", "Error opening file for saving.")


# 5. Exact equivalent of: void updateStreak(struct Habit *h, int status, const char *trigger, const char *date)
def updateStreak(h, status, trigger, date):
  # Only increase streak if it's a new day and status is 1
  if status == 1:
    if h.last_date != date:
      h.streak += 1
  else:
    h.streak = 0  # Reset streak on failure/relapse

  h.last_status = status
  h.last_trigger = trigger
  h.last_date = date


# 6. Equivalent of main() loop and switch-case menu in a GUI Window
class TrackerMainGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("DISCIPLINE & HABIT TRACKER")
    self.root.geometry("440x620")
    self.root.configure(bg="#1e1e2e")

    # Equivalent of: struct Habit habits[MAX_HABITS];
    self.habits = [Habit() for _ in range(MAX_HABITS)]
    # Equivalent of: int habit_count = loadData(habits);
    self.habit_count = loadData(self.habits)

    # Banner matching printf("==================================\n")
    tk.Label(
        root,
        text=(
            "==================================\nDISCIPLINE & HABIT"
            " TRACKER\n=================================="
        ),
        font=("Courier", 10, "bold"),
        bg="#1e1e2e",
        fg="#89b4fa",
        pady=10,
    ).pack()

    # Output screen (replaces terminal printf output screen)
    self.screen = tk.Text(
        root,
        font=("Courier", 10),
        bg="#11111b",
        fg="#cdd6f4",
        height=14,
        width=46,
        bd=2,
        relief="sunken",
    )
    self.screen.pack(pady=10, padx=10)
    self.print_to_screen(
        "System Ready. Choose an option below.\nLoaded"
        f" {self.habit_count} habit(s) from habits_data.txt.\n"
    )

    # Menu Buttons matching Options 1 to 5
    btn_frame = tk.Frame(root, bg="#1e1e2e")
    btn_frame.pack(pady=5)

    tk.Button(
        btn_frame,
        text="1. View Active Habits & Streaks",
        command=self.case_1_view_habits,
        width=34,
        bg="#313244",
        fg="white",
        font=("Helvetica", 10, "bold"),
        pady=5,
    ).pack(pady=3)

    tk.Button(
        btn_frame,
        text=f"2. Add a New Habit (Max {MAX_HABITS})",
        command=self.case_2_add_habit,
        width=34,
        bg="#89b4fa",
        fg="#11111b",
        font=("Helvetica", 10, "bold"),
        pady=5,
    ).pack(pady=3)

    tk.Button(
        btn_frame,
        text="3. Log Daily Status (Success/Failure)",
        command=self.case_3_log_status,
        width=34,
        bg="#a6e3a1",
        fg="#11111b",
        font=("Helvetica", 10, "bold"),
        pady=5,
    ).pack(pady=3)

    tk.Button(
        btn_frame,
        text="4. Delete a Habit",
        command=self.case_4_delete_habit,
        width=34,
        bg="#fab387",
        fg="#11111b",
        font=("Helvetica", 10, "bold"),
        pady=5,
    ).pack(pady=3)

    tk.Button(
        btn_frame,
        text="5. Save & Exit",
        command=self.case_5_save_exit,
        width=34,
        bg="#f38ba8",
        fg="#11111b",
        font=("Helvetica", 10, "bold"),
        pady=5,
    ).pack(pady=3)

  def print_to_screen(self, text):
    self.screen.config(state=tk.NORMAL)
    self.screen.delete(1.0, tk.END)
    self.screen.insert(tk.END, text)
    self.screen.config(state=tk.DISABLED)

  # Equivalent of: case 1:
  def case_1_view_habits(self):
    if self.habit_count == 0:
      self.print_to_screen(
          "\nNo habits tracked yet.\nChoose Option 2 to add one first!\n"
      )
    else:
      output = "--- CURRENT STREAKS ---\n\n"
      for i in range(self.habit_count):
        h = self.habits[i]
        output += (
            f"[{i + 1}] {h.name} | Streak: {h.streak} days\n    Last Logged:"
            f" {h.last_date}\n"
        )
        if h.last_status == 0 and h.last_trigger != "None":
          output += f"    Last Relapse Trigger: {h.last_trigger}\n"
        output += "\n"
      self.print_to_screen(output)

  # Equivalent of: case 2:
  def case_2_add_habit(self):
    if self.habit_count >= MAX_HABITS:
      messagebox.showwarning(
          "Limit Reached",
          "Limit reached! Focus on mastering your 5 core habits.",
      )
      self.print_to_screen(
          "\nLimit reached! Focus on mastering your 5 core habits.\n"
      )
    else:
      name = simpledialog.askstring(
          "Option 2: Add Habit",
          "Enter habit name (use_underscores, e.g., Study_C):",
      )
      if name and name.strip():
        clean_name = name.strip().replace(" ", "_")

        # Check if habit name already exists
        name_exists = any(
            self.habits[i].name == clean_name for i in range(self.habit_count)
        )
        if name_exists:
          messagebox.showerror(
              "Error", f"A habit named '{clean_name}' already exists!"
          )
          self.print_to_screen(
              f"\nError: Habit '{clean_name}' already exists!\n"
          )
          return

        self.habits[self.habit_count].name = clean_name
        self.habits[self.habit_count].streak = 0
        self.habits[self.habit_count].last_status = 1
        self.habits[self.habit_count].last_trigger = "None"
        self.habits[self.habit_count].last_date = "Not_Started"
        self.habit_count += 1
        self.print_to_screen(
            f"\nHabit '{clean_name}' registered successfully!\n"
        )
        self.case_1_view_habits()

  # Equivalent of: case 3: (including do-while validation loops)
  def case_3_log_status(self):
    if self.habit_count == 0:
      messagebox.showinfo(
          "No Habits", "No habits available to log. Add one in Option 2 first."
      )
      self.print_to_screen(
          "\nNo habits available to log. Add one in Option 2 first.\n"
      )
      return

    # Build list of habits for prompt
    habit_list_str = "Select habit to log:\n"
    for i in range(self.habit_count):
      habit_list_str += f"{i + 1}. {self.habits[i].name}\n"

    # Equivalent of do-while loop for valid habit index (1 to habit_count)
    idx = 0
    while idx < 1 or idx > self.habit_count:
      user_in = simpledialog.askstring(
          "Select Habit",
          f"{habit_list_str}\nSelect habit number (1-{self.habit_count}):",
      )
      if user_in is None:
        return  # User pressed Cancel
      try:
        idx = int(user_in)
        if idx < 1 or idx > self.habit_count:
          messagebox.showerror(
              "Mistake",
              f"Mistake: Please pick a number between 1 and {self.habit_count}.",
          )
      except ValueError:
        messagebox.showerror(
            "Mistake", "Mistake: Please type a number, not a letter."
        )
        idx = 0

    date = getTodayDate()
    selected_habit = self.habits[idx - 1]

    # Same-day check notice matching C code
    if selected_habit.last_date == date:
      messagebox.showinfo(
          "Notice",
          f"Notice: You already logged '{selected_habit.name}' today ({date})."
          " Updating today's entry...",
      )

    # Equivalent of do-while loop for status (strictly 1 or 0)
    status = -1
    while status not in (0, 1):
      status_in = simpledialog.askstring(
          "Daily Status",
          f"Did you succeed today [{date}] for '{selected_habit.name}'?\n(1 ="
          " Yes, 0 = No/Relapsed):",
      )
      if status_in is None:
        return  # User pressed Cancel
      try:
        status = int(status_in)
        if status not in (0, 1):
          messagebox.showerror(
              "Mistake", "Mistake: Only 1 (Yes) or 0 (No) is allowed."
          )
      except ValueError:
        messagebox.showerror(
            "Mistake", "Mistake: Type 1 for Yes or 0 for No, not letters."
        )
        status = -1

    trigger = "None"
    if status == 0:
      trig_in = simpledialog.askstring(
          "Relapse Trigger",
          "What was the trigger/distraction? (use_underscores):",
      )
      if trig_in and trig_in.strip():
        trigger = trig_in.strip().replace(" ", "_")
      else:
        trigger = "Unspecified_Trigger"

    # Call updateStreak passing the Habit object reference directly
    updateStreak(selected_habit, status, trigger, date)
    self.case_1_view_habits()
    messagebox.showinfo("Updated", f"Status updated automatically for {date}!")

  # Equivalent of: case 4: (Delete a Habit)
  def case_4_delete_habit(self):
    if self.habit_count == 0:
      messagebox.showinfo(
          "No Habits", "No habits available to delete."
      )
      self.print_to_screen("\nNo habits available to delete.\n")
      return

    habit_list_str = "Select habit to delete:\n"
    for i in range(self.habit_count):
      habit_list_str += f"{i + 1}. {self.habits[i].name}\n"

    del_idx = 0
    while del_idx < 1 or del_idx > self.habit_count:
      user_in = simpledialog.askstring(
          "Delete Habit",
          f"{habit_list_str}\nSelect habit number to remove (1-{self.habit_count}):",
      )
      if user_in is None:
        return  # User pressed Cancel
      try:
        del_idx = int(user_in)
        if del_idx < 1 or del_idx > self.habit_count:
          messagebox.showerror(
              "Mistake",
              f"Mistake: Pick a number between 1 and {self.habit_count}.",
          )
      except ValueError:
        messagebox.showerror(
            "Mistake", "Mistake: Please type a valid number."
        )
        del_idx = 0

    # Equivalent of C array shifting logic
    target = del_idx - 1
    for i in range(target, self.habit_count - 1):
      self.habits[i] = self.habits[i + 1]

    # Clear the trailing slot and decrease count
    self.habits[self.habit_count - 1] = Habit()
    self.habit_count -= 1

    self.print_to_screen("\nHabit successfully deleted and memory re-indexed!\n")
    self.case_1_view_habits()
    messagebox.showinfo("Deleted", "Habit successfully deleted!")

  # Equivalent of: case 5: (Save & Exit)
  def case_5_save_exit(self):
    saveData(self.habits, self.habit_count)
    messagebox.showinfo(
        "Saved", "Progress saved to habits_data.txt. Stay disciplined!"
    )
    self.root.destroy()


if __name__ == "__main__":
  root = tk.Tk()
  app = TrackerMainGUI(root)
  root.mainloop()
