# 🍎 Ứng dụng Dự đoán Độ Tươi của Trái Cây

Đây là một ứng dụng web được xây dựng bằng **Flask**, kết hợp mô hình **YOLOv8** để phát hiện trái cây trong ảnh và **MobileNetV2** để phân loại trái cây là **tươi** hoặc **hư**. Ứng dụng hỗ trợ các loại trái cây: **táo, chuối, cam**.

---

## 🚀 Tính năng

- 📷 Tải ảnh lên từ thiết bị để phân tích
- 🧠 Phát hiện vị trí trái cây trong ảnh với YOLOv8
- 🥭 Phân loại từng trái cây là tươi hay hư bằng MobileNetV2
- 🖼️ Hiển thị kết quả dự đoán trực tiếp trên ảnh
- 📁 Lưu trữ ảnh đã xử lý và vùng cắt từng trái cây

---

## 🛠 Công nghệ sử dụng

| Thành phần | Mô tả |
|-----------|-------|
| Flask | Framework Python để xây dựng ứng dụng web |
| TensorFlow + Keras | Dùng để chạy mô hình phân loại MobileNetV2 |
| YOLOv8 (Ultralytics) | Phát hiện trái cây trong ảnh |
| OpenCV & Pillow | Xử lý hình ảnh |
| HTML/CSS | Giao diện người dùng |

---

## 📦 Cài đặt và chạy dự án
# 🔢 1. Clone dự án
git clone https://github.com/ten-cua-ban/ten-du-an.git
cd ten-du-an

# 🔢 2. Tạo môi trường ảo (tuỳ chọn)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 🔢 3. Cài đặt thư viện
pip install -r requirements.txt

# 🔢 4. Chạy ứng dụng
python api.py

# Truy cập ứng dụng tại: http://127.0.0.1:5000

## 🖼️ Giao diện Ứng dụng

Ảnh dưới đây minh họa giao diện web của hệ thống khi người dùng truy cập:

![Giao diện chính](giaodienweb.png)

---

## 🎯 Kết quả Dự đoán

Kết quả sau khi tải ảnh lên và xử lý:

| Kết quả | Ảnh minh họa |
|--------|---------------|
| Kết quả 1 | ![res1](static/res1) |
| Kết quả 2 | ![res2](res2) |
| Kết quả 3 | ![res3](res3) |





