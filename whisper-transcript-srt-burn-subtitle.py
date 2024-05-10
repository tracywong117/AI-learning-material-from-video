"""
Transcript video to srt - A program to transcibe video using whisper and save as srt. Support burn srt subtitle to video.

"""

import whisper
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import os

input_video_file = "korean-drama.mp4" # file path to the video file
# input_video_file = input("Enter the video file name: ")

input_video_name = os.path.basename(input_video_file)
output_audio_file = f"audio_{input_video_name}.mp3"
transcript_file = f"transcript_{input_video_name}.srt"
output_video_file = f"{input_video_name}_subtitle.mp4"

require_transcript = False
require_burn_subtitle = True

# load model
model = whisper.load_model("small")

def convert_to_mp3(input_file, output_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)

def remove_punctuation(s):
    # s = s.replace('?', '')
    s = s.replace('!', '')
    s = s.replace('.', '')
    s = s.replace(',', '')
    return s

# turn time into hour:minute:second, millisecond
def time_to_hmsmm(time):
    time = time * 1000
    return f"{int(time/3600000):02d}:{int(time/60000)%60:02d}:{int(time/1000)%60:02d},{int(time)%1000:03d}"

# turn hour:minute:second, millisecond into time
def hmsmm_to_time(hmsmm):
    h, m, s = hmsmm.split(":")
    s, mm = s.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(mm) / 1000

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
    with open(transcript_file, "w") as file:
        for index, subtitle in enumerate(subtitle_list):
            file.write(f"{index+1}\n")
            file.write(f"{time_to_hmsmm(subtitle[0][0])} --> {time_to_hmsmm(subtitle[0][1])}\n")
            file.write(f"{subtitle[1].strip()}\n\n")

if not require_transcript:
    # load subtitle
    subtitle_list = []
    with open(transcript_file, "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):
            start, end = lines[i+1].split(" --> ")
            text = lines[i+2]
            subtitle_list.append([(hmsmm_to_time(start), hmsmm_to_time(end)), text.replace('\n', '')])

print(subtitle_list)

if require_burn_subtitle:  
    # generate subtitle on the original video
    generator = lambda txt: TextClip(txt, fontsize=32, color="white", font='NanumGothic')

    subtitles = SubtitlesClip(subtitle_list, generator)

    video = VideoFileClip(input_video_file)

    result_video = CompositeVideoClip(
        [video, subtitles.set_position(("center", video.size[1] - 100))]
    )

    # Write the result to a file
    result_video.write_videofile(output_video_file, fps=24)

    print(f"Video saved as {output_video_file}")
