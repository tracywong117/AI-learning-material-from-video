from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip


# turn time into hour:minute:second, millisecond
def time_to_hmsmm(time):
    time = time * 1000
    return f"{int(time/3600000):02d}:{int(time/60000)%60:02d}:{int(time/1000)%60:02d},{int(time)%1000:03d}"


# turn hour:minute:second, millisecond into time
def hmsmm_to_time(hmsmm):
    h, m, s = hmsmm.split(":")
    s, mm = s.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(mm) / 1000


def remove_punctuation(s):
    # s = s.replace('?', '')
    s = s.replace("!", "")
    s = s.replace(".", "")
    s = s.replace(",", "")
    return s


def save_srt(subtitle_list, transcript_file):
    with open(transcript_file, "w") as file:
        for index, subtitle in enumerate(subtitle_list):
            file.write(f"{index+1}\n")
            file.write(
                f"{time_to_hmsmm(subtitle[0][0])} --> {time_to_hmsmm(subtitle[0][1])}\n"
            )
            file.write(f"{subtitle[1].strip()}\n\n")


# read srt file to list
def read_srt_to_list(transcript_file):
    subtitle_list = []
    with open(transcript_file, "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):
            start, end = lines[i + 1].split(" --> ")
            text = lines[i + 2]
            subtitle_list.append(
                [(hmsmm_to_time(start), hmsmm_to_time(end)), text.replace("\n", "")]
            )

    return subtitle_list


# convert video to mp3
def convert_to_mp3(input_file, output_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)


def get_multiline_input(termination_word="END"):
    print("Enter the translated subtitle (type 'END' on a new line to finish):")
    input_lines = []
    while True:
        line = input()
        if line.strip() == termination_word:
            break
        input_lines.append(line)
    return "\n".join(input_lines)


def burn_one_subtitle(subtitle_list, input_video_file, output_video_file):
    video = VideoFileClip(input_video_file)

    generator = lambda txt: TextClip(
        txt, fontsize=24, font="NanumGothic", color="#CC7700"
    )
    subtitles = SubtitlesClip(subtitle_list, generator)

    result_video = CompositeVideoClip(
        [video, subtitles.set_position(("center", "bottom"))]
    )

    result_video.write_videofile(output_video_file, fps=24)
    print(f"Video saved as {output_video_file}")


def burn_two_subtitle(
    subtitle_list, translated_subtitle_list, input_video_file, output_video_file
):
    video = VideoFileClip(input_video_file)

    generator = lambda txt: TextClip(
        txt, fontsize=24, font="NanumGothic", color="#CC7700"
    )  # korean font
    subtitles = SubtitlesClip(subtitle_list, generator)

    translated_generator = lambda txt: TextClip(
        txt, fontsize=28, font="BiauKai", color="white"
    )  # chinese font
    translated_subtitles = SubtitlesClip(translated_subtitle_list, translated_generator)

    result_video = CompositeVideoClip(
        [video, subtitles.set_position(("center", video.size[1] - 60))]
    )
    result_video = CompositeVideoClip(
        [result_video, translated_subtitles.set_position(("center", "bottom"))]
    )

    result_video.write_videofile(output_video_file, fps=24)
    print(f"Video saved as {output_video_file}")
