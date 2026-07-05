import glob
import os
import re
import subprocess

from mlx_audio.tts.generate import generate_audio
from mlx_audio.tts.utils import load_model


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r'\.(?!\d)', text) if s.strip()]


def main():
    model = load_model("/Users/z/.lmstudio/models/mlx-community/pocket-tts-8bit")

    with open("news.txt") as f:
        lines = f.readlines()

    idx = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        for sentence in split_sentences(stripped):
            file_prefix = f"voice_{idx:05d}"
            generate_audio(
                model=model,
                text=sentence,
                file_prefix=file_prefix,
            )
            idx += 1

    wav_files = sorted(glob.glob("voice_*.wav"))
    if not wav_files:
        return

    filelist_path = "filelist.txt"
    with open(filelist_path, "w") as f:
        for wav in wav_files:
            f.write(f"file '{wav}'\n")

    subprocess.run(
        [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", filelist_path,
            "-c", "copy",
            "composed_voice.wav",
        ],
        check=True,
    )
    os.remove(filelist_path)
    print(f"Merged {len(wav_files)} files into composed_voice.wav")


if __name__ == "__main__":
    main()
