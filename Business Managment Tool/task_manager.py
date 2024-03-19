'''
This Python program is a task management system that allows users to register, log in, add tasks, 
view tasks, and perform various task-related actions such as marking tasks as complete, editing task details, 
and generating reports. The program utilises text files to store user data and task information. 
Users can register with unique usernames and passwords, log in securely, and then interact with tasks 
according to their assigned roles. Administrative users have additional functionalities such as generating 
reports on task statistics, including the total number of tasks, completed tasks, uncompleted tasks, and overdue tasks.
The reports also provide insights into user-specific task statistics. The program provides a user-friendly interface 
with menu options for easy navigation and interaction. The admin login details are (admin;password)'''

import os
from datetime import datetime, date

# Define the date format for datetime objects.
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to write data to a file.
def write_to_file(filename, content):
    try:
        with open(filename, "w") as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to {filename}: {str(e)}")

# Loads tasks from the tasks.txt file, parses them, and constructs a list of tasks.
def load_tasks():
    task_list = []
    if os.path.exists("tasks.txt"):
        try:
            with open("tasks.txt", 'r') as task_file:
                task_info = task_file.read().strip().split("\n\n")
                for task_str in task_info:
                    task_components = task_str.strip().split("\n")
                    if len(task_components) == 6:
                        task = {
                            "username": task_components[0].split(": ")[1],
                            "title": task_components[1].split(": ")[1],
                            "description": task_components[2].split(": ")[1],
                            "due_date": datetime.strptime(task_components[3].split(": ")[1], DATETIME_STRING_FORMAT),
                            "assigned_date": datetime.strptime(task_components[4].split(": ")[1], DATETIME_STRING_FORMAT),
                            "completed": task_components[5].split(": ")[1] == "Yes"
                        }
                        task_list.append(task)
                    else:
                        print("Invalid task format:", task_str.strip())
        except Exception as e:
            print("Error loading tasks:", str(e))
    else:
        print("No tasks file found.")
    return task_list

# Loads user data from the user.txt file, parses it, and constructs a dictionary of usernames and passwords.
def load_users():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
    try:
        with open("user.txt", 'r') as user_file:
            user_data = user_file.read().split("\n")
        username_password = {}
        for user in user_data:
            if user:
                user_info = user.split(';')
                if len(user_info) == 2:
                    username, password = user_info
                    username_password[username] = password
        return username_password
    except Exception as e:
        print("Error loading users:", str(e))
        return {}

# Allows users to log in by verifying their username and password.
def login(username_password):
    while True:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
        else:
            print("Login Successful!")
            return curr_user

# Allows for registering a new user by prompting for a new username and password.
def reg_user(username_password):
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists. Please try a different username.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        try:
            with open("user.txt", "a") as out_file:
                out_file.write(f"\n{new_username};{new_password}")
        except Exception as e:
            print("Error registering user:", str(e))
    else:
        print("Passwords do not match")

# Allows users to add a new task by entering task details.
def add_task(curr_user, task_list):
    print("ADD TASK")
    task_username = input("Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    try:
        with open("tasks.txt", "a") as task_file:
            task_info = [
                f"Task assigned to: {new_task['username']}",
                f"Task title: {new_task['title']}",
                f"Task description: {new_task['description']}",
                f"Due date: {new_task['due_date'].strftime(DATETIME_STRING_FORMAT)}",
                f"Assigned date: {new_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}",
                f"Completed: {'Yes' if new_task['completed'] else 'No'}",
                ""
            ]
            task_file.write("\n".join(task_info))
            task_file.write("\n")
        print("Task successfully added.")
    except Exception as e:
        print("Error adding task:", str(e))

# Displays all tasks in the task list.
def view_all(task_list):
    print("VIEW ALL TASKS")
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Displays tasks assigned to the current user with an option to select a task for further action.
def view_mine(task_list, curr_user):
    print("VIEW MY TASKS")
    print("Your Tasks:")
    for idx, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            completion_status = 'Yes' if t['completed'] else 'No'  
            disp_str = f"Task {idx}: \n"
            disp_str += f"Title: \t\t {t['title']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Description: \n {t['description']}\n"
            disp_str += f"Completed: \t {completion_status}\n"  
            print(disp_str)
    return task_list

# Function to mark a task as complete.
def mark_task_complete(task_list, task_index):
    if 0 < task_index <= len(task_list):
        if not task_list[task_index - 1]['completed']:
            task_list[task_index - 1]['completed'] = True
            print("Task marked as complete.")
            update_tasks_file(task_list)
        else:
            print("Task is already marked as complete.")
    else:
        print("Invalid task index.")

# Function to edit the username of a task.
def edit_username(task_list, task_index):
    if 0 < task_index <= len(task_list):
        if not task_list[task_index - 1]['completed']:
            new_username = input("Enter new username to reassign the task: ")
            task_list[task_index - 1]['username'] = new_username
            update_tasks_file(task_list)
            print("Username updated successfully.")
        else:
            print("Completed tasks cannot be edited.")
    else:
        print("Invalid task index.")

# Function to edit the due date of a task.
def edit_due_date(task_list, task_index):
    if 0 < task_index <= len(task_list):
        if not task_list[task_index - 1]['completed']:
            new_due_date = input("Enter new due date for the task (YYYY-MM-DD): ")
            try:
                new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                task_list[task_index - 1]['due_date'] = new_due_date
                update_tasks_file(task_list)
                print("Due date updated successfully.")
            except ValueError:
                print("Invalid datetime format.")
        else:
            print("Completed tasks cannot be edited.")
    else:
        print("Invalid task index.")

# Function to generate reports on task statistics for admin users.
def generate_reports(task_list, username_password):
    try:
        total_tasks = len(task_list)
        if total_tasks == 0:
            print("No tasks available to generate reports.")
            return
        completed_tasks = sum(1 for t in task_list if t['completed'])
        uncompleted_tasks = total_tasks - completed_tasks
        today = date.today()
        overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < today)
        incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks != 0 else 0
        overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0
        with open("task_overview.txt", "w") as task_overview_file:
            task_overview_file.write(f"Total Tasks: {total_tasks}\n")
            task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
            task_overview_file.write(f"Uncompleted Tasks: {uncompleted_tasks}\n")
            task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
            task_overview_file.write(f"Incomplete Percentage: {incomplete_percentage:.2f}%\n")
            task_overview_file.write(f"Overdue Percentage: {overdue_percentage:.2f}%\n")
        
        # Generate user overview file.
        with open("user_overview.txt", "w") as user_overview_file:
            total_users = len(username_password)
            user_tasks = {}
            for t in task_list:
                if t['username'] not in user_tasks:
                    user_tasks[t['username']] = 1
                else:
                    user_tasks[t['username']] += 1
            for user, tasks in user_tasks.items():
                completed_user_tasks = sum(1 for t in task_list if t['username'] == user and t['completed'])
                incomplete_user_tasks = tasks - completed_user_tasks
                overdue_user_tasks = sum(1 for t in task_list if t['username'] == user and not t['completed'] and t['due_date'].date() < today)
                user_task_percentage = (tasks / total_tasks) * 100 if total_tasks != 0 else 0
                completed_user_task_percentage = (completed_user_tasks / tasks) * 100 if tasks != 0 else 0
                incomplete_user_task_percentage = (incomplete_user_tasks / tasks) * 100 if tasks != 0 else 0
                overdue_user_task_percentage = (overdue_user_tasks / tasks) * 100 if tasks != 0 else 0
                user_overview_file.write(f"User: {user}\n")
                user_overview_file.write(f"Total Tasks Assigned: {tasks}\n")
                user_overview_file.write(f"Percentage of Total Tasks: {user_task_percentage:.2f}%\n")
                user_overview_file.write(f"Percentage of Completed Tasks: {completed_user_task_percentage:.2f}%\n")
                user_overview_file.write(f"Percentage of Incomplete Tasks: {incomplete_user_task_percentage:.2f}%\n")
                user_overview_file.write(f"Percentage of Overdue Tasks: {overdue_user_task_percentage:.2f}%\n")
                user_overview_file.write("\n")
        
        print("Reports generated successfully.")
    except Exception as e:
        print(f"Error generating reports: {str(e)}")

# Displays statistics on task completion and overdue tasks.
def display_statistics():
    generate_reports(load_tasks(), load_users())  # Ensure reports are generated
    try:
        with open("task_overview.txt", "r") as task_overview_file:
            print(task_overview_file.read())
    except FileNotFoundError:
        print("Task overview file not found. Please generate reports.")

    try:
        with open("user_overview.txt", "r") as user_overview_file:
            print(user_overview_file.read())
    except FileNotFoundError:
        print("User overview file not found. Please generate reports.")

# Function to update tasks.txt file with the latest task information.
def update_tasks_file(task_list):
    try:
        with open("tasks.txt", "w") as task_file:
            for task in task_list:
                task_info = [
                    f"Task assigned to: {task['username']}",
                    f"Task title: {task['title']}",
                    f"Task description: {task['description']}",
                    f"Due date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}",
                    f"Assigned date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}",
                    f"Completed: {'Yes' if task['completed'] else 'No'}",
                    ""
                ]
                task_file.write("\n".join(task_info))
                task_file.write("\n")
    except Exception as e:
        print("Error updating tasks file:", str(e))

if __name__ == "__main__":
    # Load tasks and user data.
    task_list = load_tasks()
    username_password = load_users()

    # User login.
    curr_user = login(username_password)

    # Main loop for user interaction.
    while True:
        print()
        valid_choice = False  # Flag to track if the user's choice was valid.

        # Display menu options based on user role.
        if curr_user == 'admin':
            menu = input('''Select one of the following Options below:
            r - Register a new user
            a - Add a task
            va - View all tasks
            vm - View my tasks
            gr - Generate reports
            ds - Display statistics
            e - Exit
            : ''').lower()
        else:
            menu = input('''Select one of the following Options below:
            a - Add a task
            va - View all tasks
            vm - View my tasks
            e - Exit
            : ''').lower()

        if curr_user == 'admin':
            if menu == 'gr':
                generate_reports(task_list, username_password)
                valid_choice = True
            elif menu == 'ds':
                display_statistics()
                valid_choice = True

        if valid_choice:
            continue

        if menu == 'r':
            reg_user(username_password)
        elif menu == 'a':
            add_task(curr_user, task_list)
        elif menu == 'va':
            view_all(task_list)
        elif menu == 'vm':
            task_list = view_mine(task_list, curr_user)
            task_index = int(input("Enter the task number you want to perform action on (or -1 to return to the main menu): "))
            if task_index == -1:
                continue
            action = input("Enter 'u' to edit username, 'd' to edit due date: ").lower()
            if action == 'u':
                edit_username(task_list, task_index)
            elif action == 'd':
                edit_due_date(task_list, task_index)
            else:
                print("Invalid action.")
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")

