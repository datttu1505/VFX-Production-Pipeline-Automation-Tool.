# VFX Production Pipeline Automation Tool

A Python-based automation tool for VFX production pipelines that processes Baselight and Xytech workstation data, matches frame ranges with file locations, generates timecodes with handle padding, and creates Excel reports with video thumbnails.

## Description

This tool streamlines the VFX production workflow by automating the tedious process of matching render file locations with frame ranges from color grading sessions. It bridges the gap between Xytech workstation paths and Baselight frame data, converting frame numbers to timecodes and generating visual thumbnails for quick reference.

**Key Features:**
- **Intelligent Path Matching**: Automatically matches Xytech file system paths with Baselight frame sequences
- **Frame Range Consolidation**: Combines consecutive frames into ranges and adds 48-frame handles for conform
- **Timecode Conversion**: Converts frame numbers to SMPTE timecode format (HH:MM:SS:FF at 24fps)
- **Video Thumbnail Generation**: Extracts thumbnails from video at specific timecodes using FFmpeg
- **MongoDB Integration**: Stores and manages production data in MongoDB collections
- **Excel Export**: Generates formatted Excel reports with embedded thumbnails for client review

## Use Case

In VFX production, colorists work with Baselight systems that reference frames from network storage (e.g., `/baselightfilesystem1/`), while render farms and workstations use different path structures (e.g., `/hpsans13/production/`). This tool reconciles these differences, identifies which frames were worked on, adds appropriate handles, and generates client-ready reports with visual references.

## Requirements

### Software Dependencies
- Python 3.7+
- MongoDB (local or remote instance)
- FFmpeg (for thumbnail generation)

### Python Packages
```bash
pip install pymongo openpyxl
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/vfx-pipeline-tool.git
cd vfx-pipeline-tool
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg:**
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

4. **Start MongoDB:**
```bash
# macOS/Linux
mongod --dbpath /path/to/your/db

# Or use MongoDB service
sudo systemctl start mongod
```

## Usage

### Step 1: Import Source Files

Import Xytech workstation paths and Baselight frame data into MongoDB:

```bash
python script.py --xytech Xytech.txt --baselight Baselight_export.txt
```

**Input File Formats:**

*Xytech.txt* - Network paths (one per line):
```
/hpsans13/production/reel1/partA/1920x1080
/hpsans13/production/reel1/partB/1920x1080
```

*Baselight_export.txt* - Baselight paths with frame numbers:
```
/baselightfilesystem1/reel1/partA/1920x1080 1001 1002 1003 1005 1006
/baselightfilesystem1/reel1/partB/1920x1080 2001 2002 2003
```

### Step 2: Process and Match Data

Match locations, consolidate frames, add handles, and generate thumbnails:

```bash
python script.py --process
```

This command will:
- Match Xytech paths with Baselight frame sequences
- Create frame ranges from consecutive frames
- Add 48-frame handles before and after each range
- Convert frame ranges to timecodes
- Extract video thumbnails at each timecode
- Store results in MongoDB's `processed` collection

**Note:** Update `VIDEO_PATH` variable in the script to point to your video file.

### Step 3: Export to Excel

Generate a formatted Excel report with thumbnails:

```bash
# Export with auto-generated filename
python script.py --export

# Export with custom filename
python script.py --export my_report.xlsx
```

The Excel file includes:
- Location: Full Xytech path to the asset
- Frames: Frame ranges with 48-frame handles (e.g., "953-1054")
- Timecode: SMPTE timecode ranges (e.g., "00:00:39:17 to 00:00:43:22")
- Thumbnail: Visual reference extracted from the video

## Configuration

### MongoDB Settings

Change database name or connection URI:
```bash
python script.py --db-name my_database --mongo-uri mongodb://localhost:27017/
```

### Video Path

Edit the `VIDEO_PATH` constant in `script.py`:
```python
VIDEO_PATH = "path/to/your/video.mov"
```

## Database Collections

The tool creates three MongoDB collections:

- **xytech**: Stores filtered Xytech workstation paths
- **baselight**: Stores Baselight paths with frame numbers
- **processed**: Stores matched results with timecodes and thumbnail paths

## Example Workflow

```bash
# 1. Import source data
python script.py --xytech Xytech.txt --baselight Baselight_export.txt

# 2. Process and generate thumbnails
python script.py --process

# 3. Export to Excel for client review
python script.py --export client_review.xlsx
```

## Frame Padding Explained

The tool automatically adds **48 frames of padding** (2 seconds at 24fps) before and after each frame range. This provides handles for editorial conforming and transitions.

**Example:**
- Original frames: `1001-1010`
- With padding: `953-1058` (48 frames before + 10 frames + 48 frames after)

## Timecode Conversion

Timecodes are calculated at **24 frames per second**:
- Frame 0 = `00:00:00:00`
- Frame 1001 = `00:00:41:17`
- Frame 2000 = `00:01:23:08`

## Troubleshooting

**MongoDB Connection Error:**
```
Ensure MongoDB is running: sudo systemctl status mongod
Check connection URI matches your setup
```

**FFmpeg Not Found:**
```
Install FFmpeg and ensure it's in your system PATH
Verify: ffmpeg -version
```

**Video File Not Found:**
```
Update VIDEO_PATH in script.py with correct path
Ensure video file is accessible
```

**Thumbnail Generation Fails:**
```
Check video codec compatibility with FFmpeg
Verify timecodes are within video duration
Ensure sufficient disk space for temp thumbnails
```

## Output Example

**Console Output:**
```
Processing Results:
  Matched locations: 5
  Unmatched locations: 0
  Total entries created: 5

Processed Results:
Location                                                              Frames               Timecode
--------------------------------------------------------------------------------
/hpsans13/production/reel1/partA/1920x1080                           953-1054             00:00:39:17 to 00:00:43:22
/hpsans13/production/reel1/partB/1920x1080                           1953-2051            00:01:21:09 to 00:01:25:11

Generating thumbnails...
  [1/5] Generated thumbnail for 00:00:39:17
  [2/5] Generated thumbnail for 00:01:21:09
...
Generated 5/5 thumbnails

Exported 5 records to: processed_results_20260101_143022.xlsx
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for VFX production pipelines
- Supports Baselight color grading workflows
- Integrates with Xytech workstation management systems

## Contact

For questions or support, please open an issue on GitHub.

---

**Note:** This tool is designed for professional VFX production environments. Ensure you have appropriate permissions to access network storage paths and video files in your facility.