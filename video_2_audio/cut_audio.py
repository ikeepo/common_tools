from pydub import AudioSegment
import typer


def cut_audio(input_file, output_file, start_time, end_time):
    """
    Cut parts of an audio file and save it to a new file.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the output audio file.
        start_time (int): Start time in milliseconds.
        end_time (int): End time in milliseconds.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Cut the audio
    cut_audio = audio[start_time:end_time]

    # Save the cut audio to a new file
    cut_audio.export(output_file, format="mp3")


# Example usage
# input_file = "path/to/input/audio.mp3"
# output_file = "path/to/output/cut_audio.mp3"
start_time = 10000  # Start at 10 seconds
end_time = 30000  # End at 30 seconds


dp_audio = "/home/zoe/video_2_audio/audio"
dp_out = "/home/zoe/video_2_audio/audio_separate"


def main(in_name, out_name, start, end):
    fp_in = f"{dp_audio}/{in_name}.mp3"
    fp_out = f"{dp_out}/{out_name}.mp3"
    print(fp_in)
    print(fp_out)
    print(start)
    print(end)
    # exit()
    cut_audio(fp_in, fp_out, int(start), int(end))
    print("DONE")


d = {
    "03": [283000, 530500],
    "04": [552000, 780500],
    "05": [789000, 1062500],
    "07": [2500, 279000],
    "08": [288000, 545000],
    "09": [557000, 807000],
    "10": [815000, 1049000],
    "11": [1058000, 1309000],
    "12": [1316000, 1555500],
    "13": [1564000, 1811000],
    "14": [1818000, 2047000],
    "15": [2052000, 2297500],
    "16": [2309000, 2561000],
    "17": [2567000, 2848500],
    "18": [2855000, 3112000],  # 51:52
    "19": [3124000, 3380500],
    "20": [3394000, 3644500],
    "21": [3662000, 3924000],
    "22": [3939000, 4178000],
    "23": [4194000, 4438000],
    "24": [4452000, 4717500],
    "25": [4735000, 4977000],
    "26": [3000, 257500],
    "27": [264000, 514500],
    "28": [519000, 784500],
    "29": [791000, 1073500],
    "30": [1081000, 1355000],
}

if __name__ == "__main__":
    typer.run(main)
