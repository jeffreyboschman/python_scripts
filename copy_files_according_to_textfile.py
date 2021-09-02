import os
import pathlib
import argparse


def main(files_textfile, input_dir, output_dir):
    file_list = read_data_ids(files_textfile)
    ensure_directory_exists(output_dir)
    for cur_file in file_list:
        input_path = os.path.join(input_dir, cur_file)
        output_path = os.path.join(output_dir, cur_file)
        try:
            bash_command = 'cp "' + input_path +'" "' + output_path + '"'
            os.system(bash_command)
        except Exception as e:
            print(e)
            print(f"{input_path} was not copied properly")


def read_data_ids(data_id_path):
    with open(data_id_path) as file:
        data_ids = file.readlines()
        data_ids = [x.strip() for x in data_ids]
    return data_ids

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For copying certain files''')

    parser.add_argument('--files_textfile', type=str, required=True,
            help='the path to a textfile that contains lines with the file ids')
    parser.add_argument('--input_dir', type=str, required=True,
            help='the path to the root dir where the original file are saved')
    parser.add_argument('--output_dir', type=str, required=True,
            help='the path to the root dir where you want the symlinks to be')

    args = parser.parse_args()

    main(args.files_textfile, args.input_dir, args.output_dir) 
