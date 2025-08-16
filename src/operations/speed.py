from moviepy import VideoFileClip, concatenate_videoclips
import os
from ..utils.time_utils import parse_time, format_time, time_to_seconds, parse_time_with_end


def change_playback_speed(
    video_path: str,
    speed: float,
    output_path: str,
    intervals: list = None
):
    """
    Changes the playback speed of a video or specific intervals within the video.

    Args:
        video_path (str): Path to the input video file.
        speed (float): The playback speed multiplier.
        output_path (str): Path to save the output video.
        intervals (list, optional): List of time intervals to apply speed change.
            Each interval should be a list of two time strings [start, end].
            If None, applies speed change to entire video.

    Raises:
        FileNotFoundError: if input video file is not found
        Exception: if there is any error during the playback speed change
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    try:
        video = VideoFileClip(video_path)

        if intervals is None:
            # Apply speed change to entire video
            video_with_new_speed = video.with_speed_scaled(speed)
        else:
            # Apply speed change only to specified intervals
            clips = []
            current_time = 0

            for interval in intervals:
                start_time, end_time = interval
                start_seconds = time_to_seconds(start_time)
                end_seconds = parse_time_with_end(end_time, video.duration)

                # Add the part before the interval (normal speed)
                if start_seconds > current_time:
                    normal_clip = video.subclipped(current_time, start_seconds)
                    clips.append(normal_clip)

                # Add the interval with modified speed
                interval_clip = video.subclipped(start_seconds, end_seconds)
                speeded_clip = interval_clip.with_speed_scaled(speed)
                clips.append(speeded_clip)

                current_time = end_seconds

            # Add the remaining part after the last interval (normal speed)
            if current_time < video.duration:
                remaining_clip = video.subclipped(current_time, video.duration)
                clips.append(remaining_clip)

            # Concatenate all clips
            video_with_new_speed = concatenate_videoclips(clips)

        # Handle audio if present
        if video.audio:
            try:
                if intervals is None:
                    # For entire video speed change
                    audio_with_new_speed = video.audio.with_speed_scaled(speed)
                    video_with_new_speed = video_with_new_speed.with_audio(
                        audio_with_new_speed)
                else:
                    # For interval-based speed change, audio timing needs to be adjusted
                    # This is complex and may not work perfectly with moviepy
                    # For now, we'll keep the original audio
                    pass
            except Exception as e:
                print(
                    f"Warning: Could not process audio for speed change: {e}")

        # Write the output video
        video_with_new_speed.write_videofile(
            output_path, fps=60, codec="mpeg4", bitrate="8000k")

        # Clean up
        video.close()
        video_with_new_speed.close()

        if intervals:
            print(
                f"Video with {speed}x speed applied to intervals created at {output_path}")
        else:
            print(f"Video with {speed}x speed created at {output_path}")

    except Exception as e:
        raise Exception(f"Error processing video: {e}")


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
