-- ======================================
-- DATABASE: qlgv
-- ======================================
CREATE DATABASE IF NOT EXISTS qlgv;
USE qlgv;

-- ======================================
-- Bảng môn học
-- ======================================
CREATE TABLE IF NOT EXISTS monhoc (
    mamon VARCHAR(10) PRIMARY KEY,
    tenmon VARCHAR(100) NOT NULL
);

-- Dữ liệu mẫu môn học
INSERT INTO monhoc(mamon, tenmon) VALUES
('MH01', 'Toán'),
('MH02', 'Văn'),
('MH03', 'Lý'),
('MH04', 'Hóa'),
('MH05', 'Sinh'),
('MH06', 'Anh'),
('MH07', 'Sử'),
('MH08', 'Địa');

-- ======================================
-- Bảng lớp
-- ======================================
CREATE TABLE IF NOT EXISTS lop (
    malop VARCHAR(10) PRIMARY KEY,
    tenlop VARCHAR(50) NOT NULL
);

-- Dữ liệu mẫu lớp
INSERT INTO lop(malop, tenlop) VALUES
('L01','10A1'),
('L02','10A2'),
('L03','11A1'),
('L04','11A2'),
('L05','12A1'),
('L06','12A2');

-- ======================================
-- Bảng giáo viên
-- ======================================
CREATE TABLE IF NOT EXISTS giaovien (
    maso VARCHAR(10) PRIMARY KEY,
    holot VARCHAR(50) NOT NULL,
    ten VARCHAR(20) NOT NULL,
    phai ENUM('Nam','Nữ') NOT NULL,
    ngaysinh DATE,
    cnlop VARCHAR(10),
    FOREIGN KEY (cnlop) REFERENCES lop(malop) ON DELETE SET NULL
);

-- Dữ liệu mẫu giáo viên
INSERT INTO giaovien(maso, holot, ten, phai, ngaysinh, cnlop) VALUES
('GV01', 'Nguyễn Văn', 'An', 'Nam', '1980-01-01', 'L01'),
('GV02', 'Trần Thị', 'Bích', 'Nữ', '1985-05-12', NULL),
('GV03', 'Lê Văn', 'Cường', 'Nam', '1990-08-20', 'L03');

-- ======================================
-- Bảng liên kết giáo viên - môn học
-- ======================================
CREATE TABLE IF NOT EXISTS giaovien_monhoc (
    maso VARCHAR(10),
    mamon VARCHAR(10),
    PRIMARY KEY (maso, mamon),
    FOREIGN KEY (maso) REFERENCES giaovien(maso) ON DELETE CASCADE,
    FOREIGN KEY (mamon) REFERENCES monhoc(mamon) ON DELETE CASCADE
);

-- Dữ liệu mẫu liên kết giáo viên - môn học
INSERT INTO giaovien_monhoc(maso, mamon) VALUES
('GV01', 'MH01'),
('GV01', 'MH03'),
('GV02', 'MH02'),
('GV03', 'MH03'),
('GV03', 'MH04');
