# Basic blender scene creation script (for testing)
# Slightly modified from original at
#  https://adrianszatmari.medium.com/quickstart-blender-scripting-tutorial-the-plane-and-the-ball-886b9ffa2cc8

import os

# These are both blender-specific libraries
import bpy
import mathutils

from quickstart.mesh_constructors import new_sphere, new_plane


# Set the render directory
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


# Create objects
sphere = new_sphere((0, 0, 0), 1.0, "MySphere")
plane = new_plane((0, 0, -1), 10, "MyFloor")

# sphere = bpy.data.objects["MySphere"]
# plane = bpy.data.objects["MyFloor"]

# Smoothen sphere
for poly in sphere.data.polygons:
    poly.use_smooth = True

# Create TackyPlastic material
MAT_NAME = "TackyPlastic"
bpy.data.materials.new(MAT_NAME)
material = bpy.data.materials[MAT_NAME]
material.use_nodes = True
material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.2
material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
    1,
    0,
    1,
    1,
)  # Associate TackyPlastic to sphere
if len(sphere.data.materials.items()) != 0:
    sphere.data.materials.clear()
else:
    sphere.data.materials.append(material)

# Create TackyGold material
MAT_NAME = "TackyGold"
bpy.data.materials.new(MAT_NAME)
material = bpy.data.materials[MAT_NAME]
material.use_nodes = True
material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.1
material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
    0.75,
    0.5,
    0.05,
    1,
)
material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.9

# Associate TackyGold to plane
if len(plane.data.materials.items()) != 0:
    plane.data.materials.clear()
else:
    plane.data.materials.append(material)

# Lighten the world light
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
    0.7,
    0.7,
    0.7,
    1,
)

# Move camera
cam = bpy.data.objects["Camera"]
cam.location = cam.location + mathutils.Vector((0.1, 0, 0))
