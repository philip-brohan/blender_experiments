# Make image based on the view of the Front Range from Louisville, CO

import os
import sys
import math
import numpy as np

# These are both blender-specific libraries
import bpy
import mathutils

from library.utilities import set_render_filename
from library.constructors.meshes import new_grid
from library.constructors.cameras import new_camera, set_viewpoint
from library.constructors.images import make_image_from_numpy, make_numpy_from_image

# Script directory - to find the textures
bindir = os.path.abspath(os.path.dirname(__file__))

# Filename for the rendered image (will have '_000.png' appended)
set_render_filename("Louisville", relative=True)

# Clear the scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Were going to make a scene with 1x1 degrees of terrain
horizontal_scale = 10.0  # m per degree at equator
vertical_scale = 100.0  # m per unit elevation
polygons_per_degree = 1000

# Set the view location and orientation
view_lat = 39.97724
view_lon = -105.18807
view_height_above_ground = 0.035
view_direction = (math.radians(104), 0, math.radians(180))

# Set the terrain data range
lat_range = (39.5, 40.5)
lon_range = (-106.0, -105.0)
# Load the terrain as an image texture
terrain_img = bpy.data.images.load("%s/get_DEM/Boulder.tif" % bindir)
terrain_np = make_numpy_from_image(terrain_img)
# Get height at the viewpoint
view_lat_fraction = (view_lat - lat_range[0]) / (lat_range[1] - lat_range[0])
view_lon_fraction = (view_lon - lon_range[0]) / (lon_range[1] - lon_range[0])
view_height = terrain_np[
    int(
        terrain_np.shape[0] * (view_lat - lat_range[0]) / (lat_range[1] - lat_range[0])
    ),
    int(
        terrain_np.shape[1] * (view_lon - lon_range[0]) / (lon_range[1] - lon_range[0])
    ),
    0,
]

# Make a plane to be the terrain
terrain = new_grid(
    location=(0.0, 0.0, 0.0),
    size=horizontal_scale,
    name="Terrain",
    xres=polygons_per_degree,
    yres=polygons_per_degree,
    rotation=(0.0, 0.0, math.radians(90)),  # West is left,
)
# Scale from geographic projecvtion to (approximately) actual shape
terrain.scale.x = math.cos(math.radians(view_lat))

# Smooth the terrain
for poly in terrain.data.polygons:
    poly.use_smooth = True

# Move the camera to the viewpoint outside Louisville
camera_lon_fraction = (view_lat - lat_range[0]) / (lat_range[1] - lat_range[0])
camera_lat_fraction = (view_lon - lon_range[0]) / (lon_range[1] - lon_range[0])
camera_location = (
    horizontal_scale * (camera_lon_fraction - 0.5) * terrain.scale.x,
    horizontal_scale * (camera_lat_fraction - 0.5),
    view_height * vertical_scale + view_height_above_ground,
)
camera = new_camera(camera_location, view_direction, "Camera", lens=5.0, active=True)
# Set the camera image aspect ratio - wide and short
# bpy.context.scene.render.resolution_x = 4000
# bpy.context.scene.render.resolution_y = 500

# Set the viewpoint in the 3D Viewport
# Doesn't work properly. Have not figured out why not.
# set_viewpoint((0, 2, 2), view_direction)


# Add a displace modifier to the terrain for the mountains
# Take the displacement from the Boulder.tif file
displace_modifier = terrain.modifiers.new(name="Displacement", type="DISPLACE")
displace_modifier.strength = vertical_scale
displace_modifier.direction = "Z"
displace_modifier.mid_level = 0.0
displace_modifier.texture_coords = "UV"
displace_modifier.texture = bpy.data.textures.new(name="Displacement", type="IMAGE")
displace_modifier.texture.extension = "EXTEND"
displace_modifier.texture.image = terrain_img

# Calculate the curvature of the Earth down from the viewpoint
# Add it to the terrain as a second displace modifier
grid_lats = np.linspace(lat_range[0], lat_range[1], polygons_per_degree)
grid_lons = np.linspace(lon_range[0], lon_range[1], polygons_per_degree)
grid_lats, grid_lons = np.meshgrid(grid_lats, grid_lons)
grid_lats -= view_lat
grid_lons -= view_lon
distance = np.sqrt(grid_lats**2 + (grid_lons * terrain.scale.x) ** 2) * 111.111  # km
dropoff = 6371 - np.sqrt(6371**2 - distance**2)  # km
dropoff = np.maximum(0, dropoff)
dropoff = dropoff / 233.000  # Empirical scale km to terrain units
dropoff = dropoff.T  # Transpose to match Blender's UV coordinates
dropoff_scale = np.max(dropoff)
dropoff_img = make_image_from_numpy(dropoff, name="Dropoff", rescale=True)
dropoff_img.update()
# Add the dropoff texture as a displace modifier
displace_modifier = terrain.modifiers.new(name="Dropoff", type="DISPLACE")
displace_modifier.strength = -vertical_scale * dropoff_scale
displace_modifier.direction = "Z"
displace_modifier.mid_level = 0.0
displace_modifier.texture_coords = "UV"
displace_modifier.texture = bpy.data.textures.new(name="Dropoff", type="IMAGE")
displace_modifier.texture.extension = "EXTEND"
displace_modifier.texture.image = dropoff_img

# Colour the terrain
terrain_col_img = bpy.data.images.load("%s/textures/20CRv3_E-grid.png" % bindir)

# terrain_col_tx.update()
# Then use the texture in a material
bpy.data.materials.new("Terrain")
terrain_material = bpy.data.materials["Terrain"]
terrain_material.name = "Terrain"
terrain_material.diffuse_color = (0.5, 0.5, 0.5, 1.0)
terrain_material.use_nodes = True
terrain_material.node_tree.nodes["Principled BSDF"].inputs[
    "Roughness"
].default_value = 0.5
terrain_material.node_tree.nodes["Principled BSDF"].inputs[
    "Metallic"
].default_value = 0.0
# Create a Mapping node
mapping_node = terrain_material.node_tree.nodes.new(type="ShaderNodeMapping")
# Set the rotation to 90 degrees on the Z axis
mapping_node.inputs["Rotation"].default_value[2] = math.pi * 0
# Create a Texture Coordinate node
tex_coord_node = terrain_material.node_tree.nodes.new(type="ShaderNodeTexCoord")
texture_node = terrain_material.node_tree.nodes.new(type="ShaderNodeTexImage")
texture_node.image = terrain_col_img
terrain_material.node_tree.links.new(
    tex_coord_node.outputs["UV"], mapping_node.inputs["Vector"]
)
terrain_material.node_tree.links.new(
    mapping_node.outputs["Vector"], texture_node.inputs["Vector"]
)
terrain_material.node_tree.links.new(
    texture_node.outputs["Color"],
    terrain_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"],
)
# Then apply the material to the terain mesh
terrain.data.materials.append(terrain_material)

# Add a backdrop
bpy.ops.mesh.primitive_plane_add(
    size=horizontal_scale,
    calc_uvs=True,
    enter_editmode=False,
    align="WORLD",
    location=(
        0.0,
        -terrain.scale.x * horizontal_scale / 2,
        0.75 * horizontal_scale / 2,
    ),
    rotation=(math.pi * 2 - view_direction[0], 0, 0),  # Perpendicular to camera angle
    scale=(1.0, 1.0, 1.0),
)
current_name = bpy.context.view_layer.objects.selected[0].name
backdrop = bpy.data.objects[current_name]
backdrop.name = "Backdrop"
backdrop.data.name = backdrop.name + "_mesh"
# Wider in y because of wide angle camera
backdrop.scale.x = 6
backdrop.scale.y = 0.75
# add a backdrop image
backdrop_tx = bpy.data.images.load(
    "%s/textures/Farragut-DD-348-1942-01-0021.jpg" % bindir
)
bpy.data.materials.new("Backdrop")
backdrop_material = bpy.data.materials["Backdrop"]
backdrop_material.name = "Backdrop"
backdrop_material.diffuse_color = (0.5, 0.5, 0.5, 1.0)
backdrop_material.use_nodes = True
backdrop_material.node_tree.nodes["Principled BSDF"].inputs[
    "Roughness"
].default_value = 0.5
backdrop_material.node_tree.nodes["Principled BSDF"].inputs[
    "Metallic"
].default_value = 0.0
backdrop_mapping_node = backdrop_material.node_tree.nodes.new(type="ShaderNodeMapping")
backdrop_mapping_node.inputs["Rotation"].default_value[2] = math.pi * 0.5
backdrop_tex_coord_node = backdrop_material.node_tree.nodes.new(
    type="ShaderNodeTexCoord"
)
backdrop_texture_node = backdrop_material.node_tree.nodes.new(type="ShaderNodeTexImage")
backdrop_texture_node.image = backdrop_tx
backdrop_material.node_tree.links.new(
    backdrop_tex_coord_node.outputs["UV"], backdrop_mapping_node.inputs["Vector"]
)
backdrop_material.node_tree.links.new(
    backdrop_mapping_node.outputs["Vector"], backdrop_texture_node.inputs["Vector"]
)
backdrop_material.node_tree.links.new(
    backdrop_texture_node.outputs["Color"],
    backdrop_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"],
)
backdrop.data.materials.append(backdrop_material)

# Add sky lighting
bpy.context.scene.world = bpy.data.worlds.new("Sky")
bpy.context.scene.world.use_nodes = True
world_nodes = bpy.context.scene.world.node_tree.nodes
world_links = bpy.context.scene.world.node_tree.links

# Clear existing nodes to start fresh
world_nodes.clear()

# Create a new Sky Texture node
sky_texture_node = world_nodes.new(type="ShaderNodeTexSky")

# Create a Background node
background_node = world_nodes.new(type="ShaderNodeBackground")

# Create an Output node (World Output)
output_node = world_nodes.new(type="ShaderNodeOutputWorld")

# Link Sky Texture node to Background node
world_links.new(sky_texture_node.outputs["Color"], background_node.inputs["Color"])

# Link Background node to World Output node
world_links.new(background_node.outputs["Background"], output_node.inputs["Surface"])
