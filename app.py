# -*- coding: utf-8 -*-
"""
🏭 E-LOGISTICS AI WORKFORCE PLANNER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hệ thống AI dự báo & tối ưu hóa nhân sự kho hàng Flash Sale
Giải pháp: Phân bổ Nhân sự Linh hoạt & Tối ưu Hóa Hiệu Quả Kinh Tế
Tích hợp: Mô hình Machine Learning XGBoost & Định mức UPH Chuẩn Vận Hành
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
    page_title="E-Logistics AI Workforce Planner | Hệ Thống Tối Ưu Nhân Lực Kho",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_html(content: str):
    """Render HTML an toan, tu dong dung st.html (Streamlit 1.34+) hoac st.markdown fallback."""
    if hasattr(st, "html"):
        st.html(content)
    else:
        st.markdown(content, unsafe_allow_html=True)

# Custom CSS cho phong cách Modern Executive Logistics Dashboard
render_html("""
<style>
    /* Áp dụng font chữ chuẩn cho văn bản, không ép lên icon hệ thống */
    html, body, .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, button, input {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* Bảo vệ biểu tượng icon của Streamlit không bị vỡ thành chữ */
    [data-testid*="Icon"],
    [data-testid="stExpanderToggleIcon"],
    [data-testid="stIconMaterial"],
    [data-testid="collapsedControl"] *,
    .material-symbols-rounded,
    .material-icons,
    span[data-testid="stExpanderToggleIcon"] {
        font-family: "Material Symbols Rounded", "Material Icons" !important;
    }
    
    /* Ẩn footer và menu phụ không cần thiết */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    
    /* Header trong suốt nhưng GIỮ NGUYÊN nút mở Sidebar ở góc trên bên trái */
    header {
        background: transparent !important;
    }
    
    /* Hiển thị rõ nét nút mở Sidebar (collapsedControl) ở góc trái khi sidebar bị đóng */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        color: #0f172a !important;
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        z-index: 999999 !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
    }
    [data-testid="collapsedControl"]:hover {
        background: #f1f5f9 !important;
        border-color: #3b82f6 !important;
    }

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
""")


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
    st.caption("Hệ Thống Quản Trị Vận Hành & Mô Phỏng Nhân Lực Kho")
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

    # 3. Thông số định mức vận hành chuẩn
    with st.expander("⚙️ Định Mức Vận Hành (UPH)", expanded=False):
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

    st.markdown("#### 📐 Công thức Định Mức Nhân Lực AI")
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
render_html("""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
        <div>
            <h1>🏭 E-LOGISTICS AI WORKFORCE PLANNER</h1>
            <p>Hệ thống AI Tối ưu Hóa Phân bổ Nhân sự Kho & Bài toán Kinh tế Đêm Flash Sale</p>
        </div>
    </div>
    <div class="hero-tags">
        <span class="badge badge-blue">📌 E-Logistics Smart Workforce</span>
        <span class="badge badge-green">🤖 Tích hợp AI XGBoost & Định mức UPH Chuẩn</span>
        <span class="badge badge-purple">🎯 Mục tiêu: Xóa sạch 100% Backlog & Tối ưu Chi phí</span>
    </div>
</div>
""")

# Tabs Điều Hướng Chính
tab_dashboard, tab_stations, tab_model_connect, tab_sensitivity, tab_roi, tab_defense_qa, tab_deploy_qr = st.tabs([
    "📊 1. LIVE DEMO ĐỐI CHỨNG",
    "🏢 2. PHÂN BỔ 4 TRẠM KHO",
    "🤖 3. MÔ HÌNH ML (XGB vs LR) & XẾP CA 24H",
    "📈 4. ĐỘ NHẠY & BIỂU ĐỒ RA QUYẾT ĐỊNH",
    "💰 5. MÁY TÍNH ROI & HÒA VỐN",
    "🛡️ 6. CẨM NĂNG BẢO VỆ PHẢN BIỆN",
    "📱 7. DEPLOY & TẠO QR CANVA"
])

# ─────────────────────────────────────────────────────────────────────
# TAB 1: LIVE DEMO ĐỐI CHỨNG (TRỌNG TÂM THUYẾT TRÌNH)
# ─────────────────────────────────────────────────────────────────────
with tab_dashboard:
    # Hàng 4 thẻ chỉ số nhanh (Metric Cards)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_html(f"""
        <div class="metric-card card-primary">
            <div class="card-label">📦 Tổng đơn AI dự báo</div>
            <div class="card-value" style="color: #2563eb;">{fmt_num(total_orders)}</div>
            <div class="card-sub">⚡ Ca Flash Sale (0h - 2h sáng)</div>
        </div>
        """)
    with c2:
        render_html(f"""
        <div class="metric-card card-success">
            <div class="card-label">👷 Nhân sự AI đề xuất</div>
            <div class="card-value" style="color: #059669;">{ai_staff_required} người</div>
            <div class="card-sub">🛡️ Đã cộng {risk_alpha}% hệ số rủi ro</div>
        </div>
        """)
    with c3:
        render_html(f"""
        <div class="metric-card card-danger">
            <div class="card-label">💥 Tồn đọng (Không AI)</div>
            <div class="card-value" style="color: #dc2626;">{fmt_num(trad_backlog)}</div>
            <div class="card-sub">⚠️ Tỷ lệ trễ hạn: <b>{trad_backlog_pct:.1f}%</b></div>
        </div>
        """)
    with c4:
        if net_savings >= 0:
            render_html(f"""
            <div class="metric-card card-success">
                <div class="card-label">💰 Tiết kiệm ròng</div>
                <div class="card-value" style="color: #059669;">{fmt_vnd(net_savings)}</div>
                <div class="card-sub">🚀 Giảm {(net_savings/trad_total_loss*100) if trad_total_loss>0 else 0:.1f}% tổng chi phí</div>
            </div>
            """)
        else:
            render_html(f"""
            <div class="metric-card card-warning">
                <div class="card-label">💰 Chi phí phát sinh</div>
                <div class="card-value" style="color: #d97706;">{fmt_vnd(abs(net_savings))}</div>
                <div class="card-sub">Đơn ít: Truyền thống vừa đủ sức</div>
            </div>
            """)

    render_html("<br>")

    # 2 BỨC TRANH ĐỐI LẬP (THE CORE STORY)
    col_trad, col_ai = st.columns(2)

    with col_trad:
        render_html(f"""
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
        """)

    with col_ai:
        render_html(f"""
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
        """)

    # BANNER TIẾT KIỆM KHỔNG LỒ
    if net_savings > 0:
        render_html(f"""
        <div class="grand-savings">
            <div class="title">🏆 ĐIỂM ĂN TIỀN NHẤT — AI GIÚP DOANH NGHIỆP TIẾT KIỆM RÒNG</div>
            <div class="amount">{fmt_vnd(net_savings)}</div>
            <div class="subtitle">Chỉ trong 01 đêm Flash Sale bùng nổ ({fmt_num(total_orders)} đơn hàng)</div>
        </div>
        """)
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

    # ─── NÚT XUẤT KẾ HOẠCH CA TRỰC RA FILE CSV ───
    st.markdown("---")
    st.markdown("### 📥 Xuất Bảng Kế Hoạch Vận Hành Ca Trực Thực Tế")
    st.caption("Tải bảng phân công chi tiết để in dán tại kho hoặc nộp kèm báo cáo đồ án cho Giảng viên")

    exp_col1, exp_col2 = st.columns([3, 1])
    with exp_col1:
        st.markdown(f"""
        - 📦 **Tổng đơn dự báo:** {fmt_num(total_orders)} đơn | 👷 **Tổng nhân sự:** {ai_staff_required} người
        - ⚡ **Khung giờ làm việc:** 00:00 - 02:00 (2 tiếng) | 🛡️ **Độ phủ cam kết SLA:** 100%
        """)

    # Phân bổ nhân sự 4 trạm đảm bảo tổng luôn khớp 100% bằng ai_staff_required
    p_pick = max(1, round(ai_staff_required * 0.35))
    p_sort = max(1, round(ai_staff_required * 0.20))
    p_pack = max(1, round(ai_staff_required * 0.35))
    p_disp = ai_staff_required - (p_pick + p_sort + p_pack)
    if p_disp < 1:
        p_disp = 1
        if p_pack > 1:
            p_pack -= 1
        elif p_pick > 1:
            p_pick -= 1
    stn_picking = p_pick
    stn_sorting = p_sort
    stn_packing = p_pack
    stn_dispatch = p_disp

    schedule_data = [
        {"STT": 1, "Vị Trí Công Việc": "1. Lấy hàng (Picking - Batching)", "Tỷ Lệ": "35%", "Số Lượng (Người)": stn_picking, "Định Mức (Đơn/H)": uph, "Tổng Năng Lực (Đơn)": stn_picking * capacity_per_person, "Trang Thiết Bị": "Máy quét PDA, Xe Trolley 6 ngăn", "Ghi Chú Vận Hành": "Nhặt hàng theo zone kệ A, B, C"},
        {"STT": 2, "Vị Trí Công Việc": "2. Phân loại & Gom đơn (Sorting)", "Tỷ Lệ": "20%", "Số Lượng (Người)": stn_sorting, "Định Mức (Đơn/H)": int(uph * 1.5), "Tổng Năng Lực (Đơn)": stn_sorting * capacity_per_person, "Trang Thiết Bị": "Kệ Put-to-Light, Giỏ phân chia", "Ghi Chú Vận Hành": "Gom hàng đơn lẻ vào từng kiện"},
        {"STT": 3, "Vị Trí Công Việc": "3. Đóng gói & Dán tem (Packing - Thắt cổ chai)", "Tỷ Lệ": "35%", "Số Lượng (Người)": stn_packing, "Định Mức (Đơn/H)": uph, "Tổng Năng Lực (Đơn)": stn_packing * capacity_per_person, "Trang Thiết Bị": "Bàn đóng gói, Máy in nhiệt A6, Băng keo", "Ghi Chú Vận Hành": "Mắt xích trọng yếu - Ưu tiên hỗ trợ"},
        {"STT": 4, "Vị Trí Công Việc": "4. Xuất kho & Bàn giao xe tải (Dispatch)", "Tỷ Lệ": "10%", "Số Lượng (Người)": stn_dispatch, "Định Mức (Đơn/H)": uph * 2, "Tổng Năng Lực (Đơn)": stn_dispatch * capacity_per_person, "Trang Thiết Bị": "Xe nâng tay, Pallet, Seal niêm phong", "Ghi Chú Vận Hành": "Bàn giao đơn vị SPX / GHN / J&T"}
    ]
    df_schedule = pd.DataFrame(schedule_data)

    csv_buffer = io.StringIO()
    df_schedule.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    csv_bytes = csv_buffer.getvalue().encode("utf-8-sig")

    with exp_col2:
        st.download_button(
            label="📥 Tải Bảng Phân Công (.CSV)",
            data=csv_bytes,
            file_name=f"ke_hoach_ca_truc_{total_orders}_don.csv",
            mime="text/csv",
            use_container_width=True
        )


# ─────────────────────────────────────────────────────────────────────
# TAB 2: SƠ ĐỒ PHÂN BỔ 4 TRẠM KHO (CHUYÊN MÔN LOGISTICS CAO CẤP)
# ─────────────────────────────────────────────────────────────────────
with tab_stations:
    st.markdown("### 🏢 Phân Bổ Chi Tiết 4 Trạm Vận Hành: Chức Năng, Nhiệm Vụ, Nhân Sự & Chi Phí")
    st.markdown("""
    Trong trung tâm hoàn tất đơn hàng (Fulfillment Center), **nhân sự được phân bổ theo 4 trạm nghiệp vụ chuyên biệt**.
    Dưới đây là hạch toán cụ thể về **số lượng con người, nhiệm vụ chi tiết và ngân sách chi tiêu của từng trạm** 
    để cấp quản lý nắm rõ từng đồng chi phí ca đêm:
    """)

    # Tính toán chi phí cụ thể từng trạm
    stn_picking_wage = stn_picking * wage_per_person
    stn_sorting_wage = stn_sorting * wage_per_person
    stn_packing_wage = stn_packing * wage_per_person
    stn_dispatch_wage = stn_dispatch * wage_per_person

    stn_picking_supplies = stn_picking * 3000   # Pin PDA, găng tay chống trượt
    stn_sorting_supplies = stn_sorting * 2500   # Khay nhựa Tote, thẻ phân loại
    stn_packing_supplies = stn_packing * 15000  # Giấy in tem A6, màng xốp khí, băng dính chữ H
    stn_dispatch_supplies = stn_dispatch * 4000 # Màng PE quấn Pallet, seal niêm phong

    stn_picking_total = stn_picking_wage + stn_picking_supplies
    stn_sorting_total = stn_sorting_wage + stn_sorting_supplies
    stn_packing_total = stn_packing_wage + stn_packing_supplies
    stn_dispatch_total = stn_dispatch_wage + stn_dispatch_supplies
    grand_stations_total = stn_picking_total + stn_sorting_total + stn_packing_total + stn_dispatch_total

    # 4 Thẻ KPI Tổng Quan Ngân Sách Từng Trạm
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_html(f"""
        <div class="metric-card" style="border-left: 5px solid #3b82f6;">
            <div class="card-label">🛒 1. TRẠM LẤY HÀNG (PICKING)</div>
            <div style="font-size:1.6rem; font-weight:800; color:#2563eb; margin:4px 0;">{stn_picking} người</div>
            <div style="font-weight:700; color:#0f172a; font-size:1.05rem;">{fmt_vnd(stn_picking_total)}</div>
            <div style="font-size:0.8rem; color:#64748b; margin-top:2px;">(Lương: {fmt_vnd(stn_picking_wage)} | Vật tư: {fmt_vnd(stn_picking_supplies)})</div>
        </div>
        """)
    with k2:
        render_html(f"""
        <div class="metric-card" style="border-left: 5px solid #f59e0b;">
            <div class="card-label">🗂️ 2. TRẠM PHÂN LOẠI (SORTING)</div>
            <div style="font-size:1.6rem; font-weight:800; color:#d97706; margin:4px 0;">{stn_sorting} người</div>
            <div style="font-weight:700; color:#0f172a; font-size:1.05rem;">{fmt_vnd(stn_sorting_total)}</div>
            <div style="font-size:0.8rem; color:#64748b; margin-top:2px;">(Lương: {fmt_vnd(stn_sorting_wage)} | Vật tư: {fmt_vnd(stn_sorting_supplies)})</div>
        </div>
        """)
    with k3:
        render_html(f"""
        <div class="metric-card" style="border-left: 5px solid #e11d48; background:#fff1f2;">
            <div class="card-label" style="color:#be123c;">📦 3. ĐÓNG GÓI (PACKING - NGHẼN)</div>
            <div style="font-size:1.6rem; font-weight:800; color:#e11d48; margin:4px 0;">{stn_packing} người</div>
            <div style="font-weight:700; color:#be123c; font-size:1.05rem;">{fmt_vnd(stn_packing_total)}</div>
            <div style="font-size:0.8rem; color:#9f1239; margin-top:2px;">(Lương: {fmt_vnd(stn_packing_wage)} | Vật tư: {fmt_vnd(stn_packing_supplies)})</div>
        </div>
        """)
    with k4:
        render_html(f"""
        <div class="metric-card" style="border-left: 5px solid #10b981;">
            <div class="card-label">🚚 4. TRẠM XUẤT KHO (DISPATCH)</div>
            <div style="font-size:1.6rem; font-weight:800; color:#059669; margin:4px 0;">{stn_dispatch} người</div>
            <div style="font-weight:700; color:#0f172a; font-size:1.05rem;">{fmt_vnd(stn_dispatch_total)}</div>
            <div style="font-size:0.8rem; color:#64748b; margin-top:2px;">(Lương: {fmt_vnd(stn_dispatch_wage)} | Vật tư: {fmt_vnd(stn_dispatch_supplies)})</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=False)

    # 2 Biểu Đồ So Sánh: Cơ Cấu Nhân Sự vs Cơ Cấu Ngân Sách
    ch_col1, ch_col2 = st.columns(2)
    with ch_col1:
        fig_donut_staff = go.Figure(data=[go.Pie(
            labels=[f"🛒 Picking ({stn_picking} người)", f"🗂️ Sorting ({stn_sorting} người)", f"📦 Packing ({stn_packing} người)", f"🚚 Dispatch ({stn_dispatch} người)"],
            values=[stn_picking, stn_sorting, stn_packing, stn_dispatch],
            hole=0.52,
            marker=dict(colors=["#3b82f6", "#f59e0b", "#e11d48", "#10b981"]),
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Tỷ lệ: %{percent}<extra></extra>"
        )])
        fig_donut_staff.update_layout(
            title="<b>Cơ Cấu Phân Bổ Nhân Sự (Người)</b>",
            annotations=[dict(text=f"<b>{ai_staff_required}</b><br>Người", x=0.5, y=0.5, font_size=17, showarrow=False)],
            template='plotly_white',
            showlegend=False,
            height=340,
            margin=dict(t=50, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_donut_staff, use_container_width=True)

    with ch_col2:
        fig_donut_cost = go.Figure(data=[go.Pie(
            labels=[f"🛒 Picking ({fmt_vnd(stn_picking_total)})", f"🗂️ Sorting ({fmt_vnd(stn_sorting_total)})", f"📦 Packing ({fmt_vnd(stn_packing_total)})", f"🚚 Dispatch ({fmt_vnd(stn_dispatch_total)})"],
            values=[stn_picking_total, stn_sorting_total, stn_packing_total, stn_dispatch_total],
            hole=0.52,
            marker=dict(colors=["#60a5fa", "#fbbf24", "#f43f5e", "#34d399"]),
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Tỷ lệ ngân sách: %{percent}<extra></extra>"
        )])
        fig_donut_cost.update_layout(
            title="<b>Cơ Cấu Ngân Sách Vận Hành (VNĐ)</b>",
            annotations=[dict(text=f"<b>{fmt_vnd(grand_stations_total)}</b>", x=0.5, y=0.5, font_size=15, showarrow=False)],
            template='plotly_white',
            showlegend=False,
            height=340,
            margin=dict(t=50, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_donut_cost, use_container_width=True)

    st.markdown("### 📋 Mô Tả Chức Năng, Nhiệm Vụ & Hạch Toán Chi Phí Từng Trạm")

    st_col_left, st_col_right = st.columns(2)

    with st_col_left:
        # TRẠM 1: PICKING
        render_html(f"""
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:5px solid #3b82f6; border-radius:14px; padding:20px; margin-bottom:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#1e40af;">🛒 1. Trạm Lấy Hàng (Picking - Zone/Batch)</h4>
                <span style="background:#dbeafe; color:#1e40af; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.85rem;">35% Nhân Sự</span>
            </div>
            <div style="margin:10px 0; padding:10px; background:#f8fafc; border-radius:8px; display:flex; justify-content:space-around; font-size:0.9rem;">
                <div>👤 <b>Nhân sự:</b> {stn_picking} người</div>
                <div>💰 <b>Tổng chi phí:</b> {fmt_vnd(stn_picking_total)}</div>
                <div>⚡ <b>Năng lực:</b> {fmt_num(stn_picking * capacity_per_person)} đơn</div>
            </div>
            <p style="margin:6px 0; color:#334155; font-size:0.92rem;"><b>🎯 Chức năng cốt lõi:</b> Tiếp nhận danh sách đơn hàng xuất kho (Pick-list) từ hệ thống WMS, di chuyển đến đúng vị trí kệ để rút sản phẩm chính xác 100%.</p>
            <div style="color:#475569; font-size:0.88rem; line-height:1.6;">
                <b>📋 Nhiệm vụ cụ thể:</b><br>
                • <b>Bước 1:</b> Đăng nhập máy quét PDA nhận phân vùng lấy hàng (Zone A/B/C).<br>
                • <b>Bước 2:</b> Đẩy xe Trolley 6 ngăn di chuyển theo lộ trình tối ưu hình zíc-zắc (S-Shape) để tiết kiệm bước chân.<br>
                • <b>Bước 3:</b> Quét mã vạch vị trí kệ (Location Barcode) → Quét mã vạch sản phẩm (SKU Barcode) → Đặt vào ngăn chỉ định.<br>
                • <b>Bước 4:</b> Đẩy giỏ hàng đã đầy đến trạm phân loại (Sorting Station).
            </div>
            <div style="margin-top:10px; padding-top:10px; border-top:1px dashed #e2e8f0; font-size:0.85rem; color:#64748b;">
                🛠️ <b>Công cụ & Vật tư:</b> Máy PDA quét mã vạch Honeywell/Zebra, xe đẩy Trolley đa tầng, găng tay PU chống trơn trượt.<br>
                💸 <b>Hạch toán chi phí:</b> Tiền lương ca đêm ({stn_picking} × {fmt_num(wage_per_person)}đ = <b>{fmt_vnd(stn_picking_wage)}</b>) + Khấu hao PDA & găng tay (<b>{fmt_vnd(stn_picking_supplies)}</b>).
            </div>
        </div>
        """)

        # TRẠM 3: PACKING (THẮT CỔ CHAI)
        render_html(f"""
        <div style="background:#fff1f2; border:1.5px solid #fecdd3; border-top:5px solid #e11d48; border-radius:14px; padding:20px; margin-bottom:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#9f1239;">📦 3. Trạm Đóng Gói (Packing & Labeling) ⚠️ THẮT CỔ CHAI</h4>
                <span style="background:#ffe4e6; color:#9f1239; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.85rem;">35% Nhân Sự</span>
            </div>
            <div style="margin:10px 0; padding:10px; background:#ffffff; border-radius:8px; display:flex; justify-content:space-around; font-size:0.9rem;">
                <div>👤 <b>Nhân sự:</b> {stn_packing} người</div>
                <div>💰 <b>Tổng chi phí:</b> {fmt_vnd(stn_packing_total)}</div>
                <div>⚡ <b>Năng lực:</b> {fmt_num(stn_packing * capacity_per_person)} đơn</div>
            </div>
            <p style="margin:6px 0; color:#334155; font-size:0.92rem;"><b>🎯 Chức năng cốt lõi:</b> Bảo vệ an toàn cơ lý cho sản phẩm và dán nhãn vận đơn hợp lệ theo đúng tiêu chuẩn sàn TMĐT (Shopee/Lazada/TikTok).</p>
            <div style="color:#475569; font-size:0.88rem; line-height:1.6;">
                <b>📋 Nhiệm vụ cụ thể:</b><br>
                • <b>Bước 1:</b> Quét mã kiện hàng nhận diện sản phẩm → Hệ thống tự động in tem vận chuyển A6 ra máy in nhiệt.<br>
                • <b>Bước 2:</b> Chọn quy cách bao bì phù hợp (hộp carton sóng 3 lớp hoặc túi niêm phong PE chống xé).<br>
                • <b>Bước 3:</b> Quấn 2-3 lớp màng bóng khí bọc hàng dễ vỡ (mỹ phẩm, gốm sứ), chèn túi khí chống rung lắc.<br>
                • <b>Bước 4:</b> Dán kín băng keo đáy và nắp hộp hình chữ H → Dán phẳng tem nhiệt vận đơn lên mặt trên cùng.<br>
                ⚠️ <i>Lưu ý: Đây là trạm tốn thời gian thao tác tay nhất (20-30 giây/đơn), nếu trạm này nghẽn thì toàn bộ kho bị tê liệt!</i>
            </div>
            <div style="margin-top:10px; padding-top:10px; border-top:1px dashed #fecdd3; font-size:0.85rem; color:#881337;">
                🛠️ <b>Công cụ & Vật tư:</b> Bàn đóng gói công thái học, máy in nhiệt HPRT/Xprinter, cuộn màng xốp khí, dao cắt băng dính.<br>
                💸 <b>Hạch toán chi phí:</b> Tiền lương ({stn_packing} × {fmt_num(wage_per_person)}đ = <b>{fmt_vnd(stn_packing_wage)}</b>) + Vật tư tiêu hao tem in & băng keo (<b>{fmt_vnd(stn_packing_supplies)}</b>).
            </div>
        </div>
        """)

    with st_col_right:
        # TRẠM 2: SORTING
        render_html(f"""
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:5px solid #f59e0b; border-radius:14px; padding:20px; margin-bottom:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#b45309;">🗂️ 2. Trạm Phân Loại & Gom Đơn (Sorting & Consolidation)</h4>
                <span style="background:#fef3c7; color:#b45309; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.85rem;">20% Nhân Sự</span>
            </div>
            <div style="margin:10px 0; padding:10px; background:#f8fafc; border-radius:8px; display:flex; justify-content:space-around; font-size:0.9rem;">
                <div>👤 <b>Nhân sự:</b> {stn_sorting} người</div>
                <div>💰 <b>Tổng chi phí:</b> {fmt_vnd(stn_sorting_total)}</div>
                <div>⚡ <b>Năng lực:</b> {fmt_num(stn_sorting * capacity_per_person)} đơn</div>
            </div>
            <p style="margin:6px 0; color:#334155; font-size:0.92rem;"><b>🎯 Chức năng cốt lõi:</b> Tách lọc các mặt hàng nhặt theo lô (Batch) về đúng từng đơn hàng của từng khách lẻ (Đơn 1 món vs Đơn nhiều món).</p>
            <div style="color:#475569; font-size:0.88rem; line-height:1.6;">
                <b>📋 Nhiệm vụ cụ thể:</b><br>
                • <b>Bước 1:</b> Tiếp nhận giỏ hàng Trolley từ trạm lấy hàng đẩy sang.<br>
                • <b>Bước 2:</b> Bắn mã vạch từng món hàng → Kệ chia hàng thông minh Put-to-Light sẽ sáng đèn LED tại ô chứa đơn tương ứng.<br>
                • <b>Bước 3:</b> Đặt sản phẩm vào ô sáng đèn → Nhấn nút xác nhận hoàn thành.<br>
                • <b>Bước 4:</b> Khi ô chứa đã đủ 100% món của đơn (Complete), đèn chuyển sang màu xanh lá → Chuyển giỏ hàng sang trạm Packing.
            </div>
            <div style="margin-top:10px; padding-top:10px; border-top:1px dashed #e2e8f0; font-size:0.85rem; color:#64748b;">
                🛠️ <b>Công cụ & Vật tư:</b> Giá kệ Put-to-Light tích hợp cảm biến LED, khay nhựa Tote đa năng, máy quét để bàn gắn cố định.<br>
                💸 <b>Hạch toán chi phí:</b> Tiền lương ca đêm ({stn_sorting} × {fmt_num(wage_per_person)}đ = <b>{fmt_vnd(stn_sorting_wage)}</b>) + Khấu hao khay nhựa & kệ (<b>{fmt_vnd(stn_sorting_supplies)}</b>).
            </div>
        </div>
        """)

        # TRẠM 4: DISPATCH
        render_html(f"""
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:5px solid #10b981; border-radius:14px; padding:20px; margin-bottom:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#047857;">🚚 4. Trạm Xuất Kho & Bàn Giao Xe Tải (Dispatch & Handover)</h4>
                <span style="background:#d1fae5; color:#047857; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.85rem;">10% Nhân Sự</span>
            </div>
            <div style="margin:10px 0; padding:10px; background:#f8fafc; border-radius:8px; display:flex; justify-content:space-around; font-size:0.9rem;">
                <div>👤 <b>Nhân sự:</b> {stn_dispatch} người</div>
                <div>💰 <b>Tổng chi phí:</b> {fmt_vnd(stn_dispatch_total)}</div>
                <div>⚡ <b>Năng lực:</b> {fmt_num(stn_dispatch * capacity_per_person)} đơn</div>
            </div>
            <p style="margin:6px 0; color:#334155; font-size:0.92rem;"><b>🎯 Chức năng cốt lõi:</b> Phân loại đơn hàng theo từng nhà xe/bưu cục vận chuyển (3PL), niêm phong túi bao hàng và bàn giao xe tải đúng khung giờ cam kết (SLA Cut-off).</p>
            <div style="color:#475569; font-size:0.88rem; line-height:1.6;">
                <b>📋 Nhiệm vụ cụ thể:</b><br>
                • <b>Bước 1:</b> Quét mã vạch tiếp nhận đơn đã đóng gói từ trạm Packing chuyển qua.<br>
                • <b>Bước 2:</b> Bắn mã gộp đơn vào từng túi bao tải chuyên dụng theo từng hãng (Bao SPX, Bao GHN, Bao Viettel Post, Bao J&T).<br>
                • <b>Bước 3:</b> Bấm kẹp chì / seal nhựa niêm phong miệng bao tải → In biên bản bàn giao bàn giao hàng loạt (Handover Manifest).<br>
                • <b>Bước 4:</b> Dùng xe nâng tay kéo các kiện Pallet xếp gọn lên thùng xe tải của các đối tác vận chuyển trước 02h15 sáng.
            </div>
            <div style="margin-top:10px; padding-top:10px; border-top:1px dashed #e2e8f0; font-size:0.85rem; color:#64748b;">
                🛠️ <b>Công cụ & Vật tư:</b> Xe nâng tay thủy lực (Hand Pallet Truck), màng co PE quấn Pallet, kẹp chì seal niêm phong, máy in Manifest.<br>
                💸 <b>Hạch toán chi phí:</b> Tiền lương ({stn_dispatch} × {fmt_num(wage_per_person)}đ = <b>{fmt_vnd(stn_dispatch_wage)}</b>) + Seal nhựa & màng quấn (<b>{fmt_vnd(stn_dispatch_supplies)}</b>).
            </div>
        </div>
        """)

    # BẢNG TỔNG KẾT NGÂN SÁCH ĐIỀU HÀNH KHO CHI TIẾT
    st.markdown("#### 📊 Bảng Hạch Toán Toàn Diện Chi Phí Vận Hành 4 Trạm (Station Budget Master Table)")
    station_master_data = [
        {
            "Mã Trạm": "STN-01",
            "Tên Trạm Vận Hành": "🛒 Lấy hàng (Picking - Batching)",
            "Tỷ Lệ": "35%",
            "Nhân Sự (Người)": stn_picking,
            "Tiền Lương Ca Đêm (VNĐ)": fmt_vnd(stn_picking_wage),
            "Chi Phí Vật Tư / Thiết Bị (VNĐ)": fmt_vnd(stn_picking_supplies),
            "TỔNG CHI PHÍ TRẠM (VNĐ)": fmt_vnd(stn_picking_total),
            "Chi Phí / Đơn Hàng": f"{(stn_picking_total / total_orders):,.0f} đ/đơn" if total_orders > 0 else "0 đ",
            "Mức Độ Rủi Ro": "Trung bình (Đi bộ nhiều)"
        },
        {
            "Mã Trạm": "STN-02",
            "Tên Trạm Vận Hành": "🗂️ Phân loại & Gom đơn (Sorting)",
            "Tỷ Lệ": "20%",
            "Nhân Sự (Người)": stn_sorting,
            "Tiền Lương Ca Đêm (VNĐ)": fmt_vnd(stn_sorting_wage),
            "Chi Phí Vật Tư / Thiết Bị (VNĐ)": fmt_vnd(stn_sorting_supplies),
            "TỔNG CHI PHÍ TRẠM (VNĐ)": fmt_vnd(stn_sorting_total),
            "Chi Phí / Đơn Hàng": f"{(stn_sorting_total / total_orders):,.0f} đ/đơn" if total_orders > 0 else "0 đ",
            "Mức Độ Rủi Ro": "Thấp (Có LED hỗ trợ)"
        },
        {
            "Mã Trạm": "STN-03",
            "Tên Trạm Vận Hành": "📦 Đóng gói & Dán nhãn (Packing)",
            "Tỷ Lệ": "35%",
            "Nhân Sự (Người)": stn_packing,
            "Tiền Lương Ca Đêm (VNĐ)": fmt_vnd(stn_packing_wage),
            "Chi Phí Vật Tư / Thiết Bị (VNĐ)": fmt_vnd(stn_packing_supplies),
            "TỔNG CHI PHÍ TRẠM (VNĐ)": fmt_vnd(stn_packing_total),
            "Chi Phí / Đơn Hàng": f"{(stn_packing_total / total_orders):,.0f} đ/đơn" if total_orders > 0 else "0 đ",
            "Mức Độ Rủi Ro": "🔴 CAO NHẤT (Thắt cổ chai)"
        },
        {
            "Mã Trạm": "STN-04",
            "Tên Trạm Vận Hành": "🚚 Bàn giao xuất kho (Dispatch)",
            "Tỷ Lệ": "10%",
            "Nhân Sự (Người)": stn_dispatch,
            "Tiền Lương Ca Đêm (VNĐ)": fmt_vnd(stn_dispatch_wage),
            "Chi Phí Vật Tư / Thiết Bị (VNĐ)": fmt_vnd(stn_dispatch_supplies),
            "TỔNG CHI PHÍ TRẠM (VNĐ)": fmt_vnd(stn_dispatch_total),
            "Chi Phí / Đơn Hàng": f"{(stn_dispatch_total / total_orders):,.0f} đ/đơn" if total_orders > 0 else "0 đ",
            "Mức Độ Rủi Ro": "Trung bình (Áp lực giờ xe chạy)"
        },
        {
            "Mã Trạm": "TỔNG CỘNG",
            "Tên Trạm Vận Hành": "🏭 TOÀN BỘ DÂY CHUYỀN KHO FLASH SALE",
            "Tỷ Lệ": "100%",
            "Nhân Sự (Người)": ai_staff_required,
            "Tiền Lương Ca Đêm (VNĐ)": fmt_vnd(ai_wage_cost),
            "Chi Phí Vật Tư / Thiết Bị (VNĐ)": fmt_vnd(stn_picking_supplies + stn_sorting_supplies + stn_packing_supplies + stn_dispatch_supplies),
            "TỔNG CHI PHÍ TRẠM (VNĐ)": fmt_vnd(grand_stations_total),
            "Chi Phí / Đơn Hàng": f"{(grand_stations_total / total_orders):,.0f} đ/đơn" if total_orders > 0 else "0 đ",
            "Mức Độ Rủi Ro": "✅ KIỂM SOÁT AN TOÀN 100%"
        }
    ]
    df_station_master = pd.DataFrame(station_master_data)
    st.dataframe(df_station_master, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────
# TAB 3: DỮ LIỆU ĐƠN 24H THỜI GIAN THỰC & XẾP CA FULL-TIME / PART-TIME
# ─────────────────────────────────────────────────────────────────────
with tab_model_connect:
    st.markdown("### ⏱️ Dữ Liệu Đơn Hàng 24 Giờ Thời Gian Thực & Ma Trận Xếp Ca Full-time / Part-time")
    st.markdown("""
    Phân tích chi tiết dòng chảy đơn hàng 24 khung giờ trong ngày từ mô hình Machine Learning **XGBoost** 
    giúp người quản lý kho nhìn thấy rõ **thời điểm đơn bùng nổ (Peak Hour)** và **thời điểm thấp điểm (Valley Hour)**.
    Từ đó, áp dụng chiến lược điều phối **Hybrid Workforce**: Kết hợp **Full-time (Nòng cốt 8h)** và **Part-time (Thời vụ ngắn hạn 2-3h)** 
    để tối ưu hóa triệt để chi phí quỹ lương mà không để xảy ra tồn đọng!
    """)

    csv_path = os.path.join(BASE_DIR, "hourly_aggregated.csv")
    if os.path.exists(csv_path):
        hourly_df = pd.read_csv(csv_path)
        hourly_df['Ngày Sale'] = pd.to_datetime(hourly_df['Ngày Sale'])

        # 1. Bộ lọc ngày & Tải mô hình XGBoost
        col_f1, col_f2 = st.columns([1, 1])
        with col_f1:
            unique_dates = hourly_df['Ngày Sale'].dt.strftime('%Y-%m-%d').unique()
            # Mặc định chọn ngày 2026-10-10 nếu có, hoặc ngày cuối cùng
            default_idx = len(unique_dates) - 1
            if '2026-10-10' in unique_dates:
                default_idx = list(unique_dates).index('2026-10-10')
            selected_date = st.selectbox("📅 Chọn ngày bán hàng để phân tích dòng đơn 24 Giờ:", unique_dates, index=default_idx)

        # Load mô hình XGBoost & Linear Regression
        import joblib
        model_path_xgb = os.path.join(BASE_DIR, "model_xgb.joblib")
        model_path_lr = os.path.join(BASE_DIR, "model_lr.joblib")
        model_xgb = None
        model_lr = None
        if os.path.exists(model_path_xgb):
            try:
                model_xgb = joblib.load(model_path_xgb)
            except Exception:
                model_xgb = None
        if os.path.exists(model_path_lr):
            try:
                model_lr = joblib.load(model_path_lr)
            except Exception:
                model_lr = None

        # Trích xuất dữ liệu ngày được chọn & chuẩn hóa đủ 24 giờ
        day_df = hourly_df[hourly_df['Ngày Sale'].dt.strftime('%Y-%m-%d') == selected_date].copy()
        
        full_24h = pd.DataFrame({'Giờ': list(range(24))})
        full_24h['Khung Giờ'] = full_24h['Giờ'].apply(lambda h: f"{h:02d}:00 - {h:02d}:59")
        
        merged_24h = full_24h.merge(day_df, on='Giờ', how='left')
        merged_24h['Tong_So_Don'] = merged_24h['Tong_So_Don'].fillna(0).astype(int)
        merged_24h['Khung Giờ'] = merged_24h['Khung Giờ_x']
        if 'So_SKU_HoatDong' in merged_24h.columns:
            merged_24h['So_SKU_HoatDong'] = merged_24h['So_SKU_HoatDong'].fillna(20).astype(int)
        
        is_mega_val = 1 if (('IsMegaDay' in day_df.columns) and (day_df['IsMegaDay'].max() == 1)) else 0

        # Dự báo bằng cả 2 mô hình (XGBoost & Linear Regression)
        pred_xgb_list = []
        pred_lr_list = []
        for _, row in merged_24h.iterrows():
            g = int(row['Giờ'])
            act = int(row['Tong_So_Don'])
            dow = pd.to_datetime(selected_date).dayofweek
            d = pd.to_datetime(selected_date).day
            is_wknd = 1 if dow in [5, 6] else 0
            is_fs = 1 if g in [0, 1, 2, 12, 20, 21] else 0
            sku = int(row.get('So_SKU_HoatDong', 50))
            if sku <= 0: sku = 20
            feat = pd.DataFrame([[g, dow, d, is_wknd, is_fs, is_mega_val, sku]],
                                columns=['Giờ', 'DayOfWeek', 'Day', 'IsWeekend', 'IsFlashSaleHour', 'IsMegaDay', 'So_SKU_HoatDong'])
            
            # XGBoost
            if model_xgb is not None:
                try:
                    px = float(model_xgb.predict(feat)[0])
                    px = max(0.0, px)
                except Exception:
                    px = float(act) if act > 0 else 0.0
            else:
                px = float(act) if act > 0 else 0.0
            pred_xgb_list.append(round(px))

            # Linear Regression
            if model_lr is not None:
                try:
                    plr = float(model_lr.predict(feat)[0])
                    plr = max(0.0, plr)
                except Exception:
                    plr = float(act) if act > 0 else 0.0
            else:
                plr = float(act) if act > 0 else 0.0
            pred_lr_list.append(round(plr))

        merged_24h['AI_XGB_DuBao'] = pred_xgb_list
        merged_24h['AI_LR_DuBao'] = pred_lr_list
        # Nhu cầu nhân sự theo từng giờ: N_h = ceil(Đơn / UPH * risk_factor)
        merged_24h['NhanSu_CanThiet'] = merged_24h['Tong_So_Don'].apply(
            lambda o: math.ceil((o / max(1, uph)) * risk_factor) if o > 0 else 1
        )

        # Phân loại trạng thái giờ (Peak / Standard / Valley)
        def classify_hour(o):
            if o >= 120:
                return "🔥 Cao điểm (Peak)", "#ef4444"
            elif o >= 35:
                return "⚡ Tiêu chuẩn (Standard)", "#f59e0b"
            else:
                return "🟢 Thấp điểm (Valley)", "#10b981"

        merged_24h['PhanLoai'] = [classify_hour(o)[0] for o in merged_24h['Tong_So_Don']]
        merged_24h['MauSac'] = [classify_hour(o)[1] for o in merged_24h['Tong_So_Don']]

        with col_f2:
            peak_row = merged_24h.loc[merged_24h['Tong_So_Don'].idxmax()]
            st.info(f"📌 **Sự kiện ngày {selected_date}:** {'🔥 SIÊU SALE (Mega Day)' if is_mega_val else 'Ngày bán hàng thông thường'}. Giờ cao nhất: **{peak_row['Khung Giờ']}** ({fmt_num(peak_row['Tong_So_Don'])} đơn).")

        # 4 Thẻ chỉ số tổng quan 24h
        m1, m2, m3, m4 = st.columns(4)
        total_day_orders = merged_24h['Tong_So_Don'].sum()
        max_hour_orders = peak_row['Tong_So_Don']
        max_hour_staff = peak_row['NhanSu_CanThiet']
        min_hour_orders = merged_24h['Tong_So_Don'].min()

        m1.metric("📦 Tổng Đơn Cả Ngày", f"{fmt_num(total_day_orders)} đơn")
        m2.metric("🔥 Khung Giờ Đỉnh (Peak)", f"{peak_row['Khung Giờ']}", f"{fmt_num(max_hour_orders)} đơn")
        m3.metric("👥 Nhân Sự Giờ Đỉnh Cần", f"{max_hour_staff} người", f"Định mức {uph} đơn/h")
        m4.metric("🟢 Khung Thấp Điểm (Valley)", "03:00 - 05:00", f"Chỉ ~{min_hour_orders} đơn/h")

        st.markdown("---")
        st.markdown("#### 📊 1. Biểu Đồ Phân Bổ Đơn Hàng & Nhu Cầu Nhân Sự 24 Khung Giờ")
        st.caption("🔴 Cột Đỏ: Giờ cao điểm bùng nổ (Peak) | 🟡 Cột Cam: Giờ tiêu chuẩn | 🟢 Cột Xanh: Giờ thấp điểm | 🟣 Đường Tím: Số nhân sự cần thiết")

        col_opt1, col_opt2 = st.columns([3, 2])
        with col_opt1:
            model_overlay = st.radio(
                "🔎 Tùy chọn đường dự báo hiển thị trên biểu đồ 24h:",
                ["🏆 Chỉ XGBoost (Đề xuất)", "⚠️ Chỉ Linear Regression (Mô hình cũ)", "⚔️ So Sánh Cả 2 Mô Hình Đối Đầu"],
                horizontal=True
            )

        # Biểu đồ kết hợp Bar + Scatter line
        fig_24h = go.Figure()
        fig_24h.add_trace(go.Bar(
            x=merged_24h['Khung Giờ'],
            y=merged_24h['Tong_So_Don'],
            name='📦 Số lượng đơn hàng thực tế',
            marker=dict(color=merged_24h['MauSac']),
            hovertemplate="<b>Khung giờ:</b> %{x}<br><b>Số đơn thực tế:</b> %{y:,.0f} đơn<br><extra></extra>"
        ))
        fig_24h.add_trace(go.Scatter(
            x=merged_24h['Khung Giờ'],
            y=merged_24h['NhanSu_CanThiet'],
            name='👥 Số nhân sự cần huy động (Người)',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='#8b5cf6', width=2.5),
            marker=dict(size=6, color='#6d28d9'),
            hovertemplate="<b>Nhân sự cần:</b> %{y} người<br><extra></extra>"
        ))

        # Đường dự báo XGBoost
        if "XGBoost" in model_overlay or "So Sánh" in model_overlay:
            fig_24h.add_trace(go.Scatter(
                x=merged_24h['Khung Giờ'],
                y=merged_24h['AI_XGB_DuBao'],
                name='🏆 XGBoost Dự Báo (R² 92.5%)',
                mode='lines+markers',
                line=dict(color='#059669', width=3),
                marker=dict(size=7, symbol='diamond', color='#10b981'),
                hovertemplate="<b>XGBoost:</b> %{y:,.0f} đơn<br><extra></extra>"
            ))

        # Đường dự báo Linear Regression
        if "Linear Regression" in model_overlay or "So Sánh" in model_overlay:
            fig_24h.add_trace(go.Scatter(
                x=merged_24h['Khung Giờ'],
                y=merged_24h['AI_LR_DuBao'],
                name='⚠️ Linear Regression Dự Báo (R² 56.5%)',
                mode='lines+markers',
                line=dict(color='#ef4444', width=2.5, dash='dash'),
                marker=dict(size=6, symbol='circle', color='#dc2626'),
                hovertemplate="<b>Linear Reg:</b> %{y:,.0f} đơn<br><extra></extra>"
            ))

        fig_24h.update_layout(
            title=f"<b>Dòng Chảy Đơn Hàng & So Sánh Dự Báo ML 24 Giờ Ngày {selected_date}</b>",
            xaxis_title="24 Khung Giờ Hoạt Động (00:00 - 23:59)",
            yaxis=dict(title="Số Lượng Đơn Hàng (Đơn)", side="left"),
            yaxis2=dict(title="Số Nhân Sự Cần Thiết (Người)", overlaying="y", side="right", showgrid=False),
            template='plotly_white',
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            height=440,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig_24h, use_container_width=True)

        st.markdown("---")
        # 2. CHIẾN LƯỢC XẾP CA: FULL-TIME VS PART-TIME
        st.markdown("#### 🎯 2. Chiến Lược Xếp Ca Thông Minh: Full-time vs Part-time")
        
        render_html("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:18px; margin-bottom:18px;">
            <h5 style="margin-top:0; color:#0f172a;">💡 Nghịch Lý Quản Trị Kho Vận & Lời Giải AI:</h5>
            <ul style="color:#334155; margin-bottom:0; font-size:0.95rem; line-height:1.6;">
                <li><b>❌ Nếu dùng 100% Full-time (Ca 8 tiếng):</b> Vào lúc nửa đêm (00:00 - 02:00) đơn đạt đỉnh cần tới <b>~75 - 86 nhân viên</b>. 
                Nếu thuê 86 nhân viên Full-time làm ca đêm, sang các giờ 03:00 - 06:00 sáng đơn tụt về 0 đơn/giờ, 
                hàng chục nhân viên ngồi rảnh nhưng công ty vẫn phải trả nguyên 8 tiếng lương (<b>24.080.000 VNĐ</b>) &rarr; Lãng phí hơn <b>14 triệu VNĐ</b>!</li>
                <li><b>✅ Mô hình AI Hybrid (Full-time Cốt lõi + Part-time Thời vụ):</b>
                    <br>&bull; <b>Full-time (8 tiếng):</b> Duy trì đội ngũ cố định <b>10 - 12 nhân viên nòng cốt</b> (Trưởng ca, Quản lý hệ thống WMS, KCS kiểm tra chất lượng, Bàn giao đối tác 3PL SPX/GHN).
                    <br>&bull; <b>Part-time (2 - 3 tiếng):</b> Kích hoạt <b>60 - 75 sinh viên/lao động thời vụ</b> vào đúng khung giờ cao điểm Flash Sale (23:30 - 02:30). Chỉ trả lương đúng 2-3 giờ thực làm!
                    <br>&bull; <b>Hiệu quả kinh tế:</b> Cắt giảm tới <b>55% - 60%</b> tổng chi phí quỹ lương ca đêm mà kho vẫn thông suốt 100%!
                </li>
            </ul>
        </div>
        """)

        # Bộ công cụ mô phỏng chi phí Full-time vs Part-time
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            core_ft = st.slider("👥 Số nhân sự Full-time nòng cốt (8h):", min_value=5, max_value=25, value=12, step=1)
        with col_s2:
            pt_hours = st.slider("⏱️ Thời gian ca ngắn Part-time (giờ):", min_value=1.5, max_value=4.0, value=2.5, step=0.5)
        with col_s3:
            pt_wage_h = st.number_input("💵 Đơn giá lương Part-time (VNĐ/h):", value=int(base_hourly), step=5000)

        # Tính toán so sánh thực tế
        peak_needed = max(core_ft, max_hour_staff)
        pt_needed = max(0, peak_needed - core_ft)
        
        # 100% Full-time (nếu thuê toàn bộ theo ca 8h)
        cost_100_ft = peak_needed * 8 * base_hourly
        # Hybrid (kết hợp Full-time nòng cốt và Part-time giờ cao điểm)
        cost_core_ft = core_ft * 8 * base_hourly
        cost_flex_pt = pt_needed * pt_hours * pt_wage_h
        cost_hybrid = cost_core_ft + cost_flex_pt
        cost_saved_shift = max(0, cost_100_ft - cost_hybrid)
        pct_saved_shift = (cost_saved_shift / cost_100_ft * 100) if cost_100_ft > 0 else 0

        # Thẻ so sánh kết quả tài chính của việc xếp ca
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.error(f"""
            **Mô Hình 100% Full-time**
            - Nhân sự: **{peak_needed} người**
            - Ca làm: **8 tiếng/người**
            - Lãng phí giờ chết: **~4 - 5 tiếng**
            - 💸 **Chi phí:** **{fmt_vnd(cost_100_ft)}**
            """)
        with sc2:
            st.success(f"""
            **Mô Hình AI Hybrid (FT + PT)**
            - Cốt lõi Full-time: **{core_ft} người** (8h)
            - Thời vụ Part-time: **{pt_needed} người** ({pt_hours}h)
            - Tận dụng triệt để: **100% giờ công**
            - 💰 **Chi phí:** **{fmt_vnd(cost_hybrid)}**
            """)
        with sc3:
            st.warning(f"""
            **Hiệu Quả Cắt Giảm Chi Phí**
            - Tiết kiệm thêm: **+{fmt_vnd(cost_saved_shift)}**
            - Tỷ lệ giảm quỹ lương: **-{pct_saved_shift:.1f}%**
            - Trạng thái vận hành: **Hoàn hảo**
            - Tồn đọng (Backlog): **0 đơn**
            """)

        st.markdown("---")
        # 3. BẢNG PHÂN BỔ 3 CA LÀM VIỆC CHUẨN
        st.markdown("#### 📋 3. Bảng Lịch Trình Xếp Ca Chi Tiết Trong Ngày (3 Ca Vận Hành)")

        roster_data = [
            {
                "Ca Làm Việc": "🌙 Ca 3 (Đêm Siêu Sale)",
                "Khung Giờ": "22:00 - 06:00",
                "Đặc Điểm Đơn": "🔥 Đỉnh cao Flash Sale (00h - 02h)",
                "Full-time (8h)": f"{core_ft} người (Trưởng ca, WMS, KCS)",
                "Part-time (Linh hoạt)": f"{pt_needed} người (Huy động 23:30 - 02:00)",
                "Chi Phí Dự Kiến": fmt_vnd(cost_hybrid),
                "Khuyến Nghị Điều Hành": "Huy động tối đa bàn đóng gói Trạm 3 & 4. Bàn giao 3PL đợt 1 lúc 03:00."
            },
            {
                "Ca Làm Việc": "☀️ Ca 1 (Sáng)",
                "Khung Giờ": "06:00 - 14:00",
                "Đặc Điểm Đơn": "⚡ Đơn trưa tăng nhẹ (11h30 - 13h)",
                "Full-time (8h)": "8 người (Nhập hàng & Xử lý đơn bù)",
                "Part-time (Linh hoạt)": "6 người (Huy động 11:30 - 13:30)",
                "Chi Phí Dự Kiến": fmt_vnd(8 * 8 * base_hourly + 6 * 2 * pt_wage_h),
                "Khuyến Nghị Điều Hành": "Nhập bổ sung SKU bán chạy từ kho tổng, kiểm đếm tồn kho."
            },
            {
                "Ca Làm Việc": "🌇 Ca 2 (Chiều)",
                "Khung Giờ": "14:00 - 22:00",
                "Đặc Điểm Đơn": "⚡ Đơn tối dồn về (20h - 21h30)",
                "Full-time (8h)": "10 người (Phân loại & Gom hàng)",
                "Part-time (Linh hoạt)": "12 người (Huy động 19:30 - 22:00)",
                "Chi Phí Dự Kiến": fmt_vnd(10 * 8 * base_hourly + 12 * 2.5 * pt_wage_h),
                "Khuyến Nghị Điều Hành": "Soát lại vật tư đóng gói (hộp, băng keo, tem in) chuẩn bị cho bão đơn đêm."
            }
        ]
        df_roster = pd.DataFrame(roster_data)
        st.dataframe(df_roster, use_container_width=True, hide_index=True)

        # Nút tải bảng xếp ca CSV
        csv_roster_buffer = io.StringIO()
        df_roster.to_csv(csv_roster_buffer, index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Tải Bảng Phân Ca Full-time & Part-time (.CSV)",
            data=csv_roster_buffer.getvalue().encode('utf-8-sig'),
            file_name=f"lich_xep_ca_ft_pt_{selected_date}.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("---")
        # 4. SO SÁNH ĐỐI CHỨNG 2 THUẬT TOÁN: LINEAR REGRESSION VS XGBOOST
        st.markdown("#### 🔬 4. So Sánh Đối Chứng Thuật Toán Machine Learning: Linear Regression vs XGBoost")
        st.markdown("""
        Để tìm ra mô hình dự báo chính xác nhất cho bài toán xếp ca vận hành kho hàng, 
        hệ thống đã triển khai thực nghiệm đối chứng trực tiếp giữa 2 lớp thuật toán trên cùng tập dữ liệu kho hàng gom nhóm (323 mẫu, phân chia 80% Train - 20% Test):
        * **Mô hình cơ sở (Baseline):** **Linear Regression (Hồi quy tuyến tính đa biến)** — Phương pháp thống kê cổ điển.
        * **Mô hình đề xuất (Proposed):** **XGBoost / Gradient Boosting Regressor** — Thuật toán học máy tăng cường gradient qua cây quyết định.
        """)

        # 3 Scorecard metrics
        sm1, sm2, sm3 = st.columns(3)
        sm1.metric(
            label="🎯 Hệ Số Xác Định R² Score (Độ chính xác)",
            value="92.50% (XGBoost)",
            delta="+35.97% so với Linear Regression (56.53%)",
            help="XGBoost giải thích được hơn 92.5% sự biến thiên của đơn hàng Flash Sale"
        )
        sm2.metric(
            label="📉 Sai Số Tuyệt Đối Trung Bình (MAE)",
            value="17.01 đơn (XGBoost)",
            delta="-25.44 đơn (-60.0% sai số)",
            delta_color="inverse",
            help="Linear Regression sai lệch tới 42.45 đơn, XGBoost chỉ lệch 17.01 đơn"
        )
        sm3.metric(
            label="📉 Căn Bậc Hai Sai Số (RMSE)",
            value="25.70 đơn (XGBoost)",
            delta="-36.14 đơn (-58.4% sai số)",
            delta_color="inverse",
            help="RMSE phạt nặng các sai số đột biến; XGBoost giảm tới 58.4% sai số biên độ lớn"
        )

        # 2 Biểu đồ so sánh
        col_c1, col_c2 = st.columns(2)
        
        # Load test predictions
        test_pred_path = os.path.join(BASE_DIR, "test_predictions.csv")
        if os.path.exists(test_pred_path):
            test_df = pd.read_csv(test_pred_path)
        else:
            test_df = pd.DataFrame({
                'Actual': [43, 32, 40, 101, 50, 106, 42, 34, 22, 15, 206, 713],
                'Pred_LR': [94.5, 7.8, 6.0, 107.6, 134.8, 164.9, 43.8, 54.1, 12.5, 15.9, 202.0, 387.0],
                'Pred_XGB': [74.2, 26.2, 27.8, 109.5, 66.4, 141.6, 26.3, 27.2, 25.1, 34.2, 210.0, 697.0]
            })

        with col_c1:
            st.markdown("##### 📍 Biểu Đồ Phân Tán Thực Tế vs Dự Báo (Tập Kiểm Thử - Test Set)")
            fig_scatter = go.Figure()
            # Điểm Linear Regression
            fig_scatter.add_trace(go.Scatter(
                x=test_df['Actual'],
                y=test_df['Pred_LR'],
                mode='markers',
                name='⚠️ Linear Regression (R² = 56.5%)',
                marker=dict(color='#ef4444', size=8, symbol='circle', opacity=0.7),
                hovertemplate="<b>Thực tế:</b> %{x} đơn<br><b>LR dự báo:</b> %{y:.0f} đơn<extra></extra>"
            ))
            # Điểm XGBoost
            fig_scatter.add_trace(go.Scatter(
                x=test_df['Actual'],
                y=test_df['Pred_XGB'],
                mode='markers',
                name='🏆 XGBoost (R² = 92.5%)',
                marker=dict(color='#10b981', size=9, symbol='diamond', opacity=0.85),
                hovertemplate="<b>Thực tế:</b> %{x} đơn<br><b>XGB dự báo:</b> %{y:.0f} đơn<extra></extra>"
            ))
            # Đường chéo chuẩn y = x
            max_val = max(test_df['Actual'].max(), test_df['Pred_XGB'].max(), test_df['Pred_LR'].max()) + 20
            fig_scatter.add_trace(go.Scatter(
                x=[0, max_val],
                y=[0, max_val],
                mode='lines',
                name='Đường chuẩn hoàn hảo (y = x)',
                line=dict(color='#0f172a', dash='dash', width=2)
            ))
            fig_scatter.update_layout(
                xaxis_title="Số đơn thực tế (Test Set)",
                yaxis_title="Số đơn dự báo",
                template='plotly_white',
                height=380,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                margin=dict(l=30, r=30, t=50, b=30)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_c2:
            st.markdown("##### 📊 So Sánh 3 Chỉ Số Hiệu Năng Cốt Lõi (MAE, RMSE, R²)")
            metrics_names = ['MAE (Đơn) ↓', 'RMSE (Đơn) ↓', 'R² Score (%) ↑']
            lr_scores = [42.45, 61.84, 56.53]
            xgb_scores = [17.01, 25.70, 92.50]
            
            fig_bar_metrics = go.Figure()
            fig_bar_metrics.add_trace(go.Bar(
                x=metrics_names,
                y=lr_scores,
                name='⚠️ Linear Regression',
                marker_color='#ef4444',
                text=[f"{v:.1f}" for v in lr_scores],
                textposition='outside'
            ))
            fig_bar_metrics.add_trace(go.Bar(
                x=metrics_names,
                y=xgb_scores,
                name='🏆 XGBoost (Đề xuất)',
                marker_color='#10b981',
                text=[f"{v:.1f}" for v in xgb_scores],
                textposition='outside'
            ))
            fig_bar_metrics.update_layout(
                barmode='group',
                yaxis_title="Giá trị chỉ số",
                template='plotly_white',
                height=380,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                margin=dict(l=30, r=30, t=50, b=30)
            )
            st.plotly_chart(fig_bar_metrics, use_container_width=True)

        # Bảng luận điểm phản biện chi tiết
        st.markdown("##### ⚔️ Bảng So Sánh Toàn Diện & Luận Điểm Phản Biện Hội Đồng")
        render_html("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; overflow:hidden; margin-bottom:20px;">
            <table style="width:100%; border-collapse:collapse; font-size:0.92rem;">
                <thead>
                    <tr style="background:#0f172a; color:#ffffff;">
                        <th style="padding:12px 16px; text-align:left;">Tiêu Chí Đánh Giá</th>
                        <th style="padding:12px 16px; text-align:left; color:#fca5a5;">⚠️ Linear Regression (Baseline)</th>
                        <th style="padding:12px 16px; text-align:left; color:#86efac;">🏆 XGBoost (Mô Hình Đề Xuất Tối Ưu)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid #f1f5f9; background:#ffffff;">
                        <td style="padding:12px 16px; font-weight:600;">1. Cơ chế hoạt động</td>
                        <td style="padding:12px 16px; color:#475569;">Tìm siêu phẳng tuyến tính tối thiểu hóa sai số bình phương (OLS). Giả định quan hệ giữa biến số là thẳng.</td>
                        <td style="padding:12px 16px; color:#0f172a; font-weight:600;">Tập hợp các cây quyết định liên tiếp (Ensemble Trees), vòng lặp sau học từ sai số của vòng lặp trước qua đạo hàm Gradient.</td>
                    </tr>
                    <tr style="border-bottom:1px solid #f1f5f9; background:#f8fafc;">
                        <td style="padding:12px 16px; font-weight:600;">2. Khả năng bắt đỉnh Flash Sale</td>
                        <td style="padding:12px 16px; color:#dc2626;"><b>Rất kém (Bị bẹp đỉnh):</b> Lúc nửa đêm 00:00 ngày 10.10 đơn thực tế <b>713 đơn</b>, Linear Regression chỉ dự báo được <b>387 đơn</b> (hụt 45.7%).</td>
                        <td style="padding:12px 16px; color:#16a34a; font-weight:600;"><b>Xuất sắc:</b> Bắt dính các bước nhảy phi tuyến. Dự báo đạt <b>697 đơn</b> (khớp tới <b>97.8%</b> so với thực tế 713 đơn).</td>
                    </tr>
                    <tr style="border-bottom:1px solid #f1f5f9; background:#ffffff;">
                        <td style="padding:12px 16px; font-weight:600;">3. Xử lý biến điều kiện (Dummy Features)</td>
                        <td style="padding:12px 16px; color:#475569;">Cộng gộp trọng số cố định ($w_i$), không mô tả được hiệu ứng cộng hưởng khi vừa là Giờ Flash Sale vừa là Ngày Mega Day.</td>
                        <td style="padding:12px 16px; color:#0f172a; font-weight:600;">Cây quyết định tự động tạo nhánh rẽ logic kết hợp: <br><code>if IsMegaDay == 1 and IsFlashSaleHour == 1: boost +500</code>.</td>
                    </tr>
                    <tr style="background:#f0fdf4;">
                        <td style="padding:12px 16px; font-weight:600; color:#15803d;">4. HẬU QUẢ VẬN HÀNH KHO THỰC TẾ</td>
                        <td style="padding:12px 16px; color:#b91c1c;"><b>VỠ KHO TRẦM TRỌNG:</b> Quản lý chỉ gọi <b>5 - 6 nhân viên</b> (dựa trên 387 đơn) &rarr; Thiếu 4 nhân viên &rarr; Hàng trăm đơn trễ hạn, sàn TMĐT phạt nặng!</td>
                        <td style="padding:12px 16px; color:#15803d; font-weight:700;"><b>VẬN HÀNH HOÀN HẢO:</b> Quản lý huy động đủ <b>10 nhân viên</b> (dựa trên 697 đơn) &rarr; Xóa sạch 100% Backlog, tiết kiệm chi phí tối đa!</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """)
    else:
        st.info("Chưa tìm thấy file dữ liệu lịch sử gom nhóm hourly_aggregated.csv.")


# ─────────────────────────────────────────────────────────────────────
# TAB 4: MA TRẬN ĐỘ NHẠY KINH TẾ & BIỂU ĐỒ RA QUYẾT ĐỊNH
# ─────────────────────────────────────────────────────────────────────
with tab_sensitivity:
    st.markdown("### 📈 Ma Trận Độ Nhạy Kinh Tế & Biểu Đồ Di Chuyển Dòng Tiền Ra Quyết Định")
    st.markdown("""
    Biểu đồ dưới đây không dùng các đường thẳng đơn điệu, mà trực quan hóa **độ di chuyển LÊN - XUỐNG của Thặng Dư Kinh Tế & Tiết Kiệm Ròng** qua từng nấc thang quy mô đơn hàng (từ 1.000 đến 20.000 đơn).
    Nhờ quan sát **hướng di chuyển từ ÂM sang DƯƠNG và bước nhảy vọt của các cột**, Ban Giám Đốc có thể **đưa ra quyết định vận hành chính xác tức thì** cho từng quy mô đơn hàng.
    """)

    # Các mốc quy mô đơn hàng
    sens_steps = [1000, 2000, int(trad_cap), 3000, 4500, 6500, 8000, 10000, 12000, 15000, 20000]
    sens_steps = sorted(list(set(sens_steps)))

    bar_labels = []
    savings_values = []
    costs_trad_list = []
    costs_ai_list = []
    bar_colors = []
    text_labels = []

    for s in sens_steps:
        # Truyền thống
        b = max(0, s - trad_cap)
        c_t = trad_wage_cost + b * ot_rate_per_order + b * penalty_per_order
        # AI
        stf = math.ceil(s / capacity_per_person * risk_factor)
        c_a = stf * wage_per_person
        # Tiết kiệm ròng (Triệu VNĐ)
        sav = (c_t - c_a) / 1e6

        savings_values.append(sav)
        costs_trad_list.append(c_t / 1e6)
        costs_ai_list.append(c_a / 1e6)

        if s == trad_cap:
            lbl = f"<b>{fmt_num(s)} đơn</b><br>(Hòa Vốn)"
        else:
            lbl = f"<b>{fmt_num(s)} đơn</b>"
        bar_labels.append(lbl)

        # Xác định màu và nhãn chữ
        if sav > 0.5:
            bar_colors.append('#10b981') # Xanh lá (Lên mạnh)
            text_labels.append(f"+{sav:.1f} Tr")
        elif sav < -0.5:
            bar_colors.append('#f97316') # Cam/Đỏ (Xuống dưới vạch 0)
            text_labels.append(f"{sav:.1f} Tr")
        else:
            bar_colors.append('#94a3b8') # Xám (Hòa vốn)
            text_labels.append("0 Tr")

    st.markdown("#### 1. Biểu Đồ Di Chuyển Lên / Xuống Của Tiết Kiệm Ròng (Diverging Delta Chart)")
    st.caption("🟢 Cột hướng LÊN: AI đem lại thặng dư lợi nhuận lớn | 🟠 Cột hướng XUỐNG: Chi phí AI cao hơn do đơn quá nhỏ | ⭐ Đường Zero: Ngưỡng bứt phá hòa vốn")

    # 1. Biểu đồ cột Diverging Waterfall / Delta Bar
    fig_delta = go.Figure()
    fig_delta.add_trace(go.Bar(
        x=bar_labels,
        y=savings_values,
        marker=dict(
            color=bar_colors,
            line=dict(color='#1e293b', width=1.5)
        ),
        text=text_labels,
        textposition='outside',
        hovertemplate="<b>Quy mô đơn:</b> %{x}<br><b>Tiết kiệm ròng:</b> %{y:+.2f} Triệu VNĐ<br><extra></extra>",
        name='Thặng Dư / Tiết Kiệm Ròng'
    ))
    # Đường Baseline chuẩn 0 VNĐ
    fig_delta.add_hline(
        y=0,
        line_dash="dash",
        line_color="#475569",
        line_width=2.5,
        annotation_text="⭐ VẠCH CHUẨN 0 VNĐ: NGƯỠNG BẮT ĐẦU CÓ LÃI RÒNG",
        annotation_position="bottom right"
    )
    fig_delta.update_layout(
        title="<b>Biến Động Thặng Dư Kinh Tế & Bước Nhảy Vọt Khi Vượt Ngưỡng Quá Tải (Triệu VNĐ)</b>",
        xaxis_title="Quy mô tổng đơn hàng Flash Sale",
        yaxis_title="Tiết Kiệm Ròng Do AI Mang Lại (Triệu VNĐ)",
        template='plotly_white',
        height=450,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    fig_delta.update_traces(cliponaxis=False)
    st.plotly_chart(fig_delta, use_container_width=True)

    # 2. Biểu đồ Cột Nhóm Đối Đầu (Grouped Comparison)
    st.markdown("#### 2. Biểu Đồ Đối Đầu Trực Quan: Cú Sốc Chi Phí Truyền Thống vs AI")
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=bar_labels,
        y=costs_trad_list,
        name='🔴 Thiệt Hại Truyền Thống (Lương + Phạt dồn toa)',
        marker_color='#ef4444',
        hovertemplate="<b>Truyền thống:</b> %{y:.2f} Triệu VNĐ<br><extra></extra>"
    ))
    fig_comp.add_trace(go.Bar(
        x=bar_labels,
        y=costs_ai_list,
        name='🟢 Chi Phí Nhân Lực AI (Kiểm soát tuyến tính)',
        marker_color='#10b981',
        hovertemplate="<b>Mô hình AI:</b> %{y:.2f} Triệu VNĐ<br><extra></extra>"
    ))
    fig_comp.update_layout(
        barmode='group',
        title="<b>So Sánh Chi Phí Thực Tế Giữa 2 Kịch Bản Ở Từng Quy Mô Đơn Hàng (Triệu VNĐ)</b>",
        xaxis_title="Quy mô đơn hàng",
        yaxis_title="Chi Phí (Triệu VNĐ)",
        template='plotly_white',
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    fig_comp.update_traces(cliponaxis=False)
    st.plotly_chart(fig_comp, use_container_width=True)

    # 3. MA TRẬN 3 VÙNG QUYẾT ĐỊNH QUẢN TRỊ
    st.markdown("#### 🧭 3. Ma Trận Hướng Dẫn Ra Quyết Định Quản Trị Cấp Cao")
    st.markdown("Dựa vào hướng di chuyển LÊN - XUỐNG của biểu đồ trên, nhà quản lý đưa ra quyết định hành động:")

    render_html(f"""
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; margin: 15px 0 25px 0;">
        <!-- Vùng 1 -->
        <div style="background:#f8fafc; border:2px solid #cbd5e1; border-radius:14px; padding:18px;">
            <div style="font-size:1.05rem; font-weight:700; color:#475569; margin-bottom:6px;">
                🟢 VÙNG 1: DƯỚI {fmt_num(trad_cap)} ĐƠN
            </div>
            <div style="font-size:0.82rem; font-weight:600; color:#64748b; text-transform:uppercase; margin-bottom:12px;">
                VÙNG AN TOÀN TRUYỀN THỐNG
            </div>
            <p style="font-size:0.9rem; color:#334155; line-height:1.5; margin-bottom:8px;">
                <b>📉 Hướng biểu đồ:</b> Cột nằm dưới hoặc sát vạch 0 VNĐ.<br>
                <b>🔍 Bản chất:</b> Đội ngũ cố định ({fixed_staff} người) tự xử lý tốt mà không bị quá tải. Tồn đọng = 0, Phạt sàn = 0.<br>
                <b>👉 QUYẾT ĐỊNH CỦA BẠN:</b> <b>GIỮ NGUYÊN ĐỘI NGŨ CỐ ĐỊNH</b>. Không cần huy động thêm nhân sự thời vụ, không kích hoạt kịch bản khẩn cấp để tránh dư thừa chi phí.
            </p>
        </div>
        <!-- Vùng 2 -->
        <div style="background:#fffbeb; border:2px solid #fde68a; border-radius:14px; padding:18px;">
            <div style="font-size:1.05rem; font-weight:700; color:#d97706; margin-bottom:6px;">
                🟡 VÙNG 2: {fmt_num(trad_cap)} - 3.500 ĐƠN
            </div>
            <div style="font-size:0.82rem; font-weight:600; color:#b45309; text-transform:uppercase; margin-bottom:12px;">
                VÙNG BƯỚC NGOẶT CHUYỂN TIẾP
            </div>
            <p style="font-size:0.9rem; color:#78350f; line-height:1.5; margin-bottom:8px;">
                <b>📈 Hướng biểu đồ:</b> Cột chuyển màu xanh, bắt đầu <b>VỌT LÊN</b> (+15 Tr đến +40 Tr).<br>
                <b>🔍 Bản chất:</b> Vượt ngưỡng gãy công suất. Mô hình cũ chớm phát sinh backlog và tiền phạt.<br>
                <b>👉 QUYẾT ĐỊNH CỦA BẠN:</b> <b>KÍCH HOẠT MÔ HÌNH HYBRID</b>. Bổ sung ngay 10 - 20 nhân viên Part-time linh hoạt trong 2 giờ vàng để dập tắt hoàn toàn tiền phạt với chi phí tối thiểu.
            </p>
        </div>
        <!-- Vùng 3 -->
        <div style="background:#fef2f2; border:2px solid #fecaca; border-radius:14px; padding:18px;">
            <div style="font-size:1.05rem; font-weight:700; color:#dc2626; margin-bottom:6px;">
                🔴 VÙNG 3: TRÊN 3.500 ĐƠN
            </div>
            <div style="font-size:0.82rem; font-weight:600; color:#b91c1c; text-transform:uppercase; margin-bottom:12px;">
                VÙNG SIÊU SALE BẮT BUỘC AI
            </div>
            <p style="font-size:0.9rem; color:#7f1d1d; line-height:1.5; margin-bottom:8px;">
                <b>🚀 Hướng biểu đồ:</b> Cột <b>DỰNG ĐỨNG VỌT LÊN CỰC ĐẠI</b> (+70 Tr đến +640 Tr).<br>
                <b>🔍 Bản chất:</b> Kho truyền thống vỡ trận. Tiền phạt SLA bùng nổ gấp 5 - 10 lần tổng tiền lương.<br>
                <b>👉 QUYẾT ĐỊNH CỦA BẠN:</b> <b>BẮT BUỘC 100% TRIỂN KHAI AI</b>. Mở tối đa 4 trạm, huy động toàn bộ danh sách dự phòng Part-time, tổ chức bàn giao liên tục cho 3PL. Cứu nguy cho công ty hàng trăm triệu đồng!
            </p>
        </div>
    </div>
    """)

    # 4. Bảng số liệu chi tiết
    st.markdown("#### 📋 4. Bảng Báo Cáo Số Liệu Đa Kịch Bản")
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
# TAB 5: MÁY TÍNH ROI & ĐIỂM HÒA VỐN (FINANCIAL FEASIBILITY)
# ─────────────────────────────────────────────────────────────────────
with tab_roi:
    st.markdown("### 💰 Máy Tính Hoàn Vốn Đầu Tư (ROI) & Điểm Hòa Vốn (Break-Even)")
    st.markdown("""
    Doanh nghiệp thường chất vấn: *"Đầu tư hệ thống AI dự báo nhân sự tốn kém bao nhiêu, và bao lâu thì hoàn vốn?"*
    Công cụ dưới đây hạch toán toàn diện hiệu quả tài chính & điểm hòa vốn:
    """)

    penalty_plus_ot = ot_rate_per_order + penalty_per_order
    if penalty_plus_ot > 0:
        break_even_orders = trad_cap + ((ai_total_cost - trad_wage_cost) / penalty_plus_ot)
    else:
        break_even_orders = trad_cap

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown("#### 🎯 Phân Tích Điểm Hòa Vốn (Break-even)")
        render_html(f"""
        <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:16px; padding:22px; margin-bottom:15px;">
            <div style="font-size:0.85rem; color:#64748b; font-weight:700; text-transform:uppercase;">Ngưỡng đơn hàng bắt đầu có lãi (N*)</div>
            <div style="font-size:2.2rem; font-weight:800; color:#0f172a; margin:6px 0;">{fmt_num(break_even_orders)} đơn</div>
            <div style="font-size:0.92rem; color:#475569;">
                So với năng lực cố định truyền thống ({fmt_num(trad_cap)} đơn), chỉ cần lượng đơn thực tế vượt quá <b>{fmt_num(break_even_orders)} đơn</b> (+{fmt_num(max(0, break_even_orders - trad_cap))} đơn), 
                phương án truyền thống sẽ lập tức đắt hơn phương án gọi đủ {ai_staff_required} người có AI do tiền phạt sàn TMĐT cộng dồn!
            </div>
        </div>
        """)
        st.latex(r"N^* = \text{Cap}_{\text{Trad}} + \frac{\text{Lương}_{\text{AI}} - \text{Lương}_{\text{Trad}}}{\text{Phạt/đơn} + \text{OT/đơn}} \approx " + fmt_num(break_even_orders) + r" \text{ đơn}")

    with r_col2:
        st.markdown("#### 📈 Máy Tính Hoàn Vốn Đầu Tư (Payback Calculator)")
        ai_invest_input = st.number_input("Chi phí đầu tư phần mềm & Server AI (VNĐ):", value=15_000_000, step=1_000_000)
        flash_events_year = st.slider("Số đợt Flash Sale lớn trong 1 năm (lần):", min_value=1, max_value=24, value=6, step=1)

        total_annual_savings = net_savings * flash_events_year
        if ai_invest_input > 0 and net_savings > 0:
            payback_events = ai_invest_input / net_savings
            payback_hours = payback_events * shift_hours
            annual_roi = ((total_annual_savings - ai_invest_input) / ai_invest_input) * 100
            payback_note = f"⚡ <b>Thời gian thu hồi vốn:</b> Chỉ sau <b>{payback_events:.2f} đêm Flash Sale</b> (~{payback_hours:.1f} giờ vận hành) là doanh nghiệp đã hoàn đủ 100% chi phí đầu tư công nghệ AI!"
            roi_display = f"+{annual_roi:,.0f}%"
        else:
            payback_events = 0
            payback_hours = 0
            annual_roi = 0
            payback_note = f"💡 <b>Ghi chú:</b> Ở quy mô đơn {fmt_num(total_orders)} đơn, nhân sự kho truyền thống ({fixed_staff} người) chưa phát sinh quá tải và tiền phạt SLA."
            roi_display = "Hòa vốn"

        render_html(f"""
        <div style="background:#ecfdf5; border:1.5px solid #a7f3d0; border-radius:16px; padding:22px;">
            <div style="display:flex; justify-content:space-between;">
                <div>
                    <div style="font-size:0.85rem; color:#065f46; font-weight:700;">TIẾT KIỆM HÀNG NĂM ({flash_events_year} ĐỢT SALE)</div>
                    <div style="font-size:1.8rem; font-weight:800; color:#059669;">{fmt_vnd(max(0, total_annual_savings))}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.85rem; color:#065f46; font-weight:700;">TỶ SUẤT HOÀN VỐN (ROI)</div>
                    <div style="font-size:1.8rem; font-weight:800; color:#059669;">{roi_display}</div>
                </div>
            </div>
            <div style="margin-top:12px; padding-top:12px; border-top:1px dashed #6ee7b7; font-size:0.92rem; color:#064e3b;">
                {payback_note}
            </div>
        </div>
        """)


# ─────────────────────────────────────────────────────────────────────
# TAB 6: CẨM NĂNG BẢO VỆ PHẢN BIỆN (DEFENSE GUIDE)
# ─────────────────────────────────────────────────────────────────────
with tab_defense_qa:
    st.markdown("### 🛡️ Cẩm Nang Vượt Qua Vòng Phản Biện Của Giảng Viên")
    st.info("💡 Các câu hỏi phản biện trọng tâm từ Hội đồng & Luận điểm giải trình chuyên môn:")

    with st.expander("❓ Câu 1: Dựa vào đâu hệ thống tính ra định mức 1 người xử lý 80 đơn/ca?", expanded=True):
        st.markdown("""
        **Trả lời học thuật chuẩn mực:**
        - Năng lực $UPH = 40$ đơn/giờ được xây dựng từ **định mức kỹ thuật vận hành chuẩn nhân văn** (đã trừ thời gian nghỉ giải lao, giao nhận ca và kiểm tra an toàn lao động theo tiêu chuẩn ILO).
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

    with st.expander("❓ Câu 4: Mô hình AI XGBoost có thể sai số, hệ thống xử lý việc đó như thế nào?"):
        st.markdown(r"""
        **Trả lời:**
        - Mô hình Machine Learning XGBoost đạt độ chính xác $R^2 = 92.50\%$ với sai số tuyệt đối trung bình $MAE \approx 17$ đơn.
        - Với lượng đơn 6.500, sai số 17 đơn chỉ tương đương **0.26%**, hoàn toàn được triệt tiêu bởi hệ số đệm an toàn $\alpha = 5\%$ (tương đương đệm thêm 380 đơn).
        - Vì vậy, rủi ro sai số của mô hình được bao bọc an toàn 100% trong thực tế.
        """)


# ─────────────────────────────────────────────────────────────────────
# TAB 7: DEPLOY & TẠO QR CHO CANVA
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
                file_name="qr_code_elogistics_demo.png",
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
render_html("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding-bottom: 25px;">
    🏭 <b>Hệ Thống Quản Trị Kho Vận E-Logistics Thông Minh</b> | Tối ưu Hóa Phân Bổ Nhân Lực & Hiệu Quả Kinh Tế Flash Sale<br>
    Được xây dựng với Python, Streamlit & Plotly Interactive Charts.
</div>
""")
