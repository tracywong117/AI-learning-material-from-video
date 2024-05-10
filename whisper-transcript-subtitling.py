"""
Transcript video to srt - A program to transcibe video using whisper and save as srt. Support burn srt subtitle to video.

"""

import os
from utils import *

# Parameters
input_video_file = "korean-drama.mp4" # file path to the video file
require_transcript = True # True: use whisper to transcript; False: load existing transcript file
require_burn_subtitle = True # True: burn subtitle to video; False: do not burn subtitle to video

input_video_name = os.path.basename(input_video_file)
output_audio_file = f"audio_{input_video_name}.mp3"
transcript_file = f"transcript_{input_video_name}.srt"
output_video_file = f"{input_video_name}_subtitle.mp4"

if require_transcript:
    import whisper
    model = whisper.load_model("small")

if require_transcript:
    # convert video to mp3
    print("Converting video to mp3...")
    convert_to_mp3(input_video_file, output_audio_file)
    print("Done!")

    # transcribe mp3 using whisper
    print("Transcribing...")
    transcribe_result = model.transcribe(
        audio=output_audio_file, word_timestamps=True, task="transcribe"
    )
    print("Done!")
    print(transcribe_result["text"])

    subtitle_list = []
    for segment in transcribe_result['segments']:
        subtitle_list.append([(segment['start'], segment['end']), remove_punctuation(segment['text'])])

    # save transcript as srt
    save_srt(subtitle_list, transcript_file)

if not require_transcript:
    # load subtitle
    subtitle_list = read_srt_to_list(transcript_file)

    print(subtitle_list)

if require_burn_subtitle:
    burn_one_subtitle(subtitle_list, input_video_file, output_video_file)
