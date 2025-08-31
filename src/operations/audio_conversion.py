from moviepy import VideoFileClip
import os
from typing import Optional


def convert_video_to_audio(
    video_path: str,
    output_path: str,
    audio_format: str = "mp3",
    audio_codec: str = "mp3",
    bitrate: str = "192k",
    verbose: bool = True
) -> None:
    """
    Converts MP4 video to audio format (MP3 by default).

    Args:
        video_path (str): Path to the input video file.
        output_path (str): Path to save the output audio file.
        audio_format (str): Output audio format (mp3, wav, etc.). Defaults to "mp3".
        audio_codec (str): Audio codec to use. Defaults to "mp3".
        bitrate (str): Audio bitrate (e.g., "128k", "192k", "320k"). Defaults to "192k".
        verbose (bool): Whether to print progress information. Defaults to True.

    Raises:
        FileNotFoundError: If input video file not found.
        ValueError: If output path is invalid or audio format is unsupported.
        Exception: If there is any error during the conversion process.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Validate output path
    if not output_path:
        raise ValueError("Output path must be specified")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Validate audio format
    supported_formats = ["mp3", "wav", "ogg", "aac", "m4a"]
    if audio_format.lower() not in supported_formats:
        raise ValueError(
            f"Unsupported audio format: {audio_format}. Supported formats: {supported_formats}")

    video = None
    try:
        if verbose:
            print(f"Loading video: {video_path}")

        # Load the video file
        video = VideoFileClip(video_path)

        if verbose:
            print(f"Video duration: {video.duration:.2f} seconds")
            print(f"Converting to {audio_format.upper()}...")

        # Extract audio and save
        audio = video.audio
        if audio is None:
            raise Exception("No audio track found in the video")

        # Write audio file
        audio.write_audiofile(
            output_path,
            codec=audio_codec,
            bitrate=bitrate,
            logger=None if not verbose else "bar"
        )

        if verbose:
            print(f"Audio conversion completed: {output_path}")

    except Exception as e:
        raise Exception(f"Error during audio conversion: {e}")
    finally:
        # Clean up resources
        if video is not None:
            video.close()


def extract_audio_segment(
    video_path: str,
    output_path: str,
    start_time: float = 0.0,
    end_time: Optional[float] = None,
    audio_format: str = "mp3",
    audio_codec: str = "mp3",
    bitrate: str = "192k",
    verbose: bool = True
) -> None:
    """
    Extracts a specific segment of audio from a video file.

    Args:
        video_path (str): Path to the input video file.
        output_path (str): Path to save the output audio file.
        start_time (float): Start time in seconds. Defaults to 0.0.
        end_time (float, optional): End time in seconds. If None, uses video duration.
        audio_format (str): Output audio format. Defaults to "mp3".
        audio_codec (str): Audio codec to use. Defaults to "mp3".
        bitrate (str): Audio bitrate. Defaults to "192k".
        verbose (bool): Whether to print progress information. Defaults to True.

    Raises:
        FileNotFoundError: If input video file not found.
        ValueError: If time parameters are invalid.
        Exception: If there is any error during the extraction process.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if start_time < 0:
        raise ValueError("start_time must be non-negative")

    video = None
    video_segment = None
    try:
        if verbose:
            print(f"Loading video: {video_path}")

        # Load the video file
        video = VideoFileClip(video_path)

        # Validate time parameters
        if end_time is None:
            end_time = video.duration
        elif end_time > video.duration:
            raise ValueError(
                f"end_time ({end_time}) exceeds video duration ({video.duration})")
        elif end_time <= start_time:
            raise ValueError("end_time must be greater than start_time")

        if verbose:
            print(
                f"Extracting audio from {start_time:.2f}s to {end_time:.2f}s...")

        # Extract the specified segment using the correct MoviePy method
        video_segment = video.subclipped(start_time, end_time)
        audio = video_segment.audio

        if audio is None:
            raise Exception("No audio track found in the video segment")

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write audio file
        audio.write_audiofile(
            output_path,
            codec=audio_codec,
            bitrate=bitrate,
            logger=None if not verbose else "bar"
        )

        if verbose:
            print(f"Audio segment extracted: {output_path}")

    except Exception as e:
        raise Exception(f"Error during audio extraction: {e}")
    finally:
        # Clean up resources
        if video is not None:
            video.close()
        if video_segment is not None:
            video_segment.close()


def create_test_video_with_audio(
    output_path: str = "test_video_with_audio.mp4",
    duration: float = 10.0,
    verbose: bool = True
) -> str:
    """
    Creates a test video with audio for testing purposes.

    Args:
        output_path (str): Path to save the test video.
        duration (float): Duration of the test video in seconds.
        verbose (bool): Whether to print progress information.

    Returns:
        str: Path to the created test video.

    Raises:
        Exception: If there is any error during video creation.
    """
    try:
        from moviepy import VideoFileClip, AudioFileClip
        import numpy as np

        if verbose:
            print(f"Creating test video with audio: {output_path}")

        # Create a simple video (black frame)
        from moviepy.video.VideoClip import ColorClip
        video = ColorClip(size=(640, 480), color=(0, 0, 0), duration=duration)
        video.fps = 24

        # Create a simple audio (sine wave)
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * 440 * t) * 0.3  # 440 Hz sine wave

        # Convert to audio clip
        from moviepy.audio.AudioClip import AudioArrayClip
        audio = AudioArrayClip(audio_data.reshape(-1, 1), fps=sample_rate)

        # Combine video and audio using the correct method
        final_video = video.with_audio(audio)

        # Write video file
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            logger=None if not verbose else "bar"
        )

        if verbose:
            print(f"Test video created successfully: {output_path}")

        return output_path

    except Exception as e:
        raise Exception(f"Error creating test video: {e}")
    finally:
        # Clean up resources
        if 'video' in locals():
            video.close()
        if 'audio' in locals():
            audio.close()
        if 'final_video' in locals():
            final_video.close()
