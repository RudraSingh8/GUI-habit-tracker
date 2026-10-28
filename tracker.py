import json
import os
import time
import tkinter as tk
from tkinter import messagebox, simpledialog

# ==============================================================================
# 1. GLOBAL VARIABLES & CONSTANTS
# ==============================================================================
# MAX_HABITS limits the total number of habits a user can add to 5.
MAX_HABITS = 5
# habits_list is an empty array that will store dictionary items for each habit.
habits_list = []


# ==============================================================================
# 2. HELPER FUNCTIONS
# ==============================================================================


def get_today_date():
  """Gets the current date as a string (DD-MM-YYYY) using the system clock."""
  # time.localtime() gets system clock details, time.strftime formats it to text.
  # Example output string: "28-10-2026"
  return time.strftime("%d-%m-%Y", time.localtime())


def load_data():
  """Loads data from a JSON file into our global habits list when starting."""
  global habits_list
  # Check if the data storage file exists on the hard drive.
  if os.path.exists("habits_simple_data.json"):
    try:
      # Open the file in read mode ("r").
      with open("habits_simple_data.json", "r") as file:
        # json.load converts text data from the file back into a Python list of dicts.
        habits_list = json.load(file)
    except json.JSONDecodeError:
      # If the file contains bad text, show a pop-up warning box.
      messagebox.showwarning(
          "Warning",
          "Data file was corrupted. Starting with an empty habit list.",
      )
      # Reset list to empty because data was broken.
      habits_list = []
    except Exception:
      # Catch-all block for any other unexpected file reading errors.
      habits_list = []


def save_data():
  """Saves the current habits list out to a structured JSON file."""
  try:
    # Open the file in write mode ("w") which overwrites or creates a new file.
    with open("habits_simple_data.json", "w") as file:
      # json.dump converts our list of dicts into text layout with 4 spaces indent.
      json.dump(habits_list, file, indent=4)
  except Exception:
    # Show an error pop-up window if the system cannot write the file.
    messagebox.showerror("Error", "Could not save your progress to the file!")


def print_to_screen(text_to_show):
  """Clears the text monitor widget and displays a fresh message string."""
  # Change state to NORMAL so Python can write text inside the Tkinter Text box.
  screen.config(state=tk.NORMAL)
  # Delete all existing text from index 1.0 (start) to tk.END (very end).
  screen.delete(1.0, tk.END)
  # Insert the new string variable at the very end of the text box layout.
  screen.insert(tk.END, text_to_show)
  # Change state back to DISABLED so the user cannot manually type inside it.
  screen.config(state=tk.DISABLED)


# ==============================================================================
# 3. BUTTON MAIN ACTIONS
# ==============================================================================


def view_habits():
  """Option 1: Compiles a clean text summary of all current tracked habits."""
  # If the length of the list is 0, it means no habits are active yet.
  if len(habits_list) == 0:
    # Send a helpful reminder notice string to the screen widget.
    print_to_screen(
        "\nNo habits tracked yet.\nChoose Option 2 to add one first!\n"
    )
    # Stop execution here, do not run the rest of this function.
    return

  # Start building a long text string with a header line.
  output_text = "--- CURRENT STREAKS ---\n\n"

  # Loop through every slot position in the habits list using index numbers.
  for i in range(len(habits_list)):
    # Grab the habit dictionary located at position 'i' in the list.
    current_habit = habits_list[i]
    # Extract keys out of the single habit dictionary.
    name = current_habit["name"]
    streak = current_habit["streak"]
    last_date = current_habit["last_date"]
    last_status = current_habit["last_status"]
    last_trigger = current_habit["last_trigger"]

    # Format data cleanly into lines and append them to output_text.
    # [i + 1] shifts 0-indexed positions to user-friendly numbers like.
    output_text += f"[{i + 1}] {name} | Streak: {streak} days\n"
    output_text += f"    Last Logged: {last_date}\n"

    # If last log was a failure (0) and there is a real reason recorded.
    if last_status == 0 and last_trigger != "None":
      output_text += f"    Last Relapse Trigger: {last_trigger}\n"

    # Add a blank separation line between habits.
    output_text += "\n"

  # Push the final built text block onto the visual GUI screen widget.
  print_to_screen(output_text)


def add_habit():
  """Option 2: Prompts user for a habit name and registers a new tracking dictionary."""
  # Check if our list size matches or exceeds the constant value 5.
  if len(habits_list) >= MAX_HABITS:
    # Show warning pop-up box to prevent adding more habits.
    messagebox.showwarning(
        "Limit Reached", "Limit reached! Focus on mastering your 5 core habits."
    )
    # Stop function execution right here.
    return

  # Open a standard GUI prompt box asking the user to type text input.
  input_name = simpledialog.askstring("Add Habit", "Enter habit name:")

  # Check if input exists and is not just empty whitespace characters.
  if input_name and input_name.strip():
    # Remove leading/trailing spaces and turn interior spaces into underscores.
    # Example input "Read Book " becomes clean_name "Read_Book"
    clean_name = input_name.strip().replace(" ", "_")

    # Set up a flag tracker variable to see if this name is already taken.
    name_exists = False
    # Loop through all existing dictionary objects in our list.
    for habit in habits_list:
      # Compare names converted to lowercase to avoid duplicates like "Gym" and "gym".
      if habit["name"].lower() == clean_name.lower():
        name_exists = True

    # If the flag changed to True, block registration process.
    if name_exists:
      # Show error dialog alert window.
      messagebox.showerror("Error", f"A habit named '{clean_name}' exists!")
      # Stop function execution here.
      return

    # Create a fresh standard key-value map dictionary object for this habit.
    new_habit_dict = {
        "name": clean_name,
        "streak": 0,
        "last_status": 1,
        "last_trigger": "None",
        "last_date": "Not_Started",
    }

    # Insert this new habit dictionary setup directly into our list array.
    habits_list.append(new_habit_dict)
    # Print status confirmation message string to UI monitor window.
    print_to_screen(f"\nHabit '{clean_name}' registered successfully!\n")
    # Instantly trigger view function to refresh layout visualization.
    view_habits()


def log_status():
  """Option 3: Logs daily success or failure status for a targeted habit."""
  # If list is empty, stop user because there is nothing to track status for.
  if len(habits_list) == 0:
    messagebox.showinfo("No Habits", "Add a habit using Option 2 first.")
    return

  # Create an option listing layout string to show inside the popup box.
  menu_options = "Select habit number to log:\n"
  for i in range(len(habits_list)):
    menu_options += f"{i + 1}. {habits_list[i]['name']}\n"

  # Ask user to pick a target habit number by typing it out.
  user_input = simpledialog.askstring("Select Habit", menu_options)
  # If user clicks cancel, exit function cleanly.
  if user_input is None:
    return

  try:
    # Convert typed text into a real integer and subtract 1 to get index.
    # Example: User types "1" -> choice_index becomes 0.
    choice_index = int(user_input) - 1
    # Check if number falls outside actual valid index bounds of the array list.
    if choice_index < 0 or choice_index >= len(habits_list):
      messagebox.showerror("Error", "Invalid selection number!")
      return
  except ValueError:
    # Runs if conversion fails because user typed alphabet characters.
    messagebox.showerror("Error", "Please type a valid number, not text.")
    return

  # Extract the targeted habit dictionary using our computed array index.
  selected_habit = habits_list[choice_index]
  # Fetch current date string using system clock helper function.
  today_date = get_today_date()

  # If user already ran a log action today, give an overwrite notice.
  if selected_habit["last_date"] == today_date:
    messagebox.showinfo(
        "Notice", "You already logged this today. Updating your entry..."
    )

  # Prompt user to choose between 1 (Success) and 0 (Failure).
  status_input = simpledialog.askstring(
      "Daily Status", "Did you succeed today?\n(1 = Yes, 0 = No/Relapsed):"
  )
  # If user clicks cancel, exit function safely.
  if status_input is None:
    return

  # Ensure string input matches exactly "1" or "0", otherwise block it.
  if status_input != "1" and status_input != "0":
    messagebox.showerror("Error", "You must enter exactly 1 or 0.")
    return

  # Convert validated input to a clean integer variable.
  status_num = int(status_input)
  # Set default starting text value for trigger reason.
  trigger_reason = "None"

  # If log value is failure (0), ask for a specific trigger reason.
  if status_num == 0:
    reason_input = simpledialog.askstring("Relapse", "What was the trigger?")
    # Clean up typed text reason if user filled it out.
    if reason_input and reason_input.strip():
      trigger_reason = reason_input.strip().replace(" ", "_")
    else:
      # Default placeholder if user left the text prompt blank.
      trigger_reason = "Unspecified_Trigger"

  # Math adjustments for streak counter:
  if status_num == 1:
    # Only add to streak if they haven't already advanced it today.
    if selected_habit["last_date"] != today_date:
      selected_habit["streak"] += 1
  else:
    # Set the habit's internal streak number directly to 0 in memory.
    selected_habit["streak"] = 0

  # Update the habit dictionary's status tracking key with the 1 or 0 value.
  selected_habit["last_status"] = status_num
  # Update the habit dictionary's tracking key with the clean trigger string.
  selected_habit["last_trigger"] = trigger_reason
  # Save today's system date string into the habit's tracking dictionary.
  selected_habit["last_date"] = today_date

  # Refresh the textual window monitor display to show the updated metrics.
  view_habits()
  # Pop up a clean desktop notification confirming the save operation worked.
  messagebox.showinfo("Updated", f"Status updated for {today_date}!")


def delete_habit():
  """Option 4: Removes a designated habit from the tracking index completely."""
  # Prevent running delete logic if there are zero tracking items in memory.
  if len(habits_list) == 0:
    # Pop up an informational alert box indicating no data items exist.
    messagebox.showinfo("No Habits", "No habits available to delete.")
    # Stop function execution right here.
    return

  # Build selector menu listing text structure for layout prompt box.
  menu_options = "Select habit number to delete:\n"
  # Loop across the list using array indexes to collect current habit names.
  for i in range(len(habits_list)):
    # Append each habit's numeric choice value and actual name to the block.
    menu_options += f"{i + 1}. {habits_list[i]['name']}\n"

  # Gather user selection number using a pop-up window prompt tool.
  user_input = simpledialog.askstring("Delete Habit", menu_options)
  # If the user clicks the cancel option button, exit the function cleanly.
  if user_input is None:
    # Stop running code immediately.
    return

  try:
    # Parse text entry into array offset position integer.
    delete_index = int(user_input) - 1
    # Check if number falls outside actual valid index bounds of the array list.
    if delete_index < 0 or delete_index >= len(habits_list):
      # Display an error message indicating selection index is out of bounds.
      messagebox.showerror("Error", "Invalid selection number!")
      # Stop execution loop.
      return
  except ValueError:
    # Runs if conversion fails because user typed alphabet characters.
    messagebox.showerror("Error", "Please type a valid number.")
    # Exit execution routine safely.
    return

  # .pop() extracts and removes the chosen item index directly from habits_list.
  removed = habits_list.pop(delete_index)
  # Print confirmation data and refresh GUI presentation frame layout.
  print_to_screen(f"\nHabit '{removed['name']}' successfully deleted!\n")
  # Run the display updater module to show changes on screen.
  view_habits()
  # Alert user via a pop-up panel that target item was removed from storage.
  messagebox.showinfo("Deleted", "Habit successfully removed!")


def save_and_exit():
  """Option 5: Exports memory data states securely and disposes the GUI pipeline."""
  # Call helper function to write our active array lists safely out to hard drive.
  save_data()
  # Close and terminate the Tkinter window process cleanly.
  window.destroy()


# ==============================================================================
# 4. TKINTER GUI APP WINDOW LAYOUT
# ==============================================================================
# Create the root Tkinter application canvas container window framework.
window = tk.Tk()
# Set application header bar title string.
window.title("DISCIPLINE & HABIT TRACKER")
# Configure pixel dimension layout size constraints (Width x Height).
window.geometry("440x620")
# Assign specific background color tone string using hex value format.
window.configure(bg="#1e1e2e")

# Run load data routine immediately at launch to rebuild active memory data state.
load_data()

# CRITICAL FIX: Intercept default window exit control button ('X') to auto-save file data.
window.protocol("WM_DELETE_WINDOW", save_and_exit)

# Header title banner layout label setup:
banner = tk.Label(
    window,
    text=(
        "==================================\nDISCIPLINE & HABIT"
        " TRACKER\n=================================="
    ),
    font=("Courier", 10, "bold"),
    bg="#1e1e2e",
    fg="#89b4fa",
    pady=10,
)
# Render the label inside the application frame.
banner.pack()

# Text output screen widget layout monitoring block:
screen = tk.Text(
    window,
    font=("Courier", 10),
    bg="#11111b",
    fg="#cdd6f4",
    height=14,
    width=46,
    bd=2,
    relief="sunken",
)
# Position the text block within the layout matrix grid.
screen.pack(pady=10, padx=10)

# Display application initialization message inside text container frame.
print_to_screen(
    "System Ready. Choose an option below.\nLoaded"
    f" {len(habits_list)} habit(s) from file data.\n"
)

# Button layout grouping structural container layout:
btn_frame = tk.Frame(window, bg="#1e1e2e")
# Attach structural layout block into window space frames.
btn_frame.pack(pady=5)

# Button 1 UI Component configuration:
tk.Button(
    btn_frame,
    text="1. View Active Habits & Streaks",
    command=view_habits,
    width=34,
    bg="#313244",
    fg="white",
    font=("Helvetica", 10, "bold"),
    pady=5,
).pack(pady=3)

# Button 2 UI Component configuration:
tk.Button(
    btn_frame,
    text=f"2. Add a New Habit (Max {MAX_HABITS})",
    command=add_habit,
    width=34,
    bg="#89b4fa",
    fg="#11111b",
    font=("Helvetica", 10, "bold"),
    pady=5,
).pack(pady=3)

# Button 3 UI Component configuration:
tk.Button(
    btn_frame,
    text="3. Log Daily Status (Success/Failure)",
    command=log_status,
    width=34,
    bg="#a6e3a1",
    fg="#11111b",
    font=("Helvetica", 10, "bold"),
    pady=5,
).pack(pady=3)

# Button 4 UI Component configuration:
tk.Button(
    btn_frame,
    text="4. Delete a Habit",
    command=delete_habit,
    width=34,
    bg="#fab387",
    fg="#11111b",
    font=("Helvetica", 10, "bold"),
    pady=5,
).pack(pady=3)

# Button 5 UI Component configuration:
tk.Button(
    btn_frame,
    text="5. Save & Exit",
    command=save_and_exit,
    width=34,
    bg="#f38ba8",
    fg="#11111b",
    font=("Helvetica", 10, "bold"),
    pady=5,
).pack(pady=3)

# Start engine listener framework loop to hold application window active.
window.mainloop()