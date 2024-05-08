
# Python-based GUI for Interactive Cell Analysis and Quantification
This is a script that builds upon a previous repository by ZachPenn called "CellCounting." The goal of the project was to make a pipeline version of the code to streamline and simplify automatic cell counting for wet lab researchers who are not comfortable interfacing with code.

## Overview
Cell counting is an important technique in a range of experimental disciplines related to liquid cell culture and tissue analysis. Accurate manual cell counting is tedious and time consuming, but there are many automatic image processing packages that serve to streamline this process. The backend of this script makes use of image pre-processing by median filter and Gaussian blur followed by a Watershed segmentation algorithm to achieve accurate (>90%) counting of crowded tissue images. 

In the backend, this script repairs deprecated code from the "CellCounting" repository and builds upon it by automating the optimization --> data processing pipeline by pre-selecting the best parameters for average cell diameter and threshold. The other significant feature is a GUI that allows users to select working directories and minimum particle size cutoffs without interfacing with raw code, and further allowing the user to visualize their results within the applet. As written, the code can only handle one channel but could be updated in the future to handle multichannel counting and overlap correction.

## User guide

### Preparing files to run the script
The program relies on a specific subdirectory naming scheme as represented in the example **Template.zip**. A composite image to be used for optimizing parameters should be placed in the "Composite" subdirectory. A manually counted mask of that composite image (prepared by ImageJ or another method of your choice) should be placed in the "ManualCounts" subdirectory. Finally, all of the cell images that you wish to be counted should be placed in the "Ch1" subdirectory.

### Running the script
As long as all the necessary packages and dependencies inidicated in the `requirements.txt` file are downloaded the script can be run from any directory. Simply follow the GUI instructions to select a path for analysis, select a minimum particle size (we recommend 0.05, but this will depend on your composite image and the experimental images you're counting), and decide whether or not to use Watershed segmentation (recommended). 


### Note for future improvement
Due to an apparent difference in float handling between Python 3.11 (where the backend was written) and Python 3.9 (where the front end was written), the GUI-based algorithm can only accept minimum particle values ≥ 0.5. Since a version of PySide2 is not yet available for Python 3.11, the FrontEnd cannot handle smaller minimum cell area thresholds, which may temporarily limit the accuracy of the counter.

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
  - `SavedOutput/Ch1/filename_cellinfo.csv`: Contains the detailed results of cell analysis for each of the cells detected.
  - `SavedOutput/Ch1_Counts.csv`: Summary of the cell analysis including counts and average cell areas.

## Usage

1. Run `GUI_frontend.py` to launch the GUI.
2. Select an image directory and set parameters.
3. Click submit to start the analysis.
4. View the results in the GUI.
5. Inspect output .csv files for further detail about the cell detection

## Contributors
This code was written in collaboration between: <br />
Valentina Matos Romero: vmatosr1@jh.edu  <br />
Noah Smith: nsmit132@jh.edu

=======
