import tkinter as tk
from tkinter import messagebox
import time
import threading
import math
 
class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("蕃茄鐘")
 
        self.work_time = tk.DoubleVar(value=25.0)
        self.break_time = tk.DoubleVar(value=5.0)
        self.show_notification = tk.BooleanVar(value=True)
        self.always_on_top = tk.BooleanVar(value=False)
        self.auto_start = tk.BooleanVar(value=False)
        self.current_phase = tk.StringVar(value="未開始")
        self.time_left = tk.StringVar(value="00:00")
 
        self.is_running = False
        self.is_paused = False
        self.timer_thread = None
 
        self.create_widgets()
 
    def create_widgets(self):
        tk.Label(self.root, text="工作時間(分鐘)").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.work_time, width=7).grid(row=0, column=1)
 
        tk.Label(self.root, text="休息時間(分鐘)").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.break_time, width=7).grid(row=1, column=1)
 
        tk.Checkbutton(self.root, text="跳出提醒", variable=self.show_notification).grid(row=0, column=2)
        tk.Checkbutton(self.root, text="視窗置頂", variable=self.always_on_top, command=self.toggle_always_on_top).grid(row=1, column=2)
       
        tk.Button(self.root, text="開始", command=self.start).grid(row=2, column=0)
        tk.Button(self.root, text="暫停", command=self.pause_timer).grid(row=2, column=1)
        tk.Button(self.root, text="重設", command=self.reset_timer).grid(row=2, column=2)
        # tk.Button(self.root, text="開始工作", command=self.start_work).grid(row=2, column=0)
        # tk.Button(self.root, text="開始休息", command=self.start_break).grid(row=2, column=1)
        # tk.Button(self.root, text="暫停", command=self.pause_timer).grid(row=2, column=2)
        # tk.Button(self.root, text="重設", command=self.reset_timer).grid(row=2, column=3)
 
        # tk.Label(self.root, text="-" * 60).grid(row=3, columnspan=4)
 
        # tk.Label(self.root, text="目前階段:").grid(row=4, column=0)
        tk.Label(self.root, textvariable=self.current_phase).grid(row=4, column=0)
 
        # tk.Label(self.root, text=" |     剩餘時間:").grid(row=4, column=1)
        tk.Label(self.root, textvariable=self.time_left).grid(row=4, column=1, columnspan=2)
 
    def toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top.get())
 
    def start(self):
        if self.current_phase.get() == "工作":
                self.start_break()
        else:
            self.start_work()
 
    def start_work(self):
        self.current_phase.set("工作")
        self.start_timer(math.ceil(self.work_time.get() * 60), "工作時間到！")
 
    def start_break(self):
        self.current_phase.set("休息")
        self.start_timer(math.ceil(self.break_time.get() * 60), "休息時間到！")
 
    def start_timer(self, duration, message):
        if self.timer_thread and self.timer_thread.is_alive():
            self.is_running = False
            if threading.current_thread() is not self.timer_thread:
                self.timer_thread.join(timeout=1)
        self.is_running = True
        self.is_paused = False
        self.timer_thread = threading.Thread(target=self.countdown, args=(duration, message))
        self.timer_thread.start()
 
    def countdown(self, duration, message):
        while duration > 0 and self.is_running:
            if not self.is_paused:
                mins, secs = divmod(duration, 60)
                secs = math.ceil(secs)  # 將秒數進位為整數
                self.time_left.set(f'{mins:02d}:{secs:02d}')
                time.sleep(1)
                duration -= 1
 
        if self.is_running:
            self.time_left.set("00:00")
            if self.show_notification.get():
                self.show_message(message)
            if self.current_phase.get() == "工作":
                self.start_break()
            else:
                self.start_work()
 
    def pause_timer(self):
        self.is_paused = not self.is_paused
 
    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
        self.time_left.set("00:00")
        self.current_phase.set("未開始")
 
    def show_message(self, message):
        messagebox.showinfo("通知", message)
 
if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("200x200")
    root.resizable(False, False)
    app = PomodoroTimer(root)
    root.mainloop()