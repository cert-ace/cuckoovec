import struct

def delta(m1, m2):
  return [v2-v1 for v1,v2 in zip(m1,m2)]

def deltas(M): 
  return [delta(m1,m2) for m1,m2 in zip(M[:],M[1:])] 
  
def readDetections(binfile):  
  with open(binfile, 'rb') as input:
    num_templates = struct.unpack('<H', input.read(2))[0]
    num_frames = struct.unpack('<I', input.read(4))[0]

    T = num_frames * [None]
    f = 0
    
    print(num_frames)
    print(num_templates)
    input.read(16)

    b = input.read(4)
    while len(b) > 0:
      T[f] = num_templates * [None]
      i = struct.unpack('<I', b)[0]
      print(i)
      for t in range(num_templates):
        T[f][t] = struct.unpack('<d', input.read(8))[0] # Read confidence
        input.read(4) # Read position      

      f += 1
      b = input.read(4)

  return T