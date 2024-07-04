# AI-learning-material-from-video
This repository contains Python application designed for automatically transcribing video into text, translating the text, and burning the subtitles into the video. The application utilizes the Whisper model for transcription and optionally integrates with the OpenAI GPT-4 API for translation.

## Features
- **Automatic Transcription**: Utilizes Whisper's model to transcribe audio into text, complete with timestamps.
- **Subtitle File Creation**: Converts transcription results into the SRT subtitle format.
- **Translation**: Offers an option to translate subtitles using manual input or automated translation via the OpenAI GPT-4 API.
- **Subtitle Burning**: Embeds subtitles directly into the video, providing an option to burn both original and translated subtitles.
- **Generate Learning Material from video (TODO)**

## Update
- Added Groq inference for Whisper 


### Groq inference
Groq provides free and fast inference within a quota. Check out https://console.groq.com/playground. All you need to do is signing up and create an API key.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/tracywong117/AI-learning-material-from-video.git
   cd AI-learning-material-from-video
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Obtain an API key from OpenAI if you intend to use automated translation via GPT-4. Set this key in your environment variables or directly in your script securely.

## Usage
1. **Transcription and Subtitling**:
   - Modify the `input_video_file` path in the script to point to your video file.
   - Set `require_transcript` to `True` if transcription is needed; otherwise, it can load an existing transcript.
   - Set `require_burn_subtitle` to `True` if burning subtitle is needed.
   - Set `use_Groq` to `True` if you want to use Groq inference instead of local inference (Whisper)
   - Set `groq_api_key` to your Groq Api Key
   - Run the script to transcribe, translate (if using the API), and burn subtitles:
     ```bash
     python whisper-transcript-subtitling.py
     ```

2. **Translation and Subtitling**:
   - Ensure the transcript SRT file is named correctly and in the same directory as your script.
   - If using the GPT-4 API for translation, ensure `translate_option` is set to `"api"` and your API key is correctly configured.
   - Set `require_burn_subtitle` to `True` if burning subtitle is needed.
   - Run the script:
     ```bash
     python gpt-translate-subtitling.py
     ```

## Notes
- Review the subtitles for accuracy and synchronization issues after using the AI.

## Support
For issues, suggestions, or contributions, please open an issue or a pull request in this repository.
