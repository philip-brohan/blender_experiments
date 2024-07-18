import unittest
import os
import bpy

# Assuming library.utilities is the correct path
from library.utilities import set_render_filename


class TestSetRenderFilename(unittest.TestCase):
    def setUp(self):
        """
        Setup that runs before each test method.
        """
        # Store the original filepath to restore it after tests
        self.original_filepath = bpy.context.scene.render.filepath

    def tearDown(self):
        """
        Cleanup that runs after each test method.
        """
        # Restore the original filepath
        bpy.context.scene.render.filepath = self.original_filepath

    def test_relative_path(self):
        """
        Test if the function correctly sets a relative file path.
        """
        set_render_filename("testImage", relative=True)
        expected_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "testImage_"
        )
        self.assertEqual(bpy.context.scene.render.filepath, expected_path)

    def test_absolute_path(self):
        """
        Test if the function correctly sets an absolute file path.
        """
        # Use a hypothetical absolute path for testing
        test_path = "/tmp/testImage"
        set_render_filename(test_path, relative=False)
        self.assertEqual(bpy.context.scene.render.filepath, test_path + "_")


if __name__ == "__main__":
    unittest.main()
