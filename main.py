import datetime
import heapq
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Task:
    def __init__(self, name, duration, deadline, description, resources=1, dependencies= None):
        self.name = name
        self.duration = duration
        self.deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d")
        self.description = description
        self.resources = resources
        self.completion_time = None
        self.dependencies = dependencies if dependencies else []

    def __str__(self):
        return f'Task: {self.name}\nDuration: {self.duration} hours\nDeadline: {self.deadline}\nDescription: {self.description}\nRequired Resources: {self.resources}'


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def add_task(self, priority, task):
        heapq.heappush(self._queue, (priority, self._index, task))
        self._index += 1

    def remove_task(self):
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0


class TaskScheduler:
    def __init__(self, num_resources):
        self.tasks = PriorityQueue()
        self.available_resources = num_resources

    def add_task(self, task):
        self.tasks.add_task(task.deadline, task)

    def get_next_task(self):
        if self.tasks.is_empty():
            return None
        return self.tasks.remove_task()

    def display_tasks(self):
        if self.tasks.is_empty():
            print("No tasks scheduled")
        else:
            while not self.tasks.is_empty():
                task = self.tasks.remove_task()
                print(task)
                print("---")

    def schedule_tasks(self):
        scheduled_tasks = []

        while not self.tasks.is_empty():
            task = self.tasks.remove_task()

            if not self._check_dependencies(task, scheduled_tasks):
                self.add_task(task)
                continue

            if self._check_deadline(task):
                print(f"Task {task.name} exceeds its deadline. Skipping...")
                continue

            if not self._assign_resources(task):
                print(f"Insufficient resources to schedule task '{task.name}'. Skipping...")
                continue

            scheduled_tasks.append(task)

        if not scheduled_tasks:
            print("No tasks to schedule")
        else:
            print("Scheduled Tasks:")
            for task in scheduled_tasks:
                print(task)
                print("---")

        return scheduled_tasks

    def _check_dependencies(self, task, scheduled_tasks):
        for dependency in task.dependencies:
            if dependency not in scheduled_tasks:
                return False
        return True

    def _check_deadline(self, task):
        current_time = datetime.datetime.now()
        return task.deadline < current_time

    def _assign_resources(self, task):
        if task.resources <= self.available_resources:
            self.available_resources -= task.resources
            return True
        return False


# class TaskSchedulerGUI:
#     def __init__(self):
#         self.window = tk.Tk()
#         self.window.title("Task Scheduler")

#         self.style = ttk.Style()
#         self.style.configure("TLabel", font=("Helvetica", 12))
#         self.style.configure("TEntry", font=("Helvetica", 12))
#         self.style.configure("TButton", font=("Helvetica", 12))

#         self.task_name_label = ttk.Label(self.window, text="Task Name:")
#         self.task_name_label.pack(pady=10)
#         self.task_name_entry = ttk.Entry(self.window)
#         self.task_name_entry.pack(pady=5)

#         self.duration_label = ttk.Label(self.window, text="Duration (hours):")
#         self.duration_label.pack(pady=10)
#         self.duration_entry = ttk.Entry(self.window)
#         self.duration_entry.pack(pady=5)

#         self.deadline_label = ttk.Label(self.window, text="Deadline:")
#         self.deadline_label.pack(pady=10)
#         self.deadline_entry = ttk.Entry(self.window)
#         self.deadline_entry.pack(pady=5)

#         self.description_label = ttk.Label(self.window, text="Description:")
#         self.description_label.pack(pady=10)
#         self.description_entry = ttk.Entry(self.window)
#         self.description_entry.pack(pady=5)

#         self.add_button = ttk.Button(self.window, text="Add Task", command=self.add_task)
#         self.add_button.pack(pady=10)

#         self.show_tasks_button = ttk.Button(self.window, text="Show Tasks", command=self.show_tasks)
#         self.show_tasks_button.pack(pady=10)

#         self.task_scheduler = TaskScheduler(num_resources=5)

#         self.task_list = tk.Listbox(self.window, width=50)

#         self.task_tree = ttk.Treeview(self.window)
#         self.task_tree["columns"] = ("name", "duration", "deadline", "description")
#         self.task_tree.heading("#0", text="ID")
#         self.task_tree.heading("name", text="Name")
#         self.task_tree.heading("duration", text="Duration (hours)")
#         self.task_tree.heading("deadline", text="Deadline")
#         self.task_tree.heading("description", text="Description")
#         self.task_tree.pack(pady=10)
        
#         self.add_button = ttk.Button(self.window, text="Add Task", command=self.add_task)
#         self.add_button.pack(pady=10)

#         self.show_tasks_button = ttk.Button(self.window, text="Show Tasks", command=self.show_tasks)
#         self.show_tasks_button.pack(pady=10)

#         self.delete

#     def add_task(self):
#         task_name = self.task_name_entry.get()
#         duration = self.duration_entry.get()
#         deadline = self.deadline_entry.get()
#         description = self.description_entry.get()

#         task = Task(task_name, duration, deadline, description)
#         self.task_scheduler.add_task(task)

#         messagebox.showinfo("Task Added", "Task has been added to the scheduler.")

#         self.task_name_entry.delete(0, tk.END)
#         self.duration_entry.delete(0, tk.END)
#         self.deadline_entry.delete(0, tk.END)
#         self.description_entry.delete(0, tk.END)

#     def show_tasks(self):
#         self.task_tree.delete(*self.task_tree.get_children())
#         scheduled_tasks = self.task_scheduler.schedule_tasks()
#         for i, task in enumerate(scheduled_tasks):
#             self.task_tree.insert("", "end", text=str(i+1), values=(task.name, task.duration, task.deadline, task.description))

#     def clear_task_list(self):
#         self.task_list.delete(0, tk.END)

#     def run(self):
#         self.window.mainloop()


# scheduler_gui = TaskSchedulerGUI()
# scheduler_gui.run()
