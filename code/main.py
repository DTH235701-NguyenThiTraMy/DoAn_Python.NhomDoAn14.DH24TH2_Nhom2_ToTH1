import tkinter as tk
from tkinter import messagebox
from teacher_ui import open_teacher_management
from subject_ui import open_subject_management
from class_ui import open_class_management
from utils import center_window

def check_login():
    user = entry_user.get()
    pw = entry_pass.get()
    if user == "gv" and pw == "2025":
        login_win.destroy()
        open_main_menu()
    else:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

def open_main_menu():
    global root
    root = tk.Tk()
    root.title("Phần mềm quản lý trường học")
    center_window(root, 700, 400)
    root.configure(bg="#E3F2FD")

    tk.Label(root, text="CHÀO MỪNG ĐẾN VỚI PHẦN MỀM QUẢN LÝ GIÁO VIÊN",
             font=("Arial", 16, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=30)

    def make_button(text, cmd, bg="#36F1DE"):
        return tk.Button(root, text=text, width=25, height=2,
                         command=lambda: cmd(root, open_main_menu),
                         bg=bg, fg="black", font=("Arial", 11, "bold"),
                         relief="raised", cursor="hand2", activebackground="#4DB6AC")

    make_button("Quản lý giáo viên", open_teacher_management).pack(pady=10)
    make_button("Quản lý môn học", open_subject_management).pack(pady=10)
    make_button("Quản lý lớp", open_class_management).pack(pady=10)
    tk.Button(root, text="Thoát", width=25, height=2, command=root.destroy,
              bg="#B0BEC5", fg="black", font=("Arial", 11, "bold")).pack(pady=10)

   # root.mainloop()

# ===== Đăng nhập =====
login_win = tk.Tk()
login_win.title("Đăng nhập hệ thống")
center_window(login_win, 700, 350)
login_win.configure(bg="#E3F2FD")

lbl_title = tk.Label(login_win, text="ĐĂNG NHẬP HỆ THỐNG",
                     font=("Arial", 20, "bold"), bg="#E3F2FD", fg="#1565C0")
lbl_title.pack(pady=(20, 10))

frame_login = tk.Frame(login_win, bg="#FFFFFF", padx=20, pady=20, bd=2, relief="groove")
frame_login.pack(pady=10)

tk.Label(frame_login, text="Tên đăng nhập:", bg="#FFFFFF", fg="#0D47A1", 
         font=("Arial", 12)).grid(row=0, column=0, pady=8, sticky="e")
tk.Label(frame_login, text="Mật khẩu:", bg="#FFFFFF", fg="#0D47A1", 
         font=("Arial", 12)).grid(row=1, column=0, pady=8, sticky="e")

entry_user = tk.Entry(frame_login, width=30, font=("Arial", 12))
entry_user.grid(row=0, column=1, pady=8)
entry_pass = tk.Entry(frame_login, show="*", width=30, font=("Arial", 12))
entry_pass.grid(row=1, column=1, pady=8)

frame_buttons = tk.Frame(login_win, bg="#E3F2FD")
frame_buttons.pack(pady=20)

btn_login = tk.Button(frame_buttons, text="Đăng nhập", width=14, height=1,
                      bg="#36F1DE", fg="black", activebackground="#4DB6AC",
                      font=("Arial", 11, "bold"), cursor="hand2", relief="raised",
                      command=check_login)
btn_login.pack(side="left", padx=12)

btn_exit = tk.Button(frame_buttons, text="Thoát", width=14, height=1,
                     bg="#B0BEC5", fg="black", activebackground="#CFD8DC",
                     font=("Arial", 11, "bold"), cursor="hand2", relief="raised",
                     command=login_win.quit)
btn_exit.pack(side="left", padx=12)
 
login_win.mainloop()