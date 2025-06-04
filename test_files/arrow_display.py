import tkinter as tk
import os

class KeyboardDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Simulation Display")
        self.root.geometry("400x200")
        self.root.configure(bg="black")

        self.label = tk.Label(root, text="Waiting...", font=("Helvetica", 32), bg="black", fg="white")
        self.label.pack(expand=True)

        self.last_status = ""
        self.update_display()

    def update_display(self):
        try:
            if os.path.exists("key_status.txt"):
                with open("key_status.txt", "r") as f:
                    status = f.read().strip()
            else:
                status = "Waiting..."

            if status != self.last_status:
                if status == "Turn Left":
                    self.label.config(text="← Left Key Simulated", fg="cyan")
                elif status == "Turn Right":
                    self.label.config(text="→ Right Key Simulated", fg="yellow")
                elif status == "Straight":
                    self.label.config(text="⇨ Straight", fg="white")
                else:
                    self.label.config(text="Waiting...", fg="white")
                self.last_status = status
        except Exception as e:
            print(f"Error reading status file: {e}")

        self.root.after(100, self.update_display)  # Poll every 100ms

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardDisplay(root)
    root.mainloop()
