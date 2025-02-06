from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import argparse


def main(input):
    model_dir = "iic/SenseVoiceSmall"

    model = AutoModel(
        model=model_dir,
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",
        disable_update=True,
    )

    # en
    res = model.generate(
        input=input,
        cache={},
        language="auto",  # "zn", "en", "yue", "ja", "ko", "nospeech"
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,  #
        merge_length_s=15,
    )

    text = rich_transcription_postprocess(res[0]["text"])
    return text


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input", type=str, default="example/en.mp3")
    args = arg_parser.parse_args()
    input = args.input
    print(f"parseing {input}")
    text = main(input)
    print(text)
