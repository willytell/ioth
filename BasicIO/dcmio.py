import numpy as np
import os
import pydicom

""" Basic functions to load a set of DCMs into a Numpy array and to get metadata stored in a DCM file.

@author: Guillermo Torres
@email:  gtorres@cvc.uab.es

"""


def readMetadataFromDicom(filename):
    """Read and print the metadata contained in a DCM image file.

    Note
        ds.PixelData has the raw data bytes of the image, and
        ds.pixel_array has the numpy array of the image.
        More information at https://pydicom.github.io/pydicom/stable/base_element.html#dataset

    Parameter
    ---------
    filename : str
        Path to the file.

    Returns
    -------
    ds : pydicom.dataset.FileDataset
        Metadata of the DCM file.
    """

    ds = pydicom.dcmread(filename)
    return ds



def lookForMetadataElements(fileDataset, pattern):
    """Find the DICOM keywords that match the 'str' string.

    Parameters
    ----------
    fileDataset : pydicom.dataset.FileDataset
        Image and metadata

    pattern : str
        String pattern to look for in the metadata

    Returns
    -------
         : list
        List of DICOM keyword (tags) that match the pattern.
    """

    return fileDataset.dir(pattern)


####################################################################
# Author: Adamos Kyriakou
# Repository: https://gist.github.com/somada141/8dd67a02e330a657cf9e
# Related article: https://pyscience.wordpress.com/2014/09/08/dicom-in-python-importing-medical-image-data-into-numpy-with-pydicom-and-vtk/
def readDicom (dicomPath):
    """Load DICOM data into a NumPy array.

    Parameter
    ---------
    dicomPath : str
        Path of the folder/directory that contains the .dcm files

    Returns
    -------
    dicomArray : numpy array
        3D Volume conformed from the .dcm files
    """

    lstFilesDCM = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(dicomPath):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check whether the file's DICOM
                lstFilesDCM.append(os.path.join(dirName,filename))

    # Get ref file
    ds = pydicom.read_file(lstFilesDCM[0])

    # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
    ConstPixelDims = (int(ds.Rows), int(ds.Columns), len(lstFilesDCM))

    # Load spacing values (in mm)
    # ConstPixelSpacing = (float(ds.PixelSpacing[0]), float(ds.PixelSpacing[1]), float(ds.SliceThickness))

    # The array is sized based on 'ConstPixelDims'
    dicomArray = np.zeros(ConstPixelDims, dtype=ds.pixel_array.dtype)

    # loop through all the DICOM files
    for filenameDCM in lstFilesDCM:
        # read the file
        ds = pydicom.read_file(filenameDCM)
        # store the raw image data
        dicomArray[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array

    return dicomArray

####################################################################


def debug():
    """This is only for test and to shows a way of use the different function.

    Example
    -------
        $ python dcmio.py
    """


    # reading the metadata of a DICOM file
    ds = readMetadataFromDicom('/home/willytell/Escritorio/LungCTDataBase/LIDC-IDRI/LIDC-IDRI-0002/01-01-2000-98329/3000522-04919/000070.dcm')
    print(ds)

    print("----------------")

    # looking the pattern 'pat' in the metadata
    data_elements = lookForMetadataElements(ds, 'pat')
    for de in data_elements:
        print(ds.data_element(de))

    print("----------------")

    # loading all the .dcm files into a NumPy array
    volume = readDicom('/home/willytell/Escritorio/LungCTDataBase/LIDC-IDRI/LIDC-IDRI-0002/01-01-2000-98329/3000522-04919/')
    print("Volume shape: {}".format(volume.shape))


if __name__ == '__main__':
    debug()