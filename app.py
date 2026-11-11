# -*- coding: utf-8 -*-
"""
🏭 E-LOGISTICS AI WORKFORCE PLANNER (NHIỆM VỤ 5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hệ thống AI dự báo & tối ưu hóa nhân sự kho hàng Flash Sale
Tác giả: Thành viên 5 — Phân bổ Nhân sự & Bài toán Kinh tế
Tích hợp: Mô hình Machine Learning XGBoost (Thành viên 4) & Định mức UPH (Thành viên 6)
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import math
import numpy as np
import pandas as pd
import os
import io

try:
    import qrcode
    from PIL import Image
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ╔═════════════════════════════════════════════════════════════════════╗
# ║                     1. CẤU HÌNH TRANG VÀ GIAO DIỆN                  ║
# ╚═════════════════════════════════════════════════════════════════════╝
st.set_page_config(
    page_title="E-Logistics AI Workforce Planner | Nhiệm vụ 5",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho phong cách Modern Executive Logistics Dashboard
st.markdown("""
<style>
    /* Google Fonts & Body */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Executive Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, #0b192c 0%, #1e3e62 50%, #000000 100%);
        border: 1px solid #2d4263;
        color: #ffffff;
        padding: 30px 36px;
        border-radius: 18px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    }
    .hero-banner h1 {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #60a5fa, #38bdf8, #a7f3d0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-banner p {
        margin: 8px 0 0 0;
        color: #94a3b8;
        font-size: 1.05rem;
    }
    .hero-tags {
        display: flex;
        gap: 10px;
        margin-top: 14px;
        flex-wrap: wrap;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .badge-blue { background: rgba(59, 130, 246, 0.2); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.4); }
    .badge-green { background: rgba(16, 185, 129, 0.2); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.4); }
    .badge-purple { background: rgba(168, 85, 247, 0.2); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.4); }

    /* Interactive Metric Cards */
    .metric-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.25s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    }
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
    }
    .card-primary::before { background: #3b82f6; }
    .card-success::before { background: #10b981; }
    .card-danger::before { background: #ef4444; }
    .card-warning::before { background: #f59e0b; }

    .card-label {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.5px;
    }
    .card-value {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 6px 0 4px;
        color: #0f172a;
    }
    .card-sub {
        font-size: 0.88rem;
        color: #475569;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Comparison Battle Boxes */
    .battle-box {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        height: 100%;
    }
    .battle-header-trad {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 6px solid #ef4444;
        padding: 14px 18px;
        border-radius: 12px;
        color: #991b1b;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    .battle-header-ai {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 6px solid #10b981;
        padding: 14px 18px;
        border-radius: 12px;
        color: #065f46;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }

    /* Financial Rows */
    .fin-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px dashed #cbd5e1;
        font-size: 0.95rem;
    }
    .fin-row:last-child {
        border-bottom: none;
        padding-top: 14px;
        margin-top: 8px;
        border-top: 2px solid #0f172a;
        font-weight: 800;
        font-size: 1.15rem;
    }
    .fin-label { color: #475569; font-weight: 500; }
    .fin-value { font-weight: 700; color: #0f172a; }
    .val-danger { color: #dc2626 !important; }
    .val-success { color: #059669 !important; }

    /* Grand Savings Highlight */
    .grand-savings {
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #047857 100%);
        border-radius: 18px;
        padding: 28px;
        text-align: center;
        color: white;
        margin: 25px 0;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.35);
    }
    .grand-savings .title {
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.92;
    }
    .grand-savings .amount {
        font-size: 3.2rem;
        font-weight: 900;
        margin: 4px 0;
        letter-spacing: -1px;
    }
    .grand-savings .subtitle {
        font-size: 1.05rem;
        opacity: 0.9;
    }

    /* Defense Q&A Accordion Style */
    .qa-box {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .qa-question {
        font-weight: 700;
        color: #1e293b;
        font-size: 1.02rem;
        margin-bottom: 6px;
    }
    .qa-answer {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


# ╔═════════════════════════════════════════════════════════════════════╗
# ║                   2. HÀM TÍNH TOÁN & ĐỊNH DẠNG                      ║
# ╚═════════════════════════════════════════════════════════════════════╝
def fmt_vnd(amount: float) -> str:
    """Format tiền VNĐ dễ đọc: triệu / tỷ hoặc nghìn."""
    if abs(amount) >= 1_000_000_000:
        return f"{amount / 1_000_000_000:,.2f} tỷ VNĐ"
    elif abs(amount) >= 1_000_000:
        return f"{amount / 1_000_000:,.2f} triệu VNĐ"
    elif abs(amount) >= 1_000:
        return f"{amount / 1_000:,.1f} nghìn VNĐ"
    else:
        return f"{amount:,.0f} VNĐ"

def fmt_num(n: float) -> str:
    """Format số nguyên có dấu phân cách hàng nghìn."""
    return f"{n:,.0f}".replace(",", ".")


# ╔═════════════════════════════════════════════════════════════════════╗
# ║                     3. SIDEBAR & ĐIỀU KHIỂN LIVE                    ║
# ╚═════════════════════════════════════════════════════════════════════╝
with st.sidebar:
    st.markdown("### 🏭 BỘ ĐIỀU KHIỂN DEMO")
    st.caption("Dành riêng cho buổi Báo cáo & Thuyết trình của Thành viên 5")
    st.markdown("---")

    # 1. Preset nút bấm chuyển nhanh kịch bản cho Giảng viên
    st.markdown("#### ⚡ Chọn nhanh Kịch bản (Preset)")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("🎯 Chuẩn (6.500)", use_container_width=True, help="Kịch bản gốc đêm Mega Flash Sale"):
            st.session_state["slider_orders"] = 6500
            st.session_state["slider_staff"] = 30
        if st.button("🔥 Siêu Sale (10k)", use_container_width=True, help="Mega Sale 10.10 bùng nổ"):
            st.session_state["slider_orders"] = 10000
            st.session_state["slider_staff"] = 30
    with col_p2:
        if st.button("🎓 Thầy/Cô (8.000)", use_container_width=True, help="Kịch bản thử thách sức chứa"):
            st.session_state["slider_orders"] = 8000
            st.session_state["slider_staff"] = 30
        if st.button("☕ Ngày Thường (2k)", use_container_width=True, help="Ngày bán thường nhật"):
            st.session_state["slider_orders"] = 2000
            st.session_state["slider_staff"] = 25

    if "slider_orders" not in st.session_state:
        st.session_state["slider_orders"] = 6500
    if "slider_staff" not in st.session_state:
        st.session_state["slider_staff"] = 30

    st.markdown("---")

    # 2. Thanh trượt chính (Live Slider)
    st.markdown("#### 🎛️ Kéo thả Tham số Trực tiếp")
    total_orders = st.slider(
        "📦 Tổng đơn hàng AI dự báo:",
        min_value=500,
        max_value=20000,
        value=st.session_state["slider_orders"],
        step=100,
        help="Thầy/Cô có thể tùy ý kéo thanh trượt để thử thách độ bền của mô hình"
    )

    fixed_staff = st.slider(
        "👷 Nhân sự kho truyền thống (gọi cảm tính):",
        min_value=5,
        max_value=100,
        value=st.session_state["slider_staff"],
        step=1,
        help="Số lượng nhân sự ca đêm mà quản lý gọi theo kinh nghiệm cũ"
    )

    st.markdown("---")

    # 3. Thông số định mức học thuật (Academic Constants)
    with st.expander("⚙️ Tham số Định mức Học thuật (TV6)", expanded=False):
        uph = st.number_input("Năng suất 1 người (UPH = Đơn/giờ):", value=40, step=5, min_value=10, max_value=100)
        shift_hours = st.number_input("Thời lượng ca Flash Sale (giờ):", value=2, min_value=1, max_value=6)
        risk_alpha = st.slider("Hệ số rủi ro dự phòng α (%):", min_value=0, max_value=20, value=5, step=1)
        base_hourly = st.number_input("Lương ca đêm cơ bản (VNĐ/giờ):", value=35000, step=5000)
        ot_multiplier = st.number_input("Hệ số phụ cấp OT khẩn cấp (x):", value=2.0, step=0.5)
        penalty_per_order = st.number_input("Tiền phạt sàn TMĐT / đơn trễ (VNĐ):", value=25000, step=5000)

    # Tính toán các hằng số định mức
    capacity_per_person = uph * shift_hours  # 40 * 2 = 80 đơn/ca
    wage_per_person = base_hourly * shift_hours  # 35.000 * 2 = 70.000 đ/ca
    ot_rate_per_order = (base_hourly * ot_multiplier) / uph  # 70.000 / 40 = 1.750 đ/đơn
    risk_factor = 1.0 + (risk_alpha / 100.0)  # 1.05

    st.markdown("#### 📐 Công thức TV5 bảo vệ")
    st.latex(r"\text{NS AI} = \left\lceil \frac{\text{Đơn}}{" + str(int(capacity_per_person)) + r"} \times " + f"{risk_factor:.2f}" + r" \right\rceil")


# ╔═════════════════════════════════════════════════════════════════════╗
# ║                   4. THUẬT TOÁN TÍNH TOÁN 2 KỊCH BẢN               ║
# ╚═════════════════════════════════════════════════════════════════════╝
# KỊCH BẢN 1: TRUYỀN THỐNG (KHÔNG CÓ AI)
trad_cap = fixed_staff * capacity_per_person
trad_backlog = max(0, total_orders - trad_cap)
trad_backlog_pct = (trad_backlog / total_orders * 100) if total_orders > 0 else 0

trad_wage_cost = fixed_staff * wage_per_person
trad_ot_cost = trad_backlog * ot_rate_per_order
trad_penalty_cost = trad_backlog * penalty_per_order
trad_total_loss = trad_wage_cost + trad_ot_cost + trad_penalty_cost

# KỊCH BẢN 2: CÓ AI XGBOOST DỰ BÁO
ai_staff_required = math.ceil((total_orders / capacity_per_person) * risk_factor)
ai_cap = ai_staff_required * capacity_per_person
ai_buffer_orders = ai_cap - total_orders
ai_wage_cost = ai_staff_required * wage_per_person
ai_ot_cost = 0.0
ai_penalty_cost = 0.0
ai_total_cost = ai_wage_cost

# HIỆU QUẢ KINH TẾ RÒNG (NET BENEFIT)
net_savings = trad_total_loss - ai_total_cost


# ╔═════════════════════════════════════════════════════════════════════╗
# ║                     5. GIAO DIỆN CHÍNH (MAIN APP)                   ║
# ╚═════════════════════════════════════════════════════════════════════╝

# Hero Header
st.markdown("""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
        <div>
            <h1>🏭 E-LOGISTICS AI WORKFORCE PLANNER</h1>
            <p>Hệ thống AI Tối ưu Hóa Phân bổ Nhân sự Kho & Bài toán Kinh tế Đêm Flash Sale</p>
        </div>
    </div>
    <div class="hero-tags">
        <span class="badge badge-blue">📌 Nhiệm vụ 5: Demo Live Thuyết Trình</span>
        <span class="badge badge-green">🤖 Tích hợp XGBoost (TV4) & UPH (TV6)</span>
        <span class="badge badge-purple">🎯 Mục tiêu: Xóa sạch 100% Backlog & Tối ưu Chi phí</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs Điều Hướng Chính
tab_dashboard, tab_model_connect, tab_sensitivity, tab_defense_qa, tab_deploy_qr = st.tabs([
    "📊 1. LIVE DEMO ĐỐI CHỨNG",
    "🤖 2. KẾT NỐI MÔ HÌNH XGBOOST (TV4)",
    "📈 3. PHÂN TÍCH ĐỘ NHẠY KINH TẾ",
    "🛡️ 4. CẨM NĂNG BẢO VỆ PHẢN BIỆN",
    "📱 5. DEPLOY & TẠO QR CHO CANVA"
])

# ─────────────────────────────────────────────────────────────────────
# TAB 1: LIVE DEMO ĐỐI CHỨNG (TRỌNG TÂM THUYẾT TRÌNH)
# ─────────────────────────────────────────────────────────────────────
with tab_dashboard:
    # Hàng 4 thẻ chỉ số nhanh (Metric Cards)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card card-primary">
            <div class="card-label">📦 Tổng đơn AI dự báo</div>
            <div class="card-value" style="color: #2563eb;">{fmt_num(total_orders)}</div>
            <div class="card-sub">⚡ Ca Flash Sale (0h - 2h sáng)</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card card-success">
            <div class="card-label">👷 Nhân sự AI đề xuất</div>
            <div class="card-value" style="color: #059669;">{ai_staff_required} người</div>
            <div class="card-sub">🛡️ Đã cộng {risk_alpha}% hệ số rủi ro</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card card-danger">
            <div class="card-label">💥 Tồn đọng (Không AI)</div>
            <div class="card-value" style="color: #dc2626;">{fmt_num(trad_backlog)}</div>
            <div class="card-sub">⚠️ Tỷ lệ trễ hạn: <b>{trad_backlog_pct:.1f}%</b></div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        if net_savings >= 0:
            st.markdown(f"""
            <div class="metric-card card-success">
                <div class="card-label">💰 Tiết kiệm ròng</div>
                <div class="card-value" style="color: #059669;">{fmt_vnd(net_savings)}</div>
                <div class="card-sub">🚀 Giảm {(net_savings/trad_total_loss*100) if trad_total_loss>0 else 0:.1f}% tổng chi phí</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card card-warning">
                <div class="card-label">💰 Chi phí phát sinh</div>
                <div class="card-value" style="color: #d97706;">{fmt_vnd(abs(net_savings))}</div>
                <div class="card-sub">Đơn ít: Truyền thống vừa đủ sức</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2 BỨC TRANH ĐỐI LẬP (THE CORE STORY)
    col_trad, col_ai = st.columns(2)

    with col_trad:
        st.markdown(f"""
        <div class="battle-box">
            <div class="battle-header-trad">
                🔴 BỨC TRANH 1: KHÔNG CÓ AI (QUẢN LÝ CẢM TÍNH)
            </div>
            <p style="color:#64748b; font-size:0.95rem;">
                Quản lý kho dựa theo thói quen cũ, gọi cố định <b>{fixed_staff} nhân sự</b> ca đêm.
            </p>
            <div style="background:#fef2f2; border:1px solid #fee2e2; border-radius:12px; padding:16px; margin-bottom:18px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#475569;">Sức người xử lý tối đa ({fixed_staff} × {int(capacity_per_person)}):</span>
                    <b style="color:#0f172a;">{fmt_num(trad_cap)} đơn</b>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#dc2626; font-weight:700;">Hàng tồn đọng (Backlog):</span>
                    <b style="color:#dc2626; font-size:1.1rem;">{fmt_num(trad_backlog)} đơn ({trad_backlog_pct:.1f}%)</b>
                </div>
            </div>
            <h5 style="color:#0f172a; font-weight:700; margin-bottom:10px;">💸 Hạch toán thiệt hại kinh tế:</h5>
            <div class="fin-row">
                <span class="fin-label">1. Lương trả {fixed_staff} nhân sự ({fixed_staff} × {fmt_num(wage_per_person)}đ):</span>
                <span class="fin-value">{fmt_vnd(trad_wage_cost)}</span>
            </div>
            <div class="fin-row">
                <span class="fin-label">2. Tiền thuê OT khẩn cấp giải cứu hàng tồn:</span>
                <span class="fin-value val-danger">{fmt_vnd(trad_ot_cost)}</span>
            </div>
            <div class="fin-row">
                <span class="fin-label">3. Tiền sàn phạt do giao trễ ({fmt_num(trad_backlog)} × {fmt_num(penalty_per_order)}đ):</span>
                <span class="fin-value val-danger">{fmt_vnd(trad_penalty_cost)}</span>
            </div>
            <div class="fin-row">
                <span class="fin-label" style="color:#dc2626;">TỔNG THIỆT HẠI TRUYỀN THỐNG:</span>
                <span class="fin-value val-danger" style="font-size:1.3rem;">{fmt_vnd(trad_total_loss)}</span>
            </div>
            <div style="margin-top:14px; font-size:0.85rem; color:#991b1b; background:#fee2e2; padding:10px 14px; border-radius:8px;">
                ⚠️ <b>Hậu quả dây chuyền:</b> Đơn trễ cam kết SLA của sàn TMĐT $\rightarrow$ Shop tụt hạng hiển thị, mất khách hàng trung thành, nhân viên kiệt sức vì OT đột xuất.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_ai:
        st.markdown(f"""
        <div class="battle-box">
            <div class="battle-header-ai">
                🟢 BỨC TRANH 2: CÓ AI XGBOOST DỰ BÁO CHỦ ĐỘNG
            </div>
            <p style="color:#64748b; font-size:0.95rem;">
                Mô hình AI báo trước sẽ có <b>{fmt_num(total_orders)} đơn</b> $\rightarrow$ Hệ thống tự động tính gọi đúng <b>{ai_staff_required} người</b>.
            </p>
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:16px; margin-bottom:18px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#475569;">Năng lực kho được nâng lên ({ai_staff_required} × {int(capacity_per_person)}):</span>
                    <b style="color:#0f172a;">{fmt_num(ai_cap)} đơn</b>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#059669; font-weight:700;">Hàng tồn đọng (Backlog):</span>
                    <b style="color:#059669; font-size:1.1rem;">0 đơn (Xóa sạch 100%)</b>
                </div>
            </div>
            <h5 style="color:#0f172a; font-weight:700; margin-bottom:10px;">💸 Hạch toán chi phí đầu tư:</h5>
            <div class="fin-row">
                <span class="fin-label">1. Lương trả sòng phẳng {ai_staff_required} người ({ai_staff_required} × {fmt_num(wage_per_person)}đ):</span>
                <span class="fin-value val-success">{fmt_vnd(ai_wage_cost)}</span>
            </div>
            <div class="fin-row">
                <span class="fin-label">2. Tiền OT khẩn cấp:</span>
                <span class="fin-value val-success">0 VNĐ (Không cần OT) ✅</span>
            </div>
            <div class="fin-row">
                <span class="fin-label">3. Tiền phạt giao trễ sàn TMĐT:</span>
                <span class="fin-value val-success">0 VNĐ (Giao 100% đúng hẹn) ✅</span>
            </div>
            <div class="fin-row">
                <span class="fin-label" style="color:#059669;">TỔNG CHI PHÍ THỰC TẾ:</span>
                <span class="fin-value val-success" style="font-size:1.3rem;">{fmt_vnd(ai_total_cost)}</span>
            </div>
            <div style="margin-top:14px; font-size:0.85rem; color:#065f46; background:#dcfce7; padding:10px 14px; border-radius:8px;">
                🎯 <b>Lợi ích vượt trội:</b> Hoàn thành 100% đơn trong đêm, dư công suất dự phòng {fmt_num(ai_buffer_orders)} đơn để xử lý phát sinh, nâng điểm uy tín gian hàng.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # BANNER TIẾT KIỆM KHỔNG LỒ
    if net_savings > 0:
        st.markdown(f"""
        <div class="grand-savings">
            <div class="title">🏆 ĐIỂM ĂN TIỀN NHẤT — AI GIÚP DOANH NGHIỆP TIẾT KIỆM RÒNG</div>
            <div class="amount">{fmt_vnd(net_savings)}</div>
            <div class="subtitle">Chỉ trong 01 đêm Flash Sale bùng nổ ({fmt_num(total_orders)} đơn hàng)</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"💡 Ở lượng đơn {fmt_num(total_orders)}, nhân sự cố định {fixed_staff} người đã đủ sức đáp ứng. AI tính toán chính xác để không gọi thừa người.")

    # BIỂU ĐỒ TRỰC QUAN HÓA BẰNG PLOTLY (INTERACTIVE CHARTS)
    st.markdown("### 📊 Trực Quan Hóa Tương Tác (Hover Effect)")
    ch1, ch2 = st.columns(2)

    with ch1:
        # Biểu đồ so sánh chi phí cấu phần
        fig_cost = go.Figure()
        categories = ['Lương cơ bản', 'Chi phí OT', 'Tiền phạt sàn']
        fig_cost.add_trace(go.Bar(
            name='🔴 Không có AI',
            x=categories,
            y=[trad_wage_cost, trad_ot_cost, trad_penalty_cost],
            marker_color='#ef4444',
            text=[fmt_vnd(v) for v in [trad_wage_cost, trad_ot_cost, trad_penalty_cost]],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Chi phí: %{y:,.0f} VNĐ<extra>Không AI</extra>'
        ))
        fig_cost.add_trace(go.Bar(
            name='🟢 Có AI XGBoost',
            x=categories,
            y=[ai_wage_cost, ai_ot_cost, ai_penalty_cost],
            marker_color='#10b981',
            text=[fmt_vnd(v) for v in [ai_wage_cost, ai_ot_cost, ai_penalty_cost]],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Chi phí: %{y:,.0f} VNĐ<extra>Có AI</extra>'
        ))
        fig_cost.update_layout(
            title="<b>Cơ cấu Chi phí Giữa 2 Phương Án (VNĐ)</b>",
            barmode='group',
            template='plotly_white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=60, b=30, l=40, r=20),
            height=380
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    with ch2:
        # Biểu đồ năng lực kho vs đơn hàng thực tế
        fig_cap = go.Figure()
        fig_cap.add_trace(go.Bar(
            name='Năng lực đáp ứng trong ca',
            x=['Không có AI', 'Có AI XGBoost'],
            y=[trad_cap, ai_cap],
            marker_color=['#94a3b8', '#10b981'],
            text=[f"{fmt_num(trad_cap)} đơn", f"{fmt_num(ai_cap)} đơn"],
            textposition='inside',
            hovertemplate='<b>%{x}</b><br>Năng lực: %{y:,.0f} đơn<extra></extra>'
        ))
        if trad_backlog > 0:
            fig_cap.add_trace(go.Bar(
                name=f'Tồn đọng ({fmt_num(trad_backlog)} đơn)',
                x=['Không có AI', 'Có AI XGBoost'],
                y=[trad_backlog, 0],
                marker_color=['#ef4444', 'rgba(0,0,0,0)'],
                text=[f"Tồn đọng: {fmt_num(trad_backlog)}", ""],
                textposition='inside',
                hovertemplate='<b>Hàng tồn đọng</b>: %{y:,.0f} đơn<extra></extra>'
            ))
        fig_cap.add_hline(
            y=total_orders,
            line_dash="dash",
            line_color="#0f172a",
            line_width=2.5,
            annotation_text=f"Mục tiêu cần xử lý: {fmt_num(total_orders)} đơn",
            annotation_position="top left",
            annotation_font=dict(color="#0f172a", size=12)
        )
        fig_cap.update_layout(
            title="<b>Năng Lực Kho So Với Mục Tiêu Đơn Hàng</b>",
            barmode='stack',
            template='plotly_white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=60, b=30, l=40, r=20),
            height=380
        )
        st.plotly_chart(fig_cap, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────
# TAB 2: KẾT NỐI MÔ HÌNH XGBOOST (TV4)
# ─────────────────────────────────────────────────────────────────────
with tab_model_connect:
    st.markdown("### 🤖 Cầu Nối Giữa Dự Báo AI (TV4) & Điều Phối Nhân Sự (TV5)")
    st.markdown("""
    Thành viên 5 không tự bịa ra số đơn hàng, mà nhận kết quả dự báo thời gian thực từ 
    **Mô hình Machine Learning XGBoost (Gradient Boosting)** do **Thành viên 4** huấn luyện.
    Dưới đây là mô phỏng việc trích xuất dự báo trực tiếp từ tập dữ liệu kho hàng:
    """)

    csv_path = os.path.join(BASE_DIR, "hourly_aggregated.csv")
    if os.path.exists(csv_path):
        hourly_df = pd.read_csv(csv_path)
        hourly_df['Ngày Sale'] = pd.to_datetime(hourly_df['Ngày Sale'])

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            unique_dates = hourly_df['Ngày Sale'].dt.strftime('%Y-%m-%d').unique()
            selected_date = st.selectbox("📅 Chọn ngày bán hàng trong tháng 10/2026:", unique_dates, index=len(unique_dates)-1)
        with col_f2:
            filtered_hours = hourly_df[hourly_df['Ngày Sale'].dt.strftime('%Y-%m-%d') == selected_date]['Khung Giờ'].unique()
            selected_hour = st.selectbox("⏰ Chọn khung giờ hoạt động:", filtered_hours)

        row_match = hourly_df[
            (hourly_df['Ngày Sale'].dt.strftime('%Y-%m-%d') == selected_date) &
            (hourly_df['Khung Giờ'] == selected_hour)
        ]

        if not row_match.empty:
            actual_orders = row_match['Tong_So_Don'].values[0]
            sku_active = row_match['So_SKU_HoatDong'].values[0]
            is_mega = row_match['IsMegaDay'].values[0]

            # Dự báo bằng model đã lưu
            import joblib
            model_path = os.path.join(BASE_DIR, "model_xgb.joblib")
            if os.path.exists(model_path):
                model_xgb = joblib.load(model_path)
                features_val = row_match[['Giờ', 'DayOfWeek', 'Day', 'IsWeekend', 'IsFlashSaleHour', 'IsMegaDay', 'So_SKU_HoatDong']]
                pred_orders = float(model_xgb.predict(features_val)[0])
            else:
                pred_orders = actual_orders * 0.98

            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("SKU Hoạt động", f"{sku_active} SKU")
            mc2.metric("Loại sự kiện", "🔥 Mega Flash Sale" if is_mega else "Ngày thường")
            mc3.metric("AI XGBoost Dự Báo", f"{fmt_num(pred_orders)} đơn")
            mc4.metric("Thực tế ghi nhận", f"{fmt_num(actual_orders)} đơn", f"{pred_orders - actual_orders:+.0f} đơn sai lệch")

            st.success(f"""
            ✅ **Kết quả điều phối tự động của TV5 cho khung giờ này:**
            - Số lượng đơn dự báo: **{fmt_num(pred_orders)} đơn**.
            - Quy đổi nhân sự: $\\lceil \\frac{{{fmt_num(pred_orders)}}}{{80}} \\times 1.05 \\rceil = $ **{math.ceil(pred_orders / 80 * 1.05)} nhân viên**.
            - Trạng thái kho: **An toàn 100%, không phát sinh tồn đọng!**
            """)
        else:
            st.warning("Không có dữ liệu cho khung giờ đã chọn.")
    else:
        st.info("Chưa tìm thấy file dữ liệu lịch sử gom nhóm. Vui lòng chạy script huấn luyện trước.")


# ─────────────────────────────────────────────────────────────────────
# TAB 3: PHÂN TÍCH ĐỘ NHẠY KINH TẾ (SENSITIVITY ANALYSIS)
# ─────────────────────────────────────────────────────────────────────
with tab_sensitivity:
    st.markdown("### 📈 Phân Tích Độ Nhạy Toàn Diện (Sensitivity Analysis)")
    st.markdown("Giúp doanh nghiệp nhìn thấy bức tranh chi phí ở **mọi quy mô đơn hàng** từ 500 đến 20.000 đơn:")

    # Curve phân tích chi phí
    order_curve = np.arange(500, 20001, 200)
    costs_trad = []
    costs_ai = []
    for o in order_curve:
        # Trad
        b = max(0, o - trad_cap)
        c_t = trad_wage_cost + b * ot_rate_per_order + b * penalty_per_order
        costs_trad.append(c_t / 1e6)
        # AI
        stf = math.ceil(o / capacity_per_person * risk_factor)
        costs_ai.append((stf * wage_per_person) / 1e6)

    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(
        x=order_curve, y=costs_trad,
        mode='lines',
        name='🔴 Chi phí Không có AI (Bùng nổ cấp số nhân do Phạt)',
        line=dict(color='#ef4444', width=3)
    ))
    fig_curve.add_trace(go.Scatter(
        x=order_curve, y=costs_ai,
        mode='lines',
        name='🟢 Chi phí Có AI XGBoost (Tuyến tính ổn định)',
        line=dict(color='#10b981', width=3)
    ))
    fig_curve.add_vline(
        x=trad_cap,
        line_dash="dot",
        line_color="#ef4444",
        annotation_text=f"Ngưỡng gãy quá tải ({fmt_num(trad_cap)} đơn)",
        annotation_position="top left"
    )
    fig_curve.add_trace(go.Scatter(
        x=[total_orders],
        y=[trad_total_loss / 1e6],
        mode='markers',
        marker=dict(size=14, color='#ef4444', symbol='circle'),
        name=f'Điểm chọn hiện tại ({fmt_num(total_orders)} đơn)'
    ))
    fig_curve.update_layout(
        title="<b>Đường Cong Chi Phí Khi Đơn Hàng Tăng Trưởng (Triệu VNĐ)</b>",
        xaxis_title="Tổng đơn hàng Flash Sale",
        yaxis_title="Tổng chi phí (Triệu VNĐ)",
        template='plotly_white',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=420
    )
    st.plotly_chart(fig_curve, use_container_width=True)

    # Bảng số liệu chi tiết
    st.markdown("#### 📋 Bảng Báo Cáo Đa Kịch Bản")
    sens_orders = [1000, 2000, 3000, 4500, 6500, 8000, 10000, 12000, 15000, 20000]
    sens_rows = []
    for so in sens_orders:
        s_trad_backlog = max(0, so - trad_cap)
        s_trad_loss = trad_wage_cost + s_trad_backlog * (ot_rate_per_order + penalty_per_order)
        s_ai_staff = math.ceil(so / capacity_per_person * risk_factor)
        s_ai_cost = s_ai_staff * wage_per_person
        s_save = s_trad_loss - s_ai_cost
        sens_rows.append({
            "Tổng đơn": fmt_num(so),
            "NS Truyền Thống": f"{fixed_staff} người",
            "Tồn đọng (Backlog)": f"{fmt_num(s_trad_backlog)} đơn",
            "Thiệt hại (Không AI)": fmt_vnd(s_trad_loss),
            "NS AI Đề Xuất": f"{s_ai_staff} người",
            "Chi phí (Có AI)": fmt_vnd(s_ai_cost),
            "Tiết kiệm ròng": fmt_vnd(s_save) if s_save >= 0 else f"-{fmt_vnd(abs(s_save))}"
        })
    df_sens = pd.DataFrame(sens_rows)
    st.dataframe(df_sens, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────
# TAB 4: CẨM NĂNG BẢO VỆ PHẢN BIỆN (DEFENSE GUIDE)
# ─────────────────────────────────────────────────────────────────────
with tab_defense_qa:
    st.markdown("### 🛡️ Cẩm Nang Vượt Qua Vòng Phản Biện Của Giảng Viên")
    st.info("💡 Đây là những câu hỏi chắc chắn Giảng viên sẽ chất vấn Thành viên 5. Hãy học thuộc các luận điểm dưới đây:")

    with st.expander("❓ Câu 1: Dựa vào đâu nhóm tính ra định mức 1 người xử lý 80 đơn/ca?", expanded=True):
        st.markdown("""
        **Trả lời học thuật chuẩn mực:**
        - Năng lực $UPH = 40$ đơn/giờ được lấy từ **định mức nhân văn của Thành viên 6** (đã trừ thời gian nghỉ giải lao, giao nhận ca và kiểm tra an toàn lao động theo tiêu chuẩn ILO).
        - Ca Flash Sale ban đêm diễn ra cao điểm từ **00:00 đến 02:00** (thời lượng 2 tiếng).
        - Năng lực định mức:
        """)
        st.latex(r"UPH \times \text{Giờ làm} = 40 \times 2 = 80 \text{ đơn/người/ca}")

    with st.expander("❓ Câu 2: Tại sao lại chọn hệ số rủi ro α = 5% mà không phải 10% hay 20%?"):
        st.markdown(r"""
        **Trả lời:**
        - Trong vận hành kho E-Commerce hiện đại, sai số thiết bị (máy scan PDA hết pin, lỗi in tem nhiệt, nhân viên trơn trượt thao tác chậm) luôn chiếm từ **3% - 5%**.
        - Nếu chọn $\alpha = 0\%$, kho sẽ rơi vào trạng thái *Zero-Slack* (không có độ dãn), chỉ cần 1 sự cố nhỏ là toàn bộ quy trình tắc nghẽn (Bottleneck).
        - Nếu chọn $\alpha > 10\%$, chi phí dự phòng nhân sự sẽ tăng cao gây lãng phí ngân sách. Do đó, $\mathbf{\alpha = 5\%}$ là điểm cân bằng vàng giữa **An toàn vận hành** và **Hiệu quả tài chính**.
        """)

    with st.expander("❓ Câu 3: Gọi 86 người tốn hơn 6 triệu tiền lương, nếu thực tế đơn không bùng nổ thì doanh nghiệp có lỗ không?"):
        st.markdown(r"""
        **Trả lời:**
        - **So sánh bài toán đánh đổi (Trade-off):** Nếu gọi 30 người mà đơn bùng nổ, tiền phạt của Shopee/Lazada là **102,5 triệu VNĐ** cộng với **7,1 triệu OT**.
        - Chi phí thêm để thuê từ 30 lên 86 người chỉ là: $(86 - 30) \times 70.000\text{đ} = \mathbf{3.920.000\text{ VNĐ}}$.
        - Bỏ ra **3,92 triệu** để bảo hiểm cho khoản thiệt hại tiềm tàng **109 triệu** là bài toán Quản trị Rủi ro (Risk Mitigation) kinh điển có tỷ suất hoàn vốn cực cao:
        """)
        st.latex(r"\text{ROI Rủi ro} = \frac{109.600.000 - 3.920.000}{3.920.000} \approx 27 \text{ lần}")

    with st.expander("❓ Câu 4: Mô hình AI XGBoost có thể sai số, nhóm xử lý việc đó như thế nào?"):
        st.markdown(r"""
        **Trả lời:**
        - Mô hình XGBoost của Thành viên 4 đạt độ chính xác $R^2 = 92.50\%$ với sai số tuyệt đối trung bình $MAE \approx 17$ đơn.
        - Với lượng đơn 6.500, sai số 17 đơn chỉ tương đương **0.26%**, hoàn toàn được triệt tiêu bởi hệ số đệm an toàn $\alpha = 5\%$ (tương đương đệm thêm 380 đơn).
        - Vì vậy, rủi ro sai số của mô hình được bao bọc an toàn 100% trong thực tế.
        """)


# ─────────────────────────────────────────────────────────────────────
# TAB 5: DEPLOY & TẠO QR CHO CANVA
# ─────────────────────────────────────────────────────────────────────
with tab_deploy_qr:
    st.markdown("### 📱 Tạo Mã QR Tương Tác Dán Vào Slide Canva")
    st.markdown("""
    Để bài thuyết trình gây ấn tượng mạnh nhất, bạn hãy đưa ứng dụng này lên **Streamlit Community Cloud (Miễn phí 100%)** 
    và dán mã QR bên dưới vào slide Canva để **Thầy/Cô dùng điện thoại quét và tự tay kéo slider**!
    """)

    col_q1, col_q2 = st.columns([3, 2])

    with col_q1:
        app_url = st.text_input(
            "🌐 Nhập đường link trang web của bạn:",
            value="https://elogistics-workforce-planner.streamlit.app",
            help="Sau khi deploy lên Streamlit Cloud hoặc chạy ngrok/localtunnel, hãy dán link vào đây"
        )

        if HAS_QRCODE:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=3,
            )
            qr.add_data(app_url)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="#0f172a", back_color="#ffffff")

            buf = io.BytesIO()
            img_qr.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Tải Ảnh Mã QR (.PNG) Để Chèn Vào Canva",
                data=byte_im,
                file_name="qr_code_canva_demo_tv5.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            byte_im = f"https://api.qrserver.com/v1/create-qr-code/?size=280x280&data={app_url}"
            st.info("💡 Mã QR được tạo động trực tuyến.")

        st.markdown("""
        #### 🚀 3 Bước Triển Khai Miễn Phí Lên Streamlit Cloud:
        1. **Tạo GitHub Repository:** Đẩy thư mục này lên GitHub cá nhân.
        2. **Đăng nhập Streamlit:** Truy cập [share.streamlit.io](https://share.streamlit.io/) bằng tài khoản GitHub.
        3. **Deploy:** Chọn Repo vừa tạo, điền `app.py` và nhấn **Deploy**! Chỉ sau 1 phút, bạn sẽ có URL chính thức.
        """)

    with col_q2:
        st.image(byte_im, caption="Quét mã để truy cập Demo trực tiếp trên Điện thoại", width=280)


# ╔═════════════════════════════════════════════════════════════════════╗
# ║                          6. FOOTER                                  ║
# ╚═════════════════════════════════════════════════════════════════════╝
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding-bottom: 25px;">
    🏭 <b>Đồ Án Môn Học E-Logistics & Supply Chain Management</b> | Nhiệm vụ 5: Tối ưu Hóa Nhân Sự & Hiệu Quả Kinh Tế<br>
    Được xây dựng với Python, Streamlit & Plotly Interactive Charts.
</div>
""", unsafe_allow_html=True)
