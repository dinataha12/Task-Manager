import json
from datetime import datetime, date

class Task:
    def __init__(self, title, description, due_date, task_id, status):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.task_id = task_id
        self.status = status

    def __str__(self):
        return f"ID: {self.task_id}, Title: {self.title}, Description: {self.description}, Due Date: {self.due_date}, Status: {self.status}"

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "status": self.status
        }


class PersonalTask(Task):
    CATEGORIES = ["Study", "Personal", "Shopping", "Family", "Sports"]

    def __init__(self, title, description, due_date, task_id, status, category):
        super().__init__(title, description, due_date, task_id, status)
        if category not in self.CATEGORIES:
            self.CATEGORIES.append(category)
        self.category = category

    def __str__(self):
        return f"[Personal-{self.category}]{super().__str__()}"

    def get_task_type(self):
        return "personal"

    def to_dict(self):
        task_data = super().to_dict()
        task_data["category"] = self.category
        return task_data

    @staticmethod
    def get_category():
        print("Choose a category:")
        print("0. Add a new category ")
        for i, category in enumerate(PersonalTask.CATEGORIES, 1):
            print(f"{i}. {category}")
        while True:
            try:
                category_choice = int(input("Enter the number of the category (or 0 to add a new category): "))
                if category_choice == 0:
                    category = input("Enter a new category: ")
                    PersonalTask.CATEGORIES.append(category)
                    return category
                elif 1 <= category_choice <= len(PersonalTask.CATEGORIES):
                    return PersonalTask.CATEGORIES[category_choice - 1]
                else:
                    print("Invalid choice. Please enter a number between 1 and", len(PersonalTask.CATEGORIES), "or 0 to add a new category.")
            except ValueError:
                print("Invalid input. Please enter a number.")


class WorkTask(Task):
    def __init__(self, title, description, due_date, task_id, status, priority):
        super().__init__(title, description, due_date, task_id, status)
        self.priority = priority

    def __str__(self):
        return f"[Work-Priority:{self.priority}]{super().__str__()}"

    def get_task_type(self):
        return "work"

    def to_dict(self):
        task_data = super().to_dict()
        task_data["priority"] = self.priority
        return task_data


class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                tasks_data = json.load(f)
            tasks = []
            for task_data in tasks_data:
                if "type" in task_data:
                    if task_data["type"] == "personal":
                        tasks.append(PersonalTask(task_data["title"], task_data["description"], date.fromisoformat(task_data["due_date"]), task_data["task_id"],task_data["status"] ,task_data["category"]))
                    elif task_data["type"] == "work":
                        tasks.append(WorkTask(task_data["title"], task_data["description"], date.fromisoformat(task_data["due_date"]), task_data["task_id"], task_data["status"], task_data["priority"]))
                else:
                    print("Invalid task data. Skipping...")
            return tasks
        except FileNotFoundError:
            return []

    def save_tasks(self):
        tasks_data = []
        for task in self.tasks:
            task_data = task.to_dict()
            task_data["type"] = task.get_task_type()
            tasks_data.append(task_data)
        with open(self.filename, 'w') as f:
            json.dump(tasks_data, f, indent = 4)

    def add_task(self, task):
        if not self.tasks:
            task.task_id = 1
            task.status = "Incomplete"
        else:
            task.task_id = max(task.task_id for task in self.tasks) + 1
            task.status = "Incomplete"
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                break
        self.save_tasks()

    def update_task(self, task_id, title=None, description=None, due_date=None, status=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if title:
                    task.title = title
                if description:
                    task.description = description
                if due_date:
                    task.due_date = due_date
                if status:
                    task.status = status
                self.save_tasks()
                return
        raise ValueError("Task not found")

    def print_tasks(self):
        print("1. Print Personal Tasks")
        print("2. Print Work Tasks")
        print("3. Print All Tasks")

        choice = input("Choose an option: ")

        if choice == "1":
            print("Personal tasks:")
            personal_tasks = [task for task in self.tasks if task.get_task_type() == "personal"]
            if not personal_tasks:
                print("No Personal Tasks found.")
            for task in personal_tasks:
                print(task)

        elif choice == "2":
            print("Work tasks:")
            work_tasks = [task for task in self.tasks if task.get_task_type() == "work"]
            if not work_tasks:
                print("No Work Tasks found.")
            for task in work_tasks:
                print(task)

        elif choice == "3":
            print("All tasks:")
            if not self.tasks:
                print("No tasks found.")
            for task in self.tasks:
                print(task)
        else:
            print("Invalid option. Please try again.")


def get_valid_date(prompt):
    while True:
        print(prompt)
        year = int(input("Enter year (2022-2030): "))
        if 2024 <= year <= 2030:
            month = int(input("Enter month (1-12): "))
            if 1 <= month <= 12:
                day = int(input("Enter day (1-31): "))
                if 1 <= day <= 31:
                    try:
                        due_date = date(year, month, day)
                        if due_date >= date.today():
                            return due_date
                        else:
                            print("Invalid date. Please enter a date from today onwards.")
                    except ValueError:
                        print("Invalid date. Please enter a valid day for the month.")
                else:
                    print("Invalid day. Please enter a day between 1 and 31.")
            else:
                print("Invalid month. Please enter a month between 1 and 12.")
        else:
            print("Invalid year. Please enter a year between 2024 and 2030.")


def main():
    task_manager = TaskManager("tasks.json")

    while True:
        print("1. Add task")
        print("2. Remove task")
        print("3. Update task")
        print("4. Print tasks")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            task_type = input("Enter task type (Personal, Work): ").lower()
            if task_type == "personal":
                while True:
                    try:
                        title = input("Enter task title: ")
                        if title:
                            break
                        else:
                             print("Invalid Input Please Enter Your Task Title")
                    except Exception as error:
                        print(f"an errort had occured: {error}")
                description = input("Enter task description: ")
                due_date = get_valid_date("Enter task due date (YYYY-MM-DD) ")
                category = PersonalTask.get_category()
                task = PersonalTask(title, description, due_date, len(task_manager.tasks) + 1, task_manager.tasks, category)
                task_manager.add_task(task)
            elif task_type == "work":
                while True:
                    try:
                        title = input("Enter task title: ")
                        if title:
                            break
                        else:
                             print("Invalid Input Please Enter Your Task Title")
                    except Exception as error:
                        print(f"an errort had occured: {error}")
                description = input("Enter task description: ")
                due_date = get_valid_date("Enter task due date (YYYY-MM-DD) ")
                priority_List = ["High" , "Medium" , "Low"]
                priority = input("Enter task priority")
                while True:
                        for i, priority in enumerate(priority_List, 1):
                            print(f"{i}. {priority}")
                        try:
                            priority_number = int(input("Enter the number of the priority : "))
                            if 1 <= priority_number <= len(priority_List):
                                priority = priority_List[priority_number - 1]
                                break
                            else:
                                print("Invalid Input Please Enter a valid priority number")
                        except ValueError:
                            print("Invalid Input Please Enter Your Priority Number")
                task = WorkTask(title, description, due_date, len(task_manager.tasks) + 1, task_manager.tasks, priority)
                task_manager.add_task(task)
            else:
                print("Invalid task type. Please try again.")
                continue

            print("Task added successfully")

        elif choice == "2":
            print("All tasks:")
            for i, task in enumerate(task_manager.tasks, 1):
                print(f"{i}. {task.title}")
            task_number = int(input("Enter the number of the task to remove: "))
            if task_number == 0:
                continue

            if task_number > task.task_id:
                print("invalid task")

            else:
                task = task_manager.tasks[task_number - 1]
                rem = input(f"Are you sure you want to remove task tasks{[task_number - 1]} press Y (or press enter to keep current): ").lower()

                task_manager.remove_task(task.task_id)
                print("Task removed successfully")

        elif choice == "3":
            print("All tasks:")
            for i, task in enumerate(task_manager.tasks, 1):
                print(f"{i}. {task.title}")
            while True:
                try:
                    task_number = int(input("Enter the number of the task to update: "))
                except ValueError:
                    print("Invalid Input Please Enter Your Task Number")
                    continue
                if task_number in range(1, len(task_manager.tasks) +1):
                    break
                else:
                    print("Invalid Task Number, Please Enter Your Task Number")
            task = task_manager.tasks[task_number - 1]
            title = input("Enter new task title (or press enter to keep current): ")
            description = input("Enter new task description (or press enter to keep current): ")
            due_date = input("If you want to add new task date press Y (or press enter to keep current): ").lower()
            while True:
                if due_date == 'y':
                    due_date = str(get_valid_date("Enter task due date (YYYY-MM-DD) "))
                else:
                    break
            status_List = ["Incomplete" , "Complete" , "In Progress"]
            status = input(f"If you want to change you task status press Y (or press enter to keep current): ").lower()
            while True:
                if status == 'y':
                    for i, status in enumerate(status_List, 1):
                        print(f"{i}. {status}")
                    status_number = int(input("Enter the number of the status to update: "))
                    status = status_List[status_number - 1]
                else:
                    break
            try:
                task_manager.update_task(task.task_id, title if title else None, description if description else None, date.fromisoformat(due_date) if due_date else None, status if status else None)
                print("Task updated successfully")
            except ValueError:
                print("Task not found")

        elif choice == "4":
            task_manager.print_tasks()

        elif choice == "5":
            print("Thanks for Choosing SIC Task Manager :) ")
            print("Goodbye!")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()