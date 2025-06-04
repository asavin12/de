import tkinter as tk
from tkinter import ttk, messagebox
from tabs import setup_leseverstehen_teil1, setup_leseverstehen_teil2, setup_leseverstehen_teil3, setup_sprachbausteine_teil1, setup_sprachbausteine_teil2, setup_answers_tab
from handlers import handle_k, paste_from_clipboard, move_to_next_field
from utils import create_json, read_json, edit_json, upload_image_teil3
import logging
import keyboard
import threading
import queue

# Thiết lập logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telc_app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class TELCJsonApp:
    def __init__(self, root, data_queue):
        self.root = root
        self.root.title("TELC B1 JSON Creator")
        self.root.geometry("1200x800")
        self.root.focus_force()
        self.data_queue = data_queue

        logging.debug("Initializing TELCJsonApp")
        print("Starting TELCJsonApp")

        # Danh sách để lưu thứ tự focus
        self.focus_order = []
        # Biến theo dõi ô hiện tại
        self.current_field = None

        # Biến cho Leseverstehen, Teil 3
        self.teil3_image_path = tk.StringVar()

        # Khởi tạo các thuộc tính cho Sprachbausteine
        self.teil1_sprach_options = []  # Khởi tạo danh sách options cho Teil 1
        self.teil2_sprach_options = []  # Khởi tạo danh sách options cho Teil 2

        # File name và các nút
        file_frame = tk.Frame(root)
        file_frame.pack(pady=5, fill="x")
        tk.Label(file_frame, text="Tên file JSON:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.filename_entry = tk.Entry(file_frame, width=40, highlightthickness=0)
        self.filename_entry.pack(side=tk.LEFT, padx=5)
        self.focus_order.append(self.filename_entry)

        # Nút Tạo và lưu JSON
        tk.Button(file_frame, text="Tạo và lưu JSON", command=lambda: self.create_json_button()).pack(side=tk.LEFT, padx=5)
        # Nút Mở JSON
        tk.Button(file_frame, text="Mở JSON", command=lambda: self.read_json_button()).pack(side=tk.LEFT, padx=5)
        # Nút Chỉnh sửa JSON
        tk.Button(file_frame, text="Chỉnh sửa JSON", command=lambda: self.edit_json_button()).pack(side=tk.LEFT, padx=5)

        self.set_current_field(self.filename_entry)

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, fill="both", expand=True)

        # Tabs
        self.leseverstehen_teil1 = ttk.Frame(self.notebook)
        self.leseverstehen_teil2 = ttk.Frame(self.notebook)
        self.leseverstehen_teil3 = ttk.Frame(self.notebook)
        self.sprachbausteine_teil1 = ttk.Frame(self.notebook)
        self.sprachbausteine_teil2 = ttk.Frame(self.notebook)
        self.answers_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.leseverstehen_teil1, text="Leseverstehen, Teil 1")
        self.notebook.add(self.leseverstehen_teil2, text="Leseverstehen, Teil 2")
        self.notebook.add(self.leseverstehen_teil3, text="Leseverstehen, Teil 3")
        self.notebook.add(self.sprachbausteine_teil1, text="Sprachbausteine, Teil 1")
        self.notebook.add(self.sprachbausteine_teil2, text="Sprachbausteine, Teil 2")
        self.notebook.add(self.answers_tab, text="Đáp án (1-40)")

        # Danh sách focus order cho từng tab
        self.teil1_focus = []
        self.teil2_focus = []
        self.teil3_focus = []
        self.sprach1_focus = []
        self.sprach2_focus = []
        self.answers_focus = []

        # Setup tabs
        setup_leseverstehen_teil1(self)
        setup_leseverstehen_teil2(self)
        setup_leseverstehen_teil3(self)
        setup_sprachbausteine_teil1(self)
        setup_sprachbausteine_teil2(self)
        setup_answers_tab(self)

        # Gán focus order và tự động focus khi chuyển tab
        self.notebook.bind("<<NotebookTabChanged>>", lambda event: self.update_focus_order(event))

        # Gán phím nóng K trong tkinter
        try:
            self.root.bind('<Key-k>', lambda event: handle_k(self))
            print("Tkinter K binding successful")
            logging.debug("Tkinter K binding successful")
        except Exception as e:
            print(f"Failed to bind K in tkinter: {str(e)}")
            logging.error(f"Failed to bind K in tkinter: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể bind K: {str(e)}")

        # Gán phím nóng K toàn cục
        def global_hotkey():
            try:
                keyboard.on_press_key('k', lambda e: self.root.after(0, lambda: handle_k(self)))
                print("Global K binding successful")
                logging.debug("Global K binding successful")
            except Exception as e:
                print(f"Failed to bind global K: {str(e)}")
                logging.error(f"Failed to bind global K: {str(e)}")
                messagebox.showerror("Lỗi", f"Không thể bind global K: {str(e)}")

        threading.Thread(target=global_hotkey, daemon=True).start()

        # Xử lý dữ liệu từ hàng đợi
        def check_queue():
            try:
                while not self.data_queue.empty():
                    text = self.data_queue.get_nowait()
                    self.insert_text(text)
                self.root.after(100, check_queue)
            except Exception as e:
                print(f"Error in check_queue: {str(e)}")
                logging.error(f"Error in check_queue: {str(e)}")

        self.root.after(100, check_queue)

    def create_json_button(self):
        """Xử lý nút Tạo và lưu JSON"""
        logging.info("Button 'Tạo và lưu JSON' clicked")
        create_json(self)

    def read_json_button(self):
        """Xử lý nút Mở JSON"""
        logging.info("Button 'Mở JSON' clicked")
        read_json(self)

    def edit_json_button(self):
        """Xử lý nút chỉnh sửa JSON"""
        logging.info("Button 'Chỉnh sửa JSON' clicked")
        edit_json(self)

    def set_current_field(self, widget):
        """Đặt ô hiện tại và viền vàng"""
        self.current_field = widget
        for w in self.focus_order:
            w.config(highlightthickness=0)
        if widget:
            widget.config(highlightthickness=2, highlightbackground="yellow")
            print(f"Set current field: {type(widget).__name__}")
            logging.debug(f"Set current field: {type(widget).__name__} via {'double-click' if widget.winfo_pointerx() else 'other'}")
            widget.focus_set()  # Đặt focus chuột vào ô

    def insert_text(self, text):
        """Chèn văn bản vào ô hiện tại"""
        if not self.current_field:
            print("No current field selected")
            logging.warning("No current field selected")
            messagebox.showwarning("Cảnh báo", "Không có ô nào được chọn!")
            return
        try:
            if isinstance(self.current_field, tk.Entry):
                self.current_field.delete(0, tk.END)
                self.current_field.insert(0, text)
                print(f"Inserted '{text}' into Entry")
                logging.debug(f"Inserted '{text}' into Entry")
            elif isinstance(self.current_field, tk.Text):
                self.current_field.delete("1.0", tk.END)
                self.current_field.insert("1.0", text)
                print(f"Inserted '{text}' into Text")
                logging.debug(f"Inserted '{text}' into Text")
            move_to_next_field(self)
        except Exception as e:
            print(f"Error in insert_text: {str(e)}")
            logging.error(f"Error in insert_text: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể chèn văn bản: {str(e)}")

    def update_focus_order(self, event=None):
        """Cập nhật thứ tự focus khi chuyển tab"""
        try:
            current_tab = self.notebook.index(self.notebook.select())
            if current_tab == 0:
                self.focus_order = self.teil1_focus
                if self.teil1_focus and not self.current_field in self.teil1_focus:
                    self.set_current_field(self.teil1_focus[0])
            elif current_tab == 1:
                self.focus_order = self.teil2_focus
                if self.teil2_focus and not self.current_field in self.teil2_focus:
                    self.set_current_field(self.teil2_focus[0])
            elif current_tab == 2:
                self.focus_order = self.teil3_focus
                if self.teil3_focus and not self.current_field in self.teil3_focus:
                    self.set_current_field(self.teil3_focus[0])
            elif current_tab == 3:
                self.focus_order = self.sprach1_focus
                if self.sprach1_focus and not self.current_field in self.sprach1_focus:
                    self.set_current_field(self.sprach1_focus[0])
            elif current_tab == 4:
                self.focus_order = self.sprach2_focus
                if self.sprach2_focus and not self.current_field in self.sprach2_focus:
                    self.set_current_field(self.sprach2_focus[0])
            elif current_tab == 5:
                self.focus_order = self.answers_focus
                if self.answers_focus and not self.current_field in self.answers_focus:
                    self.set_current_field(self.answers_focus[0])
            print(f"Updated focus order for tab {current_tab}")
            logging.debug(f"Updated focus order for tab {current_tab}")
        except Exception as e:
            print(f"Error in update_focus_order: {str(e)}")
            logging.error(f"Error in update_focus_order: {str(e)}")