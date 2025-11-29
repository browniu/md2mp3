@echo off
REM 测试不同语速的脚本（Windows）

echo === Markdown 转 MP3 语速测试 ===
echo.

REM 检查 example.md 是否存在
if not exist "example.md" (
    echo 错误: example.md 不存在
    exit /b 1
)

REM 测试正常速度
echo 1. 测试正常速度 (1.0x)
python md2mp3.py example.md --rate 1.0
if exist "example.mp3" (
    move /y example.mp3 example_1.0x.mp3
    echo ✓ 生成: example_1.0x.mp3
)
echo.

REM 测试 1.5 倍速
echo 2. 测试 1.5 倍速
python md2mp3.py example.md --rate 1.5
if exist "example.mp3" (
    move /y example.mp3 example_1.5x.mp3
    echo ✓ 生成: example_1.5x.mp3
)
echo.

REM 测试 2 倍速
echo 3. 测试 2 倍速
python md2mp3.py example.md --rate 2
if exist "example.mp3" (
    move /y example.mp3 example_2.0x.mp3
    echo ✓ 生成: example_2.0x.mp3
)
echo.

REM 测试 0.8 倍速
echo 4. 测试 0.8 倍速
python md2mp3.py example.md --rate 0.8
if exist "example.mp3" (
    move /y example.mp3 example_0.8x.mp3
    echo ✓ 生成: example_0.8x.mp3
)
echo.

echo === 测试完成 ===
echo 生成的文件:
dir /b example_*.mp3 2>nul || echo 未找到生成的文件

pause

