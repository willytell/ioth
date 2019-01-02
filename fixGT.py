# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 20:31:23 2018

@author: debora
"""

import numpy as np
# Pyhton standard IOs Library
import os
import glob

from BasicIO.niftyio import readNifty, saveNifty

src_maskPath = '/home/willytell/Escritorio/LungCTDataBase/preprocessed/Nii_Vol/CTRoimask_nii_part1'
dst_maskPath = '/home/willytell/Escritorio/LungCTDataBase/preprocessed/Nii_Vol/CTRoimask_nii_part2'
maskPattern = '*Mask*.nii.gz'
mask_lst = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(src_maskPath, maskPattern)))]

for niiFile in mask_lst:
    niiROIGT, metadata = readNifty(os.path.join(src_maskPath, niiFile))
    i, j, k = niiROIGT.nonzero()
    #saveNifty(niiROIGT, metadata, os.path.join(maskPath, 'old', niiFile))
    niiROIGT = 0 * niiROIGT
    try:
        niiROIGT[i + 2, j + 2, k] = 1
        saveNifty(niiROIGT, metadata, os.path.join(dst_maskPath, niiFile))
    except:
        print("Error processing: {}".format(os.path.join(dst_maskPath, niiFile)))


# rm_lst = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(maskPath, 'zzz' ,maskPattern)))]
# print(rm_lst)
# for fname in rm_lst:
#     os.remove(os.path.join(maskPath, fname))
#     print("Filename removed: {}".format(os.path.join(maskPath, fname)))
