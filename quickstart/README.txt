This is a proof of concept of python scripts for blender.
It relies heavily on https://adrianszatmari.medium.com/quickstart-blender-scripting-tutorial-the-plane-and-the-ball-886b9ffa2cc8

First set up an alias to run blender from the command line 
On the mac, I used
blender () { /Applications/Blender.app/Contents/MacOS/Blender "$@"; }

Then set PYTHONPATH to include the directory above this (so the script can find sub-modules)
I do this by creating and using a conda environment (defined in ../environments/blender.yml)

Then run:
  blender --python plane+ball.py
this will launch blender, and run the script to set-up the scene. You can then continue interactively.

Alternatively:
  blender --background --python plane+ball.py -f 0
Will just produce a rendered image 

There are lots more command line options (https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html)
Notably adding -E CYCLES will use the cycles renderer (Note - you have to put extra options in front of '-f 0')

