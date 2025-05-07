import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import fitz  # PyMuPDF

from nltk_setup import setup_nltk
from text_loader import load_text, extract_text_from_pdf
from frequency_classifier import classify_filtered_words
from save_to_csv import save_each_level_to_csv

class WordbookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordbook Generator")
        self.root.geometry("600x600")

        self.file_path = None
        self.save_folder = None
        self.thumbnail = None

        # 📂 파일/저장/생성 버튼 영역 (한 줄로 배치)
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        self.file_btn = tk.Button(control_frame, text="📂 파일 선택", command=self.select_file, width=20)
        self.file_btn.pack(side="left", padx=10)

        self.save_btn = tk.Button(control_frame, text="💾 저장 폴더 선택", command=self.select_save_folder, width=20)
        self.save_btn.pack(side="left", padx=10)

        self.create_btn = tk.Button(control_frame, text="🚀 생성하기", font=("Arial", 11, "bold"), command=self.generate_wordbook, width=15)
        self.create_btn.pack(side="left", padx=10)

        # 저장 위치 라벨
        self.save_label = tk.Label(root, text="저장 위치: (선택되지 않음)", fg="gray")
        self.save_label.pack()

        # ⏱ 상태 라벨 (진행 시간 등)
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack()

        # 🔍 미리보기 영역
        self.preview_area = tk.Frame(root)
        self.preview_area.pack(pady=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text or PDF", "*.txt *.pdf")])
        if not file_path:
            return

        self.file_path = file_path
        ext = os.path.splitext(file_path)[1].lower()

        for widget in self.preview_area.winfo_children():
            widget.destroy()

        try:
            if ext == ".pdf":
                self.show_pdf_preview(file_path)
            elif ext == ".txt":
                self.show_txt_preview(file_path)
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
        doc = fitz.open(file_path)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image.thumbnail((400, 400))

        self.thumbnail = ImageTk.PhotoImage(image)
        label = tk.Label(self.preview_area, image=self.thumbnail)
        label.pack()

    def show_txt_preview(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        preview_text = ''.join(lines[:10])

        txt = scrolledtext.ScrolledText(self.preview_area, width=90, height=20)
        txt.insert(tk.END, preview_text)
        txt.config(state="disabled")
        txt.pack()

    def generate_wordbook(self):
        if not self.file_path:
            messagebox.showwarning("파일 없음", "먼저 파일을 선택하세요.")
            return
        if not self.save_folder:
            messagebox.showwarning("저장 위치 없음", "저장할 폴더를 선택하세요.")
            return

        try:
            self.status_label.config(text="⏳ 생성 중입니다...", fg="blue")
            self.root.update()  # UI 즉시 반영

            start_time = time.time()

            setup_nltk()

            ext = os.path.splitext(self.file_path)[1].lower()
            if ext == ".pdf":
                text = extract_text_from_pdf(self.file_path)
            else:
                text = load_text(self.file_path)

            level_buckets = classify_filtered_words(text)
            save_each_level_to_csv(level_buckets, self.save_folder)

            elapsed = time.time() - start_time
            self.status_label.config(text=f"✅ 완료! 생성 시간: {elapsed:.2f}초", fg="green")
            messagebox.showinfo("완료", "✅ 단어장이 성공적으로 생성되었습니다!")

        except Exception as e:
            self.status_label.config(text="❌ 오류 발생", fg="red")
            messagebox.showerror("오류 발생", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = WordbookApp(root)
    root.mainloop()
