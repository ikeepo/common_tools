import argparse
from pydub import AudioSegment


def merge_audio(file1, file2, output_file):
    """
    合并两个音频文件，并保存为新的文件。

    :param file1: 第一个音频文件路径
    :param file2: 第二个音频文件路径
    :param output_file: 输出的合并文件路径
    """
    try:
        # 加载音频文件
        audio1 = AudioSegment.from_file(file1)
        audio2 = AudioSegment.from_file(file2)

        # 合并音频（顺序拼接）
        combined = audio1 + audio2

        # 导出合并后的音频文件
        combined.export(output_file, format="mp3")
        print(f"✅ 合并完成！保存到: {output_file}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")


# 解析命令行参数
def main():
    parser = argparse.ArgumentParser(description="合并两个音频文件")
    parser.add_argument("file1", help="第一个音频文件路径")
    parser.add_argument("file2", help="第二个音频文件路径")
    parser.add_argument(
        "-o",
        "--output",
        default="merged_audio.mp3",
        help="输出文件名（默认为 merged_audio.mp3）",
    )

    args = parser.parse_args()

    merge_audio(args.file1, args.file2, args.output)


if __name__ == "__main__":
    main()
