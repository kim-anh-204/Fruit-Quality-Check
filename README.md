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

## 📂 Cấu trúc thư mục

