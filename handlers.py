import tkinter as tk
from tkinter import messagebox
import pyperclip
import pyautogui
import time
import logging

# Thiết lập logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telc_app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def handle_k(app):
    print("K pressed")
    logging.debug("K pressed")
    try:
        # Mô phỏng Ctrl+C
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.2)
        print("Simulated Ctrl+C")
        logging.debug("Simulated Ctrl+C")

        # Kiểm tra clipboard
        clipboard_content = pyperclip.paste().strip()
        if not clipboard_content:
            print("Clipboard is empty")
            logging.warning("Clipboard is empty")
            messagebox.showwarning("Cảnh báo", "Clipboard rỗng! Vui lòng bôi đen văn bản trước khi nhấn K.")
            return

        # Chèn nội dung từ clipboard
        app.insert_text(clipboard_content)
    except Exception as e:
        print(f"Error in handle_k: {str(e)}")
        logging.error(f"Error in handle_k: {str(e)}")
        messagebox.showerror("Lỗi", f"Không thể xử lý K: {str(e)}")

def paste_from_clipboard(app):
    """Hàm cũ, giữ lại để tương thích"""
    if not app.current_field:
        print("No current field selected")
        logging.warning("No current field selected")
        return
    try:
        clipboard_content = pyperclip.paste().strip()
        if not clipboard_content:
            print("Clipboard is empty in paste_from_clipboard")
            logging.warning("Clipboard is empty in paste_from_clipboard")
            return
        if isinstance(app.current_field, tk.Entry):
            app.current_field.delete(0, tk.END)
            app.current_field.insert(0, clipboard_content)
            print(f"Pasted '{clipboard_content}' into Entry")
            logging.debug(f"Pasted '{clipboard_content}' into Entry")
        elif isinstance(app.current_field, tk.Text):
            app.current_field.delete("1.0", tk.END)
            app.current_field.insert("1.0", clipboard_content)
            print(f"Pasted '{clipboard_content}' into Text")
            logging.debug(f"Pasted '{clipboard_content}' into Text")
    except Exception as e:
        print(f"Error in paste_from_clipboard: {str(e)}")
        logging.error(f"Error in paste_from_clipboard: {str(e)}")
        messagebox.showerror("Lỗi", f"Không thể dán từ clipboard: {str(e)}")

def move_to_next_field(app):
    try:
        if app.current_field in app.focus_order:
            current_index = app.focus_order.index(app.current_field)
            if current_index < len(app.focus_order) - 1:
                # Nhảy sang ô tiếp theo trong tab hiện tại
                next_index = current_index + 1
                app.set_current_field(app.focus_order[next_index])
                print(f"Moved to next field: index {next_index}")
                logging.debug(f"Moved to next field: index {next_index}")
            else:
                # Đến ô cuối tab, chuyển sang tab tiếp theo
                current_tab = app.notebook.index(app.notebook.select())
                next_tab = (current_tab + 1) % app.notebook.index("end")
                app.notebook.select(next_tab)
                app.update_focus_order()
                print(f"Switched to next tab: {next_tab}")
                logging.debug(f"Switched to next tab: {next_tab}")
        else:
            print("Current field not in focus_order")
            logging.warning("Current field not in focus_order")
            if app.focus_order:
                app.set_current_field(app.focus_order[0])
    except Exception as e:
        print(f"Error in move_to_next_field: {str(e)}")
        logging.error(f"Error in move_to_next_field: {str(e)}")
        messagebox.showerror("Lỗi", f"Không thể nhảy sang ô tiếp theo: {str(e)}")