from PySide2 import QtWidgets, QtCore
from cell_counter_backend import getdirinfo, cellcounting_param_optimizer, cellcounting_batch
import os
import main


class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.submit_PB.clicked.connect(self.fill_form)
        self.browseimagepath_TB.clicked.connect(self.select_imagedir)

    def select_imagedir(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Image Directory', os.getcwd())
        if folder_path:
            self.image_LE.setText(folder_path)

    def fill_form(self):
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
        dirinfo = getdirinfo(dirinfo)  # Populates dirinfo with paths to composite, mask, cell images, and an output
        # container.

        params =   {'diam': 6,
                    'particle_min': min_size,
                    'UseWatershed': True
                    }

        # Call backend function to optimize parameters
        optimal_diameter, optimal_threshold = cellcounting_param_optimizer(dirinfo, params)

        # Call backend function to perform cell counting with parameters input though the GUI
        params['ch1_diam'] = optimal_diameter
        params['ch1_thresh'] = optimal_threshold

        output = cellcounting_batch(dirinfo, "Ch1", params, save_intensities=True)
        print(output)

    def display_data(self, output):
        # Display data in QTableView
        model = PandasModel(output)
        self.qtable.setModel(model)

# def load_data_and_display():
#     import pickle
#     pth = r'C:\Users\Valentina\OneDrive - Johns Hopkins\Courses\Software carpentry\FP\output.pkl'
#     with open(pth, 'rb') as f:
#         output = pickle.load(f)
#     return output

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(PandasModel, self).__init__()
        self._data = data
        self._headers = data.columns.tolist()

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section < len(self._headers):
                return self._headers[section]
        return super(PandasModel, self).headerData(section, orientation, role)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = MyQtApp()
    qt_app.show()
    app.exec_()
