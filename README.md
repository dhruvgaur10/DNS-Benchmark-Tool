# DNS-Benchmark-Tool

A DNS benchmarking and analyzer tool developed using Python and Tkinter. This tool allows users to measure, compare, and analyze the performance of various DNS servers based on real time latency and response data.

## Features

- Latency measurement for multiple DNS servers
- Network ping check for connectivity validation
- DNS recommendation based on real-time performance
- Side-by-side comparison of tested DNS servers
- Manual addition and testing of custom DNS servers
- Graphical visualization of results using Matplotlib
- Desktop interface built with Tkinter
- Automated system DNS configuration with elevated privileges
- PDF report generation using ReportLab
- Standalone executable for easy distribution

## Key Differentiators

- Complete graphical interface - no command line interaction required
- Real-time dynamic graph plotting for immediate visual feedback
- DNS recommendations tailored to user's actual network conditions
- One-click system DNS update using Windows network utilities (netsh & ipconfig)
- Fully standalone executable for easy distribution and usage
- End-to-end solution from analysis to system configuration

## Screenshot

<p align="center">
  <img src="screenshots/overview.png" alt="DNS Benchmark Tool" width="700">
</p>

## Tech Stack

- Python
- Tkinter
- Matplotlib
- ReportLab
- Socket
- Threading

## Requirements

- Python 3.8+
- Matplotlib
- Tkinter (included with standard Python installations)
- ReportLab

## Installation

```
git clone https://github.com/dhruvgaur10/DNS-Benchmark-Tool.git
cd DNS-Benchmark-Tool
pip install -r requirements.txt
```
## Usage
### Option 1: Run from Source
```
python main.py
```
Option 2: Use Executable
Download 'DNS Analyzer Tool.exe' from releases and run directly.

### Build Executable
```
pyinstaller --onefile --windowed main.py
```

## Author

Dhruv Gaur
