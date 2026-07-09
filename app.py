import streamlit as st
import pandas as pd
from datetime import datetime


# ================= CẤU HÌNH =================

st.set_page_config(
    page_title="Quản lý nhà trọ thông minh",
    page_icon="🏠",
    layout="wide"
)


st.title("🏠 HỆ THỐNG QUẢN LÝ NHÀ TRỌ THÔNG MINH")

st.write(
    "Tính tiền - Theo dõi doanh thu - Quản lý 10 phòng"
)

st.divider()


# ================= CẤU HÌNH GIÁ =================

st.sidebar.header("⚙️ CẤU HÌNH GIÁ")


gia_phong = st.sidebar.number_input(
    "Tiền phòng (VNĐ)",
    value=2500000
)

gia_dien = st.sidebar.number_input(
    "Giá điện/kWh",
    value=3500
)

gia_nuoc = st.sidebar.number_input(
    "Giá nước/m3",
    value=15000
)

gia_wifi = st.sidebar.number_input(
    "Wifi",
    value=100000
)

gia_rac = st.sidebar.number_input(
    "Rác + dịch vụ",
    value=50000
)



# ================= NHẬP 10 PHÒNG =================

st.header("📝 Dữ liệu 10 phòng")


ds_phong = []


trang_thai = [
    "🟢 Đã thanh toán",
    "🔴 Chưa thanh toán",
    "🟡 Đang sửa chữa",
    "⚪ Phòng trống"
]


for i in range(1,11):

    with st.expander(f"🏠 Phòng {i}"):

        c1,c2,c3,c4 = st.columns(4)


        with c1:

            dien_cu = st.number_input(
                "Điện cũ",
                min_value=0,
                key=f"diencu{i}"
            )

            dien_moi = st.number_input(
                "Điện mới",
                min_value=0,
                key=f"dienmoi{i}"
            )


        with c2:

            nuoc_cu = st.number_input(
                "Nước cũ",
                min_value=0,
                key=f"nuoccu{i}"
            )

            nuoc_moi = st.number_input(
                "Nước mới",
                min_value=0,
                key=f"nuocmoi{i}"
            )


        with c3:

            nguoi = st.number_input(
                "Số người",
                1,
                10,
                1,
                key=f"nguoi{i}"
            )


        with c4:

            tt = st.selectbox(
                "Trạng thái",
                trang_thai,
                key=f"tt{i}"
            )


        ds_phong.append(
            {
                "Phòng":f"Phòng {i}",
                "Điện cũ":dien_cu,
                "Điện mới":dien_moi,
                "Nước cũ":nuoc_cu,
                "Nước mới":nuoc_moi,
                "Người":nguoi,
                "Trạng thái":tt
            }
        )



# ================= TÍNH TOÁN =================

if st.button("🧮 TÍNH TOÀN BỘ 10 PHÒNG"):


    ketqua=[]

    tong_doanhthu=0
    tong_dien=0
    tong_nuoc=0

    tong_dien_cu=0
    tong_dien_moi=0

    tong_nuoc_cu=0
    tong_nuoc_moi=0



    for p in ds_phong:


        dien = p["Điện mới"] - p["Điện cũ"]

        nuoc = p["Nước mới"] - p["Nước cũ"]


        if dien < 0 or nuoc < 0:

            st.error(
                f"{p['Phòng']} sai chỉ số"
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


        tong_doanhthu += tong
        tong_dien += dien
        tong_nuoc += nuoc

        tong_dien_cu += p["Điện cũ"]
        tong_dien_moi += p["Điện mới"]

        tong_nuoc_cu += p["Nước cũ"]
        tong_nuoc_moi += p["Nước mới"]


        ketqua.append(
            [
                p["Phòng"],
                dien,
                nuoc,
                tong,
                p["Trạng thái"]
            ]
        )
