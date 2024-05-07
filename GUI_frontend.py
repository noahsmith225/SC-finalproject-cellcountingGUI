"""
Final Project - Development of a Python-based GUI for Interactive Cell Analysis and Quantification

Authors: Valentina Matos Romero, Noah Daniel Smith
Last Modified May 7, 2024

Note:
This script implements a Python-based GUI for interactive cell analysis and quantification. It utilizes PySide2 for the GUI framework and integrates functionality from the 'cell_counter_backend' module for image processing and analysis.

The main functionality includes:
1. Selecting an image directory.
2. Filling out a form with parameters for cell analysis.
3. Processing the images based on the provided parameters.
4. Displaying the processed data in a QTableView within the GUI.

Explanation of Input Parameters:
1. diam (diameter): Represents the diameter of objects to be analyzed in the images. It determines the minimum size of objects considered during cell analysis.
2. particle_min (minimum size object): Defines the minimum size of particles or objects to be included in the analysis. Small particles below this size threshold are ignored.
3. UseWatershed: A boolean parameter indicating whether to use watershed segmentation during image processing. When True, watershed segmentation is applied to improve the accuracy of cell segmentation.

Steps to follow to use the GUI:
1. Run the code -> A pop-up window will appear with the GUI.
2. Select an image directory.
3. Select the minimum size object though the spin button, we recommend 0.5 for the provided image
4. Set the watershed parameter value, by default TRUE, (we recommend this option)
5. Click submit and wait for the cell analysis to finish. A message will be displayed on the command window indicating it.
6. Visualize the results on the GUI.

RESULTS:



"""

from PySide2 import QtWidgets, QtCore
from cell_counter_backend import getdirinfo, cellcounting_param_optimizer, cellcounting_batch
import os
import main


class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    """Class representing the main GUI window."""

    def __init__(self):
        """Initialize the main GUI window."""
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.submit_PB.clicked.connect(self.fill_form)
        self.browseimagepath_TB.clicked.connect(self.select_imagedir)

    def select_imagedir(self):
        """Open a dialog to select an image directory."""
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Image Directory', os.getcwd())
        if folder_path:
            self.image_LE.setText(folder_path)

    def fill_form(self):
        """Process the form data and initiate image processing."""

        working_directory = self.image_LE.text()
        if not working_directory:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter image path')
            return
        min_size = self.sizeobject_SB.value()
        watershed = self.watershed_CB.currentText()

        print(f'Image directory: {working_directory}')
        print(f'Minimum size object: {min_size}')
        print(f'Watershed: {watershed}')

        dirinfo = {'main': working_directory}
        dirinfo = getdirinfo(dirinfo)

        params = {'diam': 6,
                  'particle_min': min_size,
                  'UseWatershed': True
                  }

        optimal_diameter, optimal_threshold = cellcounting_param_optimizer(dirinfo, params)

        params['ch1_diam'] = optimal_diameter
        params['ch1_thresh'] = optimal_threshold

        output = cellcounting_batch(dirinfo, "Ch1", params, save_intensities=True)
        print(output)
        print('Image processing finished! View results in GUI')

        self.display_data(output)  # Call display_data to show the output in QTableView

    def display_data(self, output):
        """Display the processed data in the QTableView."""

        model = PandasModel(output)
        self.qtable.setModel(model)

        self.qtable.resizeColumnsToContents()

class PandasModel(QtCore.QAbstractTableModel):
    """Custom model for interfacing Pandas DataFrames with Qt Views."""

    def __init__(self, data):
        """Initialize the model with the provided DataFrame."""
        super(PandasModel, self).__init__()
        self._data = data
        self._headers = data.columns.tolist()

    def rowCount(self, parent=None):
        """Return the number of rows in the DataFrame."""
        return self._data.shape[0]

    def columnCount(self, parent=None):
        """Return the number of columns in the DataFrame."""
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        """Return the header data for the specified section."""
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section < len(self._headers):
                return self._headers[section]
        return super(PandasModel, self).headerData(section, orientation, role)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Return the data for the specified index."""
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = MyQtApp()
    qt_app.show()
    app.exec_()
