# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from split import  split_flac, merge_flac, call_process
from split import wav_to_flac, flac_to_wav, wav_to_ape, ape_to_wav, wav_to_wv, wv_to_wav
from subprocess import Popen, PIPE, STDOUT
import traceback
import subprocess
import argparse
import os 
import shutil
import hashlib


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()    
    
if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, 'tests')
    os.chdir(dir_path)
    
    os.mkdir('tmp/')
    shutil.copy(os.path.join(dir_path, 'Ring.flac'), os.path.join(dir_path, 'tmp/'))
    #Test 1
    #flac -> wav -> flac
    #Check two hash string
    flac_to_wav('Ring.flac', 'Ring.wav', os.path.join(dir_path, 'tmp/'), debug=False)
    wav_to_flac('Ring.wav', 'Ring2.flac', os.path.join(dir_path, 'tmp/'), debug=False)
    hash1 = sha256_checksum('tmp/Ring.flac')
    hash2 = sha256_checksum('tmp/Ring2.flac')
    print 'Hash Test1 hash1: {0}'.format(hash1)
    print 'Hash Test1 hash2: {0}'.format(hash2)
    print ''
    assert hash1 == hash2
    
    #Test 2
    #wav -> ape -> wav
    #Check two hash string
    wav_to_ape('Ring.wav', 'Ring.ape', os.path.join(dir_path, 'tmp/'), debug=False)
    ape_to_wav('Ring.ape', 'Ring2.wav', os.path.join(dir_path, 'tmp/'), debug=False)
    hash1 = sha256_checksum('tmp/Ring.wav')
    hash2 = sha256_checksum('tmp/Ring2.wav')
    print 'Hash Test2 hash1: {0}'.format(hash1)
    print 'Hash Test2 hash2: {0}'.format(hash2)
    print ''
    assert hash1 == hash2
    
    #Test 3
    #wav -> wv -> wav
    #Check two hash string
    wav_to_wv('Ring.wav', 'Ring.wv', os.path.join(dir_path, 'tmp/'), debug=False)
    wv_to_wav('Ring.wv', 'Ring3.wav', os.path.join(dir_path, 'tmp/'), debug=False)
    hash1 = sha256_checksum('tmp/Ring.wav')
    hash2 = sha256_checksum('tmp/Ring3.wav')
    print 'Hash Test3 hash1: {0}'.format(hash1)
    print 'Hash Test3 hash2: {0}'.format(hash2)
    print ''
    assert hash1 == hash2
    
    call_process('rm', '-r', 'tmp/', root=dir_path)
    #Test 4
    #split flac file in two parts
    #two parts file join in one whole wav file
    #wav -> flac
    #check to hash string
    split_flac(dir_path, 'Ring')
    os.mkdir('tmp/')
    shutil.move(os.path.join(dir_path, '01 - Part1.flac'), os.path.join(dir_path, 'tmp/'))
    shutil.move(os.path.join(dir_path, '02 - Part2.flac'), os.path.join(dir_path, 'tmp/'))
    merge_flac('01 - Part1.flac', '02 - Part2.flac', root=os.path.join(dir_path, 'tmp'))
    shutil.copy(os.path.join(dir_path, 'Ring.flac'), os.path.join(dir_path, 'tmp/'))
    wav_to_flac('joined.wav', 'joined.flac', os.path.join(dir_path, 'tmp/'))
    hash1 = sha256_checksum('tmp/Ring.flac')
    hash2 = sha256_checksum('tmp/joined.flac')
    print 'Hash Test4 hash1: {0}'.format(hash1)
    print 'Hash Test4 hash2: {0}'.format(hash2)
    print ''
    assert hash1 == hash2
    
    call_process('rm', '-r', 'tmp/', root=dir_path)
    print 'All tests were passed successful!'
    
    
    
    
    