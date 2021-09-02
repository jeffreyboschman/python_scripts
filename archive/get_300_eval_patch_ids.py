import random
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

full_patch_ids = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/300_300_per_patient_full_ids.txt'
eval_WSI_ids = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/300_eval_WSI_ids.txt'
out_file = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/300_300_per_patient_eval_ids.txt'
seed = 1234

WSI_ids = read_data_ids(eval_WSI_ids)
full_patch_id_list = read_data_ids(full_patch_ids)

 
patch_ids = []

with open(out_file, 'w') as f:
    for WSI_id in tqdm(WSI_ids):
        for patch_id in full_patch_id_list:
            if WSI_id in patch_id:
                patch_ids.append(patch_id)

random.seed(seed)
random.shuffle(patch_ids)

count = 0
with open(out_file, 'w') as f:
    for item in patch_ids:
        f.write("%s\n" % item)
        count += 1

print('Number of lines written:', count)
