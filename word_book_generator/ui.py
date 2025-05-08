import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import fitz

from nltk_setup import setup_nltk
from text_loader import extract_text_from_pdf
from frequency_classifier import classify_filtered_words
from save_to_csv import save_each_level_to_excel


class WordbookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordbook Generator")
        self.root.geometry("550x650")

        self.file_path = None
        self.save_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.doc = None
        self.thumbnail = None
        self.start_page, self.end_page = None, None
        self.meaning_options = {
           "en": tk.BooleanVar(value=True),
           "ko": tk.BooleanVar(value=True)
        }
        self.level_options = {}

        # 📂 파일/저장 버튼 영역 (파일 선택 + 저장 위치 버튼 나란히)
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        self.file_btn = tk.Button(control_frame, text="📂 파일 선택", command=self.select_file, width=20)
        self.file_btn.pack(side="left", padx=10)

        self.save_btn = tk.Button(control_frame, text="💾 저장 폴더 선택", command=self.select_save_folder, width=20)
        self.save_btn.pack(side="left", padx=10)

        self.create_btn = tk.Button(control_frame, text="▶️ 생성하기", command=self.generate_wordbook, width=20)
        self.create_btn.pack(side="left", padx=10)

        # ⬇️ 저장 경로 라벨 (아래 단독 표시)
        self.save_label = tk.Label(root, text="저장 위치: (선택되지 않음)", fg="gray", anchor="w", wraplength=480)
        self.save_label.config(text=f"저장 위치: {self.save_folder}", fg="black")
        self.save_label.pack(fill="x", padx=20, pady=(0, 10))

        # ✅ 저장 항목 선택
        option_group = tk.LabelFrame(root, text="저장 항목 선택", padx=10, pady=5)
        option_group.pack(pady=8, fill="x", padx=15)

        # 의미 선택
        meaning_frame = tk.Frame(option_group)
        meaning_frame.pack(anchor="w", pady=3)

        tk.Label(meaning_frame, text="의미 :", width=6).pack(side="left")
        tk.Checkbutton(meaning_frame, text="영어", variable=self.meaning_options["en"]).pack(side="left", padx=5)
        tk.Checkbutton(meaning_frame, text="한글", variable=self.meaning_options["ko"]).pack(side="left", padx=5)

        # 난이도 선택
        level_frame = tk.Frame(option_group)
        level_frame.pack(anchor="w", pady=3)

        tk.Label(level_frame, text="난이도 :", width=6).pack(side="left")
        self.level_vars = {}
        for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'UD']:
            default = level in ['B2', 'C1', 'UD']
            self.level_options[level] = tk.BooleanVar(value=default)
            tk.Checkbutton(level_frame, text=level, variable=self.level_options[level]).pack(side="left", padx=5)

        # 🔢 페이지 선택 입력 영역
        page_input_frame = tk.LabelFrame(root, text="페이지 선택", padx=10, pady=5)
        page_input_frame.pack(pady=8, fill="x", padx=15)

        tk.Label(page_input_frame, text="Start Page:").pack(side="left", padx=5)
        self.start_entry = tk.Entry(page_input_frame, width=5)
        self.start_entry.pack(side="left")
        self.start_entry.bind("<FocusOut>", self.on_page_change)
        self.start_entry.bind("<Return>", self.on_page_change)

        tk.Label(page_input_frame, text="End Page:").pack(side="left", padx=5)
        self.end_entry = tk.Entry(page_input_frame, width=5)
        self.end_entry.pack(side="left")
        self.end_entry.bind("<FocusOut>", self.on_page_change)
        self.end_entry.bind("<Return>", self.on_page_change)

        self.page_info_label = tk.Label(page_input_frame, text="(페이지 없음)", fg="gray")
        self.page_info_label.pack(side="left", padx=5)

        # 🔄 미리보기 버튼
        self.preview_btn = tk.Button(page_input_frame, text="🔄 Preview", command=self.on_page_change, width=10)
        self.preview_btn.pack(side="left", padx=10)

        # 🔍 미리보기 영역
        self.preview_area = tk.Frame(root)
        self.preview_area.pack(pady=20)

        # ✅ 프로세스바 + 라벨을 한 줄로 넣을 프레임
        progress_frame = tk.Frame(root)
        progress_frame.pack(pady=5)

        # 프로세스바
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor="#e0e0e0",
                        background="#f97316",  # 진한 주황색
                        thickness=18)

        # 생성 시 적용
        self.progress = ttk.Progressbar(progress_frame,
                                        style="Custom.Horizontal.TProgressbar",
                                        orient="horizontal",
                                        mode="determinate",
                                        length=300)
        self.progress.pack(side="left")

        # 상태 표시 라벨
        self.progress_label = tk.Label(progress_frame, text="", fg="#f97316")
        self.progress_label.pack(side="left", padx=10)

        # 처음엔 모두 숨김
        progress_frame.pack_forget()
        self.progress_frame = progress_frame  # 나중에 pack()/forget() 제어용

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if not file_path:
            return

        self.file_path = file_path
        ext = os.path.splitext(file_path)[1].lower()

        for widget in self.preview_area.winfo_children():
            widget.destroy()

        try:
            if ext == ".pdf":
                self.show_pdf_preview(file_path)
            else:
                messagebox.showerror("오류", "지원되지 않는 파일 형식입니다.")
        except Exception as e:
            messagebox.showerror("미리보기 오류", str(e))

    def select_save_folder(self):
        folder = filedialog.askdirectory(title="📁 저장할 폴더 선택")
        if folder:
            self.save_folder = folder
            self.save_label.config(text=f"저장 위치: {folder}", fg="black")
        else:
            self.save_folder = None
            self.save_label.config(text="저장 위치: (선택되지 않음)", fg="gray")

    def show_pdf_preview(self, file_path):
        self.doc = fitz.open(file_path)
        self.start_page = 0
        self.end_page = len(self.doc) - 1

        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.start_entry.insert(0, str(self.start_page))
        self.end_entry.insert(0, str(self.end_page))

        # ✅ 페이지 범위 안내 라벨 업데이트
        self.page_info_label.config(text=f"(0 ~ {self.end_page})", fg="gray")

        self.update_preview()

    def update_preview(self):
        for widget in self.preview_area.winfo_children():
            widget.destroy()

        # Start page thumbnail
        start_pix = self.doc[self.start_page].get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        start_img = Image.frombytes("RGB", [start_pix.width, start_pix.height], start_pix.samples)
        start_img.thumbnail((300, 300))
        self.start_thumbnail = ImageTk.PhotoImage(start_img)

        # End page thumbnail
        end_pix = self.doc[self.end_page].get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        end_img = Image.frombytes("RGB", [end_pix.width, end_pix.height], end_pix.samples)
        end_img.thumbnail((300, 300))
        self.end_thumbnail = ImageTk.PhotoImage(end_img)

        # Display thumbnails
        tk.Label(self.preview_area, image=self.start_thumbnail).pack(side="left", padx=10)
        tk.Label(self.preview_area, image=self.end_thumbnail).pack(side="right", padx=10)

    def on_page_change(self, even=None):
        if not self.doc:
            return
        try:
            s = int(self.start_entry.get())
            e = int(self.end_entry.get())
            max_page = len(self.doc) - 1
            s = max(0, min(s, max_page))
            e = max(0, min(e, max_page))
            if s <= e:
                self.start_page = s
                self.end_page = e
                self.update_preview()
        except ValueError:
            pass  # 숫자 아닌 입력은 무시

    def generate_wordbook(self):
        if not self.file_path:
            messagebox.showwarning("파일 없음", "먼저 파일을 선택하세요.")
            return
        if not self.save_folder:
            messagebox.showwarning("저장 위치 없음", "저장할 폴더를 선택하세요.")
            return

        # 🧵 백그라운드 스레드에서 워드북 생성 실행
        threading.Thread(target=self._run_generation, daemon=True).start()

    def _run_generation(self):
        try:
            self.progress["value"] = 0
            self.progress["maximum"] = 100  # 퍼센트 기반 설정
            self.progress_frame.pack(pady=5)  # 진행률 프레임 표시
            self.progress_label.config(text="[번역 중] 0 / ? 단어 번역됨")
            self.root.update()

            start_time = time.time()

            setup_nltk()
            text = extract_text_from_pdf(self.file_path, self.start_page, self.end_page)
            include_english = self.meaning_options["en"].get()
            include_korean = self.meaning_options["ko"].get()
            selected_levels = [lvl for lvl, var in self.level_options.items() if var.get()]

            level_buckets = classify_filtered_words(
                text,
                include_english=include_english,
                include_korean=include_korean,
                levels=selected_levels,
                progress_bar=self.progress,
                progress_label=self.progress_label
            )

            save_each_level_to_excel(
                level_buckets,
                include_english=include_english,
                include_korean=include_korean,
                levels = selected_levels,
                save_folder = self.save_folder
            )

            elapsed = time.time() - start_time

            self.progress.stop()
            self.progress_frame.pack_forget()

            messagebox.showinfo("완료", f"✅ 단어장이 성공적으로 생성되었습니다!\n⏱ 생성 시간: {elapsed:.2f}초")

        except Exception as e:
            self.progress.stop()
            self.progress_frame.pack_forget()
            messagebox.showerror("오류 발생", str(e))