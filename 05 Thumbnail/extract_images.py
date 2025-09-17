import glob
import shutil

# Path to the images created by "create_preview"
image_path = "C:\\InsectScanner\\NoahSchluessel\\Quality control glb\\Lucerne Last 24\\JPG\\"
# Path to the folder containing the projects
project_path = "Z:\\01_SCANNED_AND_PROCESSED\\02 FINAL\\"


# Returns the index, elevation and rotation of the closest image
def get_closest(elevation, rotation, ref):
        best_score = 100000
        best_ele = 0
        best_rot = 0
        best_index = 0
        for i, (ele, rot) in enumerate(zip(elevation, rotation)):
            score = abs(ref[0] - ele) + abs(ref[1] - rot)
            if  score < best_score:
                best_index = i
                best_score = score
                best_ele = ele
                best_rot = rot
        return best_index, best_ele, best_rot

# Extracts the closest image for every reference value
def extract_images(image_path, ref_values):
    images = glob.glob(image_path+"*.jpeg")
    elevation = []
    rotation = []
    for image in images:
        image = image.split("\\")[-1]
        image = '.'.join(image.split(".")[:-1])
        image = image.split("_")
        elevation.append(float(image[-2]))
        rotation.append(float(image[-1]))
    res = []
    for ref in ref_values:
        index, _, _ = get_closest(elevation, rotation, ref)
        res.append(images[index])
    return res

if __name__ == '__main__':
    ref_values = [(0, 180), (-50, 30), (50, 120)] # The positions that should be extracted
    ref_strings = ['side_image', 'bottom_image', 'top_image'] # How the images should be named
    image_folder = "redof\\" # Folder to extract the images from
    images = glob.glob(image_path+"*.jpg") # Create a list of all images
    projects = set([image.removesuffix('.jpg').
                    removesuffix('_bottom_3d').
                    removesuffix('_top_3d').
                    removesuffix('_side_3d').
                    split('\\')[-1] for image in images])
    with open('out.txt', 'w') as f:
         for project in projects:
              f.write(project + "\n")
    
    for project in projects:
        print("Project ", project)
        images = extract_images(project_path + project + "\\" + image_folder, ref_values)
        for ref_string, image in zip(ref_strings, images):
            shutil.copy(image, image_path + project + "_" + ref_string +".jpg")
