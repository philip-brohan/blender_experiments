# Library functions for creating meshes in Blender
# This is just a test of the Blender API and how to use multiple files
import bpy


# Declare constructors
def new_sphere(mylocation, myradius, myname):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64, ring_count=32, radius=myradius, location=mylocation
    )
    current_name = bpy.context.selected_objects[0].name
    sphere = bpy.data.objects[current_name]
    sphere.name = myname
    sphere.data.name = myname + "_mesh"
    return sphere


def new_plane(mylocation, mysize, myname):
    bpy.ops.mesh.primitive_plane_add(
        size=mysize,
        calc_uvs=True,
        enter_editmode=False,
        align="WORLD",
        location=mylocation,
        rotation=(0, 0, 0),
        scale=(0, 0, 0),
    )
    current_name = bpy.context.selected_objects[0].name
    plane = bpy.data.objects[current_name]
    plane.name = myname
    plane.data.name = myname + "_mesh"
    return plane
