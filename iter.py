from cuckoovec import CuckooVector

vec = CuckooVector({'f1': 3, 'f2': 8, 'f9': 2})
for k,v in vec.items(): 
  print(k)