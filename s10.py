import os
import glob
import SimpleITK as sitk
import numpy as np
import pandas as pd

from radiomics import featureextractor
from collections import OrderedDict


def make_filename_list(src_image_path, src_mask_path, filename):
    # Make two list from the filename, which is an .xlsx file.
    # And return two list with positive and negative samples each one.
    # Positive = 1 and Negative = 0.

    df = pd.read_excel(filename)
    print("Reading the filename: {}".format(filename))

    positive_samples = []
    negative_samples = []
    for idx in range(0, len(df)):
        imageName = df.iloc[idx][0] + '_GT1_' + str(df.iloc[idx][1]) + '.nii.gz'
        maskName = imageName.replace('.nii.gz', '_Mask.nii.gz')

        # Check if there is the image and its corresponding mask.
        if (os.path.isfile(os.path.join(src_image_path, imageName)) and
            os.path.isfile(os.path.join(src_mask_path, maskName)) ) == True:

                diagnosis = df.iloc[idx][2]

                # Positive (maligne) = 1, Negative (benigne) = 0.
                if diagnosis == 1:
                    positive_samples.append((imageName, maskName, 1))
                else:
                    negative_samples.append((imageName, maskName, 0))

                print("Added to the sample list: ({}, {})".format(imageName, maskName))
        else:
            print("Discarded pair of samples: ({}, {})".format(imageName, maskName))

    print("Length of the sample list: {} rows.".format(len(positive_samples) + len(negative_samples)))

    return positive_samples, negative_samples


def saveXLSX(filename, df):
    # write to a .xlsx file.

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()



def getFeatures(imageName, maskName, imageITK, maskITK, y_label, paramPath):
    # extract features using pyradiomic.

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

    lst = sorted(new_row.items())  # Ordering the new_row dictionary.

    # Adding some columns
    lst.insert(0, ('diagnosis', y_label))
    lst.insert(0, ('mask_filename', maskName))
    lst.insert(0, ('image_filename', imageName))

    od = OrderedDict(lst)
    return (od)



############ MAIN PROGRAM ########################

print("Begining ...")

### >>> Parameters to be configured <<<
paramPath = os.path.join('config', 'Params.yaml')
database_path = '/home/willytell/Escritorio/GuilleSession/Databases/LIDC-IDRI_Diagnosis'
###


src_image_path = os.path.join(database_path, 'CTRoi_nii')
src_mask_path = os.path.join(database_path, 'CTRoimask_nii')
excel_filename = os.path.join(database_path, 'tci_diagnosis.xls')
output = 'features.xlsx'

# It will not overwrite the output file.
if os.path.isfile(output):
    print("Error: there is already a file named {}. Remove it.".format(output))
    raise Exception("There is already a file with the same filename. Remove it.")

# list of mask filenames.
positive_samples, negative_samples = make_filename_list(src_image_path, src_mask_path, excel_filename)
all_samples = positive_samples + negative_samples   # concatenate all the samples in one list.


mydict = []   # create an empty list

for index in range(len(all_samples)):
    imageName = all_samples[index][0]
    maskName = all_samples[index][1]
    y_label = all_samples[index][2]

    imageITK = sitk.ReadImage(os.path.join(src_image_path, imageName))
    maskITK  = sitk.ReadImage(os.path.join(src_mask_path, maskName))


    print("Extracting features from: {}".format(imageName))
    od = getFeatures(imageName, maskName, imageITK, maskITK, y_label, paramPath)
    mydict.append(od)


df = pd.DataFrame.from_dict(mydict)

print("Writing to .xlsx file.")
saveXLSX(output, df)

print("Finished.")



