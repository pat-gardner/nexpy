#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright (c) 2013, NeXpy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING, distributed with this software.
#-----------------------------------------------------------------------------

"""
Module to read in a CBF file and convert it to NeXus.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np

from nexusformat.nexus import *
from nexpy.gui.importdialog import BaseImportDialog

filetype = "CBF File"

class ImportDialog(BaseImportDialog):
    """Dialog to import a CBF file"""
 
    def __init__(self, parent=None):

        super(ImportDialog, self).__init__(parent)
        
        self.set_layout(self.filebox(), self.close_buttons())
  
        self.setWindowTitle("Import "+str(filetype))
 
    def get_data(self):
        try:
            import fabio
        except ImportError:
            raise NeXusError("Please install the 'fabio' module")
        self.import_file = self.get_filename()
        im = fabio.open(self.import_file)
        z = NXfield(im.data, name='z')
        y = NXfield(range(z.shape[0]), name='y')
        x = NXfield(range(z.shape[1]), name='x')        
        note = NXnote(type='text/plain', file_name=self.import_file)
        note.data = im.header.pop('_array_data.header_contents', '')
        note.description = im.header.pop('_array_data.header_convention', '')
        header = NXcollection()
        for k, v in im.header.items():
            header[k] = v
        return NXentry(NXdata(z,(y,x), CBF_header=note, header=header))
