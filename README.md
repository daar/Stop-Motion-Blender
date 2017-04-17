[![license](https://img.shields.io/badge/license-%20MIT-blue.svg)](../master/LICENSE) <img src="https://www.blender.org/wp-content/themes/bthree/assets/images/logo.png" alt="Blender" width="15%" height="15%"/>

# Stop motion blender
This script  adds stop motion capabilitiy to [blender](www.blender.org). For now SM-blender relies on ffmpeg and it's availbility from the commandline.

> Please be aware that for the time being *stop motion blender* is a work in progress and that some features might break, change or dissapear. In case you do have suggestions and/or want to help develop this script, please file an issue or make a fork. Please share any video demo's or other descriptions on how to use this script and a link will be put on the wiki.

## Introduction
After dowloading the stopmotion.blend file, the script *SM_blender* can be run. This will create a new tool panel in the **UV/Image Editor**.

**Connect camera**: this will connect to the current camera and setup the *UV/Image editor* and create and auto refreshing preview.

**Output dir**: This folder will contain all images being captured. 

**Capture frame**: This will capture a single frame from the camera and place the image in the folder specified. A link to this image is added in the **Video Sequence Editor** so it can be rendered later on. Make sure you keep the images in this folder.
