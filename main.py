import datetime

class Task:
    def __init__(self, name, duration, deadline, description, resources=1):
        self.name = name
        self.duration = duration
        self.deadline = deadline
        self.description = description
        self.resources = resources
        self.completion_time = None

    
    def __str__(self):
        return f'Task: {self.name}\nDuration: {self.duration} hours\nDeadline: {self.deadline}\nDescription: {self.description}\nRequired Resources: {self.resources}'


#creating a priority queue to allow us to efficiently manage tasks based on their priority

import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0 #used to handle cases where multiple tasks have the same priority
    
    #when adding a task we're pushing a tuple
    def add_task(self, priority, task):
        heapq.heappush(self._queue, (priority, self._index, task))
        self._index += 1

    #pops the highest priority from the heap
    def remove_task(self):
        return heapq.heappop(self._queue)[-1]
    
    #checks if queue is empty
    def is_empty(self):
        return len(self._queue) == 0



#responsible for managing the tasks, scheduling them based on priority and deadlines and providing methods to interact
#with the task scheduler
class TaskScheduler:
    def __init__(self, num_resources):
        self.tasks = PriorityQueue()
        self.available_resources = num_resources
    
    def add_tasks(self, task):
        self.tasks.add_task(task.deadline, task)
    
    def get_next_task(self):
        if self.tasks_isempty():
            return None
        return self.tasks.remove_task()
    
    def display_tasks(self):
        if self.tasks.isempty():
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
            
            # Check if task has unresolved dependencies
            if not self._check_dependencies(task, scheduled_tasks):
            # Task has unresolved dependencies, re-add to the task scheduler
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
            print("Scheduled Tasks: ")
            for task in scheduled_tasks:
                print(task)
                print("---")

        

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

    def _execute_tasks(self, scheduled_tasks):
        current_time = datetime.datetime.now()
    
        for task in scheduled_tasks:
            task.completion_time = current_time + datetime.timedelta(hours=task.duration)
    
    def _handle_unscheduled_tasks(self, task):
        if not self._check_dependencies(task, []):
            print(f"Unscheduled Task: {task.name} (Unresolved dependencies)")
        elif self._check_deadline(task):
            print(f"Unscheduled Task: {task.name} (Exceeded deadline)")
        else:
            print(f"Unscheduled Task: {task.name} (Insufficient Resources)")
    




task = Task("Task Name", 2, datetime.datetime(2023, 6, 1), "Task description", 3)
scheduler = TaskScheduler(1)
print(task)
print(scheduler._assign_resources(task))



    


