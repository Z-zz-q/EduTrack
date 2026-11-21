import tkinter as tk

root = tk.Tk()
root.title("EduTrack")
root.geometry("800x600")

welcome_label = tk.Label(
    root,
    text="Welcome to EduTrack!",
    font=("Arial", 20)
)
welcome_label.pack(pady=30)

root.mainloop()