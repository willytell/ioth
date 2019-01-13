import os
import glob
import SimpleITK as sitk
import numpy as np
import pandas as pd

from radiomics import featureextractor
from collections import OrderedDict


def getImageFilename(mask_filename):
    # For a given mask filename:  LIDC-IDRI-0001_GT1_1_Mask.nii.gz
    # this function obtain the corresponding image filename: LIDC-IDRI-0001_GT1_1.nii.gz
    name_splitted = mask_filename.split('.')[0].split('_')
    image_filename = name_splitted[0] + '_' + name_splitted[1] + '_' + name_splitted[2] + '.nii.gz'
    return image_filename


def saveXLSX(filename, df):
    # write to a .xlsx file

    # add extension to the filename
    filename += '.xlsx'

    # if the filename does not exist
    if not os.path.isfile(filename):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
    else:
        print("Error: there is already a file named {}. Remove it!!".format(filename))
        raise Exception("There is already a file named {}. Remove it!!!!".format(filename))


def getFeatures(image_filename, mask_filename, imageITK, maskITK, paramPath):
    # extract features using pyradiomic

    extractor = featureextractor.RadiomicsFeaturesExtractor(paramPath)

    featureVector = extractor.execute(imageITK, maskITK)

    new_row = {}
    for featureName in featureVector.keys():  # Note that featureVectors is a 'disordered dictionary'
        # print('Computed %s: %s' % (featureName, featureVector[featureName]))
        # print(featureVector[featureName])
        if ('firstorder' in featureName) or ('glszm' in featureName) or \
                ('glcm' in featureName) or ('glrlm' in featureName) or \
                ('gldm' in featureName) or ('shape' in featureName):
            new_row.update({featureName: featureVector[featureName]})

    lst = sorted(new_row.items())  # Ordering the new_row dictionary

    # Adding some columns
    lst.insert(0, ('mask_filename', mask_filename))
    lst.insert(0, ('image_filename', image_filename))

    od = OrderedDict(lst)
    return (od)




print("Begining ...")

# Configuration files
paramPath = os.path.join('config', 'Params.yaml')
database_path = '/home/willytell/Escritorio/GuilleSession/Databases/LIDC-IDRI_Diagnosis'


src_image_path = os.path.join(database_path, 'CTRoi_nii')
src_mask_path = os.path.join(database_path, 'CTRoimask_nii')
mask_pattern = '*.nii.gz'

# list of mask filenames
src_mask_list = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(src_mask_path, mask_pattern)))]

mydict = []

for i in range(len(src_mask_list)):
    mask_filename  = src_mask_list[i]
    image_filename = getImageFilename(src_mask_list[i])

    maskITK  = sitk.ReadImage(os.path.join(src_mask_path, mask_filename))
    imageITK = sitk.ReadImage(os.path.join(src_image_path, image_filename))

    print("Extracting features from: {}".format(image_filename))
    od = getFeatures(image_filename, mask_filename, imageITK, maskITK, paramPath)
    mydict.append(od)


df = pd.DataFrame.from_dict(mydict)

print("Writing to .xlsx file.")
saveXLSX('features', df)





print("Finished.")
