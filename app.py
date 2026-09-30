# congcutinhlaitietkiem
import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 ỨNG DỤNG TÍNH LÃI TIẾT KIỆM")
st.write("Tính tiền lãi theo phương pháp **lãi đơn** hoặc **lãi kép**.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

st.subheader("📌 Thông tin gửi tiết kiệm")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=500_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn",
    min_value=1,
    value=12,
    step=1
)

don_vi_ky_han = st.selectbox(
    "Đơn vị kỳ hạn",
    ["Tháng", "Năm"]
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

phuong_phap = st.selectbox(
    "Phương pháp tính lãi",
    ["Lãi đơn", "Lãi kép"]
)

hinh_thuc_lanh = st.selectbox(
    "Hình thức lãnh lãi",
    ["Lãnh lãi theo tháng", "Lãnh lãi theo quý", "Lãnh lãi cuối kỳ"]
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if ky_han <= 0:
        st.error("Vui lòng nhập kỳ hạn lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # -------------------------
    # Đổi kỳ hạn về số tháng
    # -------------------------
    if don_vi_ky_han == "Năm":
        so_thang = ky_han * 12
    else:
        so_thang = ky_han

    # Số năm
    so_nam = so_thang / 12

    # Lãi suất dạng thập phân
    lai_suat_nam = lai_suat / 100

    # =========================
    # XÁC ĐỊNH SỐ KỲ LÃNH LÃI
    # =========================
    if hinh_thuc_lanh == "Lãnh lãi theo tháng":
        so_ky = so_thang
        so_thang_moi_ky = 1

    elif hinh_thuc_lanh == "Lãnh lãi theo quý":
        # Nếu kỳ hạn không đủ 3 tháng thì vẫn tính theo số tháng thực tế
        so_ky = so_thang // 3
        so_thang_moi_ky = 3

        if so_ky == 0:
            st.warning(
                "Kỳ hạn phải từ 3 tháng trở lên để lựa chọn lãnh lãi theo quý."
            )
            st.stop()

    else:
        # Cuối kỳ chỉ có 1 lần nhận lãi
        so_ky = 1
        so_thang_moi_ky = so_thang

    # =========================
    # LÃI ĐƠN
    # =========================
    if phuong_phap == "Lãi đơn":

        # Tổng lãi:
        # I = P * r * t
        tong_lai = so_tien * lai_suat_nam * so_nam

        # Tiền lãi mỗi kỳ
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            lai_dinh_ky = so_tien * lai_suat_nam / 12

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            lai_dinh_ky = so_tien * lai_suat_nam / 4

        else:
            lai_dinh_ky = tong_lai

        tong_tien = so_tien + tong_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:

        # Lãi suất theo từng kỳ
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            lai_suat_ky = lai_suat_nam / 12
            so_ky_kep = so_thang

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            lai_suat_ky = lai_suat_nam / 4
            so_ky_kep = so_thang // 3

        else:
            # Cuối kỳ: ghép lãi theo tháng
            # để phản ánh tăng trưởng theo kỳ hạn
            lai_suat_ky = lai_suat_nam / 12
            so_ky_kep = so_thang

        # Công thức lãi kép:
        # A = P(1+r)^n
        tong_tien = so_tien * (1 + lai_suat_ky) ** so_ky_kep

        tong_lai = tong_tien - so_tien

        # -------------------------
        # Lãi định kỳ
        # -------------------------
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            # Lãi của tháng đầu tiên
            lai_dinh_ky = so_tien * lai_suat_ky

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            # Lãi của quý đầu tiên
            lai_dinh_ky = so_tien * (
                (1 + lai_suat_ky) ** 3 - 1
            )

        else:
            lai_dinh_ky = tong_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.divider()

    st.subheader("📊 KẾT QUẢ")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            dinh_dang_tien(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            dinh_dang_tien(tong_lai)
        )

    st.metric(
        "💰 Tổng tiền gốc + lãi",
        dinh_dang_tien(tong_tien)
    )

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================

    st.divider()

    st.subheader("📋 Thông tin khoản gửi")

    st.write(f"**Số tiền gửi:** {dinh_dang_tien(so_tien)}")
    st.write(f"**Kỳ hạn:** {ky_han} {don_vi_ky_han.lower()}")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương pháp:** {phuong_phap}")
    st.write(f"**Hình thức lãnh:** {hinh_thuc_lanh}")

    # =========================
    # GIẢI THÍCH
    # =========================

    with st.expander("📖 Xem cách tính"):

        if phuong_phap == "Lãi đơn":
            st.write(
                "Lãi đơn được tính dựa trên số tiền gốc ban đầu "
                "và không cộng tiền lãi vào vốn để tính lãi tiếp."
            )

            st.latex(r"I = P \times r \times t")

            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất năm, "
                "t là thời gian gửi tính theo năm."
            )

        else:
            st.write(
                "Lãi kép là hình thức tiền lãi được cộng vào vốn, "
                "sau đó tiếp tục sinh lãi ở các kỳ tiếp theo."
            )

            st.latex(r"A = P(1+r)^n")

            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất mỗi kỳ, "
                "n là số kỳ ghép lãi."
            )
