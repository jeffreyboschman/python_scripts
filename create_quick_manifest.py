import os
import argparse

def get_subtype(slide_textfile, rootdir):
    subtypes = ['CC', 'EC', 'HGSC', 'LGSC', 'MC']
    slide_list = read_data_ids(slide_textfile)
    slide_dict = dict.fromkeys(slide_list, 1)
    for slide in slide_dict:
        for subtype in subtypes:
            if os.path.isfile(os.path.join(rootdir, subtype, slide)):
                slide_dict[slide] = subtype
            else:
                continue
    print(slide_dict)

#    for slide in slide_list:
#        cur_subtype = ""
        
def read_data_ids(data_id_path):
    with open(data_id_path) as file:
        data_ids = file.readlines()
        data_ids = [x.strip() for x in data_ids]
    return data_ids



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For creating a csv with slide name and subtype''')

    parser.add_argument('--slide_textfile', type=str, required=True, help='a textfile containing the names of all the slides')
    parser.add_argument('--rootdir', type=str, required=True, help='a diretory with the structure rootidir/subtypes/slides, in order to figure out what subtype each slide is')

    args = parser.parse_args()

    get_subtype(args.slide_textfile, args.rootdir)
