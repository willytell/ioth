import SimpleITK as sitk
from radiomics import featureextractor

imageName = '/home/willytell/Escritorio/LungCTDataBase/lc3d/Nii_Vol/CTRoi_nii/LIDC-IDRI-0016_GT1_2.nii.gz'
maskName  = '/home/willytell/Escritorio/LungCTDataBase/lc3d/Nii_Vol/CTRoimask_nii/LIDC-IDRI-0016_GT1_2_Mask.nii.gz'

print("###################### USING THE ORIGINAL IMAGE AND MASK ######################")

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
    #print('Computed %s: %s' % (featureName, featureVector[featureName]))


print("###################### MODIFING ONLY THE IMAGE ######################")

volume = sitk.GetArrayFromImage(imageITK)           # Convertion from SimpleITK to Numpy array.

print("volume[0,0,0]: {}".format(volume[0,0,0]))    # Before the modification.

volume = volume * 0                                 # Set to zero all its values.

print("volume[0,0,0]: {}".format(volume[0,0,0]))    # After the modification

modifiedImage = sitk.GetImageFromArray(volume)              # Convertion from Numpy array to SimpleITK.

modifiedImage.SetOrigin(imageITK.GetOrigin())               # Set origin, spacing and direction which are necessary to
modifiedImage.SetSpacing(imageITK.GetSpacing())             # extract features properly.
modifiedImage.SetDirection(imageITK.GetDirection())

featureVector = extractor.execute(modifiedImage, maskITK)   # THE maskITK is always the same.

for featureName in featureVector.keys():
    print("Computed {}: {}".format(featureName, featureVector[featureName]))
