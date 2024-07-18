# Utility functions for Blender scripts

import os
import bpy


# Set the render file name root - this is where the rendered images will be saved
def set_render_filename(name, relative=True):
    """
    Sets the render file name root for where the rendered images will be saved.

    Parameters:
    - name (str): The base name for the rendered image files.
    - relative (bool): If True, saves the images relative to the script's directory.
      Otherwise, uses the specified name as an absolute path.
    """
    if relative:
        bindir = os.path.abspath(os.path.dirname(__file__))
        bpy.context.scene.render.filepath = os.path.join(bindir, "%s_" % name)
    else:
        bpy.context.scene.render.filepath = "%s_" % name
