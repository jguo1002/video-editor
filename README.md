# Video Editor

A Python-based video editing tool that provides various operations for video processing, including cutting, concatenation, speed adjustment, and more.

## Features

- **Video Cutting**: Cut videos into overlapping clips using a sliding window approach
- **Video Concatenation**: Combine multiple videos into a single output
- **Speed Adjustment**: Change video playback speed and subtitle timing
- **Frozen Frames**: Add frozen frames at specific timestamps
- **Interval Trimming**: Trim videos based on specific time intervals
- **Configurable Operations**: All operations can be configured via YAML files

## Project Structure

```
video_editor/
├── src/
│   ├── __init__.py
│   ├── operations/
│   │   ├── concatenation.py
│   │   ├── trimming.py
│   │   ├── speed.py
│   │   └── frozen_frame.py
│   └── utils/
│       ├── time_utils.py
│       └── config.py
├── main.py
├── config.yaml
├── config_example.yaml
└── requirements.txt
```

## Requirements

- Python 3.8+
- FFmpeg
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd video_editor
```

2. Install FFmpeg:
- On macOS: `brew install ffmpeg`
- On Ubuntu/Debian: `sudo apt-get install ffmpeg`
- On Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Configure your video operations in `config.yaml`:
```yaml
cut_video_with_sliding_window:
  video_path: "input.mp4"
  window_length: 10
  slide_step: 3
  start_time: "01:00"  # Format: MM:SS
  end_time: "07:35"    # Format: MM:SS
  output_dir: "output_clips"
```

2. Run the main script:
```bash
python main.py
```

## Configuration Examples

### Cutting Videos
```yaml
cut_video_with_sliding_window:
  video_path: "input.mp4"
  window_length: 10
  slide_step: 3
  start_time: "01:00"
  end_time: "07:35"
  output_dir: "output_clips"
```

### Concatenating Videos
```yaml
concat_videos:
  video_paths:
    - "video1.mp4"
    - "video2.mp4"
  output_path: "combined.mp4"
```

### Adding Frozen Frames
```yaml
add_frozen_frame:
  video_path: "input.mp4"
  freeze_time: "02:30"
  freeze_duration: 3
  output_path: "frozen.mp4"
  freeze_position: "end"
```

### Trimming Videos
```yaml
trim_video_by_intervals:
  video_path: "input.mp4"
  intervals:
    - start: "00:00"
      end: "01:30"
    - start: "02:00"
      end: "03:30"
  output_path: "trimmed.mp4"
```

### Speed Adjustment
```yaml
change_playback_speed:
  video_path: "input.mp4"
  speed: 1.5
  output_path: "sped_up.mp4"

change_subtitle_speed:
  video_path: "input.mp4"
  speed: 1.5
  output_path: "adjusted_subs.mp4"
```

## Notes

- All time values should be in MM:SS format (e.g., "01:30" for 1 minute and 30 seconds)
- Make sure you have sufficient disk space for output files
- For large videos, processing might take some time
- Check the `config_example.yaml` file for more configuration examples

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.