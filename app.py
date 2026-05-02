import streamlit as st
import os
import subprocess
import shutil

# Cấu hình trang web
st.set_page_config(page_title="VNU Engineering Downloader", page_icon="🚀")

st.title("🌍 Universal Downloader")
st.markdown("Dán link video (YouTube, TikTok, Facebook...) vào bên dưới để tải nhé!")

# Thư mục tạm để lưu file trên server
OUTPUT_DIR = "downloads"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Giao diện nhập liệu
url = st.text_input("🔗 Dán link vào đây:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("Chọn định dạng muốn tải:", ("🎵 Nhạc MP3", "🎬 Video MP4"))

if st.button("🚀 Bắt đầu tải"):
    if not url:
        st.error("Bạn chưa dán link kìa!")
    else:
        with st.spinner('Đang xử lý... vui lòng đợi tí nhé!'):
            try:
                # Thiết lập lệnh yt-dlp[cite: 2]
                # Lưu ý: Trên máy chủ Web, ta dùng lệnh 'yt-dlp' trực tiếp vì nó sẽ được cài qua requirements.txt
                cmd = ["yt-dlp", "--no-playlist", "-o", f"{OUTPUT_DIR}/%(title)s.%(ext)s"]
                
                if format_choice == "🎵 Nhạc MP3":
                    cmd.extend(["-x", "--audio-format", "mp3"])
                else:
                    cmd.extend(["-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]", "--merge-output-format", "mp4"])
                
                cmd.append(url)
                
                # Chạy lệnh tải
                subprocess.run(cmd, check=True)
                
                # Tìm file vừa tải xong để gửi cho người dùng
                files = os.listdir(OUTPUT_DIR)
                if files:
                    latest_file = max([os.path.join(OUTPUT_DIR, f) for f in files], key=os.path.getctime)
                    with open(latest_file, "rb") as f:
                        st.success(f"✨ Đã xử lý xong: {os.path.basename(latest_file)}")
                        st.download_button(
                            label="⬇️ Nhấn vào đây để tải về máy",
                            data=f,
                            file_name=os.path.basename(latest_file)
                        )
                
                # Dọn dẹp thư mục sau khi tải (tùy chọn)
                # shutil.rmtree(OUTPUT_DIR)
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")