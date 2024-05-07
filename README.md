# SC-finalproject-cellcountingGUI
This is a script that builds upon a previous repository by ZachPenn called "CellCounting." The goal of the project was to make a pipeline version of the code to streamline and simplify automatic cell counting for wet lab researchers who are not comfortable interfacing with code.

## Background
Cell counting is an important technique in a range of experimental disciplines related to liquid cell culture and tissue analysis. Accurate manual cell counting is tedious and time consuming, but there are many automatic image processing packages that serve to streamline this process. The backend of this script makes use of image pre-processing by median filter and Gaussian blur followed by a Watershed segmentation algorithm to achieve accurate (>90%) counting of crowded tissue images. 

In the backend, this script repairs deprecated code from the "CellCounting" repository and builds upon it by automating the optimization --> data processing pipeline by pre-selecting the best parameters for average cell diameter and threshold. The other significant feature is a GUI that allows users to select working directories and minimum particle size cutoffs without interfacing with raw code, and further allowing the user to visualize their results within the applet. As written, the code can only handle one channel but could be updated in the future to handle multichannel counting and overlap correction.

## User guide

### Preparing files to run the script
The program relies on a specific subdirectory naming scheme as represented in the example **Template.zip**. A composite image to be used for optimizing parameters should be placed in the "Composite" subdirectory. A manually counted mask of that composite image (prepared by ImageJ or another method of your choice) should be placed in the "ManualCounts" subdirectory. Finally, all of the cell images that you wish to be counted should be placed in the "Ch1" subdirectory.

### Running the script
As long as all the necessary packages and dependencies are downloaded the script can be run from any directory. Simply follow the GUI instructions to select a path for analysis, select a minimum particle size (we recommend 0.05, but this will depend on your composite image and the experimental images you're counting), and decide whether or not to use Watershed segmentation (recommended). 

### Getting your data
The total autocounts from each data file will be presented on the GUI, and also saved as a .csv file under "SavedOutput/Ch1_Counts.csv." Individual cell intensities from each experimental data file will be saved under "SavedOutput/Ch1/filename_cellinfo.csv." If you are interested, the data from threshold optimization is also saved in "SavedOutput".

### Note for future improvement
Due to an apparent difference in float handling between Python 3.11 (where the backend was written) and Python 3.9 (where the front end was written), the GUI-based algorithm can only accept minimum particle values ≥ 0.5. Since a version of PySide2 is not yet available for Python 3.11, the FrontEnd cannot handle smaller minimum cell area thresholds, which may temporarily limit the accuracy of the counter.

## Contributors
This code was written in collaboration between: <br />
Valentina Matos Romero: vmatosr1@jh.edu  <br />
Noah Smith: nsmit132@jh.edu
