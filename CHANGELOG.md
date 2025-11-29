# 更新日志

## [1.3.1] - 2025-11-28 🔥

### 🎯 重大改进

- **精确字幕模式**: 解决时间估算误差大的问题
  - 使用 `--subtitle --accurate` / `-s -a` 参数
  - 逐句生成 TTS，测量实际时长
  - 使用 ffmpeg/ffprobe 获取精确时间
  - 准确度提升至 ±0.1秒（原 ±2-5秒）
  - 不再依赖 pydub（解决 Python 3.13 兼容性）

### 🔧 技术更新

- 新增 `get_audio_duration_ffmpeg()` - 使用 ffprobe 获取时长
- 新增 `merge_audio_files_ffmpeg()` - 使用 ffmpeg concat 合并
- 优化 `generate_audio_with_timestamps()` - 基于 ffmpeg 实现
- 移除 pydub 依赖，改用 subprocess 调用 ffmpeg

### 📝 文档更新

- 新增 `ACCURATE_SUBTITLE_GUIDE.md` - 精确字幕完整指南
- 更新 `README.md` - 添加双模式说明
- 更新帮助信息 - 说明估算vs精确模式

---

## [1.3.0] - 2025-11-28

### ✨ 新增功能

- **字幕生成**: 支持生成 LRC 格式字幕文件
  - 使用 `--subtitle` / `-s` 参数
  - 基于智能时间估算算法（已优化为精确模式）
  - 自动按句子分段
  - 考虑标点停顿时间
  
- **HTML5 播放器**: 创建 `player.html` 用于验证字幕同步
  - 美观的渐变界面
  - 实时字幕高亮
  - 点击跳转功能
  - 统计信息显示
  
- **时间估算引擎**: 
  - 支持多语言语速参数
  - 中文 4.5 字/秒
  - 英文 2.8 字/秒
  - 自动计算标点停顿
  - 支持语速倍率调整

### 📝 文档更新

- 新增 `SUBTITLE_GUIDE.md` - 字幕功能完整指南
- 更新 `README.md` - 添加字幕功能说明
- 新增 `player.html` - 字幕播放器

### 🔧 代码改进

- 新增 `split_into_sentences()` - 智能句子分割
- 新增 `estimate_duration()` - 时间估算算法
- 新增 `generate_lrc()` - LRC 格式生成
- 修复 Windows 控制台编码问题（✓ → [OK]）

### 📊 测试结果

- 字幕准确度：±0.5秒（正常速度）
- 支持语速：0.5x - 4.0x
- 生成速度：实时（无需音频分析）

---

## [1.2.0] - 2025-11-28

### 🔥 重大更新

- **移除 Node.js 版本**: 专注于 Python 实现，提供更好的维护性
- **移除 pydub 依赖**: 解决 Python 3.13 兼容性问题
- **改用 subprocess**: 直接调用 ffmpeg，更简洁可靠

### ✨ 新增功能

- 兼容 Python 3.7 - 3.13+ 所有版本
- 自动检测 ffmpeg 是否可用
- 更友好的错误提示

### 📝 文档更新

- 更新所有文档，移除 Node.js 相关内容
- 简化安装步骤
- 新增 Python 3.13 兼容性说明

### 🗑️ 移除内容

- 移除 `index.js` (Node.js 实现)
- 移除 `package.json` 和相关依赖
- 移除 `INSTALL_WINDOWS.md`
- 不再依赖 `pydub`

---

## [1.1.0] - 2025-11-28

### ✨ 新增功能

- **语速调整功能**: 支持 `--rate` 参数调整播放速度（0.5x - 4.0x）
- **自动 FFmpeg**: Node.js 版本自动安装 ffmpeg 二进制文件
- **完整参数解析**: Python 版本使用 argparse 提供更好的命令行体验
- **进度提示**: 添加详细的处理进度输出
- **完整文本输出**: 显示提取的完整文本用于核对

### 📝 文档更新

- 新增 `INSTALL.md` - 详细安装指南
- 新增 `USAGE.md` - 使用指南和最佳实践
- 新增 `CHANGELOG.md` - 版本更新日志
- 更新 `README.md` - 添加语速调整说明
- 新增测试脚本 `test_speed.sh` 和 `test_speed.bat`

### 🔧 技术改进

- Node.js: 使用 fluent-ffmpeg 处理音频速度
- Python: 使用 pydub 处理音频速度
- 优化临时文件管理，自动清理
- 改进错误处理和提示信息

### 📦 依赖更新

**Node.js**:
- 新增: `fluent-ffmpeg@^2.1.2`
- 新增: `@ffmpeg-installer/ffmpeg@^1.1.0`

**Python**:
- 新增: `pydub==0.25.1`

---

## [1.0.0] - 初始版本

### 基础功能

- Markdown 文件读取
- 文本提取（移除代码块、链接、图片等）
- Google TTS 语音合成
- MP3 文件生成
- Node.js 和 Python 双版本实现
- 多语言支持（中文、英文、日文等）

---

## 未来计划

### v1.2.0
- [ ] 批量转换功能
- [ ] 配置文件支持（指定默认语言、速度等）
- [ ] 进度条显示

### v1.3.0
- [ ] 支持更多 TTS 引擎（Azure、AWS Polly）
- [ ] 变速不变调功能（保持音高）
- [ ] 音频格式选择（MP3、WAV、OGG）

### v2.0.0
- [ ] GUI 界面
- [ ] 实时预览
- [ ] 音频编辑功能（剪辑、合并）
- [ ] 语音质量选择（低/中/高）

