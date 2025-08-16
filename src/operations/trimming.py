from moviepy import VideoFileClip, concatenate_videoclips
import os
from typing import List, Tuple, Any
from ..utils.time_utils import time_to_seconds, parse_time_with_end


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
            end_seconds = parse_time_with_end(end_time, video.duration)
            subclip = video.subclipped(start_seconds, end_seconds)
            subclips.append(subclip)
            audio_clips.append(subclip.audio)
        except ValueError as e:
            raise e
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


def cut_video_with_sliding_window(video_path: str, window_length: float, slide_step: float,
                                  start_time: str = "00:00", end_time: str = None, output_dir: str = None):
    """
    Cuts a video into clips using a sliding window approach.

    Args:
        video_path (str): Path to the input video file.
        window_length (float): Length of each clip in seconds.
        slide_step (float): Step size for sliding window in seconds.
        start_time (str, optional): Start time in MM:SS format. Defaults to "00:00".
        end_time (str, optional): End time in MM:SS format. If None, uses video duration.
        output_dir (str, optional): Directory to save output clips. If None, returns clips.

    Returns:
        List[moviepy.editor.VideoFileClip]: List of video clips if output_dir is None.

    Raises:
        FileNotFoundError: If video file not found
        ValueError: If window_length or slide_step is invalid, or if time format is invalid
        Exception: If there are any errors during processing
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if window_length <= 0 or slide_step <= 0:
        raise ValueError("window_length and slide_step must be positive")

    if window_length < slide_step:
        raise ValueError(
            "window_length must be greater than or equal to slide_step")

    try:
        video = VideoFileClip(video_path)

        # Convert start_time from MM:SS to seconds
        start_seconds = time_to_seconds(start_time)

        # Convert end_time from MM:SS to seconds if provided, otherwise use video duration
        if end_time is not None:
            end_seconds = parse_time_with_end(end_time, video.duration)
        else:
            end_seconds = video.duration

        if start_seconds < 0 or end_seconds > video.duration:
            raise ValueError("Invalid start_time or end_time")

        clips = []
        current_time = start_seconds

        while current_time + window_length <= end_seconds:
            clip = video.subclipped(current_time, current_time + window_length)
            clips.append(clip)
            current_time += slide_step

        if output_dir is not None:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for i, clip in enumerate(clips):
                output_path = os.path.join(output_dir, f"clip_{i}.mp4")
                clip.write_videofile(
                    output_path, codec="libx264", bitrate="8000k")
            return None
        else:
            return clips

    except Exception as e:
        raise Exception(f"Error processing video: {e}")
    finally:
        if 'video' in locals():
            video.close()
