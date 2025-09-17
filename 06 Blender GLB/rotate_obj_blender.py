import bpy
import os
import glob
import shutil

####################################################################
# Settings
import_path = "C:\\InsectScanner\\Data\DataCurrent\\0_PREPROCESS\\0.5_BLENDER_CHRISTIAN\\" # Where the projects currently are.
export_path =  "C:\\InsectScanner\Data\DataCurrent\\0_PREPROCESS\\1_READY_FOR_BLENDER\\" # Where the projects are after the script finishes.
model_path = "Model\\"
####################################################################

projects = glob.glob(import_path+"*\\")

for project in projects:
    name = project.split("\\")[-2]
    try:
        obj_path = glob.glob(os.path.join(project, model_path, '*.obj'))[0]
    except:
        # If there is no obj file, skip the folder
        print("Skipping folder " + project)
        continue
    # Import the obj with the correct orienation
    bpy.ops.wm.obj_import(filepath=obj_path, forward_axis='X', up_axis='Z')
    # Set the transform orientation to local
    bpy.data.scenes["Scene"].transform_orientation_slots[0].type = 'LOCAL'
    # Save the blend file
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(project, model_path, (name + '.blend')))
    # Reset Blender and move folder
    bpy.ops.wm.read_factory_settings(use_empty=True)
    shutil.move(project, os.path.join(export_path, name))

