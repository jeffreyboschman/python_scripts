import os
import argparse

def copy_annotation_files(WSI_ids_file_in, original_annotation_dir, new_annotation_dir):
    failed_annotations=[]
    with open(WSI_ids_file_in) as WSI_file:
        list_of_WSI = WSI_file.readlines()
        list_of_WSI = [x.strip() for x in list_of_WSI]
    for WSI_id in list_of_WSI:
        filename = WSI_id+".txt"
        try:
            bash_command = "cp \"" + original_annotation_dir + filename + "\" \"" + new_annotation_dir + filename+"\""
            os.system(bash_command)
        except:
            print("The following annotation file was not copied:", filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For copying only the annotation files from a directory that you need (as specified in a list of WSI textfile)''')

    parser.add_argument('--annotation_path_in', type=str, required=True, help='The full path to a directory where all the annotation textfiles are')
    parser.add_argument('--annotation_path_out', type=str, required=True, help='The full path to a directory where you want your specific annotation textfiles')
    parser.add_argument('--WSI_ids_file_in', type=str, required=True, help='The full path to a textfile that contains the WSI ids of all the WSI that you want the annotation textfiles for')

    args = parser.parse_args()

    copy_annotation_files(args.WSI_ids_file_in, args.annotation_path_in, args.annotation_path_out)
