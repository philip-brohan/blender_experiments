import unittest
import bpy
import numpy as np
from images import make_numpy_from_image, make_image_from_numpy


class ImageMock:
    def __init__(self, pixels, size):
        self.pixels = pixels
        self.size = size


class TestMakeNumpyFromImage(unittest.TestCase):
    def test_make_numpy_from_image(self):
        # Simulate an Image object
        img = ImageMock(
            pixels=[
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1.0,
                1.1,
                1.2,
                1.3,
                1.4,
                1.5,
                1.6,
            ],
            size=[2, 2],
        )

        # Expected numpy array
        expected_array = np.array(
            [
                [[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]],
                [[0.9, 1.0, 1.1, 1.2], [1.3, 1.4, 1.5, 1.6]],
            ],
            dtype=np.float32,
        )

        # Call the function
        result_array = make_numpy_from_image(img)

        # Verify the result
        np.testing.assert_array_almost_equal(result_array, expected_array, decimal=2)


class TestMakeImageFromNumpy(unittest.TestCase):
    def setUp(self):
        # Cleanup before each test
        bpy.ops.wm.read_factory_settings(use_empty=True)

    def test_create_image_from_numpy(self):
        # Create a numpy array
        arr = np.random.rand(4, 4, 4).astype(np.float32)  # Example array

        # Record the number of images before the function call
        num_images_before = len(bpy.data.images)

        # Call the function to create an Image
        img = make_image_from_numpy(arr, name="test_image")

        # Verify a new Image was added
        self.assertEqual(len(bpy.data.images), num_images_before + 1)

        # Verify the Image is the one we created
        self.assertTrue(img.name in bpy.data.images)

        # Additional verifications can go here, depending on what properties
        # the image is expected to have based on the numpy array


if __name__ == "__main__":
    unittest.main()
