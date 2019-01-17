#!/usr/bin/env python

"""
__author__ = "Guillermo Torres and Debora Gil"
__license__ = "GPLv3"
__email__ = "gtorres@cvc.uab.es, debora@cvc.uab.es"
__year__ = "2019"
"""

import numpy as np
import os
from BasicIO.niftyio import readNifty
from skimage import feature


### >>> Parameters to be configured <<<
paramPath = os.path.join('config', 'Params.yaml')
database_path = '/home/willytell/Escritorio/Session15/Databases/LIDC-IDRI_Diagnosis'
imageName = os.path.join(database_path, 'CTRoi_nii', 'LIDC-IDRI-0129_GT1_1.nii.gz')
maskName = os.path.join(database_path, 'CTRoimask_nii', 'LIDC-IDRI-0129_GT1_1_Mask.nii.gz')
# imageName = '/home/willytell/Escritorio/Session17/LIDC-IDRI-0016_GT1_2.nii.gz'
# maskName = '/home/willytell/Escritorio/Session17/LIDC-IDRI-0016_GT1_2_Mask.nii.gz'
###


#### ENABLE AND DISABLE THE FOLLOWING TWO LINES TO CHOICE THE FILE TO COMPUTE HoG FEATURES.
# img_array, _ = readNifty(imageName)   # original image.
img_array, _ = readNifty('image.nii.gz')   # modified image.



#print(img_array.shape)
x, y, z = img_array.shape

# Converting from Numpy array to SimpleITK image.
img_array = np.transpose(img_array, (2, 1, 0))  # from (x,y,z) to (z,y,x)
#img_temp3 = img_temp3[z//2:z//2+1, :, :]
print(img_array.shape)
print("Selecting one slide: {}".format(z//2))
img_array = np.flip(np.flip(img_array, axis=1), axis=2)


print(img_array.shape)
image = img_array [0, :, :]


orientations = 8
pixels_per_cell = (4, 4)
cells_per_block = (2, 2)
block_norm = 'L2-Hys'
visualise = False
multichannel = False

feats = feature.hog(image, orientations=orientations,
                    pixels_per_cell=pixels_per_cell,
                    cells_per_block=cells_per_block,
                    block_norm=block_norm,
                    visualise=visualise)

print(feats)
