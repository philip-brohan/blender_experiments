#!/usr/bin/env python

import os
import rasterio
import numpy as np

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

import cmocean

img = rasterio.open("Boulder.tif")
aspect = (img.bounds.top - img.bounds.bottom) / (img.bounds.right - img.bounds.left)
rdata = img.read(1)
height = rdata.shape[0]
width = rdata.shape[1]
cols, rows = np.meshgrid(np.arange(width), np.arange(height))
xs, ys = rasterio.transform.xy(img.transform, rows, cols)
lons = np.array(xs)
lats = np.array(ys)

fig = Figure(
    figsize=(10, 10 * aspect),  # Width, Height (inches)
    dpi=300,
    facecolor=(0.5, 0.5, 0.5, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=True,
    subplotpars=None,
    tight_layout=None,
)
fig.set_frameon(False)
# Attach a canvas
canvas = FigureCanvas(fig)

font = {
    "family": "sans-serif",
    "sans-serif": "Arial",
    "weight": "normal",
    "size": 20,
}
matplotlib.rc("font", **font)
ax_dem = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax_dem.set_xlim(np.min(lons), np.max(lons))
ax_dem.set_ylim(np.min(lats), np.max(lats))
ax_dem.set_aspect("auto")
ax_dem.axis("off")

mask_img = ax_dem.pcolormesh(
    lons, lats, rdata, cmap=cmocean.cm.gray, alpha=1.0, zorder=20
)

fig.savefig("Boulder.png")
