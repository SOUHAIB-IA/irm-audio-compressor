# IRM Audio Compression Project

## Overview

The **IRM Audio Compression Project** is a custom audio encoding and playback tool designed to work with a new `.irm` audio format. This format is based on compression algorithms, specifically the **LZW (Lempel-Ziv-Welch)** encoding technique, to reduce audio file sizes while maintaining quality. The project includes functions to convert standard audio files (e.g., `.mp3`, `.wav`) to the `.irm` format and vice versa, along with an audio player for playback.

## Project Structure

- **Sample Files**:
  - `Free_Test_Data_1MB_MP3.mp3`: Example MP3 audio file.
  - `Free_Test_Data_1MB_MP3.irm`: Compressed IRM file generated from the MP3 file.
  - `Free_Test_Data_2MB_WAV.wav`: Example WAV audio file.
  - `amazing-grace-129645.mp3`: Additional MP3 file for testing.

- **Scripts**:
  - `main.py`: Contains the main encoding and decoding logic for `.irm` files.
  - `main.ipynb`: Jupyter Notebook to test and demonstrate encoding and decoding functionalities interactively.

- **Dependencies**:
  - `requirements.txt`: Lists the Python packages required to run the project.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/irm-audio-compression.git
   cd irm-audio-compression
   ```

## Usage

1. **Run the Script**:
   To encode or decode audio files, execute the main script:
   ```bash
   python main.py
   ```

2. **Convert Audio to IRM Format**:
   - Load an audio file (MP3/WAV) and use the provided functions to compress it into the `.irm` format.
   
3. **Play IRM Files**:
   - The script includes decoding functionality for `.irm` files so they can be played or analyzed.

## Key Functionalities

- **Encoding**:
  - Compress audio data using the LZW algorithm and save it in `.irm` format.
  
- **Decoding and Playback**:
  - Decode `.irm` files back to playable audio.

## Skills and Learning Outcomes

- **Audio Compression**: Practical application of LZW compression.
- **Python Scripting**: Encapsulation of encoding and decoding functions in Python.
- **Audio Libraries**: `pygame`, `pydub`, and `sounddevice` for audio handling.
- **Jupyter Notebooks**: Documentation and demonstration of functions in `main.ipynb`.

## Future Improvements

- **Algorithm Exploration**: Implement additional compression algorithms.
- **Multi-format Support**: Extend functionality to more audio types.
- **Enhanced Player**: Build a full-featured player with GUI for `.irm` files.
