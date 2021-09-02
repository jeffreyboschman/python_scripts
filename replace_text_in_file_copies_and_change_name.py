import os
import pathlib
import argparse
import shutil

def main(input_files, output_file_dir, original_filename_text, new_filename_text, original_text, new_text):
    ensure_directory_exists(output_file_dir)
    for input_file in input_files:
        input_file_filename, input_file_extension = get_file_name_and_extension(input_file)
        new_filename = input_file_filename.replace(original_filename_text, new_filename_text) + input_file_extension
        current_output_file = os.path.join(output_file_dir, new_filename)
        shutil.copyfile(input_file, current_output_file)
        replace_text_in_file(original_text, new_text, current_output_file)

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_file_name_and_extension(filepath):
    file_name, file_extension = os.path.splitext(filepath.split('/')[-1])
    return file_name, file_extension

def replace_text_in_file(old_text, new_text, filepath):
    with open(filepath, 'r') as temp_file:
        file_data = temp_file.read()
    file_data = file_data.replace(old_text, new_text)
    with open(filepath, 'w') as final_file:
        final_file.write(file_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Makes copies of all the files in input file, replacing the original_filename_text with new_filename_text in all the filenames of the input files, and also replacing all instances of original_text in the body of the file with new_text''')

    parser.add_argument('--input_files', nargs='+', type=str, 
            help='the paths to the files you want to be copied and edited. you can include more than one. ex. --input_files /path/to/file1.txt /path/to/file2.txt /path/to/file3.json')
    parser.add_argument('--output_file_dir', type=str, required=True,
            help='the path to a directory where you want the output files to be saved')
    parser.add_argument('--original_filename_text', type=str, required=True,
            help='the text in the filename you want replaced with new_filename_text')
    parser.add_argument('--new_filename_text', type=str, required=True,
            help='the text you want to replace original_filename_text in the filename copies')
    parser.add_argument('--original_text', type=str, required=True,
            help='the original text you want to replace with something else. Ex --original_text "vahadane"')
    parser.add_argument('--new_text', type=str, required=True,
            help='the text you want to replace the original_text in all the bodies of the copied files')

    args = parser.parse_args()

    main(args.input_files, args.output_file_dir, args.original_filename_text, args.new_filename_text, args.original_text, args.new_text)
