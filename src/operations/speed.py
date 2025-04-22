from moviepy.editor import VideoFileClip
from moviepy.video.fx import all as vfx
import os
from ..utils.time_utils import parse_time, format_time


def change_playback_speed(video_path: str, speed: float, output_path: str):
    """
    Changes the playback speed of a video.

    Args:
        video_path (str): Path to the input video file.
        speed (float): The playback speed multiplier.
        output_path (str): Path to save the output video.

     Raises:
        FileNotFoundError: if input video file is not found
        Exception: if there is any error during the playback speed change
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    try:
        video = VideoFileClip(video_path)
        video_with_new_speed = video.fx(vfx.speedx, speed)
    except Exception as e:
        raise Exception(f"Error loading or modifying video: {e}")

    if video.audio:
        try:
            audio_with_new_speed = video.audio.set_fps(video.audio.fps * speed)
            video_with_new_speed = video_with_new_speed.set_audio(
                audio_with_new_speed)
        except Exception as e:
            raise Exception(f"Error changing the audio speed: {e}")
    try:
        video_with_new_speed.write_videofile(
            output_path, fps=60, codec="mpeg4", bitrate="8000k")
    except Exception as e:
        raise Exception(f"Error saving video: {e}")
    print(f"Video with {speed}x speed created at {output_path}")


def change_subtitle_speed(subtitle_path: str, speed: float, output_path: str):
    """
    Changes the timing of subtitles based on the given speed.

    Args:
        subtitle_path (str): Path to the input subtitle file (.srt).
        speed (float): The speed multiplier.
        output_path (str): Path to save the output subtitle file.

    Raises:
        FileNotFoundError: if subtitle file does not exist
        Exception: if there is any error during the subtitle speed change
    """
    if not os.path.exists(subtitle_path):
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")
    _speed = speed
    speed = 1 / _speed

    try:
        with open(subtitle_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                if '-->' in line:
                    start_time_str, end_time_str = line.strip().split(' --> ')
                    start_time = parse_time(start_time_str) * speed
                    end_time = parse_time(end_time_str) * speed
                    outfile.write(
                        f"{format_time(start_time)} --> {format_time(end_time)}\n")
                else:
                    outfile.write(line)
    except Exception as e:
        raise Exception(f"Error processing subtitle file: {e}")
    print(f"Subtitles with {speed}x speed created at {output_path}")
