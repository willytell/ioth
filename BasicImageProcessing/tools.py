import numpy as np
from scipy.ndimage.morphology import distance_transform_edt


""" Useful functions for image processing.

@author: Guillermo Torres
@email:  gtorres@cvc.uab.es

"""

def distanceMap3D (volume):
    """Calculate the euclidean distance map for a given 3D numpy array.

    Note
        The function also works for a 2D or N-Dimension numpy array.

    Parameter
    ---------
        volume : numpy array
            Binary array.

    Returns
    -------
         : numpy array
        The distance map.
    """
    # return the distance map for n-Dimensions
    return distance_transform_edt(np.logical_not(volume))

def debug():

    array = np.zeros((5,5,5))
    array[2,2,2] = 1
    #a[3, 3, 3] = 1
    # a[3, 3, 4] = 1
    # a[3, 3, 2] = 1
    # a[3, 4, 3] = 1
    # a[3, 2, 3] = 1

    np.set_printoptions(precision=3)    # Easier to read the result with fewer digits.

    print("a: {}".format(array))

    distance_map = distanceMap3D(array)

    print("3D distance map: {}".format(distance_map))


if __name__ == '__main__':
    debug()
