from moviepy.editor import VideoFileClip, concatenate_videoclips, concatenate_audioclips
from moviepy.video.fx import all as vfx
# from moviepy.audio.fx import all as afx  # Not used in the provided code
from typing import Tuple, List, Any
import argparse
import os
from datetime import datetime, timedelta
import yaml
from src import (
    concat_videos,
    trim_video_by_intervals,
    cut_video_with_sliding_window,
    change_playback_speed,
    change_subtitle_speed,
    add_frozen_frame,
    load_config
)


def load_config(config_path: str) -> dict:
    """
    Loads the configuration from a YAML file.

    Args:
        config_path (str): The path to the YAML config file.

    Returns:
        dict: The configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        YAMLError: If there is an error in parsing the YAML file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML: {e}")


def time_to_seconds(time_str: str) -> float:
    """
    Converts a time string (MM:SS) to seconds.

    Args:
        time_str (str): Time string in the format MM:SS.

    Returns:
        float: Time in seconds.

    Raises:
         ValueError: If the time string is in invalid format
    """
    try:
        t = datetime.strptime(time_str, "%M:%S")
        return t.minute * 60 + t.second
    except ValueError as e:
        raise ValueError(
            f"Invalid time format {e}, time should be in format MM:SS")


def add_frozen_frame(video_path: str, freeze_time: float, freeze_duration: float, output_path: str, freeze_position: str):
    """
    Adds a frozen frame to a video at a specified position and duration.

    Args:
        video_path (str): Path to the input video file.
        freeze_time (float, optional): Time in seconds where to add the freeze frame.
            Required if `freeze_position` is set to 'middle'.
        freeze_duration (float): Duration of the frozen frame in seconds.
        output_path (str): Path to save the output video.
        freeze_position (str): Position to add the frozen frame:
            'beginning', 'end', or 'middle'.

     Raises:
        FileNotFoundError: if input video file does not exist
        ValueError: if freeze_position is middle, but no freeze time was given
        Exception: if there is any error during the process
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        raise Exception(f"Error when loading video: {e}")

    if freeze_position == 'beginning':
        freeze_time = 0.01
    elif freeze_position == 'end':
        freeze_time = video.duration - 0.01
    elif freeze_position == 'middle':
        if freeze_time is None:
            raise ValueError(
                "Please provide a freeze_time for 'middle' freeze_position")
    print(f"Freezing frame at {freeze_time}s for {freeze_duration}s...")
    try:
        frozen_frame = video.to_ImageClip(
            t=freeze_time).set_duration(freeze_duration)

        video_part1 = video.subclip(0, freeze_time)
        video_part2 = video.subclip(freeze_time)

        final_video = concatenate_videoclips(
            [video_part1, frozen_frame, video_part2])

    except Exception as e:
        raise Exception(f"Error creating a frozen frame {e}")

    try:
        final_video.write_videofile(
            output_path, codec="mpeg4", bitrate="8000k")
    except Exception as e:
        raise Exception(f"Error saving the video: {e}")

    print(
        f"Video with frozen frame at {freeze_time}s for {freeze_duration}s created at {output_path}")


def _segment_video_by_intervals(video_path: str, intervals: list) -> Tuple[List[Any], List[Any]]:
    """
    Cuts a video into subclips based on specified time intervals.

    Args:
        video_path (str): Path to the input video file.
        intervals (list): List of time intervals (tuples of start and end times in "MM:SS" format).

    Returns:
        Tuple[List[moviepy.editor.VideoFileClip], List[moviepy.editor.AudioClip]]:
            A tuple containing:
            - A list of video subclips
            - A list of audio subclips

     Raises:
         FileNotFoundError: If video file not found
        ValueError: if time intervals are not provided
        Exception: if there are any errors during the cut process
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        raise Exception(f"Error when loading video: {e}")

    subclips = []
    audio_clips = []
    if len(intervals) == 0:
        raise ValueError("Intervals must not be empty")

    for idx, (start_time, end_time) in enumerate(intervals):
        print(
            f"\nProcessing interval {idx + 1}/{len(intervals)}: {start_time} - {end_time}...")
        try:
            start_seconds = time_to_seconds(start_time)
            end_seconds = time_to_seconds(end_time)
            subclip = video.subclip(start_seconds, end_seconds)
            subclips.append(subclip)
            audio_clips.append(subclip.audio)
        except ValueError as e:
            raise e  # Re-raise the ValueError to be handled in the outer try-except block
        except Exception as e:
            raise Exception(f"Error cutting the video: {e}")

    return subclips, audio_clips


def trim_video_by_intervals(video_path: str, intervals: list, output_path: str = None, audio: bool = False):
    """
    Trims a video into parts based on intervals and saves or returns it.

    Args:
        video_path (str): Path to the input video file.
        intervals (list): List of time intervals (tuples of start and end times in "MM:SS" format).
        output_path (str, optional): Path to save the output video. If it's a directory, each subclip will be saved individually.
        audio (bool, optional): Whether to process audio (not implemented). Defaults to False.

     Raises:
        FileNotFoundError: if input video file not found
        ValueError: if output_path is not valid
        Exception: if there is any other error
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    print(f"Processing video {video_path}...")
    try:
        subclips, audio_clips = _segment_video_by_intervals(
            video_path, intervals)
    except Exception as e:
        raise e

    if output_path is not None:
        if os.path.isdir(output_path):
            try:
                for i, subclip in enumerate(subclips):
                    subclip.write_videofile(
                        os.path.join(output_path, f"{i}.mp4"), codec="libx264", bitrate="8000k")
            except Exception as e:
                raise Exception(f"Error when saving multiple video files: {e}")
        else:
            try:
                final_video = concatenate_videoclips(
                    subclips, method="compose")
                final_video.write_videofile(
                    output_path, codec="libx264", bitrate="8000k")
            except Exception as e:
                raise Exception(
                    f"Error saving the single concatenated video: {e}")
    else:
        final_video = concatenate_videoclips(subclips, method="compose")
        return final_video


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

    def parse_time(time_str):
        hours, minutes, seconds_milliseconds = time_str.split(':')
        seconds, milliseconds = seconds_milliseconds.split(',')
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

    def format_time(time_delta):
        hours, remainder = divmod(time_delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int(time_delta.microseconds / 1000)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

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


def process_video(config):
    """
    Processes a video based on the configuration provided.

    Args:
        config (dict): A dictionary containing video processing configurations.

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: If there is an error during video processing.
    """
    for operation, params in config.items():
        if operation == "concat_videos":
            video_paths = params.get("video_paths")
            output_path = params.get("output_path")

            if not video_paths:
                raise ValueError("Video path should be provided")
            try:
                concat_videos(video_paths, output_path)
            except Exception as e:
                raise Exception(f"Error with concatenate video: {e}")

        elif operation == "add_frozen_frame":
            video_path = params.get("video_path")
            freeze_time = params.get("freeze_time")
            freeze_duration = params.get("freeze_duration")
            output_path = params.get("output_path")
            freeze_position = params.get("freeze_position")

            if not all([video_path, freeze_duration, output_path, freeze_position]):
                raise ValueError(
                    "video_path, freeze_duration, output_path, and freeze_position must be specified")
            try:
                add_frozen_frame(video_path, freeze_time,
                                 freeze_duration, output_path, freeze_position)
            except Exception as e:
                raise Exception(f"Error with frozen frame: {e}")

        elif operation == "trim_video_by_intervals":
            video_path = params.get("video_path")
            intervals = params.get("intervals")
            output_path = params.get("output_path")
            if not all([video_path, intervals]):
                raise ValueError(
                    "video_path and intervals must be specified")
            try:
                trim_video_by_intervals(video_path, intervals, output_path)
            except Exception as e:
                raise Exception(f"Error with cut video: {e}")

        elif operation == "cut_video_with_sliding_window":
            video_path = params.get("video_path")
            window_length = params.get("window_length")
            slide_step = params.get("slide_step")
            start_time = params.get("start_time", 0)
            end_time = params.get("end_time")
            output_dir = params.get("output_dir")

            if not all([video_path, window_length, slide_step]):
                raise ValueError(
                    "video_path, window_length, and slide_step must be specified")
            try:
                cut_video_with_sliding_window(
                    video_path, window_length, slide_step, start_time, end_time, output_dir)
            except Exception as e:
                raise Exception(f"Error with sliding window cut: {e}")

        elif operation == "change_playback_speed":
            video_path = params.get("video_path")
            speed = params.get("speed")
            output_path = params.get("output_path")
            if not all([video_path, speed, output_path]):
                raise ValueError(
                    "video_path, speed, and output_path must be specified")
            try:
                change_playback_speed(video_path, speed, output_path)
            except Exception as e:
                raise Exception(f"Error with change playback speed: {e}")

        elif operation == "change_subtitle_speed":
            subtitle_path = params.get("subtitle_path")
            speed = params.get("speed")
            output_path = params.get("output_path")
            if not all([subtitle_path, speed, output_path]):
                raise ValueError(
                    "subtitle_path, speed, and output_path must be specified")
            try:
                change_subtitle_speed(subtitle_path, speed, output_path)
            except Exception as e:
                raise Exception(f"Error with change subtitle speed: {e}")


if __name__ == "__main__":
    config_file = "config.yaml"
    try:
        config = load_config(config_file)
        print(f"Processing video with config:\n{config}")
        process_video(config)
    except Exception as e:
        print(f"Error: {e}")
