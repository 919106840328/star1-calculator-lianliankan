# 计算器 + 神奇宝贝连连看

课程作业工程（原 Qt 源码）以及可直接运行的 Python 版本。

## 可执行文件

本地打包后的程序在 `exe/`（不纳入本仓库）：

- `Calculator.exe`：计算器
- `LianLianKan.exe`：连连看（使用 `LLK/Image` 中的宝可梦图片）

也可以在 `packaging/` 下用 Python 运行：

```bash
python packaging/calculator.py
python packaging/lianliankan.py
```

## 目录说明

- `testcal/`、根目录的 `calculator.*`：原 Qt 计算器
- `LLK/`：原 Qt 连连看工程（`game.h` 有完整设计，实现不完整）和宝可梦图片
- `team2/`、`QT_Team/`：另一套连连看逻辑 / 界面草稿
- `packaging/`：后来补齐的可运行版本（计算器、连连看）和打包脚本
