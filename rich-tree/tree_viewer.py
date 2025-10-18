
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
酷炫目录树显示工具
文件名: tree_viewer.py
"""

import os
import sys
from pathlib import Path
from rich.tree import Tree
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

def get_dir_size(path):
    """获取目录大小"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except PermissionError:
        pass
    return total

def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def build_tree(directory, tree, max_depth=5, current_depth=0, show_size=True, show_hidden=False):
    """递归构建目录树"""
    if current_depth >= max_depth:
        return
    
    try:
        paths = sorted(Path(directory).iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        tree.add("❌ [red]权限拒绝[/red]")
        return
    
    dirs = [p for p in paths if p.is_dir()]
    files = [p for p in paths if p.is_file()]
    
    # 过滤隐藏文件
    if not show_hidden:
        dirs = [d for d in dirs if not d.name.startswith('.')]
        files = [f for f in files if not f.name.startswith('.')]
    
    # 添加目录
    for dir_path in dirs:
        if dir_path.name.startswith('.') and not show_hidden:
            continue
        
        icon = "📁"
        style = "bold cyan"
        
        if show_size:
            size = get_dir_size(dir_path)
            label = f"{icon} [cyan]{dir_path.name}[/cyan] [dim]({format_size(size)})[/dim]"
        else:
            label = f"{icon} [{style}]{dir_path.name}[/{style}]"
        
        branch = tree.add(label)
        build_tree(dir_path, branch, max_depth, current_depth + 1, show_size, show_hidden)
    
    # 添加文件
    for file_path in files:
        if file_path.name.startswith('.') and not show_hidden:
            continue
        
        # 根据文件类型设置图标
        suffix = file_path.suffix.lower()
        if suffix in ['.py']:
            icon = "🐍"
        elif suffix in ['.txt', '.md', '.doc', '.docx']:
            icon = "📄"
        elif suffix in ['.jpg', '.png', '.gif', '.jpeg', '.svg']:
            icon = "🖼️"
        elif suffix in ['.mp4', '.avi', '.mov']:
            icon = "🎬"
        elif suffix in ['.mp3', '.wav', '.flac']:
            icon = "🎵"
        elif suffix in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            icon = "📦"
        elif suffix in ['.exe', '.app']:
            icon = "⚙️"
        elif suffix in ['.json', '.xml', '.yaml', '.yml']:
            icon = "📋"
        else:
            icon = "📄"
        
        size = file_path.stat().st_size if show_size else 0
        if show_size:
            label = f"{icon} [green]{file_path.name}[/green] [dim]({format_size(size)})[/dim]"
        else:
            label = f"{icon} [green]{file_path.name}[/green]"
        
        tree.add(label)

def display_tree(target_path=".", max_depth=5, show_size=True, show_hidden=False):
    """显示目录树"""
    console = Console()
    
    path = Path(target_path).resolve()
    
    if not path.exists():
        console.print(f"[bold red]❌ 路径不存在: {target_path}[/bold red]")
        return
    
    if not path.is_dir():
        console.print(f"[bold red]❌ 不是一个目录: {target_path}[/bold red]")
        return
    
    # 创建标题
    title = Text()
    title.append("🌳 目录结构树 🌳", style="bold magenta")
    
    # 显示面板
    console.print(Panel(
        f"[cyan]路径:[/cyan] [yellow]{path}[/yellow]\n"
        f"[cyan]深度:[/cyan] [yellow]{max_depth}[/yellow] 层",
        title="📂 扫描信息",
        border_style="blue",
        box=box.ROUNDED
    ))
    
    console.print()
    
    # 创建根树
    tree = Tree(
        f"🏠 [bold blue]{path.name or path}[/bold blue]",
        guide_style="bright_blue"
    )
    
    # 构建树
    build_tree(path, tree, max_depth, show_size=show_size, show_hidden=show_hidden)
    
    # 显示树
    console.print(tree)
    
    # 统计信息
    total_dirs = sum(1 for _ in path.rglob('*') if _.is_dir())
    total_files = sum(1 for _ in path.rglob('*') if _.is_file())
    
    console.print()
    console.print(Panel(
        f"[cyan]📁 目录数:[/cyan] [yellow]{total_dirs}[/yellow]\n"
        f"[cyan]📄 文件数:[/cyan] [yellow]{total_files}[/yellow]",
        title="📊 统计信息",
        border_style="green",
        box=box.ROUNDED
    ))

def main():
    """主函数"""
    console = Console()
    
    # 显示欢迎信息
    console.print(Panel.fit(
        "[bold cyan]🎄 酷炫目录树查看器 🎄[/bold cyan]\n"
        "[dim]Created with ❤️  using Rich[/dim]",
        border_style="magenta"
    ))
    console.print()
    
    # 获取用户输入
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        console.print("[yellow]请输入要查看的目录路径 (直接回车查看当前目录):[/yellow]")
        target = input(">>> ").strip() or "."
    
    # 配置选项
    max_depth = 5  # 最大深度
    show_size = True  # 显示文件大小
    show_hidden = False  # 显示隐藏文件
    
    # 显示目录树
    display_tree(target, max_depth, show_size, show_hidden)

if __name__ == "__main__":
    main()