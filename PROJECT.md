# 项目说明

## 项目结构

```
md2mp3/
├── md2mp3.py           # 主程序（Python 实现）
├── requirements.txt    # Python 依赖
├── example.md          # 测试示例文件
│
├── README.md           # 项目说明文档
├── QUICKSTART.md       # 快速开始指南
├── USAGE.md            # 详细使用指南
├── INSTALL.md          # 安装指南
├── CHANGELOG.md        # 更新日志
├── PROJECT.md          # 本文件
│
├── test_speed.sh       # Linux/Mac 测试脚本
└── test_speed.bat      # Windows 测试脚本
```

## 技术栈

- **语言**: Python 3.7+
- **TTS 引擎**: Google TTS (gTTS)
- **音频处理**: FFmpeg (subprocess 调用)
- **依赖管理**: pip + requirements.txt

## 核心功能

### 1. Markdown 文本提取

使用正则表达式从 Markdown 中提取纯文本：
- 移除代码块、行内代码
- 移除图片、链接语法（保留文本）
- 移除标题标记、粗体斜体标记
- 移除 HTML 标签

### 2. 文本转语音

使用 Google TTS API 将文本转换为 MP3：
- 支持多种语言
- 自动分段处理长文本
- 无需本地模型

### 3. 速度调整

使用 FFmpeg 的 atempo 滤镜：
- 支持 0.5x - 4.0x 速度范围
- 通过 subprocess 调用
- 自动清理临时文件

## 设计原则

1. **简单**: 单文件实现，易于理解和修改
2. **可靠**: 使用成熟的第三方工具（gTTS、FFmpeg）
3. **兼容**: 支持 Python 3.7 - 3.13+ 所有版本
4. **轻量**: 最小依赖，只需要 gtts 一个 Python 包

## 版本历史

- **v1.2.0**: 移除 Node.js 版本和 pydub 依赖
- **v1.1.0**: 添加语速调整功能
- **v1.0.0**: 初始版本

## 开发指南

### 本地开发

```bash
# 克隆或下载项目
cd md2mp3

# 安装依赖
pip install -r requirements.txt

# 运行测试
python md2mp3.py example.md
```

### 修改语言

编辑 `md2mp3.py` 的 argparse 默认值：

```python
parser.add_argument('--lang', '-l', default='zh-CN',  # 改这里
                   help='语言代码 (默认: zh-CN)')
```

### 添加新功能

建议的扩展方向：

1. **批量转换**: 添加目录扫描功能
2. **配置文件**: 支持 `.md2mp3rc` 配置
3. **进度条**: 使用 tqdm 显示进度
4. **更多 TTS**: 支持 Azure、AWS Polly 等
5. **变速不变调**: 使用 pyrubberband

## 依赖说明

### Python 依赖

- `gtts`: Google Text-to-Speech，纯 Python 实现
  - 稳定、免费、无需 API 密钥
  - 需要网络连接
  - 音质较好

### 系统依赖

- `ffmpeg`: 音视频处理工具
  - 仅在使用 `--rate` 参数时需要
  - 跨平台支持
  - 功能强大

## 常见问题

### 为什么移除 Node.js 版本？

- 专注于单一技术栈，便于维护
- Python 生态更适合文本处理和 TTS
- 减少重复代码和文档

### 为什么不使用 pydub？

- pydub 依赖 audioop（Python 3.13 已移除）
- 直接使用 subprocess 调用 ffmpeg 更简单
- 减少依赖，提高兼容性

### 为什么使用 Google TTS？

- 免费、无需 API 密钥
- 音质较好
- 支持多种语言
- Python 库成熟稳定

### 速度调整会影响音质吗？

- 会导致音调变化（物理特性）
- 建议使用 1.0x - 2.0x 范围
- 如需更好效果，可使用专业 TTS 服务

## 贡献指南

欢迎贡献代码和建议！请：

1. Fork 本项目
2. 创建特性分支
3. 提交 Pull Request
4. 更新相关文档

## 许可证

MIT License

## 作者

本项目由 AI 辅助创建和维护。

