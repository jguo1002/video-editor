from moviepy.editor import VideoFileClip, concatenate_videoclips
import os


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
