import unittest
import bpy
from library.constructors import cameras


class TestCameraConstructor(unittest.TestCase):
    def setUp(self):
        # Clear existing cameras before each test
        cams = [obj for obj in bpy.data.objects if obj.type == "CAMERA"]
        for cam in cams:
            bpy.data.objects.remove(cam, do_unlink=True)

    def test_camera_creation(self):
        # Expected values
        location = (0, 0, 0)
        rotation = (0, 0, 0)
        name = "TestCamera"
        type = "PERSP"
        lens = 50
        sensor_width = 36
        sensor_height = 24
        active = True

        # Call the function
        created_camera = cameras.new_camera(
            location, rotation, name, type, lens, sensor_width, sensor_height, active
        )

        # Assertions to verify the camera was created with the correct properties
        self.assertEqual(created_camera.name, name)
        self.assertEqual(created_camera.data.lens, lens)
        self.assertEqual(created_camera.data.sensor_width, sensor_width)
        self.assertEqual(created_camera.data.sensor_height, sensor_height)
        # Verify if the camera is active
        self.assertEqual(bpy.context.scene.camera, created_camera)


if __name__ == "__main__":
    unittest.main()
