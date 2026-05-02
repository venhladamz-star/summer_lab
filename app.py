import streamlit as st
import os
import subprocess
import glob

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(
    page_title="VNU Engineering - Universal Downloader",
    page_icon="🚀",
    layout="centered"
)

# Custom CSS để giao diện trông sạch sẽ hơn
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Universal Downloader")
st.info("Hỗ trợ tải Video (MP4) và Nhạc (MP3) từ YouTube, TikTok, Facebook...")

# Tạo thư mục tạm để lưu file trên server nếu chưa có
OUTPUT_DIR = "temp_downloads"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- GIAO DIỆN NHẬP LIỆU ---
url = st.text_input("🔗 Dán đường dẫn (Link) vào đây:", placeholder="https://...")

col1, col2 = st.columns(2)
with col1:
    format_choice = st.selectbox("Chọn định dạng:", ["Video MP4", "Nhạc MP3"])
with col2:
    st.write("") # Khoảng trống
    st.write("") # Khoảng trống
    run_button = st.button("🚀 Bắt đầu xử lý")

if run_button:
    if not url:
        st.warning("Vui lòng dán link trước khi nhấn tải!")
    else:
        with st.spinner('Đang tải dữ liệu từ link... vui lòng đợi trong giây lát!'):
            try:
                # Xóa các file cũ trong thư mục tạm để tránh đầy bộ nhớ server
                files = glob.glob(f'{OUTPUT_DIR}/*')
                for f in files:
                    os.remove(f)

                # Thiết lập lệnh yt-dlp dựa trên code cũ của bạn
                # Sử dụng --no-check-certificate để tránh lỗi SSL trên server
                cmd = [
                    "yt-dlp",
                    "--no-playlist",
                    "--no-check-certificate",
                    "-o", f"{OUTPUT_DIR}/%(title)s.%(ext)s"
                ]

                if format_choice == "Nhạc MP3":
                    # Chế độ tải nhạc: trích xuất audio và chuyển sang mp3
                    cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
                else:
                    # Chế độ video: ưu tiên mp4 để tương thích tốt nhất[cite: 2]
                    cmd.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])

                cmd.append(url)

                # Chạy tiến trình hệ thống
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    # Tìm file vừa mới tạo ra trong thư mục tạm
                    downloaded_files = os.listdir(OUTPUT_DIR)
                    if downloaded_files:
                        file_path = os.path.join(OUTPUT_DIR, downloaded_files[0])
                        
                        with open(file_path, "rb") as f:
                            file_data = f.read()
                            st.success(f"✅ Đã xử lý xong: **{downloaded_files[0]}**")
                            
                            # Nút bấm để người dùng tải từ server về máy cá nhân
                            st.download_button(
                                label="⬇️ NHẤN VÀO ĐÂY ĐỂ TẢI VỀ MÁY",
                                data=file_data,
                                file_name=downloaded_files[0],
                                mime="application/octet-stream"
                            )
                else:
                    st.error(f"Lỗi từ hệ thống: {result.stderr}")

            except Exception as e:
                st.error(f"Có lỗi xảy ra: {str(e)}")

st.markdown("---")
st.caption("Phát triển bởi Vũ Bảo Khuê - VNU Engineering Student")
