import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd 
import matplotlib.pyplot as mat

# Global Variables
last_sequence = []
current_loop_members = []
was_resumed = False
original_start = 0

# Parsing Function
def parse_collatz(val):
    val = val.replace(" ", "").lower()
    try:
        if "*10^" in val:
            base, exp = val.split("*10^")
            return int(float(base) * (10 ** int(exp)))
        elif "**" in val:
            base, exp = val.split("**")
            if "*10" in base:
                base_num = float(base.replace("*10", ""))
                return int(base_num * (10 ** int(exp)))
            return int(float(base) ** int(exp))
        elif "^" in val:
            base, exp = val.split("^")
            return int(float(base) ** int(exp))
        elif "e" in val:
            return int(float(val))
        return int(float(val))
    except (ValueError, IndexError, OverflowError):
        return None

# UI Update Logic 
def update_ui_state(status, bg, fg, is_loop=False, loop_members=None):
    global last_sequence, current_loop_members
    current_loop_members = loop_members if loop_members else []
    steps = len(last_sequence)
    max_v = max(last_sequence) if last_sequence else 0
    
    display_max = f"{max_v:.5e}" if abs(max_v) > 1e15 else str(max_v)
    msg = f"Status: {status}\nSteps: {steps} | Max Value: {display_max}"
    
    if is_loop and loop_members:
        loop_str = ", ".join(map(str, loop_members[:50]))
        if len(loop_members) > 50: loop_str += "... (See Export)"
        msg += f"\n\nLoop Detected ({len(loop_members)} steps):\n[{loop_str}]"

    if steps < 400 and abs(max_v) <= 1e14: 
        if not is_loop: msg += f"\n\nFull Sequence: {last_sequence}"
    else:
        msg += "\n\n(Sequence too long for display - Use 'Export CSV' for full data)"

    result.config(state='normal')
    result.delete(1.0, tk.END)
    result.insert(tk.INSERT, msg)
    result.config(bg=bg, fg=fg, state='disabled')
    
    btn_export.pack(pady=5)
    btn_visualize.pack(pady=5)
    
    if "Reached 1" in status:
        btn_continue.pack(pady=5)
    else:
        btn_continue.pack_forget()

# Main Collatz Simulation 
def collatz():
    global last_sequence, was_resumed, original_start
    was_resumed = False
    
    q = parse_collatz(inpt_1.get()) if inpt_1.get() else 3
    r = parse_collatz(inpt_2.get()) if inpt_2.get() else 1
    n = parse_collatz(inpt_3.get())

    if n is None or n == 0:
        messagebox.showerror("Error", "Enter a valid starting number (n != 0)")
        return

    original_start = n
    last_sequence = [n]
    seen = {n}
    loop_members = []

    try:
        while True:
            n = n // 2 if n % 2 == 0 else q * n + r
            if n == 1:
                last_sequence.append(n)
                update_ui_state("Reached 1", "lime", "black")
                break
            if n in seen:
                last_sequence.append(n)
                curr = n
                while True:
                    loop_members.append(curr)
                    curr = curr // 2 if curr % 2 == 0 else q * curr + r
                    if curr == n: break
                update_ui_state("Loop Detected", "tomato", "black", True, loop_members)
                break
            
            last_sequence.append(n)
            seen.add(n)
            if len(last_sequence) > 15000 or abs(n) > 1e100:
                update_ui_state("Escape Velocity Hit (Limits)", "black", "yellow")
                break
    except (OverflowError, MemoryError):
        messagebox.showerror("Hardware Limit", "RAM capacity exceeded.")

# Continue Simulation 
def continue_simulation():
    global last_sequence, was_resumed
    was_resumed = True
    q = parse_collatz(inpt_1.get()) if inpt_1.get() else 3
    r = parse_collatz(inpt_2.get()) if inpt_2.get() else 1
    
    n = last_sequence[-1]
    seen = set(last_sequence)
    loop_members = []

    try:
        while True:
            n = n // 2 if n % 2 == 0 else q * n + r
            if n in seen:
                last_sequence.append(n)
                curr = n
                while True:
                    loop_members.append(curr)
                    curr = curr // 2 if curr % 2 == 0 else q * curr + r
                    if curr == n: break
                update_ui_state("Loop Detected after Resuming", "tomato", "black", True, loop_members)
                break
            last_sequence.append(n)
            seen.add(n)
            if len(last_sequence) > 30000 or abs(n) > 1e100:
                update_ui_state("Escape Velocity (Limits)", "black", "yellow")
                break
    except (OverflowError, MemoryError):
        messagebox.showerror("Limit", "RAM capacity exceeded.")

# Visualization & Export 
def visualize_graph():
    global last_sequence
    mat.close('all')
    fig, ax = mat.subplots(figsize=(10, 6))
    ax.plot(last_sequence, color='royalblue', linewidth=1.5)
    if max(last_sequence) > 1e15: ax.set_yscale('log')
    ax.set_title(f"Collatz Path for {original_start}")
    ax.grid(True, linestyle='--', alpha=0.6)
    mat.show()

def export_csv():
    global last_sequence, current_loop_members
    filepath = filedialog.asksaveasfilename(defaultextension=".csv")
    if filepath:
        is_loop_val = [val in current_loop_members for val in last_sequence]
        df = pd.DataFrame({
            "Step": range(len(last_sequence)),
            "Value": last_sequence,
            "Is_In_Loop": is_loop_val
        })
        df.to_csv(filepath, index=False)
        messagebox.showinfo("Export", "Sequence data saved successfully.")

def clear_display():
    global last_sequence
    last_sequence = []
    result.config(state='normal')
    result.delete(1.0, tk.END)
    result.config(state='disabled', bg="turquoise")
    for widget in [btn_continue, btn_export, btn_visualize]: widget.pack_forget()
    for entry in [inpt_1, inpt_2, inpt_3]: entry.delete(0, tk.END)

# UI Setup 
root = tk.Tk()
root.geometry("700x950") 
root.title("Collatz Conjecture Visualizer")
root.config(bg="turquoise")


tk.Label(root, text="Collatz Conjecture Multiverse Simulator", 
         font=("Helvetica", 16, "bold"), bg="turquoise", fg="black").pack(pady=10)

tk.Label(root, text="Enter in the first box the multiplier, second box the modifier\n Third box the starting number", 
         bg="turquoise", fg="black").pack()

tk.Label(root, text="Scientific Notation is allowed", 
         bg="turquoise", fg="black").pack()

tk.Label(root, text="Default Multiplier=3, Modifier=1 if left blank", 
         bg="turquoise", fg="black").pack()

tk.Label(root, text="Unspeakably large numbers may give inaccurate results for your RAM's limitations,\n check README for what is recommended for accurate results.", 
         bg="turquoise", fg="black").pack(pady=5)

tk.Label(root, text="WARNING: Don't try extremely large numbers that your RAM can't handle!", 
         bg="turquoise", fg="red", font=("Helvetica", 10, "bold")).pack()

inpt_1 = tk.Entry(root, justify='center'); inpt_1.pack(padx=10, pady=5)
inpt_2 = tk.Entry(root, justify='center'); inpt_2.pack(padx=10, pady=5)
inpt_3 = tk.Entry(root, justify='center'); inpt_3.pack(padx=10, pady=5)

btn = tk.Button(root, text="Submit", command=collatz, bg="royal blue", fg="white", width=15)
btn.pack(pady=10)

btn_continue = tk.Button(root, text="Continue Simulation", command=continue_simulation, bg="dark violet", fg="white")

result = scrolledtext.ScrolledText(root, height=10, width=80, state='disabled', font=("Times New Roman", 10))
result.pack(padx=10, pady=10)

btn_visualize = tk.Button(root, text="Visualize Graph", command=visualize_graph, bg="dark orange", fg="white")
btn_export = tk.Button(root, text="Export CSV", command=export_csv, bg="forest green", fg="white")

btn_clear = tk.Button(root, text="Clear All", command=clear_display, bg="red", fg="white")
btn_clear.pack(pady=10)

root.mainloop()