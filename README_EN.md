# Ant blueCFD

[中文](README.md)

## Introduction

Ant blueCFD is a Grasshopper-based plug-in for the blueCFD AIR software. It converts geometries created in Rhino/Grasshopper to the format required by blueCFD AIR and helps run simulations and extract results.

![ScreenShot](./resources/01.png)

## Features

- Convert Grasshopper geometry into blueCFD geometry;
- Visualize models with different colors for distinct components;
- Call the locally installed blueCFD AIR software for simulations;
- Extract and decompress results for post-processing, e.g., in Paraview.

## Installation

1. Install blueCFD AIR.
2. Install blueCFD Core.
3. Install Rhino 7.
4. Run `ant_blueCFDInstaller.exe` to install the plug-in.

## Usage

1. Launch Grasshopper inside Rhino.
2. Build your model and export it using the Ant blueCFD components.
3. Run the simulation in blueCFD AIR.
4. Post-process the extracted results with tools such as Paraview.

## Notes

This project has not been extensively tested on other machines, so you may encounter environment-specific issues. Bug reports are welcome, and a detailed demonstration is available in a video on YouTube.

