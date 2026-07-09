import streamlit as st
import pandas as pd

# ================= CẤU HÌNH =================

st.set_page_config(
    page_title="Quản lý tiền phòng trọ",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 HỆ THỐNG TÍNH TIỀN PHÒNG TRỌ TỰ ĐỘNG")
st.write("Tính tiền cùng lúc cho 10 phòng trọ")

st.divider()


# ================= GIÁ DỊCH VỤ =================

st.sidebar.header("⚙️ Cấu hình bảng giá")

gia_phong = st.sidebar.number_input(
    "Tiền phòng (VNĐ)",
    value=2500000,
    step=100000
)

gia_dien = st.sidebar.number_input(
    "Giá điện/kWh",
    value=3500,
    step=100
)

gia_nuoc = st.sidebar.number_input(
    "Giá nước/khối",
    value=15000,
    step=500
)

gia_wifi = st.sidebar.number_input(
    "Wifi",
    value=100000,
    step=10000
)

gia_rac = st.sidebar.number_input(
    "Rác & dịch vụ",
    value=50000,
    step=5000
)


# ================= NHẬP 10 PHÒNG =================

st.header("📝 Nhập thông tin 10 phòng")


phong_data = []


for i in range(1,11):

    with st.expander(f"🏠 Phòng {i}"):

        col1,col2,col3 = st.columns(3)

        with col1:
            dien_cu = st.number_input(
                f"Điện cũ P{i}",
                min_value=0,
                key=f"diencu{i}"
            )

            dien_moi = st.number_input(
                f"Điện mới P{i}",
                min_value=0,
                key=f"dienmoi{i}"
            )


        with col2:

            nuoc_cu = st.number_input(
                f"Nước cũ P{i}",
                min_value=0,
                key=f"nuoccu{i}"
            )

            nuoc_moi = st.number_input(
                f"Nước mới P{i}",
                min_value=0,
                key=f"nuocmoi{i}"
            )


        with col3:

            so_nguoi = st.number_input(
                f"Số người P{i}",
                min_value=1,
                max_value=10,
                value=1,
                key=f"nguoi{i}"
            )


        phong_data.append(
            {
                "Phòng":f"Phòng {i}",
                "Điện cũ":dien_cu,
                "Điện mới":dien_moi,
                "Nước cũ":nuoc_cu,
                "Nước mới":nuoc_moi,
                "Số người":so_nguoi
            }
        )


# ================= TÍNH TOÁN =================


if st.button("🧮 TÍNH TIỀN 10 PHÒNG"):

    ket_qua=[]

    tong_doanh_thu=0


    for p in phong_data:

        dien = p["Điện mới"] - p["Điện cũ"]
        nuoc = p["Nước mới"] - p["Nước cũ"]


        if dien <0 or nuoc<0:

            st.error(
                f"{p['Phòng']} nhập sai chỉ số!"
            )

            continue


        tien_dien = dien * gia_dien

        tien_nuoc = nuoc * gia_nuoc


        tong = (
            gia_phong
            + tien_dien
            + tien_nuoc
            + gia_wifi
            + gia_rac
        )


        tong_doanh_thu += tong


        ket_qua.append(
            [
                p["Phòng"],
                dien,
                tien_dien,
                nuoc,
                tien_nuoc,
                tong
            ]
        )


    st.divider()

    st.header("📊 BẢNG TỔNG HỢP")


    df = pd.DataFrame(
        ket_qua,
        columns=[
            "Phòng",
            "Điện(kWh)",
            "Tiền điện",
            "Nước(m3)",
            "Tiền nước",
            "Tổng tiền"
        ]
    )


    st.dataframe(
        df,
        use_container_width=True
    )


    st.metric(
        "💰 TỔNG DOANH THU 10 PHÒNG",
        f"{tong_doanh_thu:,.0f} VNĐ"
    )


    st.subheader("🧾 Chi tiết hóa đơn")


    for row in ket_qua:

        st.write(
            f"""
            ### {row[0]}
            - Điện: {row[1]} kWh = {row[2]:,.0f} VNĐ
            - Nước: {row[3]} m3 = {row[4]:,.0f} VNĐ
            - Tiền phòng + dịch vụ
            - **Tổng: {row[5]:,.0f} VNĐ**
            """
        )
