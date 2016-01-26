from ngrams import cum_ngrams_arr
from deltas_bin import readDetections, deltas

# Each video is taken as a binary file of template activations,
# and converted to a sequence of deltas.
# n-gram features are computed on the fly
class DeltaGrams:
  def __init__(self, binfile, window=40):
    self.window = window
    detects = readDetections(binfile)
    self.deltas = deltas(detects)
	
  # Don't fall off window
  def __len__(self):
    return len(self.deltas) - self.window 
	
  # n-gram starting at index (frame?) i
  def __getitem__(self, i):
    return cum_ngrams_arr([self.deltas[i + s] for s in range(self.window)])
    
  