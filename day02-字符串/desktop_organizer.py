"""
桌面整理小工具
一键把你乱糟糟的桌面归归类
用法: python desktop_organizer.py
"""

import os
import shutil
from pathlib import Path

# ====== 配置 ======
DESKTOP = Path.home() / "Desktop"  # 桌面路径

# 分类规则：文件夹名 → 匹配关键词列表
RULES = {
    "开发工具": ["Visual Studio", "VS Code", "IDLE", "Python", "HexHub", "OCS", "JetBrains"],
    "AI工具":   ["Gemini", "千问", "豆包", "Trae", "Claude", "OpenAI", "ChatGPT"],
    "娱乐":     ["抖音", "虎牙", "汽水音乐", "迅雷", "bilibili", "音乐"],
    "网络工具": ["加速器", "WiFi", "SSR", "VPN", "代理", "Clash"],
    "浏览器":   ["Chrome", "Edge", "Firefox", "浏览器"],
    "学习作业": ["作业", "期末", "考试", "实验", "报告", "论文", "python", "大模型"],
    "截图工具": ["Snipaste", "截图", "录屏"],
}

# 文件扩展名分类规则：文件夹名 → 扩展名列表
EXT_RULES = {
    "图片":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "文档":    [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"],
    "压缩包":  [".zip", ".rar", ".7z", ".tar", ".gz"],
    "安装包":  [".exe", ".msi", ".dmg", ".appimage", ".deb"],
}

def get_category(name: str) -> str:
    """根据文件名判断它属于哪个分类"""
    name_lower = name.lower()  # 转小写，方便匹配

    # 先按关键词分类（针对快捷方式/文件夹名）
    for folder, keywords in RULES.items():
        for kw in keywords:
            if kw.lower() in name_lower:
                return folder

    # 再按扩展名分类（针对文件）
    ext = Path(name).suffix.lower()
    for folder, exts in EXT_RULES.items():
        if ext in exts:
            return folder

    return "其他"  # 啥都匹配不上就放这里


def organize_desktop():
    """主函数：整理桌面"""
    print("=" * 40)
    print("🦀 桌面整理开始")
    print("=" * 40)

    # 遍历桌面上所有东西
    for item in DESKTOP.iterdir():
        # ⛔ 跳过这个脚本自己（如果在桌面上）
        if item.name == "desktop_organizer.py":
            continue
        # ⛔ 跳过已经是分类文件夹的（防止把文件夹再往里搬）
        if item.name in RULES or item.name in EXT_RULES or item.name == "其他":
            continue

        # 判断这个文件/文件夹属于哪一类
        category = get_category(item.name)
        print(f"  [{category}] ← {item.name}")

        # 创建目标文件夹
        target_dir = DESKTOP / category
        target_dir.mkdir(exist_ok=True)

        # 处理重名（如果目标位置已经有同名文件）
        target_path = target_dir / item.name
        if target_path.exists():
            base = target_path.stem      # 文件名（不含扩展名）
            ext = target_path.suffix     # 扩展名
            target_path = target_dir / f"{base}_重复{ext}"

        # 搬过去
        shutil.move(str(item), str(target_path))

    print("=" * 40)
    print("✅ 整理完成！桌面干干净净 🦀")
    print("=" * 40)


if __name__ == "__main__":
    organize_desktop()
