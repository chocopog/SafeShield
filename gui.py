import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import os
from main import analyzeFile, analyzeFolder
from config import riskColors, riskOrder

selectedPath = None

def chooseFile():
    global selectedPath
    path = filedialog.askopenfilename()
    if path:
        selectedPath = path
        pathLabel.config(text=selectedPath)

def chooseFolder():
    global selectedPath
    path = filedialog.askdirectory()
    if path:
        selectedPath = path
        pathLabel.config(text=selectedPath)

def outputGui(text):
    outputBox.insert("end", text + "\n")

def updateRisk(risk, extra=""):
    color = riskColors.get(risk, "white")
    riskLabel.config(text=f"Overall Risk Level: {risk}{extra}", fg=color)

def runScan():
    if not selectedPath:
        outputBox.insert("end", "please select a file \n")
        return
    outputBox.delete("1.0", "end")
    riskLabel.config(text="Overall Risk Level: --", fg="white")

    if os.path.isdir(selectedPath):
        results = analyzeFolder(selectedPath, output=outputGui)

        counts = {level: 0 for level in riskOrder}
        worst = None

        for name, risk in results:
            if risk is None:
                continue
            counts[risk] += 1

            if worst is None or riskOrder.index(risk) > riskOrder.index(worst):
                worst = risk

        summary = " | ".join(f"{level}: {counts[level]}" for level in riskOrder)

        if worst:
            updateRisk(worst, extra=f"  ({summary})")
        else:
            riskLabel.config(text="No files could be scanned.", fg="white")

    else:
        risk = analyzeFile(selectedPath, output=outputGui)
        if risk:
            updateRisk(risk)
        else:
            riskLabel.config(text="Error scanning file.", fg="white")


root = tk.Tk()
root.config(bg="#1518c2")
root.geometry("600x500")
root.title("SAFESHIELD FILE ANALYZER")

heading = tk.Label(root, text="SafeShield File Analyzer", font=("Segoe UI", 16, "bold"), bg="#1518c2", fg="white")
heading.pack(pady=(15, 5))

pathLabel = tk.Label(root, text="no file or folder selected yet", font=("Segoe UI", 12), bg="#1518c2", fg="white")
pathLabel.pack()

buttonFile = tk.Button(root, text="choose file", command=chooseFile, bg="#4e517c")
buttonFile.pack()

buttonFolder = tk.Button(root, text="choose folder", command=chooseFolder, bg="#4e517c")
buttonFolder.pack()

buttonScan = tk.Button(root, text="Start scan", command=runScan, bg="#1565c0", fg="white", font=("Segoe UI", 11, "bold"))
buttonScan.pack()

riskLabel = tk.Label(root, text="Overall Risk Level: --", font=("Segoe UI", 13, "bold"), bg="#1518c2", fg="white")
riskLabel.pack(pady=10)

outputBox = scrolledtext.ScrolledText(root, wrap="word", height=15, bg="#4b92e2")
outputBox.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()