from moviepy import VideoFileClip, concatenate_videoclips
import os


def concat_videos(video_paths: list, output_path: str = None):
    """
    Concatenates multiple video files into a single video.

    Args:
        video_paths (list): List of video file paths.
        output_path (str, optional): Output file path. If None, the concatenated
            clip is returned rather than written. Defaults to None.

    Returns:
         moviepy.editor.VideoFileClip: concatenated video file if output path is none

    Raises:
        FileNotFoundError: if video files in video_path does not exist
        Exception: If there is an error during the concatenating process
    """
    videos = []
    for video_path in video_paths:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        try:
            videos.append(VideoFileClip(video_path))
        except Exception as e:
            raise Exception(f"Error when loading video clip: {e}")
    final_clip = concatenate_videoclips(videos)
    if output_path is None:
        return final_clip
    try:
        final_clip.write_videofile(
            output_path, codec="libx264", bitrate="8000k")
    except Exception as e:
        raise Exception(f"Error while saving: {e}")
