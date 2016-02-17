from tkinter import *
import tkinter.filedialog
import os.path
import pickle
import gzip
import numpy as np
import re

class visapp(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.init()

    def split_ngram(self, ngram):
        return re.findall('([-+][0-9]+)', ngram)
        
    def display_top_components(self, i):
        (k,s,u) = self.sv
        if u.shape[0] < u.shape[1]: u = u.T
        u = u[:,i]        
        idx = np.argsort(-np.abs(u))
        idx = [x for x in idx if len(k[x]) > 1]

        n = self.max_ngram_size
        
        for i in range(self.vis_size):
            grams = k[idx[i]]
            if len(grams) > n:
                grams = grams[-n:]

            print(grams)
            
            for j in range(len(grams)):
                img = self.img_template[int(grams[j][1:])]
                lbl_img = self.lbl_img_display[i][n-j-1]
                lbl_img.image = img
                lbl_img.config(image=img)

            self.lbl_weight[i]['text'] = str(u[idx[i]])
                
    def btn_load_onclick(self):
        filename = tkinter.filedialog.askopenfilename(
            filetypes = [("Numpy Array", "*.npy")], parent = self)
        filename = os.path.splitext(filename)[0]

        print ('Loading')
        (k,s) = pickle.load(gzip.open(filename + '.gz', 'rb'))
        u = np.load(filename + '.npy')
        k = [self.split_ngram(x) for x in k]
        self.sv = (k,s,u)
        print ('Loading Complete')

        self.display_top_components(0)
        
    def init(self):
        self.vis_size = 50
        self.max_ngram_size = 5
        
        # Load Images
        img_template = [];
        
        with open('data/templates/list.txt') as f:
            for line in f:
                img_template.append(PhotoImage(file='data/templates' + line.strip()))
                
        self.pack()

        self.img_template = img_template

        # Create controls
        btn_load = Button(self)
        btn_load["text"] = "Load File"
        btn_load["command"] = self.btn_load_onclick

        row_width = self.max_ngram_size
        btn_load.grid(row=0,columnspan=row_width)
        self.btn_load = btn_load

        lbl_img_display = [None] * self.vis_size
        lbl_weight = [None] * self.vis_size
        
        for i in range(self.vis_size):
            row = [None] * self.max_ngram_size;
            lbl_img_display[i] = row
            
            for j in range(self.max_ngram_size):
                row[j] = Label(self)
                row[j]["text"] = "     "
                row[j].configure(bg="red")
                row[j].grid(row=i+1,column=j)

            lw = Label(self)
            lw["text"] = '0'
            lw.grid(row=i+1,column=self.max_ngram_size)
            lbl_weight[i] = lw
                
        self.lbl_img_display = lbl_img_display
        self.lbl_weight = lbl_weight

        
        

print('Staring visualizer')

root = Tk()
app = visapp(master=root)
app.master.title('U Visualizer')
app.mainloop()
#root.destroy()

