import SimpleITK as sitk
from radiomics import featureextractor

imageName = '/home/willytell/Escritorio/LungCTDataBase/lc3d/Nii_Vol/CTRoi_nii/LIDC-IDRI-0016_GT1_2.nii.gz'
maskName  = '/home/willytell/Escritorio/LungCTDataBase/lc3d/Nii_Vol/CTRoimask_nii/LIDC-IDRI-0016_GT1_2_Mask.nii.gz'

# Reading image and mask
imageITK = sitk.ReadImage(imageName)
maskITK = sitk.ReadImage(maskName)

# Use a parameter file, this customizes the extraction settings and
# also specifies the input image types to use and
# which features should be extracted.
params = 'config/simpleExtraction_Params.yaml'

# Initializing the feature extractor
extractor = featureextractor.RadiomicsFeaturesExtractor(params)

# Calculating features
featureVector = extractor.execute(imageITK, maskITK)

# Showing the features and its values
for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))