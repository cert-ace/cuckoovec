import preprocess
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

file = 'data/1412.bin'

r = preprocess.readDetections(file, True)
video_length = len(r)
num_templates = len(r[0])

x_max = 1920 #max(max(x[1] for x in r[i]) for i in range(video_length))
y_max = 1200 #max(max(x[2] for x in r[i]) for i in range(video_length))

for template in range(num_templates):
    print(template)
    im = Image.new('RGB',(x_max+7,y_max+7))

    for i in range(x_max+7):
        im.putpixel((i,0),(255,255,255))
        im.putpixel((i,y_max+6),(255,255,255))

    for i in range(y_max+7):
        im.putpixel((0,i),(255,255,255))
        im.putpixel((x_max+6,i),(255,255,255))

    for t in range(video_length):
        (s,x,y) = r[t][template]
    
        red = 255;
        grn = int(255 * t / video_length)

        #print (x,y)
        if s < 0.2:
            for i in range(2,5):
                for j in range(2,5):
                    im.putpixel((x+i,y+j),(red,grn,0))
    
    im.save('motion/2dtraj_{0}.png'.format(template))

    plt.plot(np.asarray([x[template][0] for x in r]))
    plt.savefig('motion/score_{0}.png'.format(template))
    plt.figure()
    plt.plot(np.asarray([x[template][1] for x in r]))
    plt.savefig('motion/xpos_{0}.png'.format(template))
    plt.figure()
    plt.plot(np.asarray([x[template][2] for x in r]))
    plt.savefig('motion/ypos_{0}.png'.format(template))
    plt.close('all')
    

    
