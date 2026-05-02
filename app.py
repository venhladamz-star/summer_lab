import streamlit as st
import os
import subprocess
import glob
import time

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(
    page_title="VNU Engineering - Universal Downloader",
    page_icon="🚀",
    layout="centered"
)

st.title("🌍 Universal Downloader")
st.markdown("---")

# Thư mục tạm lưu file
OUTPUT_DIR = "temp_downloads"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- GIAO DIỆN NGƯỜI DÙNG ---
url = st.text_input("🔗 Dán link video/nhạc vào đây:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    format_choice = st.selectbox("Định dạng đầu ra:", ["Video MP4", "Nhạc MP3"])
with col2:
    # Thêm khoảng trống để nút bấm thẳng hàng
    st.write("##")
    run_button = st.button("🚀 Bắt đầu xử lý")

if run_button:
    if not url:
        st.warning("Bạn chưa nhập đường dẫn!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 1. Dọn dẹp file cũ
            for f in glob.glob(f"{OUTPUT_DIR}/*"):
                try: os.remove(f)
                except: pass
            
            status_text.text("🔄 Đang cấu hình hệ thống...")
            progress_bar.progress(20)

            # 2. Thiết lập lệnh yt-dlp với các tham số vượt rào
            cmd = [
                "yt-dlp",
                "--no-playlist",
                "--no-check-certificate",
                "--no-warnings",
                # Giả lập trình duyệt để tránh lỗi 403 Forbidden
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "--add-header", "Accept-Language: vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                "-o", f"{OUTPUT_DIR}/%(title)s.%(ext)s"
            ]

            if format_choice == "Nhạc MP3":
                # Chế độ tải nhạc trích xuất audio[cite: 2]
                cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
            else:
                # Chế độ video ưu tiên mp4 sẵn có để giảm tải cho server[cite: 2]
                cmd.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])

            cmd.append(url)

            # 3. Thực thi lệnh
            status_text.text("📥 Đang tải dữ liệu từ máy chủ (có thể mất vài phút)...")
            progress_bar.progress(50)
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                progress_bar.progress(90)
                downloaded_files = os.listdir(OUTPUT_DIR)
                
                if downloaded_files:
                    file_path = os.path.join(OUTPUT_DIR, downloaded_files[0])
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                        
                    status_text.success(f"✨ Xử lý thành công: {downloaded_files[0]}")
                    progress_bar.progress(100)
                    
                    st.download_button(
                        label="⬇️ TẢI FILE VỀ MÁY",
                        data=file_bytes,
                        file_name=downloaded_files[0],
                        mime="application/octet-stream"
                    )
                else:
                    st.error("Lỗi: Không tìm thấy file sau khi tải.")
            else:
                # Hiển thị lỗi chi tiết từ hệ thống để debug
                st.error("❌ Hệ thống từ chối truy cập.")
                with st.expander("Xem chi tiết lỗi"):
                    st.code(result.stderr)

        except Exception as e:
            st.error(f"Đã xảy ra sự cố: {str(e)}")

st.markdown("---")
st.caption("Ứng dụng chạy trên nền tảng Streamlit Cloud | Engine: yt-dlp")
