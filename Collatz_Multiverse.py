import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd 
import matplotlib.pyplot as mat


last_sequence = []
was_resumed = False
original_start=0
# Function to parse user input for scientific notation and exponents
def parse_collatz(val):
    val = val.replace(" ", "").lower()
    try:
        if "*" in val and "^" in val:
            base_part, rest = val.split("*")
            _, exponent_part = rest.split("^")
            
            
            if "." in base_part:
                
                return int(float(base_part) * (10 ** int(exponent_part)))
            else:
                return int(base_part) * (10 ** int(exponent_part))
        elif "^" in val:
                base_part, exponent_part = val.split("^")
                return int(base_part) ** int(exponent_part) 
        
        return int(float(val))
    except (ValueError, IndexError, OverflowError):
        return None
def collatz():
    global last_sequence, was_resumed, original_start
    was_resumed=False
    last_sequence = []

    try:
        q=parse_collatz(inpt_1.get()) if inpt_1.get() else 3
        r=parse_collatz(inpt_2.get()) if inpt_2.get() else 1
        
        n=parse_collatz(inpt_3.get())

        if n is None or n == 0:
            result.config(text="Error: Enter a valid integer and make it not larger than your RAM can handle", bg="black", fg="red")
            return 
        original_start=n
        last_sequence = [n]
        seen = {n}
        is_loop=False
        escaped=False
        while True:
            if n % 2 == 0: 
                n //= 2
            else: n = q * n + r
            if n==1:
                last_sequence.append(n)
                break # Reached 1
            if n in seen: 
                last_sequence.append(n)
                is_loop=True
                break # Loop detected

            last_sequence.append(n)
            seen.add(n)
            if len(last_sequence) > 10000 or abs(n) > 1e100: 
                escaped = True # Mark that we didn't actually finish the sequence
                break
        
        # Determine the correct status message
        if escaped:
            status = " (ESCAPE VELOCITY - Limits Hit)"
            bg_color = "black"
            fg_color = "yellow"
            btn_continue.pack_forget()
        elif is_loop:
            status = " (Loop Detected)"
            bg_color = "tomato"
            fg_color = "black"
            btn_continue.pack_forget()
        else:
            status = " (Reached 1)"
            bg_color = "lime"
            fg_color = "black"
            btn_continue.pack(pady=5)
        update_display(status, bg_color, fg_color)
        max_val=max(last_sequence)
        steps=len(last_sequence)
     
        # Check the actual number of steps in the list
        if steps >= 200 or max_val > 1e18: 
             display_text=f"Status: {status} | Steps: {steps} | Max Value: {max_val} \nSequence too long to display (Export for details)."
        else:
             sequence_str = ", ".join(map(str, last_sequence))
             display_text=f"Status: {status} | Steps: {steps} | Max Value: {max_val} \nSequence: {sequence_str}"
        result.config(text=display_text)
        btn_export.pack(pady=5)
        btn_visualize.pack(pady=5)
    except Exception as e:
        result.config(text=f"Error: {str(e)}", bg="black", fg="red")
def continue_simulation():
    global last_sequence, was_resumed
    was_resumed = True
    q = parse_collatz(inpt_1.get()) or 3
    r = parse_collatz(inpt_2.get()) or 1
    n = last_sequence[-1] # Start from 1 
    seen = set(last_sequence)
    
    
    while True:
        if n % 2 == 0: n //= 2
        else: n = q * n + r
        
        if n in seen or len(last_sequence) > 10000 or abs(n) > 1e100:
            last_sequence.append(n)
            break
        last_sequence.append(n)
        seen.add(n)
    
    update_display("Resumed: Escape Velocity Reached!", "black", "yellow")
    btn_continue.pack_forget()
def update_display(status, bg, fg):
    steps, max_v = len(last_sequence), max(last_sequence)
    msg = f"Status: {status} | Steps: {steps} | Max: {max_v}"
    if steps < 100: msg += f"\nSeq: {last_sequence}"
    result.config(text=msg, bg=bg, fg=fg)
    btn_export.pack(pady=5)
    btn_visualize.pack(pady=5)
def visualize_graph():
    global last_sequence, was_resumed, original_start
    if not last_sequence:
        return
    
    q=inpt_1.get() if inpt_1.get() else "3"
    r=inpt_2.get() if inpt_2.get() else "1"
    is_massive = max(last_sequence) > 1e18

    fig, ax = mat.subplots()
    if was_resumed:
        title_text = f"Collatz Path for {original_start}\nConjecture: {q}n+{r}\n(Resumed from 1 to find higher loops/escape)"
    else:
        title_text = f"Collatz Sequence for {original_start}\nConjecture: {q}n+{r}"
    manager = fig.canvas.manager
    try:
        manager.window.state('zoomed')          # Windows
    except AttributeError:
        try:
            manager.full_screen_toggle()        # macOS/Linux fallback
        except AttributeError:
            pass
    if is_massive:
       ax.plot(last_sequence, color='royalblue', linewidth=1)
       ax.set_yscale('log')
       ax.set_ylabel("Value (log₁₀ scale)")
       title_text += "\n(Logarithmic Scale)"
    else:
        ax.plot(last_sequence, marker='o', linestyle='-', color='royalblue')
        ax.set_ylabel("Value")
        
    ax.set_title(title_text)
    mat.xlabel("Steps")
    mat.grid(True, linestyle='--', alpha=0.7)

    if not is_massive:
        import matplotlib.ticker as ticker
        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True) 
        formatter.set_powerlimits((-3, 4)) 
        ax.yaxis.set_major_formatter(formatter)
    
    mat.show()
    btn_visualize.pack_forget()
    btn_continue.pack_forget()
    result.config(text="Graph closed. You can still export the data or enter a new number to start again though.", bg="turquoise", fg="black")
def export_csv():
    q=inpt_1.get() if inpt_1.get() else "3"
    r=inpt_2.get() if inpt_2.get() else "1"
    global last_sequence
    if not last_sequence:
        messagebox.showwarning("No Data", "Please click Submit first to generate a sequence!")
        return
    
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if filepath:
        df = pd.DataFrame(
            {"Step": range(len(last_sequence))
             , "Value": last_sequence
             , "Multiplier": q, 
             "Modifier": r}
            )
        df.to_csv(filepath, index=False)
        result.config(text=f"Data for {q}n+{r} exported successfully!", bg="lime")


root=tk.Tk()
root.geometry("600x600")
root.title("Collatz Conjecture Visualizer")
root.config(bg="turquoise")
lbl=tk.Label(root,text="Enter in the first box the multiplier, second box the modifier\n Third box the starting number", bg="turquoise", fg="black")
lbl.pack()
lbl_2=tk.Label(root,text="(Use * and ^ for scientific notation, e.g., 1.5*10^6 or 2^10)", bg="turquoise", fg="black")
lbl_2.pack()
lbl_3=tk.Label(root,text="Default Multiplier=3, Modifier=1 if left blank", bg="turquoise", fg="black")
lbl_3.pack()
lbl_4=tk.Label(root,text="WARNING: Don't try extremely large numbers that your RAM can't handle!", bg="turquoise", fg="red")
lbl_4.pack()
inpt_1=tk.Entry(root)
inpt_1.pack(padx=10, pady=5)
inpt_2=tk.Entry(root)
inpt_2.pack(padx=10, pady=5)
inpt_3=tk.Entry(root)
inpt_3.pack(padx=10, pady=5)
btn=tk.Button(root,text="Submit",command=collatz, bg="royal blue",fg="black")
btn.pack()
btn_continue=tk.Button(root,text="Continue Simulation",command=continue_simulation, bg="dark violet",fg="white")
result=tk.Label(root,text="",bg="turquoise", wraplength=580)
result.pack()
btn_export = tk.Button(root, text="Export CSV", command=export_csv, bg="forest green", fg="white")
btn_visualize = tk.Button(root, text="Visualize Graph", command=visualize_graph, bg="dark orange", fg="white")
root.mainloop()