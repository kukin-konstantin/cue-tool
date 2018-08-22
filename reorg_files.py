# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import argparse
import subprocess
import os
import shutil
from split import get_file_name_play

    
def preprocessing_cue_files(root, cue_files):
    cue_files = map(lambda x: os.path.join(root, x), cue_files)
    name_files = map(get_file_name_play, cue_files)
    name_files = map(lambda x: os.path.join(root, x), name_files)
    name_files = filter(os.path.isfile, name_files)
    if len(cue_files)==len(name_files) and len(cue_files)>1:
        for index, name_file_cue in enumerate(cue_files):
            new_place = os.path.join(root, 'CD{0}'.format(index+1))
            if not os.path.exists(new_place):
                os.makedirs(new_place)
            print name_file_cue
            shutil.move(os.path.join(root, name_file_cue), new_place)
            name_file_play = name_files[index]
            if os.path.isfile(os.path.join(root, name_file_play)):
                shutil.move(os.path.join(root, name_file_play), new_place)

def create():
    for root, dirnames, filenames in os.walk(path):
        filenames_ext = map(lambda x: os.path.splitext(x)[1], filenames)
        cue_files = filter(lambda x:  os.path.splitext(x)[1] == '.cue', filenames)
        cue_files = map(lambda x: os.path.join(root, x), cue_files)
        preprocessing_cue_files(root, cue_files)
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Creating additional directories for [flac, ape, wv] files which are in one directory')
    parser.add_argument('--path', dest='path', help='Directory for start')
    args = parser.parse_args()
    path = args.path
    
    create()