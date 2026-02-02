# DNS-Benchmark-Tool

A DNS benchmarking and analyzer tool developed using Python and Tkinter. This tool allows users to measure, compare, and analyze the performance of various DNS servers based on real time latency and response data.

## Features

- Latency measurement for multiple DNS servers
- Network ping check for connectivity validation
- DNS recommendation based on real-time performance
- Side-by-side comparison and manual testing of custom DNS servers
- Real-time graphical visualization using Matplotlib
- Desktop GUI built with Tkinter - no command line required
- One-click system DNS update using Windows utilities (netsh & ipconfig)
- PDF report generation using ReportLab
- Standalone executable for easy distribution

## Screenshot

<p align="center">
  <img src="screenshots/overview.png" alt="DNS Benchmark Tool" width="700">
</p>

## Tech Stack

`Python` `Tkinter` `Matplotlib` `ReportLab` `Socket` `Threading`

## Requirements

- Python 3.8+
- Matplotlib
- ReportLab

## Installation
```
git clone https://github.com/dhruvgaur10/DNS-Benchmark-Tool.git
cd DNS-Benchmark-Tool
pip install -r requirements.txt
```
## Usage

### Run from Source
```
python main.py
```
### Use Executable
Download `DNS Analyzer Tool.exe` from releases and run directly.

### Build Executable
```
pyinstaller --onefile --windowed main.py
```
## Author

Dhruv Gaur