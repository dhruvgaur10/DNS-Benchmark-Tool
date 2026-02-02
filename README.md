
# DNS Analyzer Tool

A DNS benchmarking and analyzer tool developed using Python and PyQt5. This tool allows users to measure, compare, and analyze the performance of various DNS servers based on real-time latency and response data.

## Features

- Latency measurement for multiple DNS servers.
- Network ping check for connectivity validation.
- DNS recommendation based on real-time performance.
- Side-by-side comparison of tested DNS servers.
- Manual addition and testing of custom DNS servers.
- Graphical visualization of results using Matplotlib.
- Desktop interface built with PyQt5.
- Standalone executable provided for users who do not wish to install Python.

## Key Differentiators

- Complete graphical interface; no command-line interaction required.
- Real-time dynamic graph plotting for immediate visual feedback.
- DNS recommendations tailored to the user's actual network conditions.
- Fully standalone executable for easy distribution and usage.
- Demonstrates complete end-to-end development including GUI, networking, data visualization, and deployment.

## Requirements

1. PyQt5
2. Matplotlib

## Usage

### Option 1: Use Executable (No Python Required)

1. Download the file: `DNS Analyzer Tool.exe` from this repository.
2. Double-click the executable to launch the application.

### Option 2 (If Source Code Provided): Run from Source (Python Required)

1. Clone the repository.
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run:
```
python main.py
```

## Build Instructions (For Developers)

To generate a standalone executable using PyInstaller:

```
pyinstaller --onefile --windowed main.py
```

## Author

Dhruv Gaur
