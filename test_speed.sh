#!/bin/bash
# 测试不同语速的脚本（Linux/Mac）

echo "=== Markdown 转 MP3 语速测试 ==="
echo ""

# 检查 example.md 是否存在
if [ ! -f "example.md" ]; then
    echo "错误: example.md 不存在"
    exit 1
fi

# 测试正常速度
echo "1. 测试正常速度 (1.0x)"
python md2mp3.py example.md --rate 1.0
if [ -f "example.mp3" ]; then
    mv example.mp3 example_1.0x.mp3
    echo "✓ 生成: example_1.0x.mp3"
fi
echo ""

# 测试 1.5 倍速
echo "2. 测试 1.5 倍速"
python md2mp3.py example.md --rate 1.5
if [ -f "example.mp3" ]; then
    mv example.mp3 example_1.5x.mp3
    echo "✓ 生成: example_1.5x.mp3"
fi
echo ""

# 测试 2 倍速
echo "3. 测试 2 倍速"
python md2mp3.py example.md --rate 2
if [ -f "example.mp3" ]; then
    mv example.mp3 example_2.0x.mp3
    echo "✓ 生成: example_2.0x.mp3"
fi
echo ""

# 测试 0.8 倍速
echo "4. 测试 0.8 倍速"
python md2mp3.py example.md --rate 0.8
if [ -f "example.mp3" ]; then
    mv example.mp3 example_0.8x.mp3
    echo "✓ 生成: example_0.8x.mp3"
fi
echo ""

echo "=== 测试完成 ==="
echo "生成的文件:"
ls -lh example_*.mp3 2>/dev/null || echo "未找到生成的文件"

