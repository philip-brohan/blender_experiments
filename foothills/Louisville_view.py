# Make image based on the view of the Front Range from Louisville, CO

import os
import math

# These are both blender-specific libraries
import bpy
import mathutils

# Set the render directory - this is where the rendered images will be saved
bindir = None
try:
    bindir = os.path.abspath(os.path.dirname(__file__))
except Exception as e:
    pass

if bindir is not None:
    bpy.context.scene.render.filepath = os.path.join(bindir, "plane+ball_")

# Remove initial cube
try:
    cube = bpy.data.objects["Cube"]
    bpy.data.objects.remove(cube, do_unlink=True)
except:
    print("Object bpy.data.objects['Cube'] not found")

bpy.ops.outliner.orphans_purge()

# Make a plane to be the terrain
bpy.ops.mesh.primitive_grid_add(
    x_subdivisions=1000,
    y_subdivisions=1000,
    size=10.0,
    calc_uvs=True,
    enter_editmode=False,
    align="WORLD",
    location=(0.0, 0.0, 0.0),
    rotation=(0.0, 0.0, 0.0),
    scale=(0.0, 0.0, 0.0),
)
current_name = bpy.context.selected_objects[0].name
terrain = bpy.data.objects[current_name]
terrain.name = "Terrain"
terrain.data.name = terrain.name + "_mesh"

# Add a displace modifier to the terrain
# Take the displacement from the Boulder.tif file
displace_modifier = terrain.modifiers.new(name="Displacement", type="DISPLACE")
displace_modifier.strength = 100.0
displace_modifier.direction = "Z"
displace_modifier.mid_level = 0.0
displace_modifier.texture_coords = "UV"
displace_modifier.texture = bpy.data.textures.new(name="Displacement", type="IMAGE")
displace_modifier.texture.image = bpy.data.images.load(
    "%s/get_DEM/Boulder.tif" % bindir
)

# Move the camera to the viewpoint outside Louisville
# Location is: lon -105.18807, lat 39.97724, height= 1.0, looking East
# Terrain data range is: -105 to -106, 39.5 to 40.5, scale is 10.0
bpy.data.objects["Camera"].location = (10 - 0.18807 * 10 - 5, 0.47724 * 10 - 5, 0.5)
bpy.data.objects["Camera"].rotation_mode = "XYZ"
bpy.data.objects["Camera"].rotation_euler = (math.radians(90), 0, math.radians(90))

# Set the camera lens - this is the focal length in mm
# Very small value (for wide angle image)
bpy.data.objects["Camera"].data.lens = 10.0
# Set the camera image aspect ratio - wide and short
bpy.context.scene.render.resolution_x = 1000
bpy.context.scene.render.resolution_y = 330
