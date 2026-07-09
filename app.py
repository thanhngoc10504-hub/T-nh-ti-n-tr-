import streamlit as st
import pandas as pd
from datetime import datetime
import os


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


# ================= SIDEBAR GIÁ =================

st.sidebar.header("⚙️ CẤU HÌNH GIÁ")


gia_phong = st.sidebar.number_input(
    "Tiền phòng",
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



# ================= NHẬP DỮ LIỆU =================

st.header("📝 Dữ liệu 10 phòng")


ds_phong=[]


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
                key=f"dc{i}"
            )


            dien_moi = st.number_input(
                "Điện mới",
                min_value=0,
                key=f"dm{i}"
            )


        with c2:

            nuoc_cu = st.number_input(
                "Nước cũ",
                min_value=0,
                key=f"nc{i}"
            )


            nuoc_moi = st.number_input(
                "Nước mới",
                min_value=0,
                key=f"nm{i}"
            )


        with c3:

            nguoi = st.number_input(
                "Số người",
                1,
                10,
                1,
                key=f"ng{i}"
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



    for p in ds_phong:


        dien = p["Điện mới"]-p["Điện cũ"]

        nuoc = p["Nước mới"]-p["Nước cũ"]



        if dien <0 or nuoc <0:

            st.error(
                f"{p['Phòng']} sai chỉ số"
            )

            continue



        tien_dien=dien*gia_dien

        tien_nuoc=nuoc*gia_nuoc



        tong=(
            gia_phong+
            tien_dien+
            tien_nuoc+
            gia_wifi+
            gia_rac
        )



        tong_doanhthu+=tong

        tong_dien+=dien

        tong_nuoc+=nuoc



        ketqua.append(
            [
                p["Phòng"],
                dien,
                nuoc,
                tong,
                p["Trạng thái"]
            ]
        )



    df=pd.DataFrame(
        ketqua,
        columns=[
            "Phòng",
            "Điện",
            "Nước",
            "Tổng tiền",
            "Trạng thái"
        ]
    )


    st.divider()

    st.header("📊 DASHBOARD")


    a,b,c=st.columns(3)


    a.metric(
        "💰 Doanh thu",
        f"{tong_doanhthu:,.0f} đ"
    )


    b.metric(
        "⚡ Tổng điện",
        f"{tong_dien} kWh"
    )


    c.metric(
        "💧 Tổng nước",
        f"{tong_nuoc} m3"
    )



    st.dataframe(
        df,
        use_container_width=True
    )



    st.subheader("📈 Biểu đồ doanh thu phòng")

    st.bar_chart(
        df.set_index("Phòng")["Tổng tiền"]
    )



    # ================= CẢNH BÁO =================


    st.subheader("⚠️ Cảnh báo")


    for row in ketqua:

        if row[1]>300:

            st.warning(
                f"{row[0]} sử dụng điện cao: {row[1]} kWh"
            )



    # ================= TIN NHẮN =================


    st.divider()

# ================= TIN NHẮN ZALO NHÓM =================

st.divider()

st.header("📱 Tin nhắn thống kê nhanh gửi nhóm Zalo")


ngay_thang = datetime.now().strftime("%d/%m/%Y")


tin_nhan_nhom = f"""
🏠 THÔNG BÁO TIỀN PHÒNG NHÀ TRỌ
📅 Ngày lập: {ngay_thang}

Kính gửi các phòng:

"""


for row in ketqua:

    phong = row[0]
    dien = row[1]
    nuoc = row[2]
    tien = row[3]
    trangthai = row[4]


    tin_nhan_nhom += f"""
━━━━━━━━━━━━━━
🏠 {phong}
⚡ Điện: {dien} kWh
💧 Nước: {nuoc} m³
💰 Tổng tiền: {tien:,.0f} VNĐ
📌 Trạng thái: {trangthai}

"""


tin_nhan_nhom += f"""
━━━━━━━━━━━━━━

📊 TỔNG KẾT NHÀ TRỌ

🏠 Số phòng: 10
💰 Tổng doanh thu: {tong_doanhthu:,.0f} VNĐ
⚡ Tổng điện: {tong_dien} kWh
💧 Tổng nước: {tong_nuoc} m³

Vui lòng kiểm tra và thanh toán đúng hạn.
Xin cảm ơn mọi người! ❤️
"""


st.text_area(
    "📋 Copy nội dung gửi nhóm Zalo",
    value=tin_nhan_nhom,
    height=450
)


    # ================= XUẤT EXCEL =================


    file="bao_cao_nha_tro.xlsx"


    df.to_excel(
        file,
        index=False
    )


    with open(file,"rb") as f:

        st.download_button(
            "📥 Tải báo cáo Excel",
            f,
            file_name=file
        )
