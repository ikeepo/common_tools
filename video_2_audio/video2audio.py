import sys
import os
from pathlib import Path
from moviepy.editor import *
import yaml
import datetime


def load_from_yaml():
    dp_pwd = Path(__file__).parent
    yaml_file_path = dp_pwd / "config.yaml"
    with open(yaml_file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def v2a(fp_src, fp_tgt):
    video = VideoFileClip(fp_src)  # 2.
    audio = video.audio  # 3.
    audio.write_audiofile(fp_tgt)  # 4.
    print(f"{fp_src}->{fp_tgt}")


def convert_dp(dp_video, dp_audio, remove_video=False):
    os.makedirs(dp_audio, exist_ok=True)
    for fn in os.listdir(dp_video):
        fp_video = os.path.join(dp_video, fn)
        if os.path.isdir(fp_video):
            continue
        if fn.endswith("mp3") or fn.endswith("DS_Store"):
            continue
        fn_audio = f"{Path(fn).stem}.mp3"
        # add today date
        today = datetime.date.today()
        fn_audio = f"{today}_{fn_audio}"
        fp_audio = f"{dp_audio}/{fn_audio}"
        if os.path.exists(fp_audio):
            print(f"{fp_audio} already exist")
        else:
            v2a(fp_video, fp_audio)
        if remove_video:
            os.remove(fp_video)


if __name__ == "__main__":
    data = load_from_yaml()
    dp_video = data.get("dp_video", "")
    dp_audio = data.get("dp_audio", "")
    convert_dp(dp_video, dp_audio, remove_video=True)
