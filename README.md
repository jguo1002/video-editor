# Video Editor Script

This Python script uses the `moviepy` library to perform various video editing tasks, including concatenating videos, adding frozen frames, trimming videos by intervals, changing playback speed, and modifying subtitle timings. It uses a YAML file for easy configuration.

## Requirements

- Python 3.6 or higher
- `moviepy` library
- `PyYAML` library

## Setup

### Using Conda (Recommended)

1.  **Create a Conda environment:**
    ```bash
    conda create -n video_editor python=3.9
    conda activate video_editor
    ```
    You can change `video_editor` to any name you prefer.

2.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Using Pip

1.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

2.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Save the script:** Save the provided Python code as `main.py`.
2.  **Prepare your files:** Make sure you have your video files (e.g., `.mp4`) and subtitle files (e.g., `.srt`) in the same folder as the script or specify the correct paths in the configuration file.
3.  **Configure the script:**
    - The script uses a YAML file (`config.yaml`) to define the editing process.
    - Place `config.yaml` in the same directory as `main.py`. You can change the config file name but make sure the name is consistent in the main file.
    - The `config.yaml` file allows you to specify multiple video editing operations. See the example below for how to use it.
4.  **Run the script:** Open your terminal, navigate to the folder containing the script, and run:
    ```bash
    python main.py
    ```
    This will apply the configurations specified in `config.yaml`, and output the edited videos/subtitles.

### Example Configuration (`config.yaml`)

```yaml
# Example configuration file
concat_videos:
    video_paths: ["input1.mp4", "input2.mp4"]
    output_path: "output_concat.mp4"
add_frozen_frame:
    video_path: "input.mp4"
    freeze_time: 10
    freeze_duration: 5
    output_path: "output_freeze.mp4"
    freeze_position: "middle" #can be beginning, middle or end
trim_video_by_intervals:
    video_path: "input.mp4"
    intervals:
      - ["00:10", "00:20"]
      - ["00:30", "00:40"]
    output_path: "output_trim.mp4" # or you can pass a folder to cut into multiple parts
change_playback_speed:
  video_path: "input.mp4"
  speed: 2 # 2x faster
  output_path: "output_speed.mp4"
change_subtitle_speed:
    subtitle_path: "input.srt"
    speed: 0.5 # 0.5x slower
    output_path: "output_subtitle.srt"