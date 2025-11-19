<h1>🏫 ĐỒ ÁN: Ứng dụng Quản Lý Giáo Viên THPT</h1>

### _Python Tkinter – MySQL • GUI Desktop App_

---

## <span style="color:#3EB489;">1. Giới thiệu</span>

Ứng dụng **Quản lý giáo viên THPT** được xây dựng bằng **Python (Tkinter)** kết hợp **MySQL** để lưu trữ dữ liệu.
Mục tiêu chính của dự án:

- Quản lý thông tin giáo viên nhanh chóng, chính xác
- Giao diện trực quan và dễ sử dụng
- Thêm – sửa – xoá – tìm kiếm – lưu – hủy – thoát

---

## <span style="color:#3EB489;">2. Giao diện chương trình</span>

<p align="center">
  <img src="https://github.com/user-attachments/assets/7b9fbe35-c0af-4c74-a5ad-9f86310f4d89" alt="Giao diện quản lý giáo viên" width="50%" style="border-radius:10px; box-shadow:0 0 10px #ccc;">
</p>

---

## <span style="color:#3EB489;">3. Chức năng chính</span>

### ✔️ **Quản lý giáo viên**

- Thêm, sửa, xoá, lưu, hủy, thoát
- Tìm kiếm theo mã giáo viên
- xuất excel

---

## <span style="color:#3EB489;">4. Công nghệ sử dụng</span>

| Thành phần          | Mô tả                                        |
| ------------------- | -------------------------------------------- |
| **Ngôn ngữ**        | Python                                       |
| **GUI**             | Tkinter, ttk                                 |
| **Database**        | MySQL                                        |
| **Thư viện hỗ trợ** | `mysql-connector-python`, `tkcalendar`, `re` |

---

## <span style="color:#3EB489;">5. Cách chạy chương trình</span>

### 📥 **Cài đặt thư viện**

```
pip install mysql-connector-python tkcalendar
```

### 🧷 **Cấu hình cơ sở dữ liệu**

Chỉnh thông tin kết nối:

```python
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="****",
        database="qlgv"
    )
```

### ▶️ **Chạy chương trình**

```
python main.py
```

---

## <span style="color:#3EB489;">7. Hướng phát triển thêm</span>

- Thống kê theo bộ môn / độ tuổi / giới tính
- Xây dựng phân quyền người dùng
- Làm thời khoá biểu cho giáo viên
- Thiết kế UI đẹp hơn bằng customTkinter

---

## <span style="color:#3EB489;">8. Tác giả</span>

| Tên               | MSSV      |
| ----------------- | --------- |
| Nguyễn Thị Trà My | DTH235701 |
| La Thanh Pats     | DTH235727 |
