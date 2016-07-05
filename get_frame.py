# A tool to extract detections of a single frame from a binary result file 
# and output them in a text format. 
# Useful for debugging individual frames without the need to read the entire binary file.
# Usage: python3 get_frame.py <file_name> <frame_number>

import sys
import struct

filename = sys.argv[1] #'/media/ahefny/Data/ace/1412_june_result.bin'
frame = int(sys.argv[2]) #3030

with open(filename, 'rb') as input:
    input.readline()
    line = input.readline()
    num_frames = int(line.split()[-1])
    line = input.readline()
    num_templates = int(line.split()[-1])

    for i in range(num_templates): input.readline()

    T = num_templates * [None]

    frame_size = 4 + num_templates * (8+4+4)
    input.seek(frame*frame_size,1)    
    b = input.read(4)

    assert (len(b) == 4)
    i = struct.unpack('<i', b)[0]

    for t in range(num_templates):
        ss = input.read(8)
        score = struct.unpack('<d', ss)[0] # Read confidence
        x_pos = struct.unpack('<i', input.read(4))[0] # Read x pos
        y_pos = struct.unpack('<i', input.read(4))[0] # Read y pos
        print(i, score, x_pos, y_pos)

