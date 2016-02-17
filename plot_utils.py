import matplotlib.pyplot as plt

def imagesc(data):
    f = plt.figure()
    ax = f.gca()
    ax.imshow(data, interpolation = 'nearest', extent = [0, 1, 0, 1])
    plt.show()
    return f

