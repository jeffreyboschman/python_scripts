from tqdm import tqdm
import os
import pathlib
import argparse
import json


def copy_pngs_from_list(patch_ids_file, input_dir, output_dir):

    count = 0
    with open(patch_ids_file, 'r') as jsonFile:
        jsonObject = json.load(jsonFile)
        for chunk in jsonObject["chunks"]:
            for img in tqdm(chunk['imgs']):
                orig_path = img
                relative_path = os.path.relpath(orig_path, input_dir)
                new_copy_path = os.path.join(output_dir, relative_path)
                print(new_copy_path)
                if not os.path.exists(os.path.dirname(new_copy_path)):
                    pathlib.Path(os.path.dirname(new_copy_path)).mkdir(parents=True, exist_ok=True)
                bash_command = "cp \""+orig_path+"\" \"" + new_copy_path +"\""
                try:
                    os.system(bash_command)
                    count +=1
                except:
                    print("the following image was not copied properly:", orig_path)
    print("number of patches copied:", count)






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
#            print("The following images were not copyed properly:", image_name)
#
#
#    print('Number of patches copyed:', count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For copying the pngs specified in a json file to another directory''')

    parser.add_argument('--patch_ids', type=str, required=True,
            help='the path to a json file that contains the patch ids you want to be copied. The patch ids should all be from the original input_dir')
    parser.add_argument('--input_dir', type=str, required=True,
            help='the path to the root dir where the original png images are saved')
    parser.add_argument('--output_dir', type=str, required=True,
            help='the path to the root dir where you want the copies to be')

    args = parser.parse_args()

    copy_pngs_from_list(args.patch_ids, args.input_dir, args.output_dir) 
