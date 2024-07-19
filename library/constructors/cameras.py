# Library functions for creating cameras in Blender

import bpy
import mathutils


def new_camera(
    location,
    rotation,
    name,
    type="PERSP",
    lens=50,
    sensor_width=36,
    sensor_height=24,
    active=True,
):
    """
    Creates a new camera in the Blender scene.

    Parameters:
    - location (tuple): The location of the camera as a (x, y, z) tuple.
    - rotation (tuple): The rotation of the camera as a (x, y, z) tuple in radians.
    - name (str): The name of the camera object.
    - type (str): The type of the camera. Can be 'PERSP' for perspective (default),
                    'ORTHO' for orthographic, 'PANO' for panoramic.
    - lens (float): The focal length of the camera in millimeters.
    - sensor_width (float): The width of the camera sensor in millimeters.
    - sensor_height (float): The height of the camera sensor in millimeters.
    - active (bool): If True, set the camera as the active camera for the scene

    Returns:
    - bpy.types.Object: The created camera object.
    """
    bpy.ops.object.camera_add(location=location, rotation=rotation)
    current_name = bpy.context.view_layer.objects.selected[0].name
    camera = bpy.data.objects[current_name]
    camera.name = name
    camera.data.name = name + "_camera"
    camera.data.type = type
    camera.data.lens = lens
    # camera.data.sensor_width = sensor_width
    # camera.data.sensor_height = sensor_height
    if active:
        bpy.context.scene.camera = camera
    return camera


# This function does not work as expected - I don't know why not
def set_viewpoint(location, rotation):
    """
    Sets the viewpoint in the 3D Viewport.

    Parameters:
    - location (tuple): The location of the viewpoint as a (x, y, z) tuple.
    - rotation (tuple): The rotation of the viewpoint as a Euler (x, y, z) tuple.
    """

    # We can't just run this. It needs to wait until the 3D Viewport is active.
    # So define a function to be called later by the app handler

    def set_viewpoint_callback(scene):
        location2 = location
        rotation2 = mathutils.Euler((0, 0, 0), "XYZ").to_quaternion()

        try:
            for area in bpy.context.screen.areas:
                if area.type == "VIEW_3D":
                    for region in area.regions:
                        if region.type == "WINDOW":
                            # Access the RegionView3D object
                            rv3d = area.spaces.active.region_3d
                            # Set the viewpoint location and rotation
                            rv3d.view_location = location2
                            # rv3d.view_rotation = rotation2
                            # Clear the handler to prevent future calls
                            bpy.app.handlers.depsgraph_update_post.remove(
                                set_viewpoint_callback
                            )
                            return
        except AttributeError as e:  # # No context available yet
            return

    # Register the function to run after graph update
    bpy.app.handlers.depsgraph_update_post.append(set_viewpoint_callback)
