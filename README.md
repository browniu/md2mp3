# Markdown 转 MP3 工具 🎵

将 Markdown 文件转换为 MP3 音频文件的 Python 工具，让你的文档"说话"。

## ✨ 功能特性

- 📝 **智能文本提取** - 自动清理 Markdown 语法（代码块、链接、图片等）
- 🔊 **高质量语音** - 基于 Google TTS，支持多种语言
- ⚡ **可调节语速** - 0.5x - 4.0x 任意调节，满足不同场景
- 🎵 **字幕同步** - 自动生成 LRC 字幕文件，支持同步显示 ⭐ 新功能
- 🌍 **多语言支持** - 中文、英文、日文、韩文等数十种语言
- 💻 **简单易用** - 命令行一键转换
- 🐍 **纯 Python 实现** - 兼容 Python 3.7 - 3.13+

---

## 🚀 快速开始

### 30秒上手

```bash
# 1. 安装依赖
pip install gtts

# 2. 转换（正常速度）
python md2mp3.py your-file.md

# 3. 转换（1.5倍速）- 需要先安装 ffmpeg
python md2mp3.py your-file.md --rate 1.5

# 4. 生成带字幕的音频（新功能！）
python md2mp3.py your-file.md --subtitle --rate 1.5

# 5. 生成精确字幕（推荐！）⭐
python md2mp3.py your-file.md --subtitle --accurate --rate 1.5
```

就这么简单！生成的 MP3 文件和 LRC 字幕文件会保存在源文件同一目录下。

**字幕模式**：
- `--subtitle` - 快速生成（时间估算，误差较大）
- `--subtitle --accurate` - 精确生成（基于实际音频，推荐）⭐

---

## 📥 安装指南

### 1. 检查 Python 版本

```bash
python --version
# 需要 Python 3.7 或更高版本
```

### 2. 安装 Python 依赖

```bash
# 方法一：使用 requirements.txt
pip install -r requirements.txt

# 方法二：直接安装
pip install gtts
```

### 3. 安装 FFmpeg（可选）

**仅在需要调整语速时才需要安装**

| 操作系统 | 安装命令 |
|---------|---------|
| **Windows** | `winget install ffmpeg` |
| **Mac** | `brew install ffmpeg` |
| **Linux** | `sudo apt-get install ffmpeg` |

安装后重启终端，运行 `ffmpeg -version` 验证。

### 4. 测试运行

```bash
# 测试基础功能（无需 ffmpeg）
python md2mp3.py example.md

# 测试语速调整（需要 ffmpeg）
python md2mp3.py example.md --rate 1.5
```

---

## 📖 使用指南

### 基本语法

```bash
python md2mp3.py <markdown文件路径> [选项]
```

### 参数说明

| 参数 | 简写 | 说明 | 默认值 | 示例 |
|------|------|------|--------|------|
| `--lang` | `-l` | 语言代码 | `zh-CN` | `-l en` |
| `--rate` | `-r` | 语速倍率 (0.5-4.0) | `1.0` | `-r 1.5` |
| `--subtitle` | `-s` | 生成 LRC 字幕文件 | 关闭 | `-s` |
| `--accurate` | `-a` | 精确字幕（需ffmpeg） | 关闭 | `-a` |

### 常用命令

```bash
# 正常速度（中文）
python md2mp3.py file.md

# 1.5倍速（最常用）
python md2mp3.py file.md -r 1.5

# 2倍速英文
python md2mp3.py file.md -l en -r 2

# 慢速学习（0.8倍）
python md2mp3.py file.md --rate 0.8

# 生成带字幕的音频（快速，但不精确）
python md2mp3.py file.md --subtitle

# 生成精确字幕（推荐）⭐
python md2mp3.py file.md --subtitle --accurate

# 组合使用：1.5倍速 + 精确字幕
python md2mp3.py file.md -s -a -r 1.5
```

### 支持的语言

| 语言 | 代码 | 语言 | 代码 |
|------|------|------|------|
| 中文（简体） | `zh-CN` | 英文 | `en` |
| 中文（繁体） | `zh-TW` | 日文 | `ja` |
| 韩文 | `ko` | 法文 | `fr` |
| 德文 | `de` | 西班牙文 | `es` |

更多语言：https://gtts.readthedocs.io/

---

## 🎯 语速选择建议

| 倍速 | 适用场景 | 特点 |
|------|---------|------|
| **0.5x - 0.8x** | 学习新知识、外语练习 | 清晰、易理解 |
| **1.0x** | 正常阅读、标准播放 | 原始速度 |
| **1.2x - 1.5x** | 日常浏览、复习内容 | 最佳性价比 ⭐ |
| **1.5x - 2.0x** | 快速浏览、熟悉内容 | 节省时间 |
| **2.0x - 4.0x** | 极速扫读 | 音调变化明显 |

💡 **推荐**：大多数情况使用 **1.5x**，既能节省时间，又不影响理解。

---

## 💼 实用场景

### 1. 学习笔记转音频

```bash
# 将学习笔记转为音频，通勤时收听
python md2mp3.py 学习笔记.md --rate 1.2
```

### 2. 技术文档转音频

```bash
# 英文技术文档，快速浏览
python md2mp3.py README.md --lang en --rate 1.5
```

### 3. 会议纪要转音频

```bash
# 快速回顾会议内容
python md2mp3.py 会议纪要.md --rate 2
```

### 4. 生成字幕文件 🎵

#### 两种模式

| 模式 | 命令 | 准确度 | 速度 | 推荐 |
|------|------|--------|------|------|
| **估算** | `--subtitle` | ±2-5秒 | ⚡ 快 | 预览 |
| **精确** | `--subtitle --accurate` | ±0.1秒 | 🐢 慢 | 正式使用 ⭐ |

#### 快速估算（不推荐）

```bash
python md2mp3.py file.md --subtitle
```

**特点**：快速但不精确，误差较大

#### 精确字幕（推荐）⭐

```bash
# 基础用法
python md2mp3.py file.md --subtitle --accurate

# 带语速调整
python md2mp3.py file.md -s -a -r 1.5

# 输出两个文件：
# - file.mp3  (音频)
# - file.lrc  (精确字幕)
```

**工作原理**：
1. 逐句生成 TTS 音频
2. 使用 ffprobe 测量实际时长
3. 合并音频并生成精确时间戳
4. 准确度：±0.1秒

**注意**：需要安装 ffmpeg

#### 查看字幕同步效果

1. 用浏览器打开 `player.html`
2. 选择生成的 MP3 和 LRC 文件
3. 播放查看字幕同步效果

#### LRC 格式示例

```lrc
[00:00.00]测试示例
[00:01.07]这是一个用于测试 Markdown 转 MP3 功能的示例文件。
[00:05.58]功能介绍
```

**详细说明**：
- 估算模式：[SUBTITLE_GUIDE.md](SUBTITLE_GUIDE.md)
- 精确模式：[ACCURATE_SUBTITLE_GUIDE.md](ACCURATE_SUBTITLE_GUIDE.md) ⭐

---

### 5. 批量转换

**Windows (batch_convert.bat)**:
```batch
@echo off
for %%f in (*.md) do (
    echo 正在转换: %%f
    python md2mp3.py "%%f" --rate 1.5
)
echo 批量转换完成！
pause
```

**Linux/Mac (batch_convert.sh)**:
```bash
#!/bin/bash
for file in *.md; do
    echo "正在转换: $file"
    python md2mp3.py "$file" --rate 1.5
done
echo "批量转换完成！"
```

---

## 🔧 工作原理

### 处理流程

```
Markdown 文件
    ↓
1. 读取文件内容
    ↓
2. 提取纯文本（移除 Markdown 语法）
    ↓
3. Google TTS 转换为语音
    ↓
4. [可选] FFmpeg 调整播放速度
    ↓
5. 保存 MP3 文件
```

### 文本提取规则

**会被移除的内容**：
- 代码块 `` ```...``` ``
- 行内代码 `` `code` ``
- 图片 `![alt](url)`
- 链接地址 `[text](url)` → 保留 "text"
- 标题符号 `#` `##`
- 粗体/斜体 `**bold**` → "bold"
- HTML 标签 `<div>content</div>` → "content"

**会被保留的内容**：
- 标题文字
- 正文段落
- 列表内容
- 表格文字
- 引用内容

### 语速调整原理

由于 Google TTS 不支持直接调速，本工具采用 **后处理方案**：

1. 先用 Google TTS 生成正常速度的 MP3
2. 使用 FFmpeg 的 `atempo` 滤镜调整播放速度
3. 输出最终的变速 MP3，自动清理临时文件

**优点**：
- ✅ 灵活，可调范围大（0.5x - 4.0x）
- ✅ 纯 Python 实现，无需额外库
- ✅ 兼容所有 Python 版本

**缺点**：
- ⚠️ 速度变化会导致音调略有变化（物理特性）

---

## ❓ 常见问题

### Q1: 支持哪些 Python 版本？

**A**: 支持 Python 3.7 及以上所有版本：
- ✅ Python 3.7+
- ✅ Python 3.13+ （已解决兼容性问题）
- ✅ 纯 Python 实现，无需额外编译

---

### Q2: 能否不安装 ffmpeg？

**A**: 可以！
- 如果只需要正常速度转换，**不需要** ffmpeg
- 只有使用 `--rate` 参数时才需要 ffmpeg
- 脚本会自动检测，如果没有会给出友好提示

---

### Q3: 语速调整会影响音质吗？

**A**: 会有一定影响
- 速度变化会导致音调变化（物理特性）
- 建议使用 1.0x - 2.0x 范围
- 超过 2.0x 音调变化明显

---

### Q4: 生成的音频没有声音？

**A**: 请检查：
1. 原始 Markdown 文件是否有文本内容
2. 查看控制台输出的"完整内容"，确认文本提取是否正确
3. 确保网络连接正常（Google TTS 需要网络）

---

### Q5: 提示找不到 ffmpeg？

**A**: 
1. 确保 ffmpeg 已正确安装：`ffmpeg -version`
2. 重新打开命令行窗口（环境变量需要重载）
3. 参考上面的"安装 FFmpeg"部分

---

### Q6: pip install 失败？

**A**: 尝试以下方法：

```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gtts

# 升级 pip
python -m pip install --upgrade pip

# 使用 --user 参数
pip install --user gtts
```

---

### Q7: MP3 文件太大？

**A**: 
- Google TTS 生成的文件通常较小（约 1MB/分钟）
- 可以用 ffmpeg 压缩：
  ```bash
  ffmpeg -i input.mp3 -b:a 64k output.mp3
  ```
- 提高播放速度可以缩短时长，从而减小文件

---

## 📊 输出示例

### 正常速度

```
正在读取文件: ./example.md
提取的文本长度: 456 字符
文本预览: 这是一个测试文档...
完整内容（用于核对）: 这是一个测试文档...
正在生成语音文件...
✓ 基础语音文件生成完成
✓ 最终音频文件: ./example.mp3
```

### 带速度调整

```
语速设置: 1.5x
正在读取文件: ./example.md
提取的文本长度: 456 字符
文本预览: 这是一个测试文档...
完整内容（用于核对）: 这是一个测试文档...
正在生成语音文件...
✓ 基础语音文件生成完成
正在调整音频速度为 1.5x...
✓ 速度调整完成
✓ 临时文件已清理
✓ 最终音频文件: ./example.mp3
```

---

## 🧪 测试工具

项目提供了测试脚本来对比不同速度：

```bash
# Windows
test_speed.bat

# Linux/Mac
chmod +x test_speed.sh
./test_speed.sh
```

这会生成多个不同速度的 MP3 文件（0.8x、1.0x、1.5x、2.0x），方便你对比选择。

---

## ⚠️ 注意事项

1. **网络连接** - Google TTS API 需要网络连接
2. **Python 版本** - 需要 Python 3.7 或更高版本
3. **FFmpeg 依赖** - 仅在使用 `--rate` 参数时需要
4. **文本长度** - 过长的文本可能需要较长处理时间
5. **音频质量** - Google TTS 生成的是合成语音，音质较好但不是真人
6. **速度与音调** - 速度调整会导致音调变化，无法完全避免

---

## 🛠️ 故障排查

### ❌ 找不到 ffmpeg

```bash
# 验证安装
ffmpeg -version

# 如果没有，按操作系统安装：
# Windows: winget install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

### ❌ Python 模块不存在

```bash
pip install -r requirements.txt
```

### ❌ 网络错误

- Google TTS 需要网络连接
- 检查代理设置
- 尝试切换网络

### ❌ 权限错误

```bash
# 使用 --user 参数安装
pip install --user gtts
```

---

## 🔮 扩展建议

想要更高级的功能？可以考虑：

### 1. 离线 TTS
使用 `pyttsx3` 库实现离线语音合成（无需网络）

### 2. 更好的音质
- Azure Cognitive Services
- Amazon Polly
- Edge TTS（微软）

### 3. 变速不变调
使用 `librosa` + `pyrubberband` 实现音高保持

### 4. 批量处理
添加目录扫描功能，自动转换多个文件

### 5. 进度显示
使用 `tqdm` 显示处理进度条

---

## 📋 依赖说明

### Python 依赖
- **gtts** - Google Text-to-Speech（唯一依赖）
  - 稳定、免费、无需 API 密钥
  - 需要网络连接
  - 音质较好

### 系统依赖
- **ffmpeg** - 音视频处理工具（可选）
  - 仅在使用 `--rate` 参数时需要
  - 跨平台支持
  - 功能强大

---

## 📜 许可证

MIT License

---

## 💬 反馈与支持

- 使用过程中遇到问题？查看上面的"常见问题"和"故障排查"
- 控制台输出的错误信息通常包含解决线索
- 确保 Python、pip、ffmpeg 版本正确

---

**享受你的 Markdown 音频之旅！** 🎉
