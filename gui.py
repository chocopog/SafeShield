import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import os
from main import analyzeFile, analyzeFolder
from config import Risk_colors, Risk_order

selected_path = None

def choosefile():
    global selected_path
    path = filedialog.askopenfilename()
    if path:
        selected_path = path
        label1.config(text=selected_path)

def choosefolder():
    global selected_path
    path = filedialog.askdirectory()
    if path:
        selected_path = path
        label1.config(text=selected_path)

def output_gui(text):
    output_box.insert("end", text + "\n")

def update_risk_label(risk_level, extra_text=""):
    color = Risk_colors.get(risk_level, "white")
    risk_label.config(text=f"Overall Risk Level: {risk_level}{extra_text}", fg=color)

def run_scan():
    if not selected_path:
        output_box.insert("end", "please select a file \n")
        return
    output_box.delete("1.0", "end")
    risk_label.config(text="Overall Risk Level: --", fg="white")

    if os.path.isdir(selected_path):
        results = analyzeFolder(selected_path, output=output_gui)

        counts = {level: 0 for level in Risk_order}
        worst_seen = None

        for filename, risk_level in results:
            if risk_level is None:
                continue
            counts[risk_level] += 1

            if worst_seen is None or Risk_order.index(risk_level) > Risk_order.index(worst_seen):
                worst_seen = risk_level

        summary_text = " | ".join(f"{level}: {counts[level]}" for level in Risk_order)

        if worst_seen:
            update_risk_label(worst_seen, extra_text=f"  ({summary_text})")
        else:
            risk_label.config(text="No files could be scanned.", fg="white")

    else:
        risk_level = analyzeFile(selected_path, output=output_gui)
        if risk_level:
            update_risk_label(risk_level)
        else:
            risk_label.config(text="Error scanning file.", fg="white")


root = tk.Tk()
root.config(bg="#1518c2")
root.geometry("600x500")
root.title("SAFESHIELD FILE ANALYZER")

heading = tk.Label(root, text="SafeShield File Analyzer", font=("Segoe UI", 16, "bold"), bg="#1518c2", fg="white")
heading.pack(pady=(15, 5))

label1 = tk.Label(root, text="no file or folder selected yet", font=("Segoe UI", 12), bg="#1518c2", fg="white")
label1.pack()

button_file = tk.Button(root, text="choose file", command=choosefile, bg="#4e517c")
button_file.pack()

button_folder = tk.Button(root, text="choose folder", command=choosefolder, bg="#4e517c")
button_folder.pack()

button_scan = tk.Button(root, text="Start scan", command=run_scan, bg="#1565c0", fg="white", font=("Segoe UI", 11, "bold"))
button_scan.pack()

risk_label = tk.Label(root, text="Overall Risk Level: --", font=("Segoe UI", 13, "bold"), bg="#1518c2", fg="white")
risk_label.pack(pady=10)

output_box = scrolledtext.ScrolledText(root, wrap="word", height=15, bg="#4b92e2")
output_box.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()