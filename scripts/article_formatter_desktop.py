#!/usr/bin/env python3
"""Simple desktop article auto-layout tool with 10 built-in styles."""

import re
import textwrap
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


STYLE_PRESETS = {
    "简洁新闻": {
        "title_prefix": "【新闻速览】",
        "paragraph_indent": "",
        "line_width": 36,
        "spacing": "\n\n",
        "bullet": "• ",
        "uppercase_title": False,
    },
    "学术论文": {
        "title_prefix": "摘要：",
        "paragraph_indent": "    ",
        "line_width": 40,
        "spacing": "\n\n",
        "bullet": "- ",
        "uppercase_title": False,
    },
    "小红书笔记": {
        "title_prefix": "✨ ",
        "paragraph_indent": "",
        "line_width": 30,
        "spacing": "\n\n",
        "bullet": "👉 ",
        "uppercase_title": False,
    },
    "公众号长文": {
        "title_prefix": "",
        "paragraph_indent": "    ",
        "line_width": 34,
        "spacing": "\n\n",
        "bullet": "▸ ",
        "uppercase_title": False,
    },
    "商务报告": {
        "title_prefix": "[REPORT] ",
        "paragraph_indent": "",
        "line_width": 38,
        "spacing": "\n\n",
        "bullet": "- ",
        "uppercase_title": True,
    },
    "极简卡片": {
        "title_prefix": "# ",
        "paragraph_indent": "",
        "line_width": 28,
        "spacing": "\n",
        "bullet": "• ",
        "uppercase_title": False,
    },
    "故事叙事": {
        "title_prefix": "《",
        "title_suffix": "》",
        "paragraph_indent": "  ",
        "line_width": 32,
        "spacing": "\n\n",
        "bullet": "- ",
        "uppercase_title": False,
    },
    "教程步骤": {
        "title_prefix": "[教程] ",
        "paragraph_indent": "",
        "line_width": 36,
        "spacing": "\n\n",
        "bullet": "Step ",
        "uppercase_title": False,
    },
    "营销文案": {
        "title_prefix": "🔥 ",
        "paragraph_indent": "",
        "line_width": 30,
        "spacing": "\n\n",
        "bullet": "✅ ",
        "uppercase_title": False,
    },
    "技术文档": {
        "title_prefix": "[DOC] ",
        "paragraph_indent": "",
        "line_width": 42,
        "spacing": "\n\n",
        "bullet": "- ",
        "uppercase_title": False,
    },
}


def split_paragraphs(raw_text: str):
    return [p.strip() for p in re.split(r"\n\s*\n", raw_text) if p.strip()]


def format_article(title: str, content: str, style_name: str):
    style = STYLE_PRESETS[style_name]
    title_text = title.strip() or "未命名标题"

    if style.get("uppercase_title"):
        title_text = title_text.upper()

    title_prefix = style.get("title_prefix", "")
    title_suffix = style.get("title_suffix", "")
    final_title = f"{title_prefix}{title_text}{title_suffix}"

    wrapped_paragraphs = []
    for idx, paragraph in enumerate(split_paragraphs(content), start=1):
        if paragraph.startswith(("- ", "* ", "• ")):
            body = paragraph[2:].strip()
            bullet = style["bullet"]
            if bullet == "Step ":
                bullet = f"Step {idx}: "
            wrapped = textwrap.fill(
                body,
                width=style["line_width"],
                initial_indent=bullet,
                subsequent_indent=" " * len(bullet),
            )
        else:
            wrapped = textwrap.fill(
                paragraph,
                width=style["line_width"],
                initial_indent=style["paragraph_indent"],
                subsequent_indent=style["paragraph_indent"],
            )
        wrapped_paragraphs.append(wrapped)

    return final_title + "\n\n" + style["spacing"].join(wrapped_paragraphs)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("自动排版文章工具（10种风格）")
        self.root.geometry("1100x700")

        top = ttk.Frame(root)
        top.pack(fill="x", padx=10, pady=8)

        ttk.Label(top, text="标题：").pack(side="left")
        self.title_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.title_var, width=45).pack(side="left", padx=6)

        ttk.Label(top, text="风格：").pack(side="left", padx=(12, 0))
        self.style_var = tk.StringVar(value=list(STYLE_PRESETS.keys())[0])
        ttk.Combobox(top, textvariable=self.style_var, values=list(STYLE_PRESETS.keys()), state="readonly", width=20).pack(side="left", padx=6)

        ttk.Button(top, text="自动排版", command=self.on_format).pack(side="left", padx=10)
        ttk.Button(top, text="保存结果", command=self.on_save).pack(side="left")

        main = ttk.Panedwindow(root, orient="horizontal")
        main.pack(fill="both", expand=True, padx=10, pady=8)

        left = ttk.Labelframe(main, text="原文")
        right = ttk.Labelframe(main, text="排版结果")
        main.add(left, weight=1)
        main.add(right, weight=1)

        self.input_text = tk.Text(left, wrap="word", font=("Microsoft YaHei", 12))
        self.input_text.pack(fill="both", expand=True, padx=8, pady=8)

        self.output_text = tk.Text(right, wrap="word", font=("Microsoft YaHei", 12))
        self.output_text.pack(fill="both", expand=True, padx=8, pady=8)

    def on_format(self):
        content = self.input_text.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("提示", "请先输入文章内容。")
            return

        result = format_article(self.title_var.get(), content, self.style_var.get())
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)

    def on_save(self):
        text = self.output_text.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("提示", "当前没有可保存的排版结果。")
            return

        filename = filedialog.asksaveasfilename(
            title="保存排版结果",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("Markdown", "*.md")],
        )
        if not filename:
            return

        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("完成", f"已保存到：{filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
