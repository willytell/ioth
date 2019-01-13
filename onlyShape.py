import SimpleITK as sitk
from radiomics import featureextractor

imageName = '/home/willytell/Escritorio/LungCTDataBase/lc3d/Nii_Vol/CTRoi_nii/LIDC-IDRI-0016_GT1_2.nii.gz'
maskName  = '/home/willytell/Escritorio/LungCTDataBase/lc3d/Nii_Vol/CTRoimask_nii/LIDC-IDRI-0016_GT1_2_Mask.nii.gz'

print("###################### USING AN IMAGE AND ITS CORRESPONDING MASK ######################")

# Reading image and mask
imageITK = sitk.ReadImage(imageName)
maskITK = sitk.ReadImage(maskName)

# Use a parameter file, this customizes the extraction settings and
# also specifies the input image types to use and
# which features should be extracted.
params = 'config/onlyShape_Params.yaml'

# Initializing the feature extractor
extractor = featureextractor.RadiomicsFeaturesExtractor(params)

# Calculating features
featureVector = extractor.execute(imageITK, maskITK)

for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))


print("###################### USING ANOTHER IMAGE ######################")

anotherImageName = '/home/willytell/Escritorio/GuilleSession/anotherImage.nii.gz'

anotherImageITK = sitk.ReadImage(anotherImageName)

featureVector = extractor.execute(anotherImageITK, maskITK)   # The maskITK is always the same.

for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))
