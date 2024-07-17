# Make image based on the view of the Front Range from Louisville, CO

import os
import sys
import math
import numpy as np

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
terrain_tx = bpy.data.images.load("%s/get_DEM/Boulder.tif" % bindir)
terrain_np = np.array(terrain_tx.pixels[:])
terrain_np = terrain_np.reshape((terrain_tx.size[1], terrain_tx.size[0], 4))  # units?
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
bpy.ops.mesh.primitive_grid_add(
    x_subdivisions=polygons_per_degree,
    y_subdivisions=polygons_per_degree,
    size=horizontal_scale,
    calc_uvs=True,
    enter_editmode=False,
    align="WORLD",
    location=(0.0, 0.0, 0.0),
    rotation=(0.0, 0.0, math.radians(90)),  # West is left
    scale=(1.0, 1.0, 1.0),
)
current_name = bpy.context.selected_objects[0].name
terrain = bpy.data.objects[current_name]
terrain.name = "Terrain"
terrain.data.name = terrain.name + "_mesh"
# Scale from geographic projecvtion to (approximately) actual shape
terrain.scale.x = math.cos(math.radians(view_lat))

# Smooth the terrain
for poly in terrain.data.polygons:
    poly.use_smooth = True

# Move the camera to the viewpoint outside Louisville
camera_lon_fraction = (view_lat - lat_range[0]) / (lat_range[1] - lat_range[0])
camera_lat_fraction = (view_lon - lon_range[0]) / (lon_range[1] - lon_range[0])
bpy.data.objects["Camera"].location = (
    horizontal_scale * (camera_lon_fraction - 0.5) * terrain.scale.x,
    horizontal_scale * (camera_lat_fraction - 0.5),
    view_height * vertical_scale + view_height_above_ground,
)
# Point the camera due west
bpy.data.objects["Camera"].rotation_mode = "XYZ"
bpy.data.objects["Camera"].rotation_euler = view_direction

# Set the camera lens - this is the focal length in mm
# Very small value (for wide angle image)
bpy.data.objects["Camera"].data.lens = 5.0
# Set the camera image aspect ratio - wide and short
bpy.context.scene.render.resolution_x = 4000
bpy.context.scene.render.resolution_y = 500


# Add a displace modifier to the terrain for the mountains
# Take the displacement from the Boulder.tif file
displace_modifier = terrain.modifiers.new(name="Displacement", type="DISPLACE")
displace_modifier.strength = vertical_scale
displace_modifier.direction = "Z"
displace_modifier.mid_level = 0.0
displace_modifier.texture_coords = "UV"
displace_modifier.texture = bpy.data.textures.new(name="Displacement", type="IMAGE")
displace_modifier.texture.extension = "EXTEND"
displace_modifier.texture.image = terrain_tx

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
# Need dropoff to have 0-1 range so it works as a texture
# But preserve the scale for the displace modifier
dropoff_scale = np.max(dropoff)
# Convert from scalar to RGB
dropoff /= np.max(dropoff)
dropoff = np.stack((dropoff, dropoff, dropoff), axis=2)
alpha = np.ones((polygons_per_degree, polygons_per_degree))
dropoff = np.dstack((dropoff, alpha))
# Convert from numpy to texture
dropoff = dropoff.flatten()
dropoff_tx = bpy.data.images.new(
    "Dropoff",
    polygons_per_degree,
    polygons_per_degree,
)
dropoff_tx.pixels[:] = dropoff
dropoff_tx.update()
# Add the dropoff texture as a displace modifier
displace_modifier = terrain.modifiers.new(name="Dropoff", type="DISPLACE")
displace_modifier.strength = -vertical_scale * dropoff_scale
displace_modifier.direction = "Z"
displace_modifier.mid_level = 0.0
displace_modifier.texture_coords = "UV"
displace_modifier.texture = bpy.data.textures.new(name="Dropoff", type="IMAGE")
displace_modifier.texture.extension = "EXTEND"
displace_modifier.texture.image = dropoff_tx

# Colour the terrain - first create an array of RGBA values
terrain_col = terrain_np.copy()  # already in RGBA format
terrain_col[:, :, 0] = np.random.random((terrain_col.shape[0], terrain_col.shape[1]))
terrain_col[:, :, 1] = np.random.random((terrain_col.shape[0], terrain_col.shape[1]))
terrain_col[:, :, 2] = np.random.random((terrain_col.shape[0], terrain_col.shape[1]))
# Then convert the array into a texture
# terrain_col_tx = bpy.data.images.new(
#    "Dropoff",
#    terrain_col.shape[0],
#    terrain_col.shape[1],
# )
# terrain_col_tx.pixels[:] = terrain_col.flatten()
terrain_col_tx = bpy.data.images.load("%s/20CRv3_E-grid.png" % bindir)

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
texture_node.image = terrain_col_tx
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
current_name = bpy.context.selected_objects[0].name
backdrop = bpy.data.objects[current_name]
backdrop.name = "Backdrop"
backdrop.data.name = backdrop.name + "_mesh"
# Wider in y because of wide angle camera
backdrop.scale.x = 6
backdrop.scale.y = 0.75
