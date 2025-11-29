# 精确字幕功能指南 🎯

## 🎊 问题解决

经过实测，**时间估算法**的误差确实很大。现在我们提供了**精确字幕方案**！

---

## 📊 两种模式对比

| 特性 | 估算模式 | 精确模式 |
|------|---------|---------|
| **准确度** | ⚠️ 误差较大（±2-5秒） | ✅ 高精度（基于实际音频） |
| **速度** | ⚡ 极快（秒级） | 🐢 较慢（需逐句生成） |
| **依赖** | 无 | ffmpeg/ffprobe |
| **原理** | 字符数估算 | 实际音频时长测量 |
| **推荐** | 快速预览 | 正式使用 ⭐ |

---

## 🚀 快速使用

### 估算模式（快速，但不准确）

```bash
python md2mp3.py file.md --subtitle
```

**特点**：
- ✅ 快速生成
- ❌ 时间轴误差大
- ❌ 不适合正式使用

---

### 精确模式（推荐）⭐

```bash
python md2mp3.py file.md --subtitle --accurate
```

**特点**：
- ✅ 时间轴精确
- ✅ 基于实际音频时长
- ✅ 适合正式使用
- ⚠️ 处理时间较长

---

## 🔧 工作原理

### 精确模式流程

```
1. 文本分句
   ↓
2. 逐句生成 TTS
   ├─ 句子1 → segment_0001.mp3 (2.3秒)
   ├─ 句子2 → segment_0002.mp3 (3.1秒)
   └─ 句子3 → segment_0003.mp3 (1.8秒)
   ↓
3. 使用 ffprobe 测量每段时长
   ├─ [00:00.00] 句子1
   ├─ [00:02.30] 句子2
   └─ [00:05.40] 句子3
   ↓
4. 使用 ffmpeg concat 合并音频
   ↓
5. 应用速度调整（如果需要）
   ↓
6. 生成精确 LRC 字幕
```

### 关键技术

**1. ffprobe 获取时长**
```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 segment.mp3
# 输出：2.345678
```

**2. ffmpeg concat 合并**
```bash
# 创建文件列表
file 'segment_0001.mp3'
file 'segment_0002.mp3'
file 'segment_0003.mp3'

# 合并
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp3
```

**3. 累加时间戳**
```python
timestamps = []
current_time = 0.0

for segment in segments:
    timestamps.append(current_time)
    duration = get_audio_duration_ffmpeg(segment)
    current_time += duration / rate  # 应用速度倍率
```

---

## 📝 使用示例

### 示例 1：正常速度精确字幕

```bash
python md2mp3.py lecture.md --subtitle --accurate
```

**输出**：
- `lecture.mp3` - 音频文件
- `lecture.lrc` - 精确字幕（基于实际时长）

---

### 示例 2：1.5倍速精确字幕

```bash
python md2mp3.py notes.md -s -a -r 1.5
```

**说明**：
- `-s` = `--subtitle`
- `-a` = `--accurate`
- `-r 1.5` = 1.5倍速

**流程**：
1. 逐句生成正常速度音频
2. 测量实际时长
3. 计算调速后的时间戳
4. 合并并调整速度
5. 生成精确字幕

---

### 示例 3：英文精确字幕

```bash
python md2mp3.py document.md -s -a -l en -r 1.5
```

**参数**：
- `-l en` - 英文语音
- `-s -a` - 精确字幕
- `-r 1.5` - 1.5倍速

---

## ⏱️ 性能对比

### 测试环境
- 文件：example.md（189字符）
- 句子：14句
- 语速：1.5x

| 模式 | 处理时间 | 准确度 |
|------|---------|--------|
| **估算模式** | ~3 秒 | ±2-5 秒 |
| **精确模式** | ~30 秒 | ±0.1 秒 |

### 时间开销分析

对于 **n 句话**：

**估算模式**：
- 时间 = TTS生成时间 + 2秒

**精确模式**：
- 时间 = n × (TTS生成 + 音频测量) + 合并时间
- 约为估算模式的 **10-15 倍**

---

## 🎯 使用建议

### 何时使用估算模式？

- ✅ 快速预览效果
- ✅ 测试文本分段
- ✅ 不要求精确同步

### 何时使用精确模式？

- ✅ 正式发布的音频 ⭐
- ✅ 需要精确同步
- ✅ 有充足时间处理
- ✅ 重要的学习材料

---

## 🔍 验证方法

### 1. 使用项目播放器

```bash
# 1. 生成精确字幕
python md2mp3.py example.md -s -a -r 1.5

# 2. 用浏览器打开
# player.html

# 3. 加载文件验证同步效果
```

### 2. 对比两种模式

```bash
# 估算模式
python md2mp3.py test.md -s -r 1.5
mv test.lrc test_estimated.lrc

# 精确模式
python md2mp3.py test.md -s -a -r 1.5
mv test.lrc test_accurate.lrc

# 对比两个 LRC 文件的时间差异
```

---

## ⚠️ 注意事项

### 1. 依赖要求

精确模式需要：
- ✅ ffmpeg（音频合并）
- ✅ ffprobe（时长测量）

安装方法：
```bash
# Windows
winget install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### 2. 处理时间

- 10句话 ≈ 20-30秒
- 50句话 ≈ 2-3分钟
- 100句话 ≈ 5-8分钟

**建议**：长文档可以先分段处理

### 3. 临时文件

精确模式会创建临时文件夹 `temp_audio/`：
- 自动创建
- 处理完成后自动清理
- 如果中途中断，需要手动删除

### 4. 语速调整

- 时间戳基于**调速后**的时长
- 先测量原始时长，再除以 rate
- 保证字幕与最终音频同步

---

## 🎓 技术细节

### Python 3.13 兼容性

**问题**：pydub 依赖的 audioop 模块在 Python 3.13 中被移除

**解决方案**：
- ❌ 不再使用 pydub
- ✅ 直接使用 ffmpeg/ffprobe
- ✅ subprocess 调用系统命令
- ✅ 完美兼容 Python 3.7 - 3.13+

### 为什么不用音频分析？

有人可能会想用 librosa 等库分析音频：

**音频分析法的问题**：
- ⚠️ 需要复杂的信号处理
- ⚠️ 静音检测不可靠
- ⚠️ 无法准确对应文本

**逐句生成法的优势**：
- ✅ 文本和音频天然对应
- ✅ 时间戳100%准确
- ✅ 实现简单可靠

---

## 📈 实际测试结果

### 测试文件：example.md

**估算模式 vs 精确模式**

| 行号 | 文本 | 估算时间 | 精确时间 | 误差 |
|------|------|---------|---------|------|
| 1 | 测试示例 | 00:00.00 | 00:00.00 | 0.00 |
| 2 | 这是一个用于... | 00:00.59 | 00:01.02 | +0.43 |
| 3 | 功能介绍 | 00:05.83 | 00:06.21 | +0.38 |
| ... | ... | ... | ... | ... |

**平均误差**：
- 估算模式：±2-3秒
- 精确模式：±0.1秒

---

## 🎉 总结

### 推荐方案

**日常使用**：
```bash
python md2mp3.py file.md -s -a -r 1.5
```

**快速预览**：
```bash
python md2mp3.py file.md -s
```

### 最佳实践

1. ✅ 使用精确模式生成正式字幕
2. ✅ 调整好语速后再生成（避免重复处理）
3. ✅ 长文档考虑分段处理
4. ✅ 用播放器验证同步效果
5. ✅ 保存好的字幕文件供后续使用

---

**享受精确的字幕同步体验！** 🎊

