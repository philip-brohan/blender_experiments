# Utility functions to make Images

import bpy
import numpy as np


def make_image_from_numpy(arr, name="img", rescale=False):
    """
    Create a new image texture from a numpy array.

    Parameters:
    - arr (numpy.ndarray): The numpy array to use for the texture.
    - name (str): The name of the image.
    - rescale (bool): If True, rescale the array to be between 0 and 1.

    Returns:
    - bpy.types.Image: The created image texture.
    """

    # Rescale the array to be between 0 and 1
    if rescale:
        arr = (arr - arr.min()) / (arr.max() - arr.min())

    # Need the numpy array to be in RBGA format
    if len(arr.shape) == 2:
        arr = np.stack((arr, arr, arr), axis=2)
    if arr.shape[2] == 3:
        alpha = np.ones((arr.shape[0], arr.shape[1]))
        arr = np.dstack((arr, alpha))

    # Create a new image
    img = bpy.data.images.new(
        name=name,
        width=arr.shape[1],
        height=arr.shape[0],
    )

    # Set the pixels of the image
    img.pixels[:] = arr.flatten()

    return img


def make_numpy_from_image(img):
    """
    Create a numpy array from an image texture.

    Parameters:
    - texture (bpy.types.Image): The image to convert.

    Returns:
    - numpy.ndarray: The numpy array of the image.
    """

    # Get the pixels of the texture
    pixels = img.pixels

    # Create a numpy array from the pixels
    arr = np.array(pixels[:])

    # Reshape the array to be in RGBA format
    arr = arr.reshape((img.size[1], img.size[0], 4))

    return arr
