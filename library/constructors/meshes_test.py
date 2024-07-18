import unittest
import bpy
from mathutils import Vector  # mathutils is provided by bpy

from library.constructors.meshes import new_sphere, new_plane, new_grid


class TestMeshConstructors(unittest.TestCase):
    def setUp(self):
        """
        Setup that runs before each test method.
        """
        # Delete all objects in the scene to start fresh
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

    def test_new_sphere(self):
        """
        Test if the new_sphere function creates a sphere with the correct properties.
        """
        sphere = new_sphere(location=(1, 2, 3), radius=1, name="TestSphere")
        self.assertEqual(sphere.name, "TestSphere")
        self.assertEqual(sphere.location, Vector((1.0, 2.0, 3.0)))
        self.assertEqual(sphere.scale, Vector((1, 1, 1)))  # Default scale
        self.assertTrue("TestSphere_mesh" in bpy.data.meshes)

    def test_new_plane(self):
        """
        Test if the new_plane function creates a plane with the correct properties.
        """
        plane = new_plane(
            location=(0, 0, 0),
            size=2,
            name="TestPlane",
            rotation=(0, 0, 0),
            scale=(1, 1, 1),
        )
        self.assertEqual(plane.name, "TestPlane")
        self.assertEqual(plane.location, Vector((0, 0, 0)))
        self.assertEqual(plane.scale, Vector((1, 1, 1)))
        self.assertTrue("TestPlane_mesh" in bpy.data.meshes)

    def test_new_grid(self):
        """
        Test if the new_grid function creates a grid with the correct properties.
        """
        grid = new_grid(
            location=(4, 5, 6),
            size=2,
            name="TestGrid",
            xres=8,
            yres=8,
            rotation=(0, 0, 0),
        )
        self.assertEqual(grid.name, "TestGrid")
        self.assertEqual(grid.location, Vector((4, 5, 6)))
        # self.assertEqual(grid.scale, Vector((1, 2, 3)))  # Setting scale has no effect. Why?
        self.assertTrue("TestGrid_mesh" in bpy.data.meshes)
        # Check for the correct number of subdivisions
        self.assertEqual(
            grid.data.vertices[0].co.x, -1
        )  # Assuming size=2 creates a grid from -1 to 1 on the x-axis
        self.assertEqual(len(grid.data.vertices), 9 * 9)  # xres*yres
        self.assertEqual(len(grid.data.polygons), 8 * 8)


if __name__ == "__main__":
    unittest.main()
