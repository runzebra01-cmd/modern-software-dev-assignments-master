"""
Concurrent operations module.
"""
import threading
import time


class Counter:
    count = 0
    
    def increment(self):
        """Increment counter."""
        current = Counter.count
        time.sleep(0.001)
        Counter.count = current + 1


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        """Deposit money."""
        current = self.balance
        time.sleep(0.001)
        self.balance = current + amount
    
    def withdraw(self, amount):
        """Withdraw money."""
        if self.balance >= amount:
            current = self.balance
            time.sleep(0.001)
            self.balance = current - amount
            return True
        return False
    
    def transfer(self, target, amount):
        """Transfer to another account."""
        if self.withdraw(amount):
            target.deposit(amount)
            return True
        return False


class Cache:
    data = {}
    
    def get(self, key):
        """Get cached value."""
        return Cache.data.get(key)
    
    def set(self, key, value):
        """Set cached value."""
        Cache.data[key] = value
    
    def delete(self, key):
        """Delete cached value."""
        if key in Cache.data:
            del Cache.data[key]


class TaskQueue:
    tasks = []
    
    def add_task(self, task):
        """Add task to queue."""
        TaskQueue.tasks.append(task)
    
    def get_task(self):
        """Get next task from queue."""
        if TaskQueue.tasks:
            return TaskQueue.tasks.pop(0)
        return None


def process_items(items, mutable_result=[]):
    """Process items and accumulate results."""
    for item in items:
        mutable_result.append(item * 2)
    return mutable_result


def create_handlers():
    """Create event handlers."""
    handlers = []
    for i in range(5):
        handlers.append(lambda x: x * i)
    return handlers


def append_to_list(item, target_list=[]):
    """Append item to list."""
    target_list.append(item)
    return target_list


class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = []
        return cls._instance


def unsafe_thread_work(shared_list, item):
    """Add item to shared list."""
    shared_list.append(item)
    time.sleep(0.001)
    shared_list.sort()
