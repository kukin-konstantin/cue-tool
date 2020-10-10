# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import argparse
from subprocess import Popen, PIPE, STDOUT
import os
import shutil
import traceback
import sys
import subprocess

def get_file_name_template_and_play(file_name):
    f = open(file_name)
    for line in f.readlines():
        if line.find('FILE')!=-1:
            beg = line.find('"')
            end = line.rfind('"')
            name_file_play = line[beg+1:end]
            middle = name_file_play.rfind('.')
            file_name_template = name_file_play[:middle]
    f.close()
    return (file_name_template, name_file_play) 

def get_file_name_template(file_name):
    return get_file_name_template_and_play(file_name)[0]

def get_file_name_play(file_name):
    return get_file_name_template_and_play(file_name)[1]
    
def number_file_and_track_in_file(file_name):
    count_file = 0
    count_track = 0
    f = open(file_name)
    def exist_file_track(line):
        return (line.find('FILE')!=-1, line.find('TRACK')!=-1)
    l = list(zip(*map(exist_file_track, f.readlines())))
    f.close()
    return sum(l[0]), sum(l[1])

def call_process(*args, **kwargs):
    root = kwargs['root']
    debug = kwargs['debug'] if 'debug' in kwargs else True
    try:
        if debug:
            process = Popen(list(args), stdout=PIPE, stderr=STDOUT, cwd=root)
        else:
            FNULL = open(os.devnull, 'w')
            process = Popen(list(args), stdout=FNULL, stderr=STDOUT, cwd=root)
            FNULL.close()
        (stdout, _) = process.communicate()
        #print 'stdout=', stdout
        process.wait()
    except Exception:
        t = traceback.format_exc()
        print(u'#### Exception: {0}'.format(t))
    
def wav_to_flac(file_input, file_output, process_dir, debug=True):
    call_process('flac', file_input, '-o', file_output, root=process_dir, debug=debug)

def flac_to_wav(file_input, file_output, process_dir, debug=True):
    call_process('flac', '-d', file_input, '-o', file_output, root=process_dir, debug=debug)

def wav_to_ape(file_input, file_output, process_dir, debug=True):
    call_process('mac', file_input, file_output, '-c2000', root=process_dir, debug=debug)

def ape_to_wav(file_input, file_output, process_dir, debug=True):
    call_process('mac', file_input, file_output, '-d', root=process_dir, debug=debug)

def wav_to_wv(file_input, file_output, process_dir, debug=True):
    call_process('wavpack', file_input, '-o', file_output, root=process_dir, debug=debug)
    
def wv_to_wav(file_input, file_output, process_dir, debug=True):
    call_process('wvunpack', file_input, '-o', file_output, root=process_dir, debug=debug)
    
def merge_flac(*args, **kwargs):
    call_process('shntool', 'join', *args, **kwargs)
    
def split_flac(root, file_name_cue, file_name_template):
    path_tmp = os.path.join(root, file_name_template)
    print('shnsplit -f \'{0}\' -t "%n - %t" -o flac \'{1}.flac\' -d \'{2}\''.format(file_name_cue, path_tmp, root))
    code = subprocess.call('shnsplit -f \'{0}\' -t "%n - %t" -o flac \'{1}.flac\' -d \'{2}\''.format(file_name_cue, path_tmp, root), shell=True)
    return code == 0
        
def remove_file(root, file_name_template, file_format):
    path_tmp = os.path.join(root, file_name_template)
    os.remove('{0}.{1}'.format(path_tmp, file_format))
    
def encode_file(root, file_name_template, in_file_format, out_file_format):
    input_file = '{0}.{1}'.format(file_name_template, in_file_format)
    output_file = '{0}.{1}'.format(file_name_template, out_file_format)
    if out_file_format == 'wav':
        if in_file_format == 'flac':
            flac_to_wav(input_file, output_file, root)
        elif in_file_format == 'ape':
            ape_to_wav(input_file, output_file, root)
        elif in_file_format == 'wv':
            wv_to_wav(input_file, output_file, root)
    elif out_file_format == 'flac' and in_file_format == 'wav':
        wav_to_flac(input_file, output_file, root)

    
def split():
    for root, dirnames, filenames in os.walk(path):
        filenames_ext = list(map(lambda x: os.path.splitext(x)[1], filenames))
        number_of_flac = filenames_ext.count('.flac')
        number_of_ape = filenames_ext.count('.ape')
        number_of_wv = filenames_ext.count('.wv')
        cue_files = filter(lambda x:  os.path.splitext(x)[1] == '.cue', filenames)
        cue_files = list(map(lambda x: os.path.join(root, x), cue_files))
        list_file_track = list(map(number_file_and_track_in_file, cue_files))
        for index, file_name in enumerate(cue_files):
            if list_file_track[index][0]!=list_file_track[index][1]:
                file_name_template, name_file_play = get_file_name_template_and_play(file_name)
                if os.path.isfile(os.path.join(root, name_file_play)):
                    print(file_name)
                    print(name_file_play)
                    try:
                        if number_of_flac>0:
                            if split_flac(root, file_name, file_name_template):
                                remove_file(root, file_name_template, 'flac')
                        elif number_of_ape>0:
                            encode_file(root, file_name_template, 'ape', 'wav')
                            
                            encode_file(root, file_name_template, 'wav', 'flac')
                            remove_file(root, file_name_template, 'wav')
                            
                            if split_flac(root, file_name, file_name_template):
                                remove_file(root, file_name_template, 'flac')
                                remove_file(root, file_name_template, 'ape')
                                
                        elif number_of_wv>0:
                            encode_file(root, file_name_template, 'wv', 'wav')
                            
                            encode_file(root, file_name_template, 'wav', 'flac')
                            remove_file(root, file_name_template, 'wav')
                        
                            if split_flac(root, file_name, file_name_template):
                                remove_file(root, file_name_template, 'flac')
                                remove_file(root, file_name_template, 'wv')
                    except Exception:
                        t = traceback.format_exc()
                        print(u'#### Exception: {0}'.format(t))
                    

    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Split whole file in many files')
    parser.add_argument('--path', dest='path', help='Directory for start')


    args = parser.parse_args()
    path = args.path
    print ("############")
    print ("args=", args)
    print ("path=", path)
    
    split()