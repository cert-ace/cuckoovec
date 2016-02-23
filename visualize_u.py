from tkinter import *
import tkinter.filedialog
from tkinter.ttk import *
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

    def clear_images(self):
        for imgs in self.lbl_img_display:
            for img in imgs:
                img.image = ''
                img.config(image='')

        for sgns in self.lbl_sign:
            for sgn in sgns:
                sgn['text'] = ''

        for lbl in self.lbl_weight:
            lbl['text'] = '0'

        for imgs in self.lbl_img_display_neg:
            for img in imgs:
                img.image = ''
                img.config(image='')

        for sgns in self.lbl_sign_neg:
            for sgn in sgns:
                sgn['text'] = ''

        for lbl in self.lbl_weight_neg:
            lbl['text'] = '0'
    
    def display_top_components(self, i, pos):        
        (k,s,u) = self.sv
        if u.shape[0] < u.shape[1]: u = u.T
        u = u[:,i]        

        #idx = [x for x in idx if len(k[x]) > 1]

        n = self.max_ngram_size

        if pos:
            idx = [x for x in np.argsort(-u) if u[x] > 0.0]
            lbl_img_display = self.lbl_img_display
            lbl_sign = self.lbl_sign
            lbl_weight = self.lbl_weight
        else:
            idx = [x for x in np.argsort(u) if u[x] < 0.0]
            lbl_img_display = self.lbl_img_display_neg
            lbl_sign = self.lbl_sign_neg
            lbl_weight = self.lbl_weight_neg
        
        V = min(self.vis_size, len(idx))    
        for i in range(V):
            grams = k[idx[i]]
            if len(grams) > n:
                grams = grams[-n:]

            print(grams)
            
            for j in range(len(grams)):                
                img = self.img_template[int(grams[j][1:])]
                lbl_img = lbl_img_display[i][n-j-1]
                lbl_img.image = img
                lbl_img.config(image=img)

                lbl_sign[i][n-j-1]['text'] = grams[j][0]

            lbl_weight[i]['text'] = str(u[idx[i]])
                
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

        nsv = len(s)
        self.cmb_sv['values'] = ['{0}: {1}'.format(i, s[i]) for i in range(nsv)]
        self.cmb_sv.current(0)

        self.clear_images()
        self.display_top_components(0, True)
        self.display_top_components(0, False)

    def cmb_sv_onchange(self, event):
        idx = int(self.cmb_sv.get().split(':')[0])
        self.clear_images()
        self.display_top_components(idx, True)
        self.display_top_components(idx, False)
        
    def init(self):
        self.vis_size = 50
        self.max_ngram_size = 5
        
        # Load Images
        img_template = [];
        
        with open('data/templates/list.txt') as f:
            for line in f:
                img_template.append(
                    PhotoImage(file='data/templates' + line.strip()))
                
        self.pack()

        self.img_template = img_template

        # Create controls
        row_width = 2*self.max_ngram_size+1

        frm_settings = Labelframe(self, text='Settings')
        frm_settings.grid(row=0,columnspan=2)
        
        btn_load = Button(frm_settings)
        btn_load["text"] = "Load File"
        btn_load["command"] = self.btn_load_onclick
        
        btn_load.grid(row=0,columnspan=2)
        self.btn_load = btn_load

        Label(frm_settings, text='SV').grid(row=1)
        cmb_sv = Combobox(frm_settings, state='readonly')
        cmb_sv.grid(row=1,column=1)
        cmb_sv.bind("<<ComboboxSelected>>", self.cmb_sv_onchange)
        self.cmb_sv = cmb_sv

        frm_pos = Labelframe(self, text='High Positives')
        frm_pos.grid(row=2)
        frm_neg = Labelframe(self, text='High Negatives')
        frm_neg.grid(row=2,column=1)
        
        lbl_img_display = [None] * self.vis_size
        lbl_sign = [None] * self.vis_size
        lbl_weight = [None] * self.vis_size
        lbl_img_display_neg = [None] * self.vis_size
        lbl_sign_neg = [None] * self.vis_size
        lbl_weight_neg = [None] * self.vis_size
        
        for i in range(self.vis_size):
            row = [None] * self.max_ngram_size;
            lbl_img_display[i] = row
            sgn_row = [None] * self.max_ngram_size;
            lbl_sign[i] = sgn_row

            row_neg = [None] * self.max_ngram_size;
            lbl_img_display_neg[i] = row_neg
            sgn_row_neg = [None] * self.max_ngram_size;
            lbl_sign_neg[i] = sgn_row_neg
                        
            for j in range(self.max_ngram_size):
                row[j] = Label(frm_pos)
                row[j]['text'] = '     '                
                row[j].grid(row=i,column=2*j+1)
                sgn_row[j] = Label(frm_pos)
                sgn_row[j]['text'] = ' '                
                sgn_row[j].grid(row=i,column=2*j)

                row_neg[j] = Label(frm_neg)
                row_neg[j]['text'] = '     '                
                row_neg[j].grid(row=i,column=2*j+1)
                sgn_row_neg[j] = Label(frm_neg)
                sgn_row_neg[j]['text'] = ' '                
                sgn_row_neg[j].grid(row=i,column=2*j)

            lw = Label(frm_pos)
            lw["text"] = '0'
            lw.grid(row=i,column=2*self.max_ngram_size+1)
            lbl_weight[i] = lw
            lw = Label(frm_neg)
            lw["text"] = '0'
            lw.grid(row=i,column=2*self.max_ngram_size+1)
            lbl_weight_neg[i] = lw
            
        self.lbl_img_display = lbl_img_display
        self.lbl_sign = lbl_sign
        self.lbl_weight = lbl_weight
        self.lbl_img_display_neg = lbl_img_display_neg
        self.lbl_sign_neg = lbl_sign_neg
        self.lbl_weight_neg = lbl_weight_neg

print('Staring visualizer')

root = Tk()
app = visapp(master=root)
app.master.title('U Visualizer')
app.mainloop()
#root.destroy()

