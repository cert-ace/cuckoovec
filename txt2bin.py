'''
Program to convert detections from text to binary format.
Use: 
python txt2bin.py <result_folder> <output_bin_file>

Binary format:
Number of templates (2 bytes unsigned int)
Number of frames (4 bytes unsigned int)
Meta-info (16 bytes [currently all zero])
Frame Records (one per frame):
  Frame Id (4 bytes unsigned int)
  Detections (one per template):
    Confidence (8 bytes double)
    X position (2 bytes unsigned short)
    Y position (2 bytes unsigned short)
'''

import os, sys, glob
import struct

folder = sys.argv[1]
binary = sys.argv[2]

with open(binary, 'wb') as output:
    output.write(struct.pack('<H', 96))
    output.write(bytes(20))

    num_frames = 0

    #Sort file names by frame number
    frame_ids = [name.split('_')[1].split('.')[0]
                 for name in glob.glob(folder + '/result_*.txt')]
        
    for i in sorted(frame_ids, key=int):
        num_frames += 1
        print(i)
        output.write(struct.pack('<I', int(i)))
        name = 'result_' + i + '.txt'
        with open(os.path.join(folder, name)) as file:
            for line in file:
                if line:
                    chunks = line.split('\t')
                    output.write(struct.pack('<d', float(chunks[0])))
                    output.write(struct.pack('<H', int(chunks[1])))
                    output.write(struct.pack('<H', int(chunks[2])))

    output.seek(2)
    output.write(struct.pack('<I', num_frames))

