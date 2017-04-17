bl_info = {
    "name": "Stop Motion",
    "description": "A script that enables stop motion for Blender",
    "author": "Darius Blaszyk",
    "version": (0, 0, 1),
    "blender": (2, 70, 0),
    "location": "UV/Image Editor > Tool Shelf (T)",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/daar/Stop-Motion-Blender/wiki",
    "tracker_url": "",
    "category": "Animation"
}

import bpy
import os
import threading

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

AutoRefresh = False

def capture_frame(fname):
    print("capture frame")
    #run the capture application from the commandline
    os.system("ffmpeg -y -f video4linux2 -i /dev/video1 -ss 0:0:1 -frames 1 " + fname)

def refresh_preview():
    #dir = context.scene.my_tool.SMB_output_directory
    dir = '/tmp/'
    fname = 'SMResult.jpg'
    newfile_name = os.path.join(dir, fname)
        
    #capture a new frame
    capture_frame(newfile_name)

    #update the image in the UV/Image Editor
    bpy.ops.image.reload()
    
    if AutoRefresh:
        threading.Timer(1, refresh_preview).start()

class SMB_ConnectCamera(bpy.types.Operator):
    """Connect to the camera"""
    bl_idname = "object.sm_connect_camera"
    bl_label = "Connect camera"

    def execute(self, context):
        print("connect camera")
        
        global AutoRefresh
        AutoRefresh = not AutoRefresh
        
        refresh_preview()

        return {'FINISHED'}

class SMB_CaptureFrame(bpy.types.Operator):
    """Capture a single frame from the active camera"""
    bl_idname = "object.sm_capture_frame"
    bl_label = "Capture frame"

    def execute(self, context):
        print("capture frame")
        print(context.scene.my_tool.SMB_output_directory)
        
        #proceed to next frame
        bpy.context.scene.frame_current += 1

        dir = context.scene.my_tool.SMB_output_directory
        fname = format(bpy.context.scene.frame_current, '04d') + '.jpg'
        newfile_name = os.path.join(dir, fname)
        
        #capture a new frame
        capture_frame(newfile_name)
        
        #refresh the Movie Clip Editor
        #bpy.ops.clip.open(directory=dir, files=[{"name":fname}])
        
        #reload the frame in the Movie Clip Editor
        bpy.context.area.type = 'SEQUENCE_EDITOR'
        fstart = bpy.context.scene.frame_current
        bpy.ops.sequencer.image_strip_add(directory=dir, files=[{"name":fname}], relative_path=True, show_multiview=False, frame_start=fstart, frame_end=fstart, channel=1)
        bpy.context.area.type = 'IMAGE_EDITOR'
        
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    store properties in the active scene
# ------------------------------------------------------------------------

class MySettings(PropertyGroup):

    my_bool = BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    my_int = IntProperty(
        name = "Set a value",
        description="An integer property",
        default = 23,
        min = 10,
        max = 100
        )

    my_float = FloatProperty(
        name = "Set a value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )

    SMB_output_directory = StringProperty(
        name="Output",
        attr="custompath",
        description="Directory/name to save the grabbed frames to",
        maxlen= 1024,
        subtype='DIR_PATH',
        default= "/tmp/"
        )

# ------------------------------------------------------------------------
#    myTool in the image editor
# ------------------------------------------------------------------------

class SB_MCE_editor(Panel):
    bl_idname = "SB_IMG_panel"
    bl_label = "Stop Motion"
    bl_category = "Stop Motion"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        #connect to the first camera
        row = layout.row()
        col = row.column()
        col.operator("object.sm_connect_camera", icon="CAMERA_DATA")

        #output folder for the screen captures 
        layout.prop(mytool, "SMB_output_directory", text="Output dir")
         
        #capture a single frame from the camera
        row = layout.row()
        col = row.column()
        col.operator("object.sm_capture_frame", icon="RENDER_STILL")

        # display the properties
        #layout.prop(mytool, "my_bool", text="Bool Property")
        #layout.prop(mytool, "my_int", text="Integer Property")
        #layout.prop(mytool, "my_float", text="Float Property")

        # check if bool property is enabled
        #if (mytool.my_bool == True):
        #    print ("Property Enabled")
        #else:
        #    print ("Property Disabled")


# ------------------------------------------------------------------------
# register and unregister functions
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(SMB_ConnectCamera)
    bpy.utils.register_class(SMB_CaptureFrame)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)

def unregister():
    bpy.utils.unregister_class(SMB_ConnectCamera)
    bpy.utils.unregister_class(SMB_CaptureFrame)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()