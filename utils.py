import tkinter as tk
from tkinter import filedialog, messagebox
import json
import shutil
import os
import logging
import unicodedata

# Thiết lập logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telc_app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def create_json(app):
    try:
        filename = app.filename_entry.get().strip()
        if not filename:
            logging.warning("Filename is empty, using default 'output.json'")
            filename = "output.json"
        if not filename.endswith('.json'):
            filename += '.json'

        # Đếm số trường trống
        empty_fields = 0
        empty_details = []

        # Leseverstehen Teil 1
        texts = [text.get("1.0", tk.END).strip() for text in app.teil1_texts]
        overschriften = [entry.get().strip() for entry in app.teil1_overschriften]
        empty_texts = sum(1 for t in texts if not t)
        empty_overschriften = sum(1 for o in overschriften if not o)
        empty_fields += empty_texts + empty_overschriften
        if empty_texts:
            empty_details.append(f"Leseverstehen Teil 1: {empty_texts} empty texts")
        if empty_overschriften:
            empty_details.append(f"Leseverstehen Teil 1: {empty_overschriften} empty overschriften")

        # Leseverstehen Teil 2
        content = app.teil2_content.get("1.0", tk.END).strip()
        questions = [q.get().strip() for q in app.teil2_questions]
        options = [[opt.get().strip() for opt in opts] for opts in app.teil2_options]
        empty_content = 1 if not content else 0
        empty_questions = sum(1 for q in questions if not q)
        empty_options = sum(1 for opts in options for opt in opts if not opt)
        empty_fields += empty_content + empty_questions + empty_options
        if empty_content:
            empty_details.append("Leseverstehen Teil 2: empty content")
        if empty_questions:
            empty_details.append(f"Leseverstehen Teil 2: {empty_questions} empty questions")
        if empty_options:
            empty_details.append(f"Leseverstehen Teil 2: {empty_options} empty options")

        # Leseverstehen Teil 3
        situations = [s.get().strip() for s in app.teil3_situations]
        image_path = app.teil3_image_path.get().strip()
        empty_situations = sum(1 for s in situations if not s)
        empty_image = 1 if not image_path else 0
        empty_fields += empty_situations + empty_image
        if empty_situations:
            empty_details.append(f"Leseverstehen Teil 3: {empty_situations} empty situations")
        if empty_image:
            empty_details.append("Leseverstehen Teil 3: empty image_path")

        # Sprachbausteine Teil 1
        sprach1_content = app.teil1_sprach_content.get("1.0", tk.END).strip()
        sprach1_options = [[opt.get().strip() for opt in opts] for opts in app.teil1_sprach_options]
        empty_sprach1_content = 1 if not sprach1_content else 0
        empty_sprach1_options = sum(1 for opts in sprach1_options for opt in opts if not opt)
        empty_fields += empty_sprach1_content + empty_sprach1_options
        if empty_sprach1_content:
            empty_details.append("Sprachbausteine Teil 1: empty content")
        if empty_sprach1_options:
            empty_details.append(f"Sprachbausteine Teil 1: {empty_sprach1_options} empty options")

        # Sprachbausteine Teil 2
        sprach2_content = app.teil2_sprach_content.get("1.0", tk.END).strip()
        sprach2_options = [opt.get().strip() for opt in app.teil2_sprach_options]
        empty_sprach2_content = 1 if not sprach2_content else 0
        empty_sprach2_options = sum(1 for opt in sprach2_options if not opt)
        empty_fields += empty_sprach2_content + empty_sprach2_options
        if empty_sprach2_content:
            empty_details.append("Sprachbausteine Teil 2: empty content")
        if empty_sprach2_options:
            empty_details.append(f"Sprachbausteine Teil 2: {empty_sprach2_options} empty options")

        # Answers
        answers = [entry.get().strip() for entry in app.answer_entries]
        empty_answers = sum(1 for a in answers if not a)
        empty_fields += empty_answers
        if empty_answers:
            empty_details.append(f"Answers: {empty_answers} empty answers")

        # Tạo dữ liệu JSON, loại bỏ sprach1_questions và sprach2_questions
        data = {
            "leseverstehen_teil1": {
                "texts": texts,
                "overschriften": overschriften
            },
            "leseverstehen_teil2": {
                "content": content,
                "questions": questions,
                "options": options
            },
            "leseverstehen_teil3": {
                "situations": situations,
                "image_path": image_path  # Lưu \images\filename
            },
            "sprachbausteine_teil1": {
                "content": sprach1_content,
                "options": sprach1_options
            },
            "sprachbausteine_teil2": {
                "content": sprach2_content,
                "options": sprach2_options
            },
            "answers": answers
        }

        # Lưu JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Created JSON file: {filename}, {empty_fields} empty fields")
        logging.info(f"Created JSON file: {filename}, {empty_fields} empty fields")
        if empty_details:
            print(f"Empty fields details: {'; '.join(empty_details)}")
            logging.debug(f"Empty fields details: {'; '.join(empty_details)}")
        messagebox.showinfo("Thành công", f"Đã tạo file {filename} ({empty_fields} trường trống)")
    except Exception as e:
        print(f"Error creating JSON: {str(e)}")
        logging.error(f"Error creating JSON: {str(e)}")
        raise  # Ném lại lỗi để edit_json xử lý

def read_json(app):
    try:
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filename:
            return

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        app.filename_entry.delete(0, tk.END)
        app.filename_entry.insert(0, os.path.basename(filename))

        # Leseverstehen Teil 1
        for i, text in enumerate(data['leseverstehen_teil1']['texts']):
            app.teil1_texts[i].delete("1.0", tk.END)
            app.teil1_texts[i].insert("1.0", text)
        for i, ov in enumerate(data['leseverstehen_teil1']['overschriften']):
            app.teil1_overschriften[i].delete(0, tk.END)
            app.teil1_overschriften[i].insert(0, ov)

        # Leseverstehen Teil 2
        app.teil2_content.delete("1.0", tk.END)
        app.teil2_content.insert("1.0", data['leseverstehen_teil2']['content'])
        for i, q in enumerate(data['leseverstehen_teil2']['questions']):
            app.teil2_questions[i].delete(0, tk.END)
            app.teil2_questions[i].insert(0, q)
        for i, opts in enumerate(data['leseverstehen_teil2']['options']):
            for j, opt in enumerate(opts):
                app.teil2_options[i][j].delete(0, tk.END)
                app.teil2_options[i][j].insert(0, opt)

        # Leseverstehen Teil 3
        for i, s in enumerate(data['leseverstehen_teil3']['situations']):
            app.teil3_situations[i].delete(0, tk.END)
            app.teil3_situations[i].insert(0, s)
        # Xử lý image_path tương đối
        image_path = data['leseverstehen_teil3'].get('image_path', '')
        app.teil3_image_path.set(image_path)

        # Sprachbausteine Teil 1
        app.teil1_sprach_content.delete("1.0", tk.END)
        app.teil1_sprach_content.insert("1.0", data['sprachbausteine_teil1']['content'])
        for i, opts in enumerate(data['sprachbausteine_teil1']['options']):
            for j, opt in enumerate(opts):
                app.teil1_sprach_options[i][j].delete(0, tk.END)
                app.teil1_sprach_options[i][j].insert(0, opt)

        # Sprachbausteine Teil 2
        app.teil2_sprach_content.delete("1.0", tk.END)
        app.teil2_sprach_content.insert("1.0", data['sprachbausteine_teil2']['content'])
        for i, opt in enumerate(data['sprachbausteine_teil2']['options']):
            app.teil2_sprach_options[i].delete(0, tk.END)
            app.teil2_sprach_options[i].insert(0, opt)

        # Answers
        for i, answer in enumerate(data['answers']):
            app.answer_entries[i].delete(0, tk.END)
            app.answer_entries[i].insert(0, answer)

        print(f"Loaded JSON file: {filename}")
        logging.info(f"Loaded JSON file: {filename}")
        messagebox.showinfo("Thành công", f"Đã tải dữ liệu từ {filename}")
    except Exception as e:
        print(f"Error reading JSON: {str(e)}")
        logging.error(f"Error reading JSON: {str(e)}")
        messagebox.showerror("Lỗi", f"Không thể đọc JSON: {str(e)}")

def edit_json(app):
    try:
        filename = app.filename_entry.get().strip()
        if not filename:
            logging.warning("Filename is empty, using default 'output.json'")
            filename = "output.json"
        if not filename.endswith('.json'):
            filename += '.json'

        if not os.path.exists(filename):
            messagebox.showerror("Lỗi", f"File {filename} không tồn tại!")
            return

        create_json(app)
        print(f"Edited JSON file: {filename}")
        logging.info(f"Edited JSON file: {filename}")
        messagebox.showinfo("Thành công", f"Đã cập nhật file {filename}")
    except Exception as e:
        print(f"Error editing JSON: {str(e)}")
        logging.error(f"Error editing JSON: {str(e)}")
        messagebox.showerror("Lỗi", f"Không thể chỉnh sửa JSON: {str(e)}")

def upload_image_teil3(app):
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
        if file_path:
            target_dir = os.path.join(os.getcwd(), "images")
            os.makedirs(target_dir, exist_ok=True)
            # Chuẩn hóa tên file để tránh ký tự không hợp lệ
            base_name = os.path.basename(file_path)
            safe_name = ''.join(c if c.isalnum() or c in '._-' else '_' for c in unicodedata.normalize('NFKD', base_name))
            target_path = os.path.join(target_dir, safe_name)
            shutil.copy2(file_path, target_path)
            # Lưu đường dẫn tương đối \images\filename
            relative_path = f"\\images\\{safe_name}"
            app.teil3_image_path.set(relative_path)
            print(f"Saved image: {target_path}, relative path: {relative_path}")
            logging.info(f"Saved image: {target_path}, relative path: {relative_path}")
            if base_name != safe_name:
                logging.warning(f"Renamed image from {base_name} to {safe_name} due to invalid characters")
            messagebox.showinfo("Thành công", f"Đã tải lên hình ảnh: {safe_name}")
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
        logging.error(f"Error uploading image: {str(e)}")
        messagebox.showerror("Lỗi", f"Không thể tải lên hình ảnh: {str(e)}")