from datetime import datetime, timedelta


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


def parse_time_with_end(time_str: str, video_duration: float = None) -> float:
    """
    Parses a time string that can include "end" as a special keyword.

    Args:
        time_str (str): Time string in format MM:SS or "end"
        video_duration (float, optional): Video duration in seconds. Required if time_str is "end".

    Returns:
        float: Time in seconds

    Raises:
        ValueError: If time_str is "end" but video_duration is not provided
        ValueError: If time_str is not in valid format
    """
    if time_str.lower() == "end":
        if video_duration is None:
            raise ValueError(
                "video_duration must be provided when using 'end'")
        return video_duration

    # Try to parse as MM:SS format
    try:
        return time_to_seconds(time_str)
    except ValueError:
        raise ValueError(
            f"Invalid time format: {time_str}. Use MM:SS format or 'end'")


def parse_time(time_str: str) -> timedelta:
    """
    Parses a time string in format HH:MM:SS,mmm to timedelta.

    Args:
        time_str (str): Time string in format HH:MM:SS,mmm

    Returns:
        timedelta: Time as timedelta object
    """
    hours, minutes, seconds_milliseconds = time_str.split(':')
    seconds, milliseconds = seconds_milliseconds.split(',')
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))


def format_time(time_delta: timedelta) -> str:
    """
    Formats a timedelta to string in format HH:MM:SS,mmm.

    Args:
        time_delta (timedelta): Time as timedelta object

    Returns:
        str: Formatted time string
    """
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(time_delta.microseconds / 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"
