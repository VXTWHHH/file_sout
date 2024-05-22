import sys
from pathlib import Path
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def sout_a(sout, s):
    path = Path(sout)
    for item in path.iterdir():
        if item.is_file():
            print(f'{s}{item.name}')
        elif item.is_dir():
            print(f'{s}{item.name}')
            sout_a(os.path.join(sout, item.name), '    ' + s)

def run_sout_a():
    directory = entry_directory.get()
    prefix = entry_prefix.get()

    if not Path(directory).exists():
        messagebox.showerror("错误", "指定的目录不存在")
        return

    # 清空文本框
    text_output.delete(1.0, tk.END)

    # 重定向标准输出到文本框
    class StdoutRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, string):
            self.text_widget.insert(tk.END, string)
            self.text_widget.see(tk.END)

        def flush(self):
            pass

    sys.stdout = StdoutRedirector(text_output)

    # 运行函数
    sout_a(directory, prefix)

    # 恢复标准输出
    sys.stdout = sys.__stdout__

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

# 创建主窗口
root = tk.Tk()
root.title("sout_a GUI")

# 创建并放置控件
tk.Label(root, text="目录路径:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_directory = tk.Entry(root, width=50)
entry_directory.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="浏览...", command=browse_directory).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="前缀字符串:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_prefix = tk.Entry(root, width=50)
entry_prefix.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="运行", command=run_sout_a).grid(row=2, column=0, columnspan=3, pady=10)

text_output = tk.Text(root, wrap=tk.NONE, width=80, height=20)
text_output.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# 运行主循环
root.mainloop()
