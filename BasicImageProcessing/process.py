import numpy as np
from scipy.ndimage.filters import gaussian_filter
from skimage.filters import threshold_otsu
from scipy.ndimage.morphology import binary_opening, binary_closing, binary_dilation, binary_erosion, generate_binary_structure
from scipy.ndimage.measurements import label

"""Example of a basic image processing.

@author: Guillermo Torres
@email:  gtorres@cvc.uab.es

"""

def basicProcessing(volume, sigma, order, output, mode, truncate):
    """This function shows an example of processing a volume.

    Parameters
    ----------
    volume : array
        Array in which different processing will be applied.

    sigma : int or sequence of int
        Standard deviation for Gaussian kernel.

    order : int or sequence of int
        An order of 0 corresponds to convolution with a Gaussian kernel. An order of 1, 2, or 3 corresponds to
        convolution with the first, second or third derivatives of a Gaussian. Higher order derivatives are
        not implemented.

    output : array or dtype
        The array in which to place the output, or the dtype of the returned array. By default an array of
        the same dtype as input will be created.

    mode : str
        The mode parameter determines how the input array is extended when the filter overlaps a border.

    truncate : float
        Truncate the filter at this many standard deviations. Default is 4.0.
    """


    #### Filters ###

    result = gaussian_filter(input=volume, sigma=sigma, order=order, output=output, mode=mode, truncate=truncate)

    val = threshold_otsu(result)
    print("val : {}".format(val))

    mask = np.zeros(volume.shape, dtype=np.int8)
    mask[volume > val] = 1
    #mask = mask.astype(int)

    print("mask shape: {}".format(mask.shape))
    print(mask)


    #### Morphological Operation ###

    # Opening removes small objects
    r1 = binary_opening(mask, structure=np.ones((3, 3, 3))).astype(int)

    # Closing removes small holes
    r2 = binary_closing(r1, structure=np.ones((3, 3, 3))).astype(np.int)

    # 3x3x3 structuring element with connectivity 4 or 8
    struct1 = generate_binary_structure(3, 1)   # no diagonal elements
    #struct1 = generate_binary_structure(3, 2)  # with diagonal elements
    ############struct1 = struct1.astype(int)
    print (struct1)



    #r3 = binary_dilation(r2).astype(int)
    r3 = binary_dilation(r2, structure=struct1).astype(int)    # using a structure element

    # Erosion removes objects smaller than the structure
    r4 = binary_erosion(r3, structure=np.ones((3, 3, 3))).astype(int)


    #### Measurements ###

    struct2 = np.ones((3, 3, 3), dtype=np.int)
    labeled_array, num_features = label(r4, structure=struct2)

    #print(labeled_array)
    print(num_features)


def debug():

    vol = np.random.randint(256, size=(10,10,10))   # create a volume of 10x10x10 with elements between 0-255


    sigma = [2, 2, 2]
    order= 0
    mode = 'reflect'
    truncate = 4.0
    output = np.float  # precision of the intermediate and final result

    basicProcessing(vol, sigma, order, output, mode, truncate)

if __name__ == '__main__':
    debug()
