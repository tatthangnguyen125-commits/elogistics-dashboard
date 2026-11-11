# 🏭 E-LOGISTICS AI WORKFORCE PLANNER (NHIỆM VỤ 5)

> **Mô hình Trực Quan Hóa Điều Phối Nhân Sự & Bài Toán Kinh Tế Đêm Flash Sale**  
> Dành cho buổi Báo cáo & Thuyết trình của **Thành viên 5** (Nhóm Đồ án E-Logistics).

---

## 🌟 TẠI SAO BẢN WEB APP NÀY VƯỢT TRỘI GOOGLE COLAB?

1. **Giao diện Giám Đốc Điều Hành (Executive Dashboard):** Không còn màn hình code đen sì, giao diện sáng đẹp, chuyên nghiệp, chia 2 cột rõ ràng.
2. **Kéo Thả Trực Tiếp (Live Slider & Presets):** Mời Giảng viên bấm nút hoặc kéo chọn số đơn bất kỳ (ví dụ: 6.500, 8.000, 10.000 đơn) $\rightarrow$ Tất cả các chỉ số (Nhân sự, Tồn đọng, Chi phí, Tiết kiệm) lập tức nhảy số trong thời gian thực!
3. **Biểu đồ Tương tác Plotly (Interactive Hover):** Rê chuột vào từng cột biểu đồ để hiện chi tiết số tiền và lượng đơn cụ thể.
4. **Cầu nối Thực tế TV4 & TV6:** Tích hợp mô hình Machine Learning **XGBoost** (Thành viên 4) và Định mức UPH chuẩn nhân văn (Thành viên 6).
5. **Tích hợp Mã QR cho Slide Canva:** Giảng viên có thể quét mã QR trên slide bằng điện thoại và tự thao tác ngay tại chỗ.
6. **Cẩm nang Vượt vòng Phản biện:** Sẵn sàng các câu trả lời hóc búa nhất về công thức, hệ số an toàn $\alpha = 5\%$, và bài toán đánh đổi kinh tế.

---

## 🚀 HƯỚNG DẪN CHẠY TRÊN LOCALHOST (1-CLICK)

1. Mở thư mục `elogistics_dashboard`.
2. Nhấp đúp chuột vào file:
   ```cmd
   run_dashboard.bat
   ```
3. Trình duyệt web sẽ tự động mở tại địa chỉ:
   ```
   http://localhost:8501
   ```

---

## 🌐 HƯỚNG DẪN DEPLOY LÊN STREAMLIT CLOUD (MIỄN PHÍ 100%)

Để có một đường link thật dạng `https://elogistics-workforce-planner.streamlit.app`:

1. **Bước 1:** Đăng nhập vào [GitHub](https://github.com/) và tạo một Repository mới (ví dụ: `elogistics-dashboard`).
2. **Bước 2:** Tải toàn bộ các file trong thư mục này lên Repo:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `model_xgb.joblib`
   - `hourly_aggregated.csv`
3. **Bước 3:** Truy cập [share.streamlit.io](https://share.streamlit.io/) $\rightarrow$ Chọn **New App** $\rightarrow$ Chọn Repository vừa tạo $\rightarrow$ Nhấn **Deploy**!
4. **Bước 4:** Lấy đường link vừa tạo, dán vào **Tab 5** trên Web App để sinh mã QR Code sắc nét, tải ảnh về dán vào Slide Canva!

---

## 📐 CÔNG THỨC & LOGIC HỌC THUẬT CỐT LÕI

- **Định mức 1 nhân sự:**
  $$UPH = 40 \text{ đơn/giờ} \implies 40 \times 2\text{h} = \mathbf{80 \text{ đơn/người/ca}}$$
- **Hệ số rủi ro dự phòng:**
  $$\alpha = 5\% \implies \text{Hệ số} = 1.05$$
- **Số nhân sự AI cần gọi:**
  $$\text{Số người} = \left\lceil \frac{\text{Tổng đơn AI dự báo}}{80} \times 1.05 \right\rceil$$

### 💸 Hạch toán Kịch bản Đêm Flash Sale 6.500 Đơn:
- **Truyền thống (30 người):** 
  - Năng lực: $30 \times 80 = 2.400$ đơn $\implies$ **Tồn đọng (Backlog): 4.100 đơn (63,1%)**.
  - Lương: 2,10 triệu VNĐ.
  - Phí OT khẩn cấp: ~7,18 triệu VNĐ.
  - Phạt giao trễ sàn TMĐT (25k/đơn): 102,50 triệu VNĐ.
  - **$\implies$ Tổng thiệt hại: ~111,78 triệu VNĐ.**
- **Có AI XGBoost (86 người):**
  - Năng lực nâng lên: $86 \times 80 = 6.880$ đơn $\implies$ **Xóa sạch 100% Backlog (Dư 380 đơn buffer)**.
  - Lương sòng phẳng 86 người: 6,02 triệu VNĐ.
  - Phạt: 0 VNĐ | OT: 0 VNĐ.
  - **$\implies$ Tiết kiệm ròng cho doanh nghiệp: HƠN 105 TRIỆU VNĐ!**
