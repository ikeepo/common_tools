import sys
import os
from pathlib import Path
from moviepy.editor import *

def v2a(fp_src, fp_tgt):
    video = VideoFileClip(fp_src) # 2.
    audio = video.audio # 3.
    audio.write_audiofile(fp_tgt) # 4.
    print(f"{fp_src}->{fp_tgt}")

def convert_dp(dp_video, dp_audio):
    os.makedirs(dp_audio, exist_ok=True)
    for fn in os.listdir(dp_video):
        fp_video = f"{dp_video}/{fn}"
        fn_audio =   f"{Path(fn).stem}.mp3"
        fp_audio = f"{dp_audio}/{fn_audio}"
        v2a(fp_video, fp_audio)

if __name__ == "__main__":
    # fp_in = f"{dp_video}/06.mp4"
    # fp_out = f"{dp_audio}/06.mp3"
    # v2a(fp_in, fp_out)
    dp_video = "/mnt/e/老王/video"
    dp_audio = "/mnt/e/老王/audio"
    convert_dp(dp_video, dp_audio)
