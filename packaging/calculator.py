# -*- coding: utf-8 -*-
"""基本计算器 + 进制窗口，对应原 Qt 项目 testcal。"""
import ast
import operator
import tkinter as tk
from tkinter import font as tkfont


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(expr):
    expr = expr.strip()
    if not expr:
        raise ValueError("empty")
    tree = ast.parse(expr, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ZeroDivisionError("div0")
            return OPS[type(node.op)](left, right)
        raise ValueError("unsupported")

    return _eval(tree)


def format_number(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, float):
        text = f"{value:.10g}"
        return text
    return str(value)


class CalculatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("基本计算器")
        self.root.resizable(False, False)
        self.root.configure(bg="#ececec")
        tkfont.nametofont("TkDefaultFont").configure(family="Microsoft YaHei UI", size=10)

        self.input_var = tk.StringVar(value="0")
        self.base_mode = "dec"  # dec / hex / bin

        self._build_main()
        self._build_base_window()

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def _btn_style(self, extra=None):
        style = {
            "font": ("Microsoft YaHei UI", 12),
            "bd": 1,
            "relief": "raised",
            "width": 6,
            "height": 2,
            "bg": "#f7f7f7",
            "activebackground": "#dcdcdc",
        }
        if extra:
            style.update(extra)
        return style

    def _build_main(self):
        frame = tk.Frame(self.root, bg="#ececec", padx=10, pady=10)
        frame.pack()

        entry = tk.Entry(
            frame,
            textvariable=self.input_var,
            font=("Consolas", 18),
            justify="right",
            bd=2,
            relief="sunken",
        )
        entry.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=2, pady=2, ipady=10)

        tk.Button(frame, text="CE", command=self.ce, **self._btn_style({"bg": "#ffd8a8"})).grid(
            row=0, column=3, sticky="nsew", padx=2, pady=2
        )
        tk.Button(frame, text="AC", command=self.ac, **self._btn_style({"bg": "#ffb4b4"})).grid(
            row=0, column=4, sticky="nsew", padx=2, pady=2
        )

        layout = [
            ("1", 1, 0), ("2", 1, 1), ("3", 1, 2), ("+", 1, 3), ("-", 1, 4),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3), ("/", 2, 4),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("=", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("(", 4, 2), (")", 4, 3),
        ]
        for text, r, c in layout:
            cmd = self.equals if text == "=" else (lambda t=text: self.append(t))
            extra = {"bg": "#cde4ff"} if text in "+-*/=" else None
            colspan = 2 if text == "=" else 1
            tk.Button(frame, text=text, command=cmd, **self._btn_style(extra)).grid(
                row=r, column=c, columnspan=colspan, sticky="nsew", padx=2, pady=2
            )

        tk.Button(
            frame,
            text="bin/hex",
            command=self.show_base_window,
            **self._btn_style({"bg": "#d4edda", "width": 8}),
        ).grid(row=4, column=4, sticky="nsew", padx=2, pady=2)

        for i in range(5):
            frame.grid_columnconfigure(i, weight=1)
            frame.grid_rowconfigure(i, weight=1)

    def _build_base_window(self):
        self.base_win = tk.Toplevel(self.root)
        self.base_win.title("进制")
        self.base_win.resizable(False, False)
        self.base_win.configure(bg="#ececec")
        self.base_win.withdraw()
        self.base_win.protocol("WM_DELETE_WINDOW", self.show_main)

        frame = tk.Frame(self.base_win, bg="#ececec", padx=10, pady=10)
        frame.pack()

        self.base_input = tk.StringVar(value="0")
        tk.Entry(
            frame,
            textvariable=self.base_input,
            font=("Consolas", 18),
            justify="right",
            bd=2,
            relief="sunken",
        ).grid(row=0, column=0, columnspan=4, sticky="nsew", padx=2, pady=2, ipady=10)

        tk.Button(frame, text="AC", command=self.base_ac, **self._btn_style({"bg": "#ffb4b4"})).grid(
            row=0, column=4, sticky="nsew", padx=2, pady=2
        )
        tk.Button(frame, text="CE", command=self.base_ce, **self._btn_style({"bg": "#ffd8a8"})).grid(
            row=0, column=5, sticky="nsew", padx=2, pady=2
        )

        keys = [
            ("1", 1, 0), ("2", 1, 1), ("3", 1, 2), ("+", 1, 3), ("-", 1, 4), ("A", 1, 5),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3), ("/", 2, 4), ("B", 2, 5),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("=", 3, 3), ("C", 3, 4), ("D", 3, 5),
            ("0", 4, 0), ("bin", 4, 1), ("hex", 4, 2), ("切换", 4, 3), ("E", 4, 4), ("F", 4, 5),
        ]
        for text, r, c in keys:
            if text == "=":
                cmd = self.base_equals
                extra = {"bg": "#cde4ff"}
            elif text == "bin":
                cmd = lambda: self.set_base("bin")
                extra = {"bg": "#fff3cd"}
            elif text == "hex":
                cmd = lambda: self.set_base("hex")
                extra = {"bg": "#fff3cd"}
            elif text == "切换":
                cmd = self.show_main
                extra = {"bg": "#d4edda"}
            else:
                cmd = lambda t=text: self.base_append(t)
                extra = {"bg": "#cde4ff"} if text in "+-*/" else None
            tk.Button(frame, text=text, command=cmd, **self._btn_style(extra)).grid(
                row=r, column=c, sticky="nsew", padx=2, pady=2
            )

        self.mode_label = tk.Label(
            frame, text="当前：十进制", bg="#ececec", font=("Microsoft YaHei UI", 10)
        )
        self.mode_label.grid(row=5, column=0, columnspan=6, pady=(8, 0))

    def append(self, ch):
        current = self.input_var.get()
        if current in ("0", "syntax error") or current.endswith("syntax error"):
            self.input_var.set(ch)
        elif "=" in current:
            self.input_var.set(ch)
        else:
            self.input_var.set(current + ch)

    def ce(self):
        current = self.input_var.get()
        if len(current) <= 1:
            self.input_var.set("0")
        else:
            self.input_var.set(current[:-1])

    def ac(self):
        self.input_var.set("0")

    def equals(self):
        expr = self.input_var.get().split("=")[0]
        try:
            value = safe_eval(expr)
            self.input_var.set(expr + "=" + format_number(value))
        except Exception:
            self.input_var.set(expr + "=syntax error")

    def show_base_window(self):
        self.base_input.set(self.input_var.get().split("=")[0] or "0")
        self.root.withdraw()
        self.base_win.deiconify()
        self.base_win.lift()

    def show_main(self):
        self.input_var.set(self.base_input.get().split("=")[0] or "0")
        self.base_win.withdraw()
        self.root.deiconify()
        self.root.lift()

    def base_append(self, ch):
        current = self.base_input.get()
        if current in ("0",) or "syntax error" in current or "=" in current:
            self.base_input.set(ch)
        else:
            self.base_input.set(current + ch)

    def base_ce(self):
        current = self.base_input.get()
        self.base_input.set("0" if len(current) <= 1 else current[:-1])

    def base_ac(self):
        self.base_input.set("0")

    def set_base(self, mode):
        self.base_mode = mode
        names = {"dec": "十进制", "hex": "十六进制", "bin": "二进制"}
        self.mode_label.config(text="当前：" + names[mode])
        text = self.base_input.get().split("=")[0]
        try:
            if mode == "hex":
                value = int(str(safe_eval(self._to_decimal_expr(text))))
                self.base_input.set(format(value, "X"))
            elif mode == "bin":
                value = int(str(safe_eval(self._to_decimal_expr(text))))
                self.base_input.set(format(value, "b"))
        except Exception:
            pass

    def _to_decimal_expr(self, text):
        if self.base_mode == "hex":
            return self._rewrite_literals(text, 16)
        if self.base_mode == "bin":
            return self._rewrite_literals(text, 2)
        return text

    def _rewrite_literals(self, text, base):
        out = []
        i = 0
        digits = "0123456789ABCDEF"[:base]
        while i < len(text):
            ch = text[i].upper()
            if ch in digits:
                j = i
                token = ""
                while j < len(text) and text[j].upper() in digits:
                    token += text[j]
                    j += 1
                out.append(str(int(token, base)))
                i = j
            else:
                out.append(text[i])
                i += 1
        return "".join(out)

    def base_equals(self):
        expr = self.base_input.get().split("=")[0]
        try:
            value = safe_eval(self._to_decimal_expr(expr))
            if self.base_mode == "hex":
                shown = format(int(value), "X")
            elif self.base_mode == "bin":
                shown = format(int(value), "b")
            else:
                shown = format_number(value)
            self.base_input.set(expr + "=" + shown)
        except Exception:
            self.base_input.set(expr + "=syntax error")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CalculatorApp().run()
