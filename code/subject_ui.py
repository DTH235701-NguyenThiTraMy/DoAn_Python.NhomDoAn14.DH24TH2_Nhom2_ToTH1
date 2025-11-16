import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from utils import center_window
import re

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="qlgv"
    )

def open_subject_management(root, open_main_menu):
    root.destroy()
    win = tk.Tk()
    win.title("Quản lý môn học")
    center_window(win, 700, 500)
    win.configure(bg="#E3F2FD")
    win.resizable(False, False)

    tk.Label(win, text="QUẢN LÝ MÔN HỌC",
             font=("Arial", 18, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=15)

    # ===== Frame thông tin =====
    frame_info = tk.LabelFrame(win, text="Thông tin môn học", bg="#FFFFFF", fg="#0D47A1",
                               font=("Arial", 12, "bold"), padx=15, pady=10)
    frame_info.pack(padx=15, pady=10, fill="x")

    tk.Label(frame_info, text="Mã môn:", bg="#FFFFFF", fg="#0D47A1").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mamon = tk.Entry(frame_info, width=10)
    entry_mamon.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tên môn:", bg="#FFFFFF", fg="#0D47A1").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_tenmon = tk.Entry(frame_info, width=25)
    entry_tenmon.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # ===== Frame danh sách =====
    frame_list = tk.LabelFrame(win, text="Danh sách môn học", bg="#FFFFFF", fg="#0D47A1",
                               font=("Arial", 12, "bold"), padx=5, pady=5)
    frame_list.pack(padx=15, pady=10, fill="both", expand=True)

    columns = ("mamon", "tenmon")
    tree = ttk.Treeview(frame_list, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150, anchor="center")
    tree.pack(padx=5, pady=5, fill="both", expand=True)

    # ===== Frame nút =====
    frame_btn = tk.Frame(win, bg="#E3F2FD")
    frame_btn.pack(padx=15, pady=10, fill="x")
    for i in range(6):
        frame_btn.columnconfigure(i, weight=1)

    def make_btn(text, cmd=None, col=0, bg="#36F1DE"):
        btn = tk.Button(frame_btn, text=text, bg=bg, fg="black",
                        font=("Arial", 10, "bold"), cursor="hand2",
                        relief="raised", activebackground="#4DB6AC", command=cmd)
        btn.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
        return btn

    # ===== Hàm CRUD =====
    def clear_input():
        entry_mamon.delete(0, tk.END)
        entry_tenmon.delete(0, tk.END)

    def load_data():
        for item in tree.get_children():
            tree.delete(item)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM monhoc ORDER BY mamon")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()

    def them():
        mamon = entry_mamon.get().strip()
        tenmon = entry_tenmon.get().strip()
        if not mamon or not tenmon:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập đầy đủ thông tin!")
            return
        if not mamon.startswith("MH"):
            messagebox.showwarning("Lỗi", "Mã môn phải bắt đầu MH")
            return
        if re.search(r'\d', tenmon):
            messagebox.showwarning("Lỗi", "Tên môn không được chứa số")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO monhoc(mamon, tenmon) VALUES (%s,%s)", (mamon, tenmon))
            conn.commit()
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def xoa():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn môn học để xoá!")
            return
        mamon = tree.item(selected)["values"][0]
        conn = connect_db()
        cur = conn.cursor()
        try:
            # Xóa tất cả liên kết trong giaovien_monhoc trước
            cur.execute("DELETE FROM giaovien_monhoc WHERE mamon=%s", (mamon,))
            cur.execute("DELETE FROM monhoc WHERE mamon=%s", (mamon,))
            conn.commit()
            load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def sua():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn môn học để sửa!")
            return
        messagebox.showinfo("Sửa", "Chỉnh sửa thông tin rồi nhấn Lưu.")

    def luu():
        mamon = entry_mamon.get().strip()
        tenmon = entry_tenmon.get().strip()
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE monhoc SET tenmon=%s WHERE mamon=%s", (tenmon, mamon))
            conn.commit()
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def huy():
        clear_input()

    def on_select(event):
        selected = tree.selection()
        if not selected: return
        values = tree.item(selected)["values"]
        entry_mamon.delete(0, tk.END); entry_mamon.insert(0, values[0])
        entry_tenmon.delete(0, tk.END); entry_tenmon.insert(0, values[1])

    # ===== Tạo nút =====
    buttons = [
        ("Thêm", them), ("Sửa", sua), ("Lưu", luu),
        ("Hủy", huy), ("Xóa", xoa), ("Thoát", lambda: (win.destroy(), open_main_menu()))
    ]
    for idx, (text, cmd) in enumerate(buttons):
        make_btn(text, cmd, bg="#B0BEC5" if text=="Thoát" else "#36F1DE").grid(row=0, column=idx, padx=5, pady=5)

    tree.bind("<<TreeviewSelect>>", on_select)
    load_data()
    win.mainloop()
