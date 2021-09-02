import os

ids = ["OOU-470", "OOU-473", "OOU-529"]

for i in ids:

    bash_command = "rsync -vP /projects/ovcare/WSI/Dataset_Slides_500_cases/mucinous_carcinoma_50/"+i+".tiff /projects/ovcare/classification/jboschman/colour_norm/bejnordi/300_WSI_copies/MC/"+i+".tif"
    os.system(bash_command)