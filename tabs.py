import tkinter as tk
from tkinter import ttk
from utils import upload_image_teil3
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

def setup_leseverstehen_teil1(app):
    main_frame = tk.Frame(app.leseverstehen_teil1)
    main_frame.pack(pady=10, fill="both", expand=True)

    # Überschriften (hiển thị bên trái)
    uberschriften_frame = tk.Frame(main_frame)
    uberschriften_frame.pack(side=tk.LEFT, padx=10)
    tk.Label(uberschriften_frame, text="10 Überschriften (a-j):").pack()
    app.teil1_overschriften = []
    for i in range(10):
        frame = tk.Frame(uberschriften_frame)
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=f"{chr(97+i)}):").pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=30, highlightthickness=0)
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind('<Double-Button-1>', lambda event, w=entry: app.set_current_field(w))
        app.teil1_overschriften.append(entry)

    # Texts (hiển thị bên phải)
    text_frame = tk.Frame(main_frame)
    text_frame.pack(side=tk.LEFT, padx=10)
    tk.Label(text_frame, text="5 đoạn văn (Text 1-5):").pack()
    app.teil1_texts = []
    for i in range(5):
        frame = tk.Frame(text_frame)
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=f"Text {i+1}:").pack(side=tk.LEFT)
        text = tk.Text(frame, height=3, width=30, highlightthickness=0)
        text.pack(side=tk.LEFT, padx=5)
        text.bind('<Double-Button-1>', lambda event, w=text: app.set_current_field(w))
        app.teil1_texts.append(text)

    # Thiết lập thứ tự focus: Überschriften trước, Texts sau
    app.teil1_focus = []
    app.teil1_focus.extend(app.teil1_overschriften)  # Thêm Überschriften đầu tiên
    app.teil1_focus.extend(app.teil1_texts)  # Thêm Texts sau
    if app.teil1_focus:
        app.set_current_field(app.teil1_focus[0])  # Focus vào ô Überschriften đầu tiên (a)

def setup_leseverstehen_teil2(app):
    main_frame = tk.Frame(app.leseverstehen_teil2)
    main_frame.pack(pady=10, fill="both", expand=True)

    # Đề đọc
    content_frame = tk.Frame(main_frame)
    content_frame.pack(fill="x", pady=5)
    tk.Label(content_frame, text="Đoạn văn chính:").pack()
    app.teil2_content = tk.Text(content_frame, height=5, width=90, highlightthickness=0)
    app.teil2_content.pack(pady=5)
    app.teil2_content.bind('<Double-Button-1>', lambda event: app.set_current_field(app.teil2_content))
    app.teil2_focus.append(app.teil2_content)

    # Questions
    app.teil2_questions = []
    app.teil2_options = []
    question_frame = tk.Frame(main_frame)
    question_frame.pack(fill="x")
    for i in range(5):
        frame = tk.Frame(question_frame)
        frame.pack(side=tk.LEFT, padx=10)
        tk.Label(frame, text=f"Câu {6+i}:").pack()
        question = tk.Entry(frame, width=30, highlightthickness=0)
        question.pack(pady=2)
        question.bind('<Double-Button-1>', lambda event, w=question: app.set_current_field(w))
        app.teil2_questions.append(question)
        app.teil2_focus.append(question)
        tk.Label(frame, text="Lựa chọn (a, b, c):").pack()
        options = []
        for j in range(3):
            opt_frame = tk.Frame(frame)
            opt_frame.pack(fill="x", pady=2)
            tk.Label(opt_frame, text=f"{chr(97+j)}):").pack(side=tk.LEFT)
            opt = tk.Entry(opt_frame, width=30, highlightthickness=0)
            opt.pack(side=tk.LEFT, padx=5)
            opt.bind('<Double-Button-1>', lambda event, w=opt: app.set_current_field(w))
            options.append(opt)
            app.teil2_focus.append(opt)
        app.teil2_options.append(options)

def setup_leseverstehen_teil3(app):
    main_frame = tk.Frame(app.leseverstehen_teil3)
    main_frame.pack(pady=10, fill="both", expand=True)

    # Situations
    situation_frame = tk.Frame(main_frame)
    situation_frame.pack(side=tk.LEFT, padx=10)
    tk.Label(situation_frame, text="10 tình huống (11-20):").pack()
    app.teil3_situations = []
    for i in range(10):
        frame = tk.Frame(situation_frame)
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=f"Tình huống {11+i}:").pack(side=tk.LEFT)
        situation = tk.Entry(frame, width=30, highlightthickness=0)
        situation.pack(side=tk.LEFT, padx=5)
        situation.bind('<Double-Button-1>', lambda event, w=situation: app.set_current_field(w))
        app.teil3_situations.append(situation)
        app.teil3_focus.append(situation)

    # Image upload
    image_frame = tk.Frame(main_frame)
    image_frame.pack(side=tk.LEFT, padx=10)
    tk.Label(image_frame, text="Hình ảnh Anzeigen (a-l):").pack()
    app.teil3_image_entry = tk.Entry(image_frame, textvariable=app.teil3_image_path, width=30, state="readonly", highlightthickness=0)
    app.teil3_image_entry.pack(pady=5)
    # Không bind double-click cho ô readonly
    tk.Button(image_frame, text="Chọn hình ảnh", command=lambda: upload_image_teil3(app)).pack(pady=5)
    app.teil3_focus.append(app.teil3_image_entry)

def setup_sprachbausteine_teil1(app):
    main_frame = tk.Frame(app.sprachbausteine_teil1)
    main_frame.pack(pady=10, fill="both", expand=True)

    # Đề đọc
    content_frame = tk.Frame(main_frame)
    content_frame.pack(fill="x", pady=5)
    tk.Label(content_frame, text="Đoạn văn chính:").pack()
    app.teil1_sprach_content = tk.Text(content_frame, height=5, width=90, highlightthickness=0)
    app.teil1_sprach_content.pack(pady=5)
    app.teil1_sprach_content.bind('<Double-Button-1>', lambda event: app.set_current_field(app.teil1_sprach_content))
    app.sprach1_focus.append(app.teil1_sprach_content)

    # Questions (không hiển thị trong UI, chỉ giữ cho JSON)
    app.teil1_sprach_questions = [""] * 10
    logging.info("Removed question fields from UI in Sprachbausteine Teil 1")

    # Dòng 1: Câu 21-25
    row1_frame = tk.Frame(main_frame)
    row1_frame.pack(fill="x", pady=5)
    tk.Label(row1_frame, text="Câu 21-25:").pack()
    for i in range(5):
        frame = tk.Frame(row1_frame)
        frame.pack(side=tk.LEFT, padx=10)
        tk.Label(frame, text=f"Câu {21+i}:").pack()
        tk.Label(frame, text="Lựa chọn (a, b, c):").pack()
        options = []
        for j in range(3):
            opt_frame = tk.Frame(frame)
            opt_frame.pack(fill="x", pady=2)
            tk.Label(opt_frame, text=f"{chr(97+j)}):").pack(side=tk.LEFT)
            opt = tk.Entry(opt_frame, width=30, highlightthickness=0)
            opt.pack(side=tk.LEFT, padx=5)
            opt.bind('<Double-Button-1>', lambda event, w=opt: app.set_current_field(w))
            options.append(opt)
            app.sprach1_focus.append(opt)
        app.teil1_sprach_options.append(options)

    # Dòng 2: Câu 26-30
    row2_frame = tk.Frame(main_frame)
    row2_frame.pack(fill="x", pady=5)
    tk.Label(row2_frame, text="Câu 26-30:").pack()
    for i in range(5):
        frame = tk.Frame(row2_frame)
        frame.pack(side=tk.LEFT, padx=10)
        tk.Label(frame, text=f"Câu {26+i}:").pack()
        tk.Label(frame, text="Lựa chọn (a, b, c):").pack()
        options = []
        for j in range(3):
            opt_frame = tk.Frame(frame)
            opt_frame.pack(fill="x", pady=2)
            tk.Label(opt_frame, text=f"{chr(97+j)}):").pack(side=tk.LEFT)
            opt = tk.Entry(opt_frame, width=30, highlightthickness=0)
            opt.pack(side=tk.LEFT, padx=5)
            opt.bind('<Double-Button-1>', lambda event, w=opt: app.set_current_field(w))
            options.append(opt)
            app.sprach1_focus.append(opt)
        app.teil1_sprach_options.append(options)

def setup_sprachbausteine_teil2(app):
    main_frame = tk.Frame(app.sprachbausteine_teil2)
    main_frame.pack(pady=10, fill="both", expand=True)

    # Đề đọc
    content_frame = tk.Frame(main_frame)
    content_frame.pack(fill="x", pady=5)
    tk.Label(content_frame, text="Đoạn văn chính:").pack()
    app.teil2_sprach_content = tk.Text(content_frame, height=5, width=90, highlightthickness=0)
    app.teil2_sprach_content.pack(pady=5)
    app.teil2_sprach_content.bind('<Double-Button-1>', lambda event: app.set_current_field(app.teil2_sprach_content))
    app.sprach2_focus.append(app.teil2_sprach_content)

    # Questions (không hiển thị trong UI, chỉ giữ cho JSON)
    app.teil2_sprach_questions = [""] * 10
    logging.info("Removed question fields from UI in Sprachbausteine Teil 2")

    # Options
    options_frame = tk.Frame(main_frame)
    options_frame.pack(side=tk.LEFT, padx=10)
    tk.Label(options_frame, text="15 từ lựa chọn (a-o):").pack()
    app.teil2_sprach_options = []
    for i in range(15):
        frame = tk.Frame(options_frame)
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=f"{chr(97+i)}):").pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=30, highlightthickness=0)
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind('<Double-Button-1>', lambda event, w=entry: app.set_current_field(w))
        app.teil2_sprach_options.append(entry)
        app.sprach2_focus.append(entry)

def setup_answers_tab(app):
    main_frame = tk.Frame(app.answers_tab)
    main_frame.pack(pady=10, fill="both", expand=True)
    app.answer_entries = []
    for i in range(4):
        frame = tk.Frame(main_frame)
        frame.pack(side=tk.LEFT, padx=10)
        tk.Label(frame, text=f"Đáp án {i*10+1}-{(i+1)*10}:").pack()
        for j in range(10):
            entry_frame = tk.Frame(frame)
            entry_frame.pack(fill="x", pady=2)
            tk.Label(entry_frame, text=f"Câu {i*10+j+1}:").pack(side=tk.LEFT)
            entry = tk.Entry(entry_frame, width=10, highlightthickness=0)
            entry.pack(side=tk.LEFT, padx=5)
            entry.bind('<Double-Button-1>', lambda event, w=entry: app.set_current_field(w))
            app.answer_entries.append(entry)
            app.answers_focus.append(entry)