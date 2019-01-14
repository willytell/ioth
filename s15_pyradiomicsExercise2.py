#!/usr/bin/env python

"""
__author__ = "Guillermo Torres and Debora Gil"
__license__ = "GPLv3"
__email__ = "gtorres@cvc.uab.es, debora@cvc.uab.es"
__year__ = "2019"
"""


import SimpleITK as sitk
from radiomics import featureextractor

imageName = '/home/willytell/Escritorio/Session15/LIDC-IDRI-0016_GT1_2.nii.gz'
maskName  = '/home/willytell/Escritorio/Session15/LIDC-IDRI-0016_GT1_2_Mask.nii.gz'

print("###################### USING AN IMAGE AND A MASK ######################")

# Reading image and mask
imageITK = sitk.ReadImage(imageName)
maskITK = sitk.ReadImage(maskName)

# Use a parameter file, this customizes the extraction settings and
# also specifies the input image types to use and
# which features should be extracted.
params = 'config/shapeFeatureExtraction_Params.yaml'

# Initializing the feature extractor
extractor = featureextractor.RadiomicsFeaturesExtractor(params)

# Calculating features
featureVector = extractor.execute(imageITK, maskITK)

for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))


print("###################### USING ANOTHER IMAGE WITH THE SAME MASK ######################")

anotherImageName = '/home/willytell/Escritorio/Session15/anotherImage.nii.gz'

anotherImageITK = sitk.ReadImage(anotherImageName)

featureVector = extractor.execute(anotherImageITK, maskITK)   # The maskITK is always the same.

for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))
