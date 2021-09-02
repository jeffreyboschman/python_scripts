import os
import glob
import pathlib
import argparse
import shutil
from openslide import OpenSlide

def main(input_WSI_dir, WSI_file_ext, output_annotation_dir):
    ensure_directory_exists(output_annotation_dir)
    ast_file_ext_string = '*' + WSI_file_ext
    for WSI in glob.glob(os.path.join(input_WSI_dir, ast_file_ext_string)):
        print(WSI)



#    for input_file in input_files:
#        input_file_filename, input_file_extension = get_file_name_and_extension(input_file)
#        for idx, new_filename_suffix in enumerate(new_filename_suffixes):
#            new_filename = input_file_filename + new_filename_suffix + input_file_extension 
#            current_output_file = os.path.join(output_file_dir, new_filename)
#            shutil.copyfile(input_file, current_output_file)
#            replace_text_in_file(original_text, new_text[idx], current_output_file)
#
def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)
#
#def get_file_name_and_extension(filepath):
#    file_name, file_extension = os.path.splitext(filepath.split('/')[-1])
#    return file_name, file_extension
#
#def replace_text_in_file(old_text, new_text, filepath):
#    with open(filepath, 'r') as temp_file:
#        file_data = temp_file.read()
#    file_data = file_data.replace(old_text, new_text)
#    with open(filepath, 'w') as final_file:
#        final_file.write(file_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Looks at all the WSIs in a directory, gets their size, and creates mock annotation files for them that contain the entire WSI. Useful for getting benign patches from a fully benign WSI when no annotations are available.''')

    parser.add_argument('--input_WSI_dir', type=str, required=True,  
            help='the full path to the directory where the WSIs are')
    parser.add_argument('--WSI_file_ext', type=str, default='.svs', 
            help='the file extension of the WSI images. Common examples are ".tif", ".tiff", ".svs"')
    parser.add_argument('--output_annotation_dir', type=str, required=True,
            help='the full path to the directory where you want the new annotation files to be created')

    args = parser.parse_args()

    main(args.input_WSI_dir, args.WSI_file_ext, args.output_annotation_dir)
