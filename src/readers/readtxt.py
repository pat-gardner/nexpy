"""
Module to read in a text file and convert it to NeXus.

This is provided as an example of writing an import dialog. Each new importer needs
to layout the GUI buttons necessary for defining the imported file and its attributes
and a single module, get_data, which returns an NXroot or NXentry object. This will be
added to the NeXpy tree.

Two GUI elements are provided for convenience:

    ImportDialog.filebox: Contains a "Choose File" button and a text box. Both can be 
                          used to set the path to the imported file. This can be 
                          retrieved as a string using self.get_filename().
    ImportDialog.buttonbox: Contains a "Cancel" and "OK" button to close the dialog. 
                            This should be placed at the bottom of all import dialogs.
"""

from IPython.external.qt import QtCore, QtGui

import numpy as np
from nexpy.api.nexus import *
from nexpy.gui.importdialog import BaseImportDialog

filetype = "Text File"

class ImportDialog(BaseImportDialog):
    """Dialog to select a text file"""
 
    def __init__(self, parent=None):

        super(ImportDialog, self).__init__(parent)
        
        skippedbox = QtGui.QHBoxLayout()
        skippedlabel = QtGui.QLabel("No. of skipped rows")
        self.skiprows = QtGui.QLineEdit()
        self.skiprows.setText('0')
        self.skiprows.setFixedWidth(20)
        skippedbox.addWidget(skippedlabel)
        skippedbox.addWidget(self.skiprows)
 
        layout = QtGui.QVBoxLayout()
        layout.addLayout(self.filebox)
        layout.addLayout(skippedbox)
        layout.addWidget(self.buttonbox)
        self.setLayout(layout)
  
        self.setWindowTitle("Import "+str(filetype))
 
    def get_data(self):
        skiprows = int(self.skiprows.text())
        data = np.loadtxt(self.get_filename(), skiprows=skiprows)
        if data.shape[1] > 1:
            x = NXfield(data[:,0], name='x')
            y = NXfield(data[:,1], name='y')
        if data.shape[1] > 2:
            e = NXfield(data[:,2], name='errors')
            return NXentry(NXdata(y,x,errors=e))
        else:
            return NXentry(NXdata(y,x))