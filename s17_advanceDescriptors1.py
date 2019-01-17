#!/usr/bin/env python

"""
__author__ = "Guillermo Torres and Debora Gil"
__license__ = "GPLv3"
__email__ = "gtorres@cvc.uab.es, debora@cvc.uab.es"
__year__ = "2019"
"""

#  For implementation details of GLCM features, look in your local installation of pyradiomics:
#  /home/willytell/.virtualenvs/virtenvPython3/lib/python3.5/site-packages/radiomics/glcm.py

import six
import numpy as np
import SimpleITK as sitk


import os
from BasicIO.niftyio import readNifty
from radiomics import featureextractor


### >>> Parameters to be configured <<<
paramPath = os.path.join('config', 's17_Excercise1_Params.yaml')
database_path = '/home/willytell/Escritorio/Session15/Databases/LIDC-IDRI_Diagnosis'
imageName = os.path.join(database_path, 'CTRoi_nii', 'LIDC-IDRI-0129_GT1_1.nii.gz')
maskName = os.path.join(database_path, 'CTRoimask_nii', 'LIDC-IDRI-0129_GT1_1_Mask.nii.gz')
# imageName = '/home/willytell/Escritorio/Session15/LIDC-IDRI-0016_GT1_2.nii.gz'
# maskName = '/home/willytell/Escritorio/Session15/LIDC-IDRI-0016_GT1_2_Mask.nii.gz'
###


img_array, img_metadata = readNifty(imageName)
mask_array, mask_metadata = readNifty(maskName)

x, y, z = img_array.shape
half_x = x // 2
half_y = y // 2

print(x)
print(y)
print(half_x)
print(half_y)

# image
img_Q1 = img_array[0:half_x, 0:half_y, :]
img_Q2 = img_array[0:half_x, half_y:,  :]
img_Q3 = img_array[half_x:, 0:half_y,  :]
img_Q4 = img_array[half_x:, half_y:,   :]


img_temp1 = np.concatenate([img_Q1, img_Q2], axis=1)
img_temp2 = np.concatenate([img_Q3, img_Q4], axis=1)
img_temp3 = np.concatenate([img_temp1, img_temp2], axis=0)


flag = np.array_equal(img_array, img_temp3)
print("This is the original image: {}".format(flag))


# mask
mask_Q1 = mask_array[0:half_x, 0:half_y, :]
mask_Q2 = mask_array[0:half_x, half_y:,  :]
mask_Q3 = mask_array[half_x:, 0:half_y,  :]
mask_Q4 = mask_array[half_x:, half_y:,   :]


mask_temp1 = np.concatenate([mask_Q1, mask_Q2], axis=1)
mask_temp2 = np.concatenate([mask_Q3, mask_Q4], axis=1)
mask_temp3 = np.concatenate([mask_temp1, mask_temp2], axis=0)


flag = np.array_equal(mask_array, mask_temp3)
print("This is the original mask: {}".format(flag))

####################### MODIFYING THE IMAGE AND MASK ###################

img_temp1 = np.concatenate([img_Q3, img_Q4], axis=1)
img_temp2 = np.concatenate([img_Q1, img_Q2], axis=1)
img_temp3 = np.concatenate([img_temp1, img_temp2], axis=0)

mask_temp1 = np.concatenate([mask_Q3, mask_Q4], axis=1)
mask_temp2 = np.concatenate([mask_Q1, mask_Q2], axis=1)
mask_temp3 = np.concatenate([mask_temp1, mask_temp2], axis=0)


# Converting from Numpy array to SimpleITK image.
img_temp3 = np.transpose(img_temp3, (2, 1, 0))  # from (x,y,z) to (z,y,x)
img_temp3 = img_temp3[z//2:z//2+1, :, :]
print("Selecting one slide: {}".format(z//2))
img_temp3 = np.flip(np.flip(img_temp3, axis=1), axis=2)
#print(img_temp3.shape)
img1 = sitk.GetImageFromArray(img_temp3)  # It is supposed that GetImageFromArray receive an array with (z,y,x)

if img_metadata is not None:
     # Setting some properties to the new image
     img1.SetOrigin(img_metadata.origen)
     img1.SetSpacing(img_metadata.spacing)
#     img1.SetDirection(img_metadata.direction)
#
sitk.WriteImage(img1, 'image.nii.gz')
print("Saving the modified image in: image.nii.gz")




# Converting from Numpy array to SimpleITK image.
mask_temp3 = np.transpose(mask_temp3, (2, 1, 0))  # from (x,y,z) to (z,y,x)
mask_temp3 = mask_temp3[z//2:z//2+1, :, :]
mask_temp3 = np.flip(np.flip(mask_temp3, axis=1), axis=2)
#print(mask_temp3.shape)
mask1 = sitk.GetImageFromArray(mask_temp3)  # It is supposed that GetImageFromArray receive an array with (z,y,x)

if mask_metadata is not None:
    #Setting some properties to the new image
    mask1.SetOrigin(mask_metadata.origen)
    mask1.SetSpacing(mask_metadata.spacing)
    #mask1.SetDirection(img_metadata.direction)

sitk.WriteImage(mask1, 'mask.nii.gz')
print("Saving the modified mask in: mask.nii.zg.")


###############################################################################################


######### BEGIN: NOW WE ARE GOING TO COMPUTE THE GLCM FEATURES

### Original Image
img_array, img_metadata = readNifty(imageName)

x, y, z = img_array.shape

img_temp3 = np.transpose(img_array, (2, 1, 0))  # from (x,y,z) to (z,y,x)
img_temp3 = img_temp3[z//2:z//2+1, :, :]
print("Selection one slide: {}".format(z//2))
img_temp3 = np.flip(np.flip(img_temp3, axis=1), axis=2)
#print(img_temp3.shape)
img1 = sitk.GetImageFromArray(img_temp3)  # It is supposed that GetImageFromArray receive an array with (z,y,x)

if img_metadata is not None:
     # Setting some properties to the new image
     img1.SetOrigin(img_metadata.origen)
     img1.SetSpacing(img_metadata.spacing)
#     img1.SetDirection(img_metadata.direction)


### Original Mask
mask_array, mask_metadata = readNifty(maskName)
mask_temp3 = np.transpose(mask_array, (2, 1, 0))  # from (x,y,z) to (z,y,x)
mask_temp3 = mask_temp3[z//2:z//2+1, :, :]
mask_temp3 = np.flip(np.flip(mask_temp3, axis=1), axis=2)
#print(mask_temp3.shape)
mask1 = sitk.GetImageFromArray(mask_temp3)  # It is supposed that GetImageFromArray receive an array with (z,y,x)

if mask_metadata is not None:
    #Setting some properties to the new image
    mask1.SetOrigin(mask_metadata.origen)
    mask1.SetSpacing(mask_metadata.spacing)
    #mask1.SetDirection(img_metadata.direction)

imageITK = img1
maskITK = mask1


# Use a parameter file, this customizes the extraction settings and
# also specifies the input image types to use and
# which features should be extracted.
params = 'config/s17_Exercise1_Params.yaml'

# Initializing the feature extractor
extractor = featureextractor.RadiomicsFeaturesExtractor(params)

# Calculating features
featureVector = extractor.execute(imageITK, maskITK)

# Showing the features and its calculated values
for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))


print ("\n")
print("###################################################")
print ("\n")

######### END: NOW WE ARE GOING TO COMPUTE THE GLCM FEATURES



######## BEGIN: NOW WE ARE GOING TO COMPUTE THE GLCM FEATURES FOR THE MODIFIED IMAGE AND MASK
# Reading image and mask
imageITK = sitk.ReadImage('image.nii.gz')
maskITK = sitk.ReadImage('mask.nii.gz')
print("Reading MODIFIED image and mask.")

print(imageITK.GetSize())
print(maskITK.GetSize())

# Use a parameter file, this customizes the extraction settings and
# also specifies the input image types to use and
# which features should be extracted.
params = 'config/s17_Exercise1_Params.yaml'

# Initializing the feature extractor
extractor = featureextractor.RadiomicsFeaturesExtractor(params)

# Calculating features
featureVector = extractor.execute(imageITK, maskITK)

# Showing the features and its calculated values
for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))


######## END: NOW WE ARE GOING TO COMPUTE THE GLCM FEATURES FOR THE MODIFIED IMAGE AND MASK
###############################################################################################