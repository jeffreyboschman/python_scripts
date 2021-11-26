import os
import argparse
import json


def create_textfile_list_from_patch_id_json(patch_ids_file, idx, input_dir):

    with open(patch_ids_file, 'r') as jsonFile:
        jsonObject = json.load(jsonFile)
        cur_chunk = jsonObject["chunks"][idx]
        for img in cur_chunk['imgs']:
            orig_path = img
            relative_path = os.path.relpath(orig_path, input_dir)
            patch_id = os.path.splitext(relative_path)[0]
            print(patch_id)





#    count = 0 
#
#    for patch_id in tqdm(patch_ids):
#        #assumes patch_id has the form: subtype/WSI_id/coordinates
#        subtype_id = patch_id.split('/')[0]
#        WSI_id = patch_id.split('/')[1]
#        coordinates_id = patch_id.split('/')[2]
#        image_name = coordinates_id + '.png'
#        image_path = os.path.join(input_dir, subtype_id, WSI_id, image_name)
#        image_out_path = os.path.join(output_dir, subtype_id, WSI_id, image_name)
#        out_directory = os.path.join(output_dir, subtype_id, WSI_id)
#        os.makedirs(out_directory, exist_ok=True)
#        try: 
#            bash_command = "ln -s \""+image_path+"\" \""+image_out_path+"\""
#            os.system(bash_command)
#            count += 1
#        except:
#            print("The following images were not symlinked properly:", image_name)
#
#
#    print('Number of patches symlinked:', count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For creating an h5 file containing all the pngs specified by a json file''')

    parser.add_argument('--patch_ids_json', type=str, required=True,
            help='the path to a json that contains chunks with the patch paths')
    parser.add_argument('--chunk_num', type=int, required=True,
            help='the chunk number you want to use')
    parser.add_argument('--input_dir', type=str, required=True,
            help='the path to the root dir where the original png images are saved')

    args = parser.parse_args()


    create_textfile_list_from_patch_id_json(args.patch_ids_json, args.chunk_num, args.input_dir)
