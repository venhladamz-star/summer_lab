import streamlit as st
import os
import subprocess
import glob

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="VNU Engineering Downloader", page_icon="🚀")

st.title("🌍 Universal Downloader")
st.info("Ứng dụng hỗ trợ tải video và nhạc. Nếu gặp lỗi 403, hãy thử lại sau vài phút.")

# Thư mục tạm lưu file trên server
OUTPUT_DIR = "temp_downloads"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- GIAO DIỆN NGƯỜI DÙNG ---
url = st.text_input("🔗 Dán link vào đây:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("Chọn định dạng:", ("🎬 Video MP4", "🎵 Nhạc MP3"))

if st.button("🚀 Bắt đầu tải"):
    if not url:
        st.warning("Bạn chưa nhập link!")
    else:
        with st.spinner('Đang xử lý... Hệ thống đang giả lập trình duyệt để vượt rào cản...'):
            try:
                # Dọn dẹp thư mục tạm trước khi tải mới
                for f in glob.glob(f"{OUTPUT_DIR}/*"):
                    os.remove(f)

                # Cấu hình lệnh yt-dlp nâng cao để tránh lỗi 403 và JS runtime
                cmd = [
                    "yt-dlp",
                    "--no-playlist",
                    "--no-check-certificate",
                    "--no-warnings",
                    # Giả lập User-Agent của trình duyệt thật
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    "--add-header", "Accept-Language: vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                    "--prefer-free-formats",
                    "-o", f"{OUTPUT_DIR}/%(title)s.%(ext)s"
                ]

                if format_choice == "🎵 Nhạc MP3":
                    cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
                else:
                    # Lấy định dạng mp4 trực tiếp để tránh phải render lại trên server
                    cmd.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])

                cmd.append(url)

                # Thực thi lệnh và lấy thông tin lỗi nếu có
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

                if result.returncode == 0:
                    files = os.listdir(OUTPUT_DIR)
                    if files:
                        file_path = os.path.join(OUTPUT_DIR, files[0])
                        with open(file_path, "rb") as f:
                            st.success(f"✅ Đã xử lý xong: {files[0]}")
                            st.download_button(
                                label="⬇️ NHẤN VÀO ĐÂY ĐỂ TẢI VỀ",
                                data=f,
                                file_name=files[0],
                                mime="application/octet-stream"
                            )
                else:
                    st.error("Hệ thống bị chặn (Lỗi 403).")
                    with st.expander("Xem chi tiết lỗi kỹ thuật"):
                        st.code(result.stderr)

            except Exception as e:
                st.error(f"Lỗi không xác định: {e}")

st.markdown("---")
st.caption("Developed by Khue Vu - VNU UET")
