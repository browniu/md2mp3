#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse
import subprocess
from pathlib import Path

try:
    from gtts import gTTS
except ImportError as e:
    print("错误: 请先安装依赖库")
    print("运行: pip install gtts")
    print("\n注意: 如果需要使用 --rate 参数调整语速，需要安装 ffmpeg")
    print("Windows: winget install ffmpeg")
    print("Mac: brew install ffmpeg")
    print("Linux: sudo apt-get install ffmpeg")
    sys.exit(1)

# pydub 在 Python 3.13 上有兼容性问题，不再依赖
PYDUB_AVAILABLE = False


def extract_text_from_markdown(content):
    """
    从markdown内容中提取纯文本
    
    Args:
        content: markdown文件内容
        
    Returns:
        提取后的纯文本
    """
    # 移除代码块
    text = re.sub(r'```[\s\S]*?```', '', content)
    
    # 移除行内代码
    text = re.sub(r'`[^`]+`', '', text)
    
    # 移除图片
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    
    # 移除链接但保留文本
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # 移除标题标记
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # 移除粗体和斜体标记
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
    
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 移除多余的空行
    text = re.sub(r'\n\s*\n', '\n', text)
    
    # 移除多余的空格
    text = text.strip()
    
    return text


def split_into_sentences(text):
    """
    将文本分割成句子
    
    Args:
        text: 输入文本
        
    Returns:
        句子列表
    """
    # 按句子结束标点分割（保留标点）
    pattern = r'([^。！？.!?\n]+[。！？.!?\n]+)'
    sentences = re.findall(pattern, text)
    
    # 处理剩余文本（没有结束标点的）
    remaining = re.sub(pattern, '', text).strip()
    if remaining:
        sentences.append(remaining)
    
    # 清理并过滤空句子
    return [s.strip() for s in sentences if s.strip()]


def estimate_duration(text, language='zh-CN', rate=1.0):
    """
    估算文本朗读时长（秒）
    
    Args:
        text: 文本内容
        language: 语言代码
        rate: 语速倍率
        
    Returns:
        估算的时长（秒）
    """
    # 不同语言的基础语速（字符/秒）
    base_speeds = {
        'zh-CN': 4.5,  # 中文
        'zh-TW': 4.5,  # 繁体中文
        'en': 2.8,     # 英文（按字符计算）
        'ja': 5.0,     # 日文
        'ko': 4.0,     # 韩文
    }
    
    # 获取基础语速
    speed = base_speeds.get(language, 4.0)
    
    # 计算字符数（排除空白）
    char_count = len(text.strip())
    if char_count == 0:
        return 0
    
    # 计算基础时长
    base_duration = char_count / speed
    
    # 应用语速倍率（rate越大，时长越短）
    adjusted_duration = base_duration / rate
    
    # 添加标点停顿时间
    pause_time = 0
    pause_time += text.count('。') * 0.5
    pause_time += text.count('！') * 0.5
    pause_time += text.count('？') * 0.5
    pause_time += text.count('，') * 0.3
    pause_time += text.count('；') * 0.3
    pause_time += text.count('：') * 0.3
    pause_time += text.count('.') * 0.4
    pause_time += text.count('!') * 0.4
    pause_time += text.count('?') * 0.4
    pause_time += text.count(',') * 0.2
    pause_time += text.count(';') * 0.2
    pause_time += text.count('\n') * 0.5
    
    return adjusted_duration + pause_time


def generate_lrc(text, language='zh-CN', rate=1.0):
    """
    生成LRC格式字幕（基于时间估算，不够精确）
    
    Args:
        text: 文本内容
        language: 语言代码
        rate: 语速倍率
        
    Returns:
        LRC格式字幕内容
    """
    sentences = split_into_sentences(text)
    lrc_lines = []
    current_time = 0.0
    
    for sentence in sentences:
        # 格式化时间 [mm:ss.xx]
        minutes = int(current_time // 60)
        seconds = current_time % 60
        time_tag = f"[{minutes:02d}:{seconds:05.2f}]"
        
        lrc_lines.append(f"{time_tag}{sentence}")
        
        # 累加时间
        duration = estimate_duration(sentence, language, rate)
        current_time += duration
    
    return '\n'.join(lrc_lines)


def generate_lrc_accurate(sentences, timestamps):
    """
    生成精确的LRC格式字幕（基于实际时长）
    
    Args:
        sentences: 句子列表
        timestamps: 时间戳列表（秒）
        
    Returns:
        LRC格式字幕内容
    """
    lrc_lines = []
    
    for i, sentence in enumerate(sentences):
        if i < len(timestamps):
            time = timestamps[i]
            minutes = int(time // 60)
            seconds = time % 60
            time_tag = f"[{minutes:02d}:{seconds:05.2f}]"
            lrc_lines.append(f"{time_tag}{sentence}")
    
    return '\n'.join(lrc_lines)


def get_audio_duration_ffmpeg(audio_file):
    """
    使用 ffmpeg 获取音频时长
    
    Args:
        audio_file: 音频文件路径
        
    Returns:
        时长（秒）或 None
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_file)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            return duration
        else:
            return None
            
    except Exception as e:
        return None


def merge_audio_files_ffmpeg(audio_files, output_file):
    """
    使用 ffmpeg 合并音频文件
    
    Args:
        audio_files: 音频文件列表
        output_file: 输出文件路径
        
    Returns:
        是否成功
    """
    try:
        # 创建文件列表
        list_file = 'temp_file_list.txt'
        with open(list_file, 'w', encoding='utf-8') as f:
            for audio_file in audio_files:
                # ffmpeg concat 格式
                f.write(f"file '{audio_file}'\n")
        
        # 使用 ffmpeg concat
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file,
            '-c', 'copy',
            '-y',
            output_file
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 清理临时文件列表
        if os.path.exists(list_file):
            os.remove(list_file)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"合并音频失败: {e}")
        return False


def generate_audio_with_timestamps(sentences, language='zh-CN', rate=1.0, temp_dir='temp_audio'):
    """
    逐句生成音频并记录实际时间戳（使用 ffmpeg）
    
    Args:
        sentences: 句子列表
        language: 语言代码
        rate: 语速倍率
        temp_dir: 临时文件目录
        
    Returns:
        (输出文件路径, 时间戳列表)
    """
    # 检查 ffmpeg/ffprobe 是否可用
    if not check_ffmpeg():
        print("错误: 未找到 ffmpeg/ffprobe，无法生成精确字幕")
        print("请安装 ffmpeg:")
        print("  Windows: winget install ffmpeg")
        print("  Mac: brew install ffmpeg")
        print("  Linux: sudo apt-get install ffmpeg")
        return None, None
    
    # 创建临时目录
    os.makedirs(temp_dir, exist_ok=True)
    
    audio_files = []
    timestamps = []
    current_time = 0.0
    
    print(f"正在逐句生成音频（共 {len(sentences)} 句）...")
    
    for i, sentence in enumerate(sentences):
        # 记录时间戳
        timestamps.append(current_time)
        
        # 生成单句音频
        temp_file = os.path.join(temp_dir, f'segment_{i:04d}.mp3')
        
        try:
            tts = gTTS(text=sentence, lang=language)
            tts.save(temp_file)
            
            # 使用 ffprobe 获取时长
            duration_sec = get_audio_duration_ffmpeg(temp_file)
            
            if duration_sec is None:
                # 如果获取失败，使用估算
                duration_sec = estimate_duration(sentence, language, 1.0)
            
            # 应用速度调整（影响累计时间）
            adjusted_duration = duration_sec / rate
            
            audio_files.append(temp_file)
            current_time += adjusted_duration
            
            # 显示进度
            if (i + 1) % 5 == 0 or (i + 1) == len(sentences):
                print(f"  进度: {i + 1}/{len(sentences)} 句")
            
        except Exception as e:
            print(f"警告: 生成第 {i+1} 句时出错: {e}")
            current_time += 2.0  # 默认2秒
    
    print(f"[OK] 所有音频片段生成完成")
    
    # 合并音频
    print("正在合并音频片段...")
    output_file = os.path.join(temp_dir, 'combined.mp3')
    
    success = merge_audio_files_ffmpeg(audio_files, output_file)
    
    if not success:
        print("警告: 音频合并失败")
        return None, None
    
    print(f"[OK] 音频合并完成")
    
    # 清理临时音频片段（保留合并后的文件）
    for temp_file in audio_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
    
    return output_file, timestamps


def check_ffmpeg():
    """
    检查 ffmpeg 是否可用
    
    Returns:
        bool: ffmpeg 是否可用
    """
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def adjust_audio_speed(input_path, output_path, rate):
    """
    调整音频速度（使用 ffmpeg）
    
    Args:
        input_path: 输入音频文件路径
        output_path: 输出音频文件路径
        rate: 速度倍率（例如：1.5 表示 1.5倍速）
    """
    print(f"正在调整音频速度为 {rate}x...")
    
    # 检查 ffmpeg 是否可用
    if not check_ffmpeg():
        print("错误: 未找到 ffmpeg，无法调整音频速度")
        print("请安装 ffmpeg:")
        print("  Windows: winget install ffmpeg")
        print("  Mac: brew install ffmpeg")
        print("  Linux: sudo apt-get install ffmpeg")
        print("安装后请重启终端")
        return False
    
    try:
        # 使用 ffmpeg 的 atempo 滤镜调整速度
        # atempo 范围是 0.5-2.0，如果超出需要链式调用
        cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-filter:a', f'atempo={rate}',
            '-vn',  # 不处理视频
            '-y',   # 覆盖输出文件
            str(output_path)
        ]
        
        # 执行 ffmpeg 命令
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[OK] 速度调整完成")
            return True
        else:
            print(f"错误: FFmpeg 处理失败")
            print(f"错误信息: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"错误: 调整音频速度时出错 - {e}")
        return False


def markdown_to_mp3(markdown_path, language='zh-CN', rate=1.0, generate_subtitle=False, accurate_subtitle=False):
    """
    将markdown文件转换为mp3音频
    
    Args:
        markdown_path: markdown文件路径
        language: 语言代码，默认中文(zh-CN)
        rate: 语速倍率，默认1.0
        generate_subtitle: 是否生成字幕文件
        accurate_subtitle: 是否使用精确字幕（需要pydub）
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(markdown_path):
            print(f"错误: 文件不存在 - {markdown_path}")
            return False
        
        # 读取markdown文件
        print(f"正在读取文件: {markdown_path}")
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # 提取文本内容
        text = extract_text_from_markdown(markdown_content)
        
        if not text or len(text.strip()) == 0:
            print("错误: 提取的文本内容为空")
            return False
        
        print(f"提取的文本长度: {len(text)} 字符")
        print(f"文本预览: {text[:100]}...")
        
        # 生成输出文件路径
        markdown_path_obj = Path(markdown_path)
        final_output_path = markdown_path_obj.with_suffix('.mp3')
        
        # 如果需要精确字幕，检查 ffmpeg
        if generate_subtitle and accurate_subtitle:
            if not check_ffmpeg():
                print("警告: 未找到 ffmpeg，将使用时间估算法生成字幕")
                print("提示: 安装 ffmpeg 以使用精确字幕")
                accurate_subtitle = False
        
        # 精确字幕模式：逐句生成
        if generate_subtitle and accurate_subtitle:
            print("使用精确字幕模式（逐句生成）...")
            sentences = split_into_sentences(text)
            print(f"共分割为 {len(sentences)} 句")
            
            # 逐句生成并获取时间戳
            temp_audio_file, timestamps = generate_audio_with_timestamps(
                sentences, language, rate
            )
            
            if temp_audio_file and timestamps:
                # 应用速度调整（如果需要）
                if rate != 1.0:
                    print(f"正在调整整体速度为 {rate}x...")
                    success = adjust_audio_speed(temp_audio_file, str(final_output_path), rate)
                    
                    if not success:
                        print("警告: 速度调整失败，使用原始速度")
                        import shutil
                        shutil.copy(temp_audio_file, str(final_output_path))
                    else:
                        print("[OK] 速度调整完成")
                else:
                    # 不需要调速，直接移动文件
                    import shutil
                    shutil.move(temp_audio_file, str(final_output_path))
                
                # 清理临时目录
                temp_dir = os.path.dirname(temp_audio_file)
                if os.path.exists(temp_dir):
                    try:
                        os.rmdir(temp_dir)
                    except:
                        pass
                
                print(f"[OK] 最终音频文件: {final_output_path}")
                
                # 生成精确字幕
                lrc_path = markdown_path_obj.with_suffix('.lrc')
                print(f"正在生成精确字幕文件...")
                lrc_content = generate_lrc_accurate(sentences, timestamps)
                
                with open(lrc_path, 'w', encoding='utf-8') as f:
                    f.write(lrc_content)
                
                print(f"[OK] 精确字幕文件: {lrc_path}")
                print(f"[OK] 生成了 {len(sentences)} 条字幕（基于实际音频时长）")
                
                return True
        
        # 普通模式或估算字幕模式
        need_speed_adjust = rate != 1.0
        temp_output_path = markdown_path_obj.with_stem(
            f"{markdown_path_obj.stem}_temp"
        ).with_suffix('.mp3') if need_speed_adjust else final_output_path
        
        # 转换为语音
        print(f"正在生成语音文件...")
        tts = gTTS(text=text, lang=language)
        tts.save(str(temp_output_path))
        print(f"[OK] 基础语音文件生成完成")
        
        # 如果需要调整速度
        if need_speed_adjust:
            success = adjust_audio_speed(str(temp_output_path), str(final_output_path), rate)
            
            if not success:
                print(f"警告: 速度调整失败，保留原始速度的文件")
                if os.path.exists(temp_output_path):
                    os.rename(temp_output_path, final_output_path)
            else:
                if os.path.exists(temp_output_path):
                    os.remove(temp_output_path)
                    print(f"[OK] 临时文件已清理")
        
        print(f"[OK] 最终音频文件: {final_output_path}")
        
        # 生成估算字幕
        if generate_subtitle and not accurate_subtitle:
            lrc_path = markdown_path_obj.with_suffix('.lrc')
            print(f"正在生成字幕文件（时间估算）...")
            lrc_content = generate_lrc(text, language, rate)
            
            with open(lrc_path, 'w', encoding='utf-8') as f:
                f.write(lrc_content)
            
            print(f"[OK] 字幕文件: {lrc_path}")
            print(f"提示: 时间估算可能不够精确，建议使用 --accurate 参数")
            
            sentence_count = len(split_into_sentences(text))
            print(f"[OK] 生成了 {sentence_count} 条字幕")
        
        return True
        
    except Exception as e:
        print(f"处理过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数 - 处理命令行参数"""
    parser = argparse.ArgumentParser(
        description='将 Markdown 文件转换为 MP3 音频文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python md2mp3.py example.md                    # 正常速度中文
  python md2mp3.py example.md --rate 1.5         # 1.5倍速中文
  python md2mp3.py example.md -r 2 --lang en     # 2倍速英文
  python md2mp3.py example.md --subtitle         # 生成字幕（估算）
  python md2mp3.py example.md -s --accurate      # 生成精确字幕
  
支持的语言代码:
  zh-CN: 中文（简体）
  zh-TW: 中文（繁体）
  en: 英文
  ja: 日文
  ko: 韩文
  更多语言请参考: https://gtts.readthedocs.io/
        """
    )
    
    parser.add_argument('file', help='Markdown 文件路径')
    parser.add_argument('--lang', '-l', default='zh-CN', 
                       help='语言代码 (默认: zh-CN)')
    parser.add_argument('--rate', '-r', type=float, default=1.0,
                       help='语速倍率 0.5-4.0 (默认: 1.0)')
    parser.add_argument('--subtitle', '-s', action='store_true',
                       help='生成 LRC 字幕文件')
    parser.add_argument('--accurate', '-a', action='store_true',
                       help='生成精确字幕（需要 pydub，处理时间较长）')
    
    args = parser.parse_args()
    
    # 验证速度参数
    if args.rate <= 0 or args.rate > 4:
        print("错误: --rate 参数必须是 0 到 4 之间的数字")
        sys.exit(1)
    
    print(f"语速设置: {args.rate}x")
    print(f"语言设置: {args.lang}")
    if args.subtitle:
        mode = "精确模式（逐句生成）" if args.accurate else "估算模式（快速）"
        print(f"字幕生成: 开启 (LRC格式 - {mode})")
        if args.accurate and not check_ffmpeg():
            print("警告: 未找到 ffmpeg，将使用估算模式")
    
    success = markdown_to_mp3(args.file, args.lang, args.rate, args.subtitle, args.accurate)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

