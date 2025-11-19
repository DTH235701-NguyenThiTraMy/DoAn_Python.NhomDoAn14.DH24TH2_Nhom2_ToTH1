import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from utils import center_window
import mysql.connector
import re
import pandas as pd

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="qlgv"
    )

def open_teacher_management(root, open_main_menu):
    root.destroy()
    win = tk.Tk()
    win.title("Quản lý giáo viên")
    center_window(win, 1000, 600)
    win.configure(bg="#E3F2FD")
    win.resizable(True, True)

    # ===== Tiêu đề =====
    tk.Label(win, text="QUẢN LÝ GIÁO VIÊN THPT",
             font=("Arial", 18, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=15)
    # ===== Frame danh sách =====
    frame_list = tk.LabelFrame(win, text="Danh sách giáo viên", bg="#FFFFFF", fg="#0D47A1",
                               font=("Arial", 12, "bold"), padx=5, pady=5)
    frame_list.pack(padx=15, pady=10, fill="both", expand=True)

    columns = ("maso","holot","ten","phai","ngaysinh","monhoc","cnlop")
    tree = ttk.Treeview(frame_list, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True)
    
    tree.heading("maso", text="Mã giáo viên")
    tree.heading("holot", text="Họ lót")
    tree.heading("ten", text="Tên")
    tree.heading("phai", text="Phái")
    tree.heading("ngaysinh", text="Ngày sinh")
    tree.heading("monhoc", text="Môn học")
    tree.heading("cnlop", text="Chủ nhiệm lớp")


    # ===== Frame nút =====
    frame_btn = tk.Frame(win, bg="#E3F2FD")
    frame_btn.pack(pady=10)

    def make_btn(text, cmd=None, bg="#36F1DE"):
        return tk.Button(frame_btn, text=text, width=10, bg=bg, fg="black",
                         font=("Arial", 10, "bold"), cursor="hand2",
                         relief="raised", activebackground="#4DB6AC", command=cmd)

    # ===== Frame thông tin =====
    frame_info = tk.LabelFrame(win, text="Thông tin giáo viên", bg="#FFFFFF", fg="#0D47A1",
                               font=("Arial", 12, "bold"), padx=15, pady=10)
    frame_info.pack(padx=15, pady=10, fill="x")

    # Entry và Combobox/Listbox
    entry_maso = tk.Entry(frame_info, width=12)
    entry_holot = tk.Entry(frame_info, width=25)
    entry_ten = tk.Entry(frame_info, width=15)
    date_entry = DateEntry(frame_info, width=12, date_pattern="yyyy-mm-dd", selectbackground="#1976D2",
    selectforeground="white")
    gender_var = tk.StringVar(value="Nam")
    gvcn_var = tk.StringVar(value="Không")
    cnlop_combo = ttk.Combobox(frame_info, width=15)
    list_monhoc = tk.Listbox(frame_info, selectmode="multiple", width=30, height=4, exportselection=False)

    # ===== Hàm bật/tắt CN lớp =====
    def toggle_cnlop():
        if gvcn_var.get() == "Có":
            cnlop_combo.config(state="readonly")
        else:
            cnlop_combo.set("")
            cnlop_combo.config(state="disabled")

    # ===== Gắn nhãn và grid =====
    # Hàng 0
    tk.Label(frame_info, text="Mã số:", bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="Môn giảng dạy:", bg="#FFFFFF").grid(row=0, column=4, padx=5, pady=5, sticky="w")  
    tk.Label(frame_info, text="GVCN", bg="#FFFFFF").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    tk.Radiobutton(frame_info, text="Có", variable=gvcn_var, value="Có", bg="#FFFFFF", command=toggle_cnlop).grid(row=0, column=3, sticky="w")
    tk.Radiobutton(frame_info, text="Không", variable=gvcn_var, value="Không", bg="#FFFFFF", command=toggle_cnlop).grid(row=0, column=3, padx=60, sticky="w")
    tk.Label(frame_info, text="Chủ nhiệm lớp", bg="#FFFFFF").grid(row=0, column=5, padx=5, pady=5, sticky="w")
    cnlop_combo.grid(row=0, column=6, padx=5, pady=5, sticky="w")
    
    # Hàng 1
    list_monhoc.grid(row=1, column=4, rowspan=2, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="Họ lót:", bg="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_holot.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="Tên:", bg="#FFFFFF").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="Tìm kiếm:", bg="#FFFFFF").grid(row=1, column=5, padx=5, pady=5, sticky="w")
    entry_search = tk.Entry(frame_info, width=15)
    entry_search.grid(row=1, column=6, padx=5, pady=5, sticky="w")

    # Hàng 2
    tk.Label(frame_info, text="Phái:", bg="#FFFFFF").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam", bg="#FFFFFF").grid(row=2, column=1, sticky="w")
    tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ", bg="#FFFFFF").grid(row=2, column=1, padx=60, sticky="w")
    tk.Label(frame_info, text="Ngày sinh:", bg="#FFFFFF").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    date_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    toggle_cnlop()

    # ===== Load môn và lớp =====
    def load_monhoc():
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT mamon, tenmon FROM monhoc ORDER BY mamon")
        rows = cur.fetchall()
        list_monhoc.delete(0, tk.END)
        global mon_dict
        mon_dict = {tenmon: mamon for mamon, tenmon in rows}
        for tenmon in mon_dict.keys():
            list_monhoc.insert(tk.END, tenmon)
        conn.close()

    def load_lop():
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT malop FROM lop")
        cnlop_combo['values'] = [row[0] for row in cur.fetchall()]
        conn.close()

    load_monhoc()
    load_lop()

    # ===== Frame danh sách =====
    frame_list = tk.LabelFrame(win, text="Danh sách giáo viên", bg="#FFFFFF", fg="#0D47A1",
                               font=("Arial", 12, "bold"), padx=5, pady=5)
    frame_list.pack(padx=15, pady=10, fill="both", expand=True)

    columns = ("maso","holot","ten","phai","ngaysinh","monhoc","cnlop")
    tree = ttk.Treeview(frame_list, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True)
    
    tree.heading("maso", text="Mã giáo viên")
    tree.heading("holot", text="Họ lót")
    tree.heading("ten", text="Tên")
    tree.heading("phai", text="Phái")
    tree.heading("ngaysinh", text="Ngày sinh")
    tree.heading("monhoc", text="Môn học")
    tree.heading("cnlop", text="Chủ nhiệm lớp")

    # ===== Frame nút =====
    frame_btn = tk.Frame(win, bg="#E3F2FD")
    frame_btn.pack(pady=10)

    def make_btn(text, cmd=None, bg="#36F1DE"):
        return tk.Button(frame_btn, text=text, width=10, bg=bg, fg="black",
                         font=("Arial", 10, "bold"), cursor="hand2",
                         relief="raised", activebackground="#4DB6AC", command=cmd)

    # ===== Hàm CRUD =====
    def clear_input():
        entry_maso.delete(0, tk.END)
        entry_holot.delete(0, tk.END)
        entry_ten.delete(0, tk.END)
        gender_var.set("Nam")
        date_entry.set_date("2000-01-01")
        gvcn_var.set("Không")
        cnlop_combo.set("")
        cnlop_combo.config(state="disabled")
        list_monhoc.selection_clear(0, tk.END)

    def load_data():
        for item in tree.get_children():
            tree.delete(item)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT g.maso, g.holot, g.ten, g.phai, g.ngaysinh,
                   GROUP_CONCAT(m.tenmon SEPARATOR ', ') AS monhoc,
                   g.cnlop
            FROM giaovien g
            LEFT JOIN giaovien_monhoc gm ON g.maso = gm.maso
            LEFT JOIN monhoc m ON gm.mamon = m.mamon
            GROUP BY g.maso
            ORDER BY g.maso
        """)
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
    def tim_kiem():
        maso = entry_search.get().strip()
        if not maso:
            messagebox.showwarning("Thiếu dữ liệu", "Hãy nhập mã giáo viên để tìm!")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT g.maso, g.holot, g.ten, g.phai, g.ngaysinh,
                GROUP_CONCAT(m.tenmon SEPARATOR ', ') AS monhoc,
                g.cnlop
            FROM giaovien g
            LEFT JOIN giaovien_monhoc gm ON g.maso = gm.maso
            LEFT JOIN monhoc m ON gm.mamon = m.mamon
            WHERE g.maso = %s
            GROUP BY g.maso
        """, (maso,))
        row = cur.fetchone()
        conn.close()

        for item in tree.get_children():
            tree.delete(item)

        if row:
            tree.insert("", tk.END, values=row)
        else:
            messagebox.showerror("Không tìm thấy", f"Không có giáo viên mã: {maso}")

    def them():
        maso = entry_maso.get().strip()
        holot = entry_holot.get().strip()
        ten = entry_ten.get().strip()
        if not maso or not holot or not ten:
            messagebox.showwarning("Thiếu dữ liệu","Nhập đầy đủ thông tin!")
            return
        if not maso.startswith("GV"):
            messagebox.showwarning("Lỗi","Mã giáo viên phải bắt đầu GV")
            return
        if not re.fullmatch(r"[A-Za-zÀ-ỹ\s]+", holot):
            messagebox.showwarning("Lỗi","Họ lót chỉ chứa chữ và khoảng trắng")
            return
        if not re.fullmatch(r"[A-Za-zÀ-ỹ\s]+", ten):
            messagebox.showwarning("Lỗi","Tên chỉ chứa chữ và khoảng trắng")
            return

        phai = gender_var.get()
        ngaysinh = date_entry.get()
        cnlop = cnlop_combo.get() if gvcn_var.get()=="Có" else None
        selected_monhoc = [mon_dict[list_monhoc.get(i)] for i in list_monhoc.curselection()]

        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM giaovien WHERE maso=%s", (maso,))
        if cur.fetchone():
            messagebox.showerror("Lỗi", f"Mã giáo viên {maso} đã tồn tại!")
            conn.close()
            return
        if cnlop:
            cur.execute("SELECT COUNT(*) FROM giaovien WHERE cnlop=%s", (cnlop,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Lỗi", f"Lớp {cnlop} đã có giáo viên chủ nhiệm")
                conn.close()
                return
        try:
            cur.execute("INSERT INTO giaovien(maso, holot, ten, phai, ngaysinh, cnlop) VALUES (%s,%s,%s,%s,%s,%s)",
                        (maso, holot, ten, phai, ngaysinh, cnlop))
            for mamon in selected_monhoc:
                cur.execute("INSERT INTO giaovien_monhoc(maso, mamon) VALUES (%s,%s)", (maso, mamon))
            conn.commit()
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def xoa():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn","Hãy chọn giáo viên để xoá!")
            return

        maso = tree.item(selected)["values"][0]

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá giáo viên {maso}?"):
            return

        conn = connect_db()
        cur = conn.cursor()

        # Kiểm tra giáo viên là chủ nhiệm lớp
        cur.execute("SELECT COUNT(*) FROM lop WHERE malop IN (SELECT cnlop FROM giaovien WHERE maso=%s)", (maso,))
        if cur.fetchone()[0] > 0:
            messagebox.showwarning("Lỗi", f"Giáo viên {maso} đang là chủ nhiệm lớp, không thể xoá!")
            conn.close()
            return

        try:
            cur.execute("DELETE FROM giaovien WHERE maso=%s", (maso,))
            conn.commit()
            tree.delete(selected)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()


    def on_select(event):
        selected = tree.selection()
        if not selected: return
        values = tree.item(selected)["values"]
        entry_maso.delete(0, tk.END); entry_maso.insert(0, values[0])
        entry_holot.delete(0, tk.END); entry_holot.insert(0, values[1])
        entry_ten.delete(0, tk.END); entry_ten.insert(0, values[2])
        gender_var.set(values[3])
        date_entry.set_date(values[4])
        cnlop_combo.set(values[6] if values[6] else "")
        if values[6]:
            gvcn_var.set("Có")
            cnlop_combo.config(state="readonly")
        else:
            gvcn_var.set("Không")
            cnlop_combo.config(state="disabled")
        monchon = values[5].split(", ") if values[5] else []
        list_monhoc.selection_clear(0, tk.END)
        for i, tenmon in enumerate(list_monhoc.get(0, tk.END)):
            if tenmon in monchon:
                list_monhoc.selection_set(i)

    def sua():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn","Hãy chọn giáo viên để sửa!")
            return
        messagebox.showinfo("Sửa","Chỉnh sửa thông tin rồi nhấn LƯU.")

    def luu():
        maso = entry_maso.get().strip()
        holot = entry_holot.get().strip()
        ten = entry_ten.get().strip()
        if not re.fullmatch(r"[A-Za-zÀ-ỹ\s]+", holot) or not re.fullmatch(r"[A-Za-zÀ-ỹ\s]+", ten):
            messagebox.showwarning("Lỗi","Họ tên chỉ chứa chữ và khoảng trắng")
            return

        phai = gender_var.get()
        ngaysinh = date_entry.get()
        cnlop = cnlop_combo.get() if gvcn_var.get()=="Có" else None
        selected_monhoc = [mon_dict[list_monhoc.get(i)] for i in list_monhoc.curselection()]

        conn = connect_db()
        cur = conn.cursor()
        if cnlop:
            cur.execute("SELECT COUNT(*) FROM giaovien WHERE cnlop=%s AND maso<>%s", (cnlop, maso))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Lỗi", f"Lớp {cnlop} đã có giáo viên chủ nhiệm")
                conn.close()
                return
        try:
            cur.execute("UPDATE giaovien SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, cnlop=%s WHERE maso=%s",
                        (holot, ten, phai, ngaysinh, cnlop, maso))
            cur.execute("DELETE FROM giaovien_monhoc WHERE maso=%s", (maso,))
            for mamon in selected_monhoc:
                cur.execute("INSERT INTO giaovien_monhoc(maso, mamon) VALUES (%s,%s)", (maso, mamon))
            conn.commit()
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def huy():
        clear_input()
        
    def export_to_excel():
        conn = connect_db()
        query = """
            SELECT 
            g.maso AS 'Mã số',
            g.ten AS 'Tên'
        FROM giaovien g
        ORDER BY g.ten;

        """
        df = pd.read_sql(query, conn)
        conn.close()

        # Mở hộp thoại chọn vị trí lưu file
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx")],
                                                title="Lưu file Excel")
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Thành công", "Xuất dữ liệu ra Excel thành công!")
    

    # ===== Tạo nút =====
    buttons = [("Tìm", tim_kiem), ("Thêm", them), ("Sửa", sua), ("Lưu", luu),
           ("Hủy", huy), ("Xóa", xoa), 
           ("Thoát", lambda: (win.destroy(), open_main_menu())), ("Xuất Excel", export_to_excel)]
    for idx, (text, cmd) in enumerate(buttons):
        if text == "Thoát":
            color = "#B0BEC5"
        elif text == "Tìm":
            color = "#6CF2E5"
        elif text == "Xuất Excel":
            color = "#4CAF50"
        else:
            color = "#36F1DE"
        make_btn(text, cmd, bg=color).grid(row=0, column=idx, padx=5, pady=5)

    tree.bind("<<TreeviewSelect>>", on_select)
    load_data()
    win.mainloop()
