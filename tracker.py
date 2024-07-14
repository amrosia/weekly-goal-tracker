import sys
import subprocess
import importlib.util

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def check_and_install(package):
    if importlib.util.find_spec(package) is None:
        install(package)
# Check and install required packages
required_packages = ['matplotlib', 'tkinter']
for package in required_packages:
    check_and_install(package)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class GoalTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Weekly Goal Tracker")
        
        self.data_file = 'goal_tracker_data.json'
        self.load_data()
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()
        
        self.set_goal_button = tk.Button(master, text="Set Weekly Goal", command=self.set_goal)
        self.set_goal_button.pack()
        
        self.update_progress_button = tk.Button(master, text="Update Daily Progress", command=self.update_progress)
        self.update_progress_button.pack()
        
        self.reset_button = tk.Button(master, text="Reset Session", command=self.reset_session)
        self.reset_button.pack()
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        if self.first_time:
            self.show_greeting()
        else:
            self.update_graph()
        
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.weekly_goal = data['weekly_goal']
                self.daily_progress = data['daily_progress']
                self.first_time = False
        else:
            self.weekly_goal = 0
            self.daily_progress = [0] * 7
            self.first_time = True
        self.days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        
    def save_data(self):
        data = {
            'weekly_goal': self.weekly_goal,
            'daily_progress': self.daily_progress
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)
        
    def set_goal(self):
        new_goal = simpledialog.askinteger("Weekly Goal", "Enter your weekly goal:")
        if new_goal is not None:
            self.weekly_goal = new_goal
            self.save_data()
            self.update_graph()
        
    def update_progress(self):
        day = simpledialog.askinteger("Update Progress", "Enter day number (1-7):", minvalue=1, maxvalue=7)
        if day is not None:
            lessons = simpledialog.askinteger("Update Progress", "Enter number of lessons completed:")
            if lessons is not None:
                self.daily_progress[day-1] = lessons
                self.save_data()
                self.update_graph()
        
    def update_graph(self):
        self.ax.clear()
        
        goal_line = [self.weekly_goal / 7 * i for i in range(8)]
        self.ax.plot(range(8), goal_line, color='gray', label='Goal')
        
        progress_line = [0] + [sum(self.daily_progress[:i+1]) for i in range(7)]
        self.ax.plot(range(8), progress_line, color='blue', label='Progress')
        
        self.ax.set_xticks(range(8))
        self.ax.set_xticklabels([''] + self.days)
        self.ax.set_ylim(0, max(self.weekly_goal, max(progress_line)) * 1.1)
        self.ax.set_title(f"Weekly Goal: {self.weekly_goal} lessons")
        self.ax.legend()
        
        if sum(self.daily_progress) >= self.weekly_goal:
            self.ax.text(0.5, 0.95, "You completed your weekly goal!", 
                         horizontalalignment='center', verticalalignment='center', 
                         transform=self.ax.transAxes, fontsize=12, color='green')
        
        self.canvas.draw()
        
    def reset_session(self):
        if messagebox.askyesno("Reset Session", "Are you sure you want to reset your session? This will clear all progress."):
            self.weekly_goal = 0
            self.daily_progress = [0] * 7
            self.save_data()
            self.update_graph()
            messagebox.showinfo("Reset Complete", "Your session has been reset.")
        
    def show_greeting(self):
        messagebox.showinfo("Welcome!", "Welcome to the Weekly Goal Tracker!\n\nTo get started, set your weekly goal using the 'Set Weekly Goal' button.")
        self.set_goal()
        
    def on_closing(self):
        self.save_data()
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GoalTracker(root)
    root.mainloop()
