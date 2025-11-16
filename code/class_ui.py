import tkinter as tk
from tkinter import ttk, messagebox
from utils import center_window
import mysql.connector
import re

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="qlgv"
    )

def open_class_management(root, open_main_menu):
    root.destroy()
    win = tk.Tk()
    win.title("Quản lý lớp")
    center_window(win, 750, 500)
    win.configure(bg="#E3F2FD")
    win.resizable(False, False)

    tk.Label(win, text="QUẢN LÝ LỚP", font=("Arial", 18, "bold"),
             bg="#E3F2FD", fg="#1565C0").pack(pady=15)

    # ===== Frame thông tin =====
    frame_info = tk.LabelFrame(win, text="Thông tin lớp", bg="#FFFFFF", fg="#0D47A1",
                               font=("Arial", 12, "bold"), padx=15, pady=10)
    frame_info.pack(padx=15, pady=10, fill="x")

    tk.Label(frame_info, text="Mã lớp:", bg="#FFFFFF", fg="#0D47A1").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_malop = tk.Entry(frame_info, width=10)
    entry_malop.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tên lớp:", bg="#FFFFFF", fg="#0D47A1").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_tenlop = tk.Entry(frame_info, width=25)
    entry_tenlop.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # ===== Frame danh sách =====
    frame_list = tk.LabelFrame(win, text="Danh sách lớp", bg="#FFFFFF", fg="#0D47A1",
                               font=("Arial", 12, "bold"), padx=5, pady=5)
    frame_list.pack(padx=15, pady=10, fill="both", expand=True)

    columns = ("malop", "tenlop")
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
        entry_malop.delete(0, tk.END)
        entry_tenlop.delete(0, tk.END)

    def load_data():
        for item in tree.get_children():
            tree.delete(item)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM lop ORDER BY malop")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()

    def them():
        malop = entry_malop.get().strip()
        tenlop = entry_tenlop.get().strip()

        # Kiểm tra dữ liệu trống
        if not malop or not tenlop:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập đầy đủ thông tin!")
            return

        # Kiểm tra mã lớp
        if not malop.startswith("L"):
            messagebox.showwarning("Lỗi", "Mã lớp phải bắt đầu bằng L")
            return

        # Kiểm tra tên lớp hợp lệ
        if re.search(r'\d{3,}', tenlop):
            messagebox.showwarning("Lỗi", "Tên lớp không hợp lệ")
            return

        conn = connect_db()
        cur = conn.cursor()

        # ---------- Kiểm tra mã lớp trùng ----------
        cur.execute("SELECT * FROM lop WHERE malop=%s", (malop,))
        if cur.fetchone():
            messagebox.showerror("Lỗi", f"Mã lớp {malop} đã tồn tại!")
            conn.close()
            return

        # ---------- Kiểm tra tên lớp trùng ----------
        cur.execute("SELECT * FROM lop WHERE tenlop=%s", (tenlop,))
        if cur.fetchone():
            messagebox.showerror("Lỗi", f"Tên lớp '{tenlop}' đã tồn tại!")
            conn.close()
            return

        # Thêm dữ liệu nếu hợp lệ
        try:
            cur.execute("INSERT INTO lop(malop, tenlop) VALUES (%s,%s)", (malop, tenlop))
            conn.commit()
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def xoa():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn lớp để xoá!")
            return

        malop = tree.item(selected)["values"][0]

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá lớp {malop}?"):
            return

        conn = connect_db()
        cur = conn.cursor()

        # Kiểm tra lớp có giáo viên chủ nhiệm không
        cur.execute("SELECT COUNT(*) FROM giaovien WHERE cnlop=%s", (malop,))
        if cur.fetchone()[0] > 0:
            messagebox.showwarning("Lỗi", f"Lớp {malop} đang có giáo viên chủ nhiệm, không thể xoá!")
            conn.close()
            return

        try:
            cur.execute("DELETE FROM lop WHERE malop=%s", (malop,))
            conn.commit()
            tree.delete(selected)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()



    def sua():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn lớp để sửa!")
            return
        messagebox.showinfo("Sửa", "Chỉnh sửa thông tin rồi nhấn Lưu.")

    def luu():
        malop = entry_malop.get().strip()
        tenlop = entry_tenlop.get().strip()
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE lop SET tenlop=%s WHERE malop=%s", (tenlop, malop))
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
        entry_malop.delete(0, tk.END); entry_malop.insert(0, values[0])
        entry_tenlop.delete(0, tk.END); entry_tenlop.insert(0, values[1])

    # ===== Tạo nút =====
    buttons = [
        ("Thêm", them), ("Sửa", sua), ("Lưu", luu),
        ("Hủy", huy), ("Xóa", xoa), ("Thoát", lambda: (win.destroy(), open_main_menu()))
    ]
    for idx, (text, cmd) in enumerate(buttons):
        if text == "Thoát":
            make_btn(text, cmd, bg="#B0BEC5").grid(row=0, column=idx, padx=5, pady=5)
        else:
            make_btn(text, cmd).grid(row=0, column=idx, padx=5, pady=5)

    tree.bind("<<TreeviewSelect>>", on_select)
    load_data()
    win.mainloop()
