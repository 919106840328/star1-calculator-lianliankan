# -*- coding: utf-8 -*-
"""连连看：使用 LLK/Image 中的宝可梦图片，规则为最多两次拐弯可消除。"""
import os
import random
import sys
from collections import deque

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance


def resource_path(*parts):
    if getattr(sys, "frozen", False):
        root = sys._MEIPASS
    else:
        root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root, *parts)


def image_dir():
    bundled = resource_path("Image")
    if os.path.isdir(bundled):
        return bundled
    return os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "LLK", "Image")
    )


class LianLianKan:
    TILE_SIZE = 56
    PAD = 10

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("神奇宝贝连连看")
        self.root.resizable(False, False)

        self.level = "medium"
        self.rows = 8
        self.cols = 10
        self.icon_count = 12
        self.time_limit = 180
        self.remaining = self.time_limit
        self.board = []
        self.selected = None
        self.hint_pair = None
        self.running = False
        self.photos = []
        self.bg_photo = None
        self.tile_empty = None
        self.canvas = None
        self.tile_files = []
        self._tile_cache = {}

        self._load_tile_files()
        self._build_ui()
        self.new_game()
        self.root.after(1000, self._tick)

    def _load_tile_files(self):
        folder = image_dir()
        files = []
        for i in range(1, 34):
            path = os.path.join(folder, "%d.png" % i)
            if os.path.isfile(path):
                files.append(path)
        extra = [
            "pipi.png",
            "wanli.png",
            "wenxiangkedou.png",
            "xaiohaishi.png",
            "xiaociguai.png",
            "xiaohuolong.png",
            "xiaohuoma.png",
            "xiaolada.png",
            "xiaoquanshi.png",
            "zoulucao.png",
        ]
        for name in extra:
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                files.append(path)
        if not files:
            raise FileNotFoundError("未找到连连看图片：%s" % folder)
        self.tile_files = files
        self.bg_files = [
            os.path.join(folder, "backgroud_%d.jpg" % i)
            for i in range(1, 6)
            if os.path.isfile(os.path.join(folder, "backgroud_%d.jpg" % i))
        ]

    def _make_tile_image(self, path, size):
        key = (path, size)
        if key in self._tile_cache:
            return self._tile_cache[key]
        src = Image.open(path).convert("RGBA")
        src.thumbnail((size - 6, size - 6), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), (255, 255, 255, 230))
        x = (size - src.width) // 2
        y = (size - src.height) // 2
        canvas.paste(src, (x, y), src)
        photo = ImageTk.PhotoImage(canvas)
        self._tile_cache[key] = photo
        return photo

    def _make_background(self, width, height):
        if not self.bg_files:
            img = Image.new("RGB", (width, height), (205, 249, 255))
            return ImageTk.PhotoImage(img)
        src = Image.open(random.choice(self.bg_files)).convert("RGB")
        src = src.resize((width, height), Image.Resampling.LANCZOS)
        src = ImageEnhance.Brightness(src).enhance(0.72)
        return ImageTk.PhotoImage(src)

    def _build_ui(self):
        self.top = tk.Frame(self.root, bg="#1e3a5f", padx=10, pady=8)
        self.top.pack(fill="x")

        tk.Label(
            self.top, text="时间：", bg="#1e3a5f", fg="white", font=("Microsoft YaHei UI", 11)
        ).pack(side="left")
        self.time_var = tk.DoubleVar(value=100)
        tk.Scale(
            self.top,
            from_=0,
            to=100,
            orient="horizontal",
            showvalue=False,
            length=360,
            variable=self.time_var,
            state="disabled",
            troughcolor="#74b9ff",
            bg="#1e3a5f",
            highlightthickness=0,
        ).pack(side="left", padx=6)

        self.time_label = tk.Label(
            self.top, text="180s", bg="#1e3a5f", fg="#ffeaa7", font=("Consolas", 12), width=6
        )
        self.time_label.pack(side="left")

        btn_style = {
            "font": ("Microsoft YaHei UI", 10),
            "bg": "#00b894",
            "fg": "white",
            "activebackground": "#55efc4",
            "bd": 0,
            "width": 8,
        }
        tk.Button(self.top, text="提示", command=self.show_hint, **btn_style).pack(side="left", padx=4)
        tk.Button(self.top, text="自动", command=self.auto_play, **btn_style).pack(side="left", padx=4)
        tk.Button(self.top, text="重排", command=self.shuffle, **btn_style).pack(side="left", padx=4)

        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="简单", command=lambda: self.set_level("basic"))
        game_menu.add_command(label="中等", command=lambda: self.set_level("medium"))
        game_menu.add_command(label="困难", command=lambda: self.set_level("hard"))
        game_menu.add_separator()
        game_menu.add_command(label="新游戏", command=self.new_game)
        menubar.add_cascade(label="游戏", menu=game_menu)
        self.root.config(menu=menubar)

        self.canvas = tk.Canvas(self.root, highlightthickness=0, cursor="hand2")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.status = tk.Label(
            self.root,
            text="点击两个相同的宝可梦，连线不超过两次拐弯即可消除",
            bg="#1e3a5f",
            fg="white",
            font=("Microsoft YaHei UI", 10),
        )
        self.status.pack(fill="x")

    def set_level(self, level):
        self.level = level
        self.new_game()

    def _level_conf(self):
        max_icons = max(2, len(self.tile_files))
        if self.level == "basic":
            return 6, 8, min(8, max_icons), 150
        if self.level == "hard":
            return 10, 14, min(28, max_icons), 240
        return 8, 10, min(16, max_icons), 180

    def new_game(self):
        self.rows, self.cols, self.icon_count, self.time_limit = self._level_conf()
        self.TILE_SIZE = 44 if self.cols >= 14 else 56
        self.remaining = self.time_limit
        self.selected = None
        self.hint_pair = None
        self.running = True
        self._prepare_images()
        self._create_map()
        self._resize_canvas()
        self._paint()
        names = {"basic": "简单", "medium": "中等", "hard": "困难"}
        self.status.config(text="难度：%s    剩余：%d" % (names[self.level], self._left_count()))

    def _prepare_images(self):
        size = self.TILE_SIZE
        self.photos = [None]
        for path in self.tile_files:
            self.photos.append(self._make_tile_image(path, size))
        empty = Image.new("RGBA", (size, size), (255, 255, 255, 40))
        self.tile_empty = ImageTk.PhotoImage(empty)

    def _resize_canvas(self):
        w = self.cols * self.TILE_SIZE + self.PAD * 2
        h = self.rows * self.TILE_SIZE + self.PAD * 2
        self.canvas.config(width=w, height=h)
        self.bg_photo = self._make_background(w, h)

    def _create_map(self):
        total = self.rows * self.cols
        if total % 2:
            total -= 1
        values = []
        icon = 1
        while len(values) < total:
            values.extend([icon, icon])
            icon = icon + 1 if icon < self.icon_count else 1
        values = values[:total]
        random.shuffle(values)
        self.board = [[0 for _ in range(self.cols + 2)] for _ in range(self.rows + 2)]
        k = 0
        for r in range(1, self.rows + 1):
            for c in range(1, self.cols + 1):
                if k < len(values):
                    self.board[r][c] = values[k]
                    k += 1
        if self._is_dead():
            self._create_map()

    def _cell_xy(self, r, c):
        x = self.PAD + (c - 1) * self.TILE_SIZE
        y = self.PAD + (r - 1) * self.TILE_SIZE
        return x, y

    def _paint(self, flash_path=None):
        self.canvas.delete("all")
        w = int(self.canvas["width"])
        h = int(self.canvas["height"])
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        for r in range(1, self.rows + 1):
            for c in range(1, self.cols + 1):
                x, y = self._cell_xy(r, c)
                value = self.board[r][c]
                if value == 0:
                    continue
                img = self.photos[value] if value < len(self.photos) else None
                if img:
                    self.canvas.create_image(x, y, image=img, anchor="nw")
                selected = self.selected == (r, c)
                hinted = self.hint_pair and (r, c) in self.hint_pair
                if selected or hinted:
                    color = "#ffeaa7" if selected else "#81ecec"
                    self.canvas.create_rectangle(
                        x + 1,
                        y + 1,
                        x + self.TILE_SIZE - 2,
                        y + self.TILE_SIZE - 2,
                        outline=color,
                        width=3,
                    )
        if flash_path and len(flash_path) >= 2:
            pts = []
            for r, c in flash_path:
                x, y = self._cell_xy(r, c)
                pts.extend([x + self.TILE_SIZE // 2, y + self.TILE_SIZE // 2])
            self.canvas.create_line(*pts, fill="#fdcb6e", width=4, capstyle="round", joinstyle="round")

    def on_canvas_click(self, event):
        c = (event.x - self.PAD) // self.TILE_SIZE + 1
        r = (event.y - self.PAD) // self.TILE_SIZE + 1
        if not (1 <= r <= self.rows and 1 <= c <= self.cols):
            return
        self.on_click(r, c)

    def on_click(self, r, c):
        if not self.running or self.board[r][c] == 0:
            return
        if self.selected is None:
            self.selected = (r, c)
            self.hint_pair = None
            self._paint()
            return
        if self.selected == (r, c):
            self.selected = None
            self._paint()
            return
        r1, c1 = self.selected
        if self.board[r1][c1] != self.board[r][c]:
            self.selected = (r, c)
            self._paint()
            return
        path = self._find_path(r1, c1, r, c)
        if path:
            self._paint(flash_path=path)
            self.board[r1][c1] = 0
            self.board[r][c] = 0
            self.selected = None
            self.hint_pair = None
            self.root.after(180, self._after_match)
        else:
            self.selected = (r, c)
            self._paint()
            self.status.config(text="这两块连不上，请再选")

    def _after_match(self):
        self._paint()
        left = self._left_count()
        self.status.config(text="消除成功！剩余：%d" % left)
        if left == 0:
            self.running = False
            messagebox.showinfo("胜利", "全部消除完成！")
        elif self._is_dead():
            self.shuffle()

    def _find_path(self, r1, c1, r2, c2):
        if (r1, c1) == (r2, c2):
            return None
        if self.board[r1][c1] == 0 or self.board[r2][c2] == 0:
            return None
        if self.board[r1][c1] != self.board[r2][c2]:
            return None

        rows = self.rows + 2
        cols = self.cols + 2
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        visited = [[[False] * 4 for _ in range(cols)] for _ in range(rows)]
        q = deque()
        for d in range(4):
            q.append((r1, c1, d, 0, [(r1, c1)]))

        while q:
            r, c, d, turns, path = q.popleft()
            dr, dc = dirs[d]
            nr, nc = r + dr, c + dc
            while 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) != (r2, c2) and self.board[nr][nc] != 0:
                    break
                if (nr, nc) == (r2, c2):
                    return path + [(nr, nc)]
                if not visited[nr][nc][d]:
                    visited[nr][nc][d] = True
                    if turns < 2:
                        for nd in range(4):
                            if nd != d:
                                q.append((nr, nc, nd, turns + 1, path + [(nr, nc)]))
                nr += dr
                nc += dc
        return None

    def _iter_tiles(self):
        for r in range(1, self.rows + 1):
            for c in range(1, self.cols + 1):
                if self.board[r][c]:
                    yield r, c

    def _left_count(self):
        return sum(1 for _ in self._iter_tiles())

    def _find_hint(self):
        tiles = list(self._iter_tiles())
        for i, (r1, c1) in enumerate(tiles):
            for r2, c2 in tiles[i + 1 :]:
                if self.board[r1][c1] == self.board[r2][c2] and self._find_path(r1, c1, r2, c2):
                    return (r1, c1), (r2, c2)
        return None

    def _is_dead(self):
        return self._left_count() > 0 and self._find_hint() is None

    def show_hint(self):
        pair = self._find_hint()
        if not pair:
            self.status.config(text="当前没有可消除的组合，试试重排")
            return
        self.hint_pair = pair
        self._paint()
        self.status.config(text="已高亮一对可消除的宝可梦")

    def shuffle(self):
        values = [self.board[r][c] for r, c in self._iter_tiles()]
        random.shuffle(values)
        k = 0
        for r in range(1, self.rows + 1):
            for c in range(1, self.cols + 1):
                if self.board[r][c]:
                    self.board[r][c] = values[k]
                    k += 1
        if self._is_dead() and values:
            self.shuffle()
            return
        self.selected = None
        self.hint_pair = None
        self._paint()
        self.status.config(text="已重排，剩余：%d" % self._left_count())

    def auto_play(self):
        if not self.running:
            return
        pair = self._find_hint()
        if not pair:
            if self._left_count() == 0:
                return
            self.shuffle()
            self.root.after(200, self.auto_play)
            return
        (r1, c1), (r2, c2) = pair
        self.board[r1][c1] = 0
        self.board[r2][c2] = 0
        self.selected = None
        self.hint_pair = None
        self._paint()
        if self._left_count() == 0:
            self.running = False
            messagebox.showinfo("胜利", "自动消除完成！")
            return
        self.root.after(180, self.auto_play)

    def _refresh_time(self):
        ratio = 0 if self.time_limit == 0 else 100.0 * self.remaining / self.time_limit
        self.time_var.set(max(0, ratio))
        self.time_label.config(text="%ds" % max(0, self.remaining))

    def _tick(self):
        if self.running:
            self.remaining -= 1
            self._refresh_time()
            if self.remaining <= 0:
                self.running = False
                messagebox.showwarning("时间到", "本局结束，再开一局吧。")
        self.root.after(1000, self._tick)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    LianLianKan().run()
