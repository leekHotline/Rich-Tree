# Rich-Tree 🌳

酷炫目录树显示工具 - 使用 Rich 库渲染美观的目录结构

<img width="1461" height="533" alt="图片" src="https://github.com/user-attachments/assets/9180a20d-63a3-44ca-898c-6b354f88ac27" />
<img width="1468" height="891" alt="图片" src="https://github.com/user-attachments/assets/39be2f6d-cc47-4684-ad01-107ba3d1600e" />

## ✨ 特性

- 🎨 美观的树形结构显示，支持彩色输出
- 📁 智能文件类型图标识别
- 📊 显示文件/目录大小统计
- 🔍 支持隐藏文件显示
- ⚙️ 可配置扫描深度
- 🌐 Windows GBK 控制台兼容（自动回退 ASCII 符号）
- 🚀 支持全局命令和模块调用

## 🚀 快速开始

### 方法一：一键脚本安装（推荐）

**克隆项目**
```cmd
git clone https://github.com/leekHotline/Rich-Tree.git
```

在项目根目录运行以下命令，**自动安装到用户环境**并配置全局可用：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-rich-tree.ps1
```

安装完成后，**重新打开**一个新的终端，即可在任意目录使用：

```bash
# 显示当前目录树
rich-tree

# 显示指定目录
rich-tree E:\Cutting-edge_software

# 指定深度和选项
rich-tree D:\work -d 3 --hidden --no-size
```

### 方法二：手动安装

1. **安装到用户环境**：
   ```bash
   py -m pip install --user .
   ```

2. **添加用户 Scripts 目录到 PATH**：
   - 典型路径：`%USERPROFILE%\AppData\Roaming\Python\Python310\Scripts`
   - 添加到系统环境变量 PATH 中

3. **重新打开终端**，即可全局使用 `rich-tree`

### 方法三：虚拟环境使用

```bash
# 激活虚拟环境
.\venv\Scripts\activate

# 使用命令
rich-tree

# 或直接调用
.\venv\Scripts\rich-tree.exe E:\some\path
```

## 📖 使用方法

### 命令行参数

```bash
rich-tree [路径] [选项]

位置参数:
  路径                  目标目录 (默认: 当前目录)

选项:
  -h, --help           显示帮助信息
  -d DEPTH, --depth DEPTH
                       最大扫描深度 (默认: 5)
  --no-size            不显示文件/目录大小
  --hidden             包含隐藏文件和目录
```

### 使用示例

```bash
# 基本用法
rich-tree                    # 显示当前目录
rich-tree C:\Users           # 显示指定目录

# 高级选项
rich-tree --depth 3          # 限制深度为 3 层
rich-tree --hidden           # 显示隐藏文件
rich-tree --no-size          # 不显示大小信息
rich-tree -d 2 --hidden      # 组合使用

# 模块方式调用
python -m rich_tree          # 等同于 rich-tree
python -m rich_tree --help   # 查看帮助
```

## 🛠️ 开发

### 项目结构

```
Rich-Tree/
├── rich_tree/              # 主包
│   ├── __init__.py         # 包初始化
│   ├── cli.py              # 命令行接口
│   ├── tree_viewer.py      # 核心渲染逻辑
│   └── __main__.py         # 模块入口
├── scripts/
│   └── setup-rich-tree.ps1 # 一键安装脚本
├── tests/                  # 测试文件
├── pyproject.toml          # 项目配置
└── readme.md               # 说明文档
```

### 本地开发

```bash
# 安装开发依赖
pip install -e .

# 运行测试
python -m rich_tree --help

# 直接运行源码
python rich_tree/tree_viewer.py
```

## 🔧 故障排除

### 常见问题

1. **`'rich-tree' 不是内部或外部命令`**
   - 确保已运行安装脚本或手动添加到 PATH
   - 重新打开终端窗口

2. **UnicodeEncodeError 错误**
   - 工具已自动处理 GBK 控制台兼容性
   - 在不支持 Unicode 的终端会自动回退到 ASCII 符号

3. **权限错误**
   - 确保对目标目录有读取权限
   - 某些系统目录可能需要管理员权限

### 卸载

```bash
# 卸载用户安装的包
py -m pip uninstall rich-tree --user

# 从 PATH 中移除 Scripts 目录（手动操作）
```

## 📄 许可证

本项目使用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**享受美观的目录树显示！** 🎉
