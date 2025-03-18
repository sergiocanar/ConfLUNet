import os
from glob import glob 
import argparse
import json
import shutil

parser = argparse.ArgumentParser()

parser.add_argument("--split", type=str, default="0", help="Data split for inference")
args = parser.parse_args()

def create_imageTs(images_dir_lt, output_dir, split_dict):
    
    val_cases = split_dict['val']
    
    for path in images_dir_lt:
        for case in val_cases:
            if case in path:
                name= path.split('/')[-1]
                final_path = os.path.join(output_dir, name)
                shutil.copy(path, final_path)
if __name__ == '__main__':
    this_dir = os.getcwd()
    nn_raw_dir = os.path.join(this_dir, 'nn_Unet_raw')
    dataset_dir = os.path.join(nn_raw_dir, 'Dataset033_MsSpine ')
    train_vol_dir = os.path.join(dataset_dir, 'imagesTr')
    test_vol_dir = os.path.join(dataset_dir, 'imagesTs')
    if not os.path.exists(test_vol_dir):
        os.mkdir(test_vol_dir)
    
    vols_lt = glob(os.path.join(train_vol_dir, '*.nii.gz'))
    
    
    nn_preproc_dir = os.path.join(this_dir, 'nnUNet_preprocessed')
    preproc_dataset_dir = os.path.join(nn_preproc_dir, 'Dataset033_MsSpine ')
    split_json = os.path.join(preproc_dataset_dir, 'splits_final.json')

    with open(split_json) as json_data:
        d = json.load(json_data)
    
    split_dict = d[args.split]
    
    create_imageTs(vols_lt, test_vol_dir, split_dict)