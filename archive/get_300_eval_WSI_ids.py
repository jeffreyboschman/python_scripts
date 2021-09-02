
from tqdm import tqdm

def read_data_ids(data_id_path):
    """Function to read data ids (i.e., any *.txt contains row based information)

    Parameters
    ----------
    data_id_path : string
        Absoluate path to the *.txt contains data ids

    Returns
    -------
    data_ids : list
        List conntains data ids

    """
    with open(data_id_path) as file:
        data_ids = file.readlines()
        data_ids = [x.strip() for x in data_ids]
    return data_ids

id_path = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/300_150_per_patients_1_2_train_3_eval_eval_ids.txt'
out_file = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/300_eval_WSI_ids.txt'

ids = read_data_ids(id_path)

 
WSI_id_list = []

for line in tqdm(ids):
    subtype_id = line.split('/')[0]
    image_id = line.split('/')[1]
    patch_id = line.split('/')[2]
    subtype_and_patch = subtype_id + '/' + image_id
    WSI_id_list.append(subtype_and_patch)

# function to get unique values 
def unique(list1): 
    # intilize a null list 
    unique_list = [] 
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x)
    return unique_list


unique_WSI_ids = unique(WSI_id_list)
unique_WSI_ids.sort()

count = 0
with open(out_file, 'w') as f:
    for item in unique_WSI_ids:
        f.write("%s\n" % item)
        count += 1

print('Number of lines written:', count)
