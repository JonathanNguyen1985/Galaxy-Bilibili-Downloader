import customtkinter as ctk
from tkinter import filedialog
import yt_dlp
import threading
import os
import webbrowser 

# Thiết lập giao diện
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- LỚP XỬ LÝ TERMINAL ẢO CHẠY NGAY TRONG TOOL ---
class TextBoxLogger(object):
    def __init__(self, textbox):
        self.textbox = textbox

    def write_log(self, msg):
        self.textbox.insert("end", msg + "\n")
        self.textbox.see("end")

    def debug(self, msg):
        self.write_log(msg)

    def warning(self, msg):
        self.write_log(f"[CẢNH BÁO] {msg}")

    def error(self, msg):
        self.write_log(f"[LỖI] {msg}")

class GalaxyBiliDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Galaxy Video Downloader Pro")
        self.geometry("920x680") # Nhích ra một xíu cho 2 nút ở header đứng thoải mái
        self.resizable(True, True) 

        # ==========================================
        # HEADER FRAME: Tiêu đề (Trái) & Tác giả, Mạng xã hội (Phải)
        # ==========================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 10))

        # Tiêu đề bên trái
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="GALAXY VIDEO DOWNLOADER", font=("Arial", 26, "bold"), text_color="#00BFFF")
        self.lbl_title.pack(side="left", padx=20)

        # Cụm Thông tin bản quyền bên phải
        self.info_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.info_frame.pack(side="right", padx=20)

        self.lbl_author = ctk.CTkLabel(self.info_frame, text="© 2026 Galaxy Downloader V1.0 | Dev: Jonathan Nguyen", font=("Arial", 11, "bold"), text_color="#ffc107")
        self.lbl_author.pack(anchor="e")

        self.lbl_note = ctk.CTkLabel(self.info_frame, text="Phát triển vì cộng đồng - Vui lòng sử dụng có trách nhiệm", font=("Arial", 11, "italic"), text_color="#a9a9a9")
        self.lbl_note.pack(anchor="e", pady=(0, 2))

        # Khung nhỏ chứa 2 nút MXH nằm ngang hàng nhau
        self.social_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.social_frame.pack(anchor="e", pady=(2, 0))

        # Nút Facebook
        self.btn_fb = ctk.CTkButton(self.social_frame, text="🌐 Facebook Admin", width=130, height=24, fg_color="#1877F2", hover_color="#165ebb", font=("Arial", 11, "bold"), command=self.open_facebook)
        self.btn_fb.pack(side="left", padx=(0, 5))

        # Nút Zalo (Màu xanh Zalo chuẩn)
        self.btn_zalo = ctk.CTkButton(self.social_frame, text="💬 Nhóm Zalo Hỗ Trợ", width=130, height=24, fg_color="#0068FF", hover_color="#0055d4", font=("Arial", 11, "bold"), command=self.open_zalo)
        self.btn_zalo.pack(side="left")
        # ==========================================

        # --- 1. KHUNG NHẬP LINK ---
        self.lbl_url_title = ctk.CTkLabel(self, text="🔗 Nhập Link Video Bilibili (Đưa link vào đây nè anh Jonathan Nguyen):", font=("Arial", 12, "bold"))
        self.lbl_url_title.pack(anchor="w", padx=40, pady=(5, 0))
        
        self.url_var = ctk.StringVar()
        self.entry_url = ctk.CTkEntry(self, textvariable=self.url_var, height=35)
        self.entry_url.pack(fill="x", padx=40, pady=(0, 10))

        # --- 2. KHUNG LƯU VIDEO ---
        self.lbl_save_title = ctk.CTkLabel(self, text="📁 Thư mục lưu Video sau khi tải xong:", font=("Arial", 12, "bold"))
        self.lbl_save_title.pack(anchor="w", padx=40, pady=(5, 0))

        self.save_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.save_frame.pack(fill="x", padx=40, pady=(0, 10))
        
        self.save_var = ctk.StringVar()
        self.save_var.set(os.getcwd()) 
        self.entry_save = ctk.CTkEntry(self.save_frame, textvariable=self.save_var, height=35)
        self.entry_save.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_browse = ctk.CTkButton(self.save_frame, text="Chọn Thư Mục", height=35, command=self.browse_folder)
        self.btn_browse.pack(side="right")

        # --- 3. KHUNG NHẬP PROXY ---
        self.lbl_proxy_title = ctk.CTkLabel(self, text="🌐 Cấu hình IP Proxy (Để trống nếu anh dùng trình duyệt Fix IP ở ngoài) - Định dạng: http://user:pass@ip:port", font=("Arial", 12, "bold"))
        self.lbl_proxy_title.pack(anchor="w", padx=40, pady=(5, 0))

        self.proxy_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.proxy_frame.pack(fill="x", padx=40, pady=(0, 15))

        self.proxy_var = ctk.StringVar()
        self.entry_proxy = ctk.CTkEntry(self.proxy_frame, textvariable=self.proxy_var, height=35, placeholder_text="Nhập link Proxy vào đây hoặc để trống...")
        self.entry_proxy.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_save_proxy = ctk.CTkButton(self.proxy_frame, text="Lưu Proxy", height=35, width=90, fg_color="#ffc107", text_color="black", hover_color="#e0a800", command=self.save_proxy_config)
        self.btn_save_proxy.pack(side="right")

        # --- NÚT BẮT ĐẦU TẢI ---
        self.btn_download = ctk.CTkButton(self, text="BẮT ĐẦU TẢI NGAY", font=("Arial", 14, "bold"), height=45, fg_color="#28a745", hover_color="#218838", command=self.start_download_thread)
        self.btn_download.pack(pady=(5, 15))

        # --- TERMINAL ẢO ---
        self.lbl_terminal = ctk.CTkLabel(self, text="📺 Terminal Tiến Trình Tải:", text_color="gray", font=("Arial", 12, "bold"))
        self.lbl_terminal.pack(anchor="w", padx=40)
        
        self.terminal_box = ctk.CTkTextbox(self, fg_color="#0a0a0a", text_color="#00FF00", font=("Consolas", 11))
        self.terminal_box.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        self.terminal_box.insert("0.0", "Hệ thống Galaxy chuẩn bị... Đợi lệnh từ admin.\n")

        # Khởi chạy hàm đọc Proxy
        self.load_proxy_config()

    # Hàm tự động mở trình duyệt vào thẳng Facebook của anh
    def open_facebook(self):
        webbrowser.open("https://www.facebook.com/jonathanNguyen421985/")

    # Hàm tự động mở trình duyệt vào thẳng nhóm Zalo
    def open_zalo(self):
        webbrowser.open("https://zalo.me/g/d2nolw7krb7xpgna1wrl")

    def load_proxy_config(self):
        config_file = "galaxy_proxy.txt"
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    saved_proxy = f.read().strip()
                    self.proxy_var.set(saved_proxy)
                    self.terminal_box.insert("end", f"[HỆ THỐNG] Đã nạp lại cấu hình Proxy cũ: {saved_proxy}\n")
                    self.terminal_box.see("end")
            except Exception as e:
                pass

    def save_proxy_config(self):
        proxy_data = self.proxy_var.get().strip()
        config_file = "galaxy_proxy.txt"
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                f.write(proxy_data)
            
            if proxy_data == "":
                self.terminal_box.insert("end", "\n[HỆ THỐNG] Đã xóa Proxy. Tool sẽ dùng mạng mặc định.\n")
            else:
                self.terminal_box.insert("end", f"\n[HỆ THỐNG] Đã lưu thành công Proxy: {proxy_data}\n")
            self.terminal_box.see("end")
        except Exception as e:
            self.terminal_box.insert("end", f"\n[LỖI LƯU FILE]: {str(e)}\n")
            self.terminal_box.see("end")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.save_var.set(folder_selected)

    def download_video(self, url, save_path, proxy_ip):
        logger = TextBoxLogger(self.terminal_box)
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'quiet': False, 
            'logger': logger, 
            'external_downloader': 'aria2c',
            'external_downloader_args': ['-x', '8', '-s', '8', '-k', '1M'],
        }

        if proxy_ip:
            ydl_opts['proxy'] = proxy_ip
            logger.write_log(f"\n=> Đang kích hoạt luồng Proxy: {proxy_ip}")
        else:
            logger.write_log("\n=> Không dùng Proxy. Đang chạy qua mạng mặc định / VPN ngoài.")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logger.write_log("\n[THÀNH CÔNG] Video đã tải xong và được lưu vào ổ đĩa!")
        except Exception as e:
            logger.write_log(f"\n[LỖI]: {str(e)}")
        finally:
            self.btn_download.configure(state="normal", text="BẮT ĐẦU TẢI NGAY", fg_color="#28a745")

    def start_download_thread(self):
        url = self.url_var.get().strip()
        save_path = self.save_var.get().strip()
        proxy_ip = self.proxy_var.get().strip()

        if not url:
            self.terminal_box.insert("end", "\n[CẢNH BÁO] Anh chưa dán link video kìa!\n")
            self.terminal_box.see("end")
            return

        self.btn_download.configure(state="disabled", text="HỆ THỐNG ĐANG TẢI...", fg_color="#dc3545")
        self.terminal_box.insert("end", "\n" + "="*50 + "\n")
        self.terminal_box.insert("end", "🚀 Khởi động luồng kéo video tốc độ cao...\n")
        self.terminal_box.see("end")

        thread = threading.Thread(target=self.download_video, args=(url, save_path, proxy_ip))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    app = GalaxyBiliDownloader()
    app.mainloop()