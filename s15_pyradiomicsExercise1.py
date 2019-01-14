#!/usr/bin/env python

"""
__author__ = "Guillermo Torres and Debora Gil"
__license__ = "GPLv3"
__email__ = "gtorres@cvc.uab.es, debora@cvc.uab.es"
__year__ = "2019"
"""


import os
import SimpleITK as sitk
from radiomics import featureextractor

#### Parameters to be configured
db_path = '/home/willytell/Escritorio/Session15/Databases/LIDC-IDRI_Diagnosis'
imageDirectory = 'CTRoi_nii'
maskDirectory =  'CTRoimask_nii'
imageName = os.path.join(db_path, imageDirectory, 'LIDC-IDRI-0124_GT1_1.nii.gz')
maskName  = os.path.join(db_path, maskDirectory, 'LIDC-IDRI-0124_GT1_1_Mask.nii.gz')
####


# Reading image and mask
imageITK = sitk.ReadImage(imageName)
maskITK = sitk.ReadImage(maskName)

# Use a parameter file, this customizes the extraction settings and
# also specifies the input image types to use and
# which features should be extracted.
params = 'config/simpleFeatureExtraction_Params.yaml'

# Initializing the feature extractor
extractor = featureextractor.RadiomicsFeaturesExtractor(params)

# Calculating features
featureVector = extractor.execute(imageITK, maskITK)

# Showing the features and its calculated values
for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))