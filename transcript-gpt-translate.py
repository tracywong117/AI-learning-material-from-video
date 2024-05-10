"""
Translate srt and burn subtitle - A program to translate transcript using GPT-4 API. Support burn srt subtitle to video.

"""

import os
from utils import *

# Parameters
input_video_file = "korean-drama.mp4" # file path to the video file
api_key = 'your_openai_api_key' # Your OpenAI API Key
translate_option = "manual" # "api": use GPT-4 API to translate; "manual": manually translate
require_burn_subtitle = True # True: burn subtitle to video; False: do not burn subtitle to video

input_video_name = os.path.basename(input_video_file).split(".")[0]
output_audio_file = f"audio_{input_video_name}.mp3"
transcript_file = f"transcript_{input_video_name}.srt"
translated_transcript_file = f"translated_transcript_{input_video_name}.srt"
output_video_file = f"{input_video_name}_subtitle.mp4"

if translate_option == "api":
    import openai
    openai.api_key = api_key

subtitle_list = read_srt_to_list(transcript_file)

simplified_subtitle_text = ""
for i, subtitle in enumerate(subtitle_list):
    text = subtitle[1]
    simplified_subtitle_text += f"{i+1} {text}\n"

instruction = """你是一個專業的韓文譯中文的翻譯員，以下是一部韓國電視劇的文字轉錄，請翻譯成繁體中文，翻譯風格應該是日常口語，並以同樣格式顯示，即每一句為{序號} {譯文}。\n"""
prompt = instruction + simplified_subtitle_text
print("Prompt:")
print(prompt)
print("-------")

if translate_option == "api":
    # call GPT-4 API to translate
    response = openai.Completion.create(
        model="gpt-4",              # Specify the model
        prompt=prompt,              # Provide the prompt
        max_tokens=300,             # Max number of tokens (adjust based on your needs)
        temperature=0.5,            # Sampling temperature
        top_p=1,                    # Nucleus sampling parameter
        stop=None                   # Token at which text generation is stopped
    )
    translated_subtitle_text = response.choices[0].text.strip()
    
elif translate_option == "manual":
    # translated_subtitle_text = input("Enter the translated subtitle:\n")
    translated_subtitle_text = get_multiline_input()
    
translated_subtitle_list = []
for i, translated_subtitle in enumerate(translated_subtitle_text.split("\n")):
    translated_subtitle_list.append([subtitle_list[i][0], translated_subtitle.split(" ", 1)[1]])
print(translated_subtitle_list)

save_srt(translated_subtitle_list, translated_transcript_file)

if require_burn_subtitle:
    burn_two_subtitle(subtitle_list, translated_subtitle_list, input_video_file, output_video_file)
