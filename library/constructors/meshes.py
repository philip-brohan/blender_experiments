# Library functions for creating meshes in Blender

import bpy


def new_sphere(location, radius, name, segments=64, ring_count=32):
    """
    Creates a new UV sphere in the Blender scene.

    Parameters:
    - location (tuple): The location of the sphere as a (x, y, z) tuple.
    - diameter (float): The diameter of the sphere.
    - name (str): The name of the sphere object.
    - segments (int): The number of segments that make up the horizontal circumference of the sphere.
    - ring_count (int): The number of rings that make up the vertical half of the sphere.
    - rotation (tuple): The rotation of the sphere as a (x, y, z) tuple in radians.

    Returns:
    - bpy.types.Object: The created sphere object.
    """
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=ring_count, radius=radius, location=location
    )
    current_name = bpy.context.view_layer.objects.selected[0].name
    sphere = bpy.data.objects[current_name]
    sphere.name = name
    sphere.data.name = name + "_mesh"
    return sphere


def new_plane(location, size, name, rotation=(0, 0, 0), scale=(1, 1, 1)):
    """
    Creates a new plane in the Blender scene.

    Parameters:
    - location (tuple): The location of the plane as a (x, y, z) tuple.
    - size (float): The size of the plane.
    - name (str): The name of the plane object.
    - rotation (tuple): The rotation of the plane as a (x, y, z) tuple in radians.
    - scale (tuple): The scale of the plane as a (x, y, z) tuple.

    Returns:
    - bpy.types.Object: The created plane object.
    """
    bpy.ops.mesh.primitive_plane_add(
        size=size,
        calc_uvs=True,
        enter_editmode=False,
        align="WORLD",
        location=location,
        rotation=rotation,
        scale=scale,
    )
    current_name = bpy.context.view_layer.objects.selected[0].name
    plane = bpy.data.objects[current_name]
    plane.name = name
    plane.data.name = name + "_mesh"
    return plane


def new_grid(location, size, name, xres=10, yres=10, rotation=(0, 0, 0)):
    """
    Creates a new grid in the Blender scene.

    Parameters:
    - location (tuple): The location of the grid as a (x, y, z) tuple.
    - size (float): The size of the grid.
    - name (str): The name of the grid object.
    - xres (int): The number of polygons along the x-axis.
    - yres (int): The number of polygons along the y-axis.
    - rotation (tuple): The rotation of the grid as a (x, y, z) tuple in radians.

    Returns:
    - bpy.types.Object: The created grid object.
    """
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=xres,
        y_subdivisions=yres,
        size=size,
        calc_uvs=True,
        enter_editmode=False,
        align="WORLD",
        location=location,
        rotation=rotation,
    )
    current_name = bpy.context.view_layer.objects.selected[0].name
    grid = bpy.data.objects[current_name]
    grid.name = name
    grid.data.name = grid.name + "_mesh"
    return grid
