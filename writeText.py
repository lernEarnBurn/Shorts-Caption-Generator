from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import pysrt
from datetime import datetime

os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\ffmpeg.exe"

def add_caption_overlay(video_path, srt_path):
    video = VideoFileClip(video_path)

    subs = pysrt.open(srt_path)

    reference_date = datetime(1900, 1, 1)  

    clips = []

    for caption in subs:
        start_time = datetime.combine(reference_date, caption.start.to_time())
        end_time = datetime.combine(reference_date, caption.end.to_time())
        caption_text = caption.text_without_tags

        duration = end_time - start_time

        text = TextClip(caption_text, fontsize=40, color='white', font='Arial', method='caption')
        text = text.set_position(('center', 'bottom')).set_start(0).set_duration(duration.total_seconds())

        clips.append(text)

    final_clip = CompositeVideoClip([video] + clips)
    final_clip = final_clip.set_duration(video.duration)
    final_clip.write_videofile('./output/test.mp4', codec='libx264', audio_codec='aac')

if __name__ == "__main__":
    add_caption_overlay('./testVid.mp4', './srtFiles/testVid.srt')