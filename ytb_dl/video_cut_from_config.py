
import subprocess
import sys
from pathlib import Path

import yaml


CONFIG_FILE = "config.yaml"


def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cut_video(input_video, start, end, output_name, output_dir):
    output_path = Path(output_dir) / output_name

    cmd = [
        "ffmpeg",
        "-y",
        "-ss", start,
        "-to", end,
        "-i", str(input_video),
        "-c", "copy",
        str(output_path),
    ]

    print("🎬 开始剪辑：")
    print(" ".join(cmd))

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ 剪辑完成：{output_path}")
    except subprocess.CalledProcessError:
        print("❌ ffmpeg 执行失败")
        sys.exit(1)


def main():
    config = load_config(CONFIG_FILE)

    video_cut = config.get("video_cut")
    if not video_cut:
        print("❌ config.yaml 中未找到 video_cut 配置")
        sys.exit(1)

    input_video = Path(video_cut["input_video"])
    start = video_cut["start"]
    end = video_cut["end"]
    output_name = video_cut["name"]

    output_dir = config.get("dl_path", input_video.parent)

    if not input_video.exists():
        print(f"❌ 输入视频不存在：{input_video}")
        sys.exit(1)

    cut_video(
        input_video=input_video,
        start=start,
        end=end,
        output_name=output_name,
        output_dir=output_dir,
    )


if __name__ == "__main__":
    main()
