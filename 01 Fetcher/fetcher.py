#Author: Si An Oliver Tran
import argparse
import sys
import os
import re
import shutil
import logging
import time
import datetime
from time import strftime

ts = time.time()
current_time = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
log_file_name = 'information_{}.log'.format(current_time).replace(" ", "_").replace(":", "-")

logger = logging.getLogger(__name__)
logging.basicConfig(filename=log_file_name, format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.INFO)

def check_existence_of_files(id_list_path, src_dir, dest_dir, collection_nr):
    #check if collection_nr exists in files
    collection_exists = False
    for dir in os.listdir(src_dir):
        if dir.startswith(collection_nr):
            collection_exists = True
            break

    return not (os.path.exists(src_dir) and collection_exists and os.path.exists(id_list_path) and os.path.exists(dest_dir))

#We assume that we work under Windows.
#TODO: Distinguish between Linux/Unix and Windows for hard-coded paths

#Data source parent directory

src_dir = 'Z:\\01_SCANNED_AND_PROCESSED\\02 FINAL'
#src_dir = 'Z:\\01_SCANNED_AND_PROCESSED\\03 DEMO'

class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('ERROR: %s\n' % message)
        self.print_help()
        sys.exit(2)

#Setup for command-line
parser = CustomParser()
#parser = argparse.ArgumentParser(description='Self-explanatory usage of program. Also see below for further information.')
#parser.add_argument('-v', '--verbose', help="Increase output verbosity (for debugging)", action="store_true")
parser.add_argument('-D', '--DEBUG', help="DEBUG mode", action="store_true")
parser.add_argument('id_list_path', help="Indicate path to file containing identifiers. 1 identifier per line.")
parser.add_argument('collection_nr', help="Collection number.")
parser.add_argument('file_types', nargs='+', help="- File type(s) to ret rieve.", type=str.lower, choices=["png", "jpg", 'obj']) #Currently accepted queries
args = parser.parse_args()


#Assume: Destination of copied files are going to be in the same folder as the list file
#Get destination
script_file_path = __file__ #os.path.dirname(os.path.realpath(__file__))
script_name = os.path.basename(script_file_path)

id_list_path = args.id_list_path
dest_dir = os.path.dirname(id_list_path)


print('Initiating copying process. Please wait.')
if args.DEBUG: #For testing and debugging purposes, use a demo directory
    src_dir = 'Z:\\01_SCANNED_AND_PROCESSED\\03 DEMO'
    #Script and argument information
    print(f"{script_file_path=}")
    print(f"{script_name=}")
    print(f"{args=}")
    print(f"{sys.argv=}")

    #Information about list, src and dest. directory
    try:
        #Check if file at id_list_path, src_dir and dest_dir exist (dest_dir is checked for future implementation, if another destination is selected)
        if check_existence_of_files(id_list_path, src_dir, dest_dir, args.collection_nr):
        #if not (os.path.exists(id_list_path) and os.path.exists(src_dir) and os.path.exists(dest_dir)):
            logger.error("\tExcecption FileNotFoundError: File(s) were not found in specified locations.")
            raise FileNotFoundError("Excecption FileNotFoundError: File(s) were not found in specified locations.")
        print(f"{id_list_path=}")
        with open(id_list_path) as f:
            for line in f:
                print(line.rstrip().encode()) #check if whitespaces and co are present in list
        print(f"{src_dir=}")
        print(f"{dest_dir=}")
        print()
    except Exception as error:
        print(error)
        logging.shutdown()
        os.remove(log_file_name)
        sys.exit(1)

try:
    #Check if file at id_list_path, src_dir and dest_dir exist (dest_dir is checked for future implementation, if another destination is selected)
    if check_existence_of_files(id_list_path, src_dir, dest_dir, args.collection_nr):
    #if not (os.path.exists(id_list_path) and os.path.exists(src_dir) and os.path.exists(dest_dir)):
        logger.error("\tExcecption FileNotFoundError: File(s) were not found in specified locations.")
        raise FileNotFoundError("Excecption FileNotFoundError: File(s) were not found in specified locations.")
    
    collection_dir = None
    collection_dir_path = None
    for dir in os.listdir(src_dir):
        if dir.startswith(args.collection_nr):
            collection_dir = dir
            collection_dir_path = os.path.join(src_dir, dir)
            break
    
    if args.DEBUG:
        print(f"{collection_dir=}")
        print(f"{collection_dir_path=}")

    #Read identifier from file, line by line
    with open(id_list_path) as f:
        for line in f:
            id = line.rstrip()
            print()
            print("Fetching files for ID = {} ...".format(id))
            try: #Find folder with ID
                id_dir_path = None
                pattern = re.compile(id)
                if id in os.listdir(collection_dir_path): #if ID is within src directory
                    #make new folder with name ID in dest
                    id_dir_path = os.path.join(collection_dir_path, id)
                    #print(f"{id_dir_path=}")
                    new_folder_dir_id = os.path.join(dest_dir, id)
                    if not os.path.exists(new_folder_dir_id):
                        if args.DEBUG:
                            print("Creating new directory {}".format(new_folder_dir_id))
                        os.makedirs(new_folder_dir_id)

                    for file_type in args.file_types:
                        try:
                            #Create new subdirectory in new_folder_id
                            dest = os.path.join(new_folder_dir_id, "{}".format(file_type))
                            #print("MAKING NEW DIRECTORY WITH NAME {}".format(dest))
                            #if not os.path.exists(dest):
                            #    os.makedirs(dest)
                            if os.path.exists(dest):
                                logger.warning("\tID = {}: Directory {} already exists.".format(id, dest))
                                raise Exception("ID = {}: Directory {} already exists.".format(id, dest))
                            
                            #Copy from src folder to new_sub_folder_dir_id
                            if file_type in ['png', 'jpg']:
                                if file_type == 'png':
                                    src = os.path.join(id_dir_path, "edof")
                                else:
                                    src = os.path.join(id_dir_path, "redof")
                                if args.DEBUG:
                                    print(f"{src=}")
                                    print(f"{dest=}")
                                    #print(os.listdir(src))
                                try:
                                    print("Copying {} files from {} to {}".format(file_type, src, dest))
                                    shutil.copytree(src, dest)
                                    logger.info("\t{} files from \t{} - SUCCESSFULLY copied.".format(file_type, id))
                                except Exception as error:
                                    logger.error("\t{} files from \t{} - ERROR during copying process. {}".format(file_type, id, error))
                                    print(error)

                                try:
                                    #Rename files: replace "image" with identifier
                                    for img_file in os.listdir(dest):
                                        os.rename(os.path.join(dest, img_file), os.path.join(dest, img_file.replace("image", id)))
                                except Exception as error:
                                    logger.error("\t{} files from \t{} - ERROR during renaming process. {}".format(file_type, id, error))
                                    print(error)
                            elif file_type == 'obj': #copy obj, mtb and png files
                                base_dest = os.path.join(new_folder_dir_id, file_type)
                                if args.DEBUG:
                                    print("Creating new directory {}".format(base_dest))
                                if not os.path.exists(base_dest):
                                    os.makedirs(base_dest)

                                for file_extension in ['obj', 'mtl', 'png']:
                                    src = os.path.join(os.path.join(id_dir_path, "Model"), id + ".{}".format(file_extension))
                                    #dest = os.path.join(new_folder_dir_id, file_type)
                                    dest = os.path.join(base_dest, "{}.{}".format(id, file_extension))
                                    if args.DEBUG:
                                        print(f"{src=}")
                                        print(f"{dest=}")
                                        #print(os.listdir(src))
                                    try:
                                        print("Copying {} file from {} to {}".format(file_extension, src, dest))
                                        shutil.copyfile(src, dest)
                                        logger.info("\t{} file from \t{} - SUCCESSFULLY copied.".format(file_extension, id))
                                    except Exception as error:
                                        logger.error("\t{} file from \t{} - ERROR during copying process. {}".format(file_extension, id, error))
                                        print(error)
                            else:
                                logger.warning("\tArgparse file type restriction bypass detected.")
                                print("Argparse file type restriction bypass detected.")
                                raise Exception("Argparse file type restriction bypass detected.")
                        except Exception as error:
                            print(error)
                            #continue with next file type, if any
                else:
                    logger.error("\tExcecption FileNotFoundError: Files for ID = {} do not exist.".format(id))
                    raise FileNotFoundError("Excecption FileNotFoundError: Files for ID = {} do not exist.".format(id))   
            except Exception as error:
                print(error)
                #continue with next id
except Exception as error:
    print(error)
    logging.shutdown()
    os.remove(log_file_name)
    sys.exit(1)

logging.shutdown()
shutil.move(log_file_name, dest_dir)
print()
print('Copying process finished.')