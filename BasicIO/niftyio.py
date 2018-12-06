import SimpleITK as sitk
import numpy as np

""" Basic functions to read from and save to an image file in Nifty format.

author: Guillermo Torres
email:  gtorres@cvc.uab.es
"""


class Metadata():
    def __init__(self, origen=None, spacing=None, direction=None):
        self.origen = origen
        self.spacing = spacing
        self.direction = direction


def readNifty(filePath):
    """Read an image that is in a Nifty format file & it is converted to an array.

    Parameter
    ---------
    filePath : str
        Full file path, e.g. '/home/user/DataBase/LIDC-IDRI-0001_GT1.nii.gz'

    Returns
    -------
    numpy array
        3-Dimension array with (x, y, z) coordinate system, that corresponds to the Nifty image.

    Metadata
        Preserve basic information of the original Nifty format file.
    """

    image = sitk.ReadImage(filePath)
    print("Reading Nifty format file from {}".format(filePath))
    print("Image size: {}".format(image.GetSize()))

    metadata = Metadata(image.GetOrigin(), image.GetSpacing(), image.GetDirection())

    # Converting from SimpleITK image to Numpy array. But also during the convert is changed the coordinate systems
    # from the image which use (x,y,z) to the array using (z,y,x).
    volume_zyx = sitk.GetArrayFromImage(image)
    volume_xyz = np.transpose(volume_zyx, (2, 1, 0))  # to back to the initial xyz coordinate system.

    print("Volume shape: {}".format(volume_xyz.shape))
    print("Minimum value: {}".format(np.min(volume_xyz)))
    print("Maximum value: {}".format(np.max(volume_xyz)))

    return volume_xyz, metadata     # return two items.


def saveNifty(volume, metadata, filename):
    """Write an image file in the Nifty format.

    Parameter
    ---------
    volume : numpy array
        3-Dimension array with (x, y, z) coordinate system

    metadata : :obj:Metadata
        Basic information necessary to save the file.

    filename: str
        The file will be saved with this name.
    """

    # Converting from Numpy array to SimpleITK image.
    volume = np.transpose(volume, (2, 1, 0)) # from (x,y,z) to (z,y,x)
    image = sitk.GetImageFromArray(volume)  # It is supposed that GetImageFromArray receive an array with (z,y,x)

    if metadata is not None:
        # Setting some properties to the new image
        image.SetOrigin(metadata.origen)
        image.SetSpacing(metadata.spacing)
        image.SetDirection(metadata.direction)

    sitk.WriteImage(image, filename)
    print("Saving the image in: {}.".format(filename))



def debug():
    vol, metadata = readNifty('/home/willytell/Escritorio/LungCTDataBase/lc3d/Nii_Vol/CTRoi_nii/LIDC-IDRI-0305_GT1_1.nii.gz')
    saveNifty(vol, metadata, '/home/willytell/Escritorio/TEST.nii.gz')

if __name__ == '__main__':
    debug()