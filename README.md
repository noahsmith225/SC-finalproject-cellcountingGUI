# Python-based GUI for Interactive Cell Analysis and Quantification

## Overview

This repository contains scripts for a Python-based GUI app designed for interactive cell analysis and quantification. The app streamlines the process of cell counting and analysis, providing wet lab scientists with a user-friendly interface to automate data collection.

### Codes:

1. **cell_counter_backend.py**:
    - Description: This script is an adaptation of a previous cell counting script by GitHub user ZachPenn's repository 'CellCounting'. It has been updated, optimized for speed, and adjusted to interface with a PyQt GUI.
    - Purpose: To perform image processing and cell counting for the GUI.

2. **GUI_frontend.py**:
    - Description: Implements the Python-based GUI using PySide2 framework. Integrates functionality from 'cell_counter_backend' for image processing and analysis.
    - Main Functionality:
        1. Selecting an image directory.
        2. Setting parameters for cell analysis.
        3. Processing images based on parameters.
        4. Displaying processed data in a QTableView within the GUI.
    - Input Parameters:
        - `diam` (diameter): Minimum size of objects for analysis.
        - `particle_min` (minimum size object): Minimum size of particles to include.
        - `UseWatershed`: Boolean to indicate watershed segmentation usage.
    - Results: Displayed in GUI providing insights into cell analysis.

3. **main.py**:
    - Description: Defines the user interface (UI) for the GUI using PySide2's QtWidgets module. Sets up widgets and layouts to create a functional interface.
    - Note: The architecture of the code was created with QT designer.

### Results:

The results displayed in the GUI provide insights into the cell analysis performed on the images. Each column represents a specific aspect of the analysis:

- AutoCount_Thresh: Threshold value automatically determined for cell counting.
- OTSU_Thresh: Threshold value calculated using Otsu's method for cell counting.
- Manual_CellDiam: Diameter manually specified for cell counting.
- Manual_Counts: Cell counts obtained through manual counting.
- AutoCount_UseWatershed: Boolean indicating whether watershed segmentation was used during automatic cell counting.
- AutoCount_Counts: Cell counts obtained through automatic counting.
- AutoCount_AvgCellArea: Average area of cells calculated during automatic counting.
- Acc_Manual_over_AutoCounts: Accuracy measure indicating the ratio of manual counts over automatic counts.

### Generated Files:

-`'SavedOutput' Subfolder`: subfolder in the specified directory containing the output cell count as a .tif file together with two .csv files:
  - `CellInfo.csv`: Contains the detailed results of cell analysis for each of the cells detected.
  - `summary.csv`: Summary of the cell analysis including counts and average cell areas.

## Usage

1. Run `GUI_frontend.py` to launch the GUI.
2. Select an image directory and set parameters.
3. Click submit to start the analysis.
4. View the results in the GUI.
5. Inspect output .csv files for further detail about the cell detection
