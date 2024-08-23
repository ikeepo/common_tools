import yaml
import yt_dlp
from pathlib import Path

def download_youtube_video(url, output_path='.'):
    try:
        # 设置下载选项
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s'
        }

        # 使用 yt-dlp 下载视频
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            ydl.download([url])
            print(f"Download completed! Video saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def load_from_yaml():
    dp_pwd = Path(__file__).parent
    yaml_file_path = dp_pwd / 'config.yaml'
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

if __name__ == "__main__":
    # YAML 文件路径


    # 从 YAML 文件中加载 URL
    data = load_from_yaml()
    video_urls = data.get('videos', [])
    # 下载路径
    download_path = data.get('dl_path', '.')
    
    
    if not video_urls:
        print("No URLs found in the YAML file.")
    else:
        for url in video_urls:
            download_youtube_video(url, download_path if download_path else '.')
