import FileDialog

import ImageTk
from Tkinter import*
from PIL import Image

import time
import datetime
from fractions import Fraction

import csv
import random
import glob, os
import picamera

import skimage
from skimage.io import* 
from skimage.feature import*
from skimage.transform import*
from skimage.morphology import binary_closing
from skimage.filters import threshold_otsu, threshold_adaptive

import numpy as np

import scipy
from scipy import ndimage as ndi

import matplotlib
import matplotlib.pyplot as plt

import test_roi_centroid1
import test_roi_centroid2


size = 310,206
root = Tk()
root.title("MEAT MARBLING METER")
root.geometry("475x275")
n=75

class Application(Frame):
    """ A GUI application with controls """
    def __init__(self, master):
        """ Initialize the Frame """
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        

    def create_widgets(self):
        """ Creates button, text and entry widgets """
        self.button = Button(self, text = "Capture Meat Image", bg="blue", fg="white", command = self.capture_image)
        self.button.grid(row = 1, column = 0, sticky = W+E+N+S)

        self.img=ImageTk.PhotoImage(Image.open('example_thumbnail.jpg'))
        self.disp_image = Label(self, image=self.img, bg="white", fg="black", width = 300, height=260)
        self.disp_image.grid(row=0, column=1, rowspan=12)

        self.button2 = Button(self, text = "Calculate Ratio", bg="green", fg="black", command = self.calculate_score)
        self.button2.grid(row = 3, column = 0, sticky = W+E+N+S)

        self.display_score = Text(self, width = 10, height =4, wrap =WORD)
        self.display_score.grid(row = 4, column = 0, sticky = W+E+N+S)

        self.close_button = Button(self, text="Quit", bg="red", fg="white",command=self.quit_pressed)
        self.close_button.grid(row = 9, column = 0, columnspan=1, sticky = W+E+N+S)

  
    def capture_image(self):
        """ code to capture an image """
        current_time = datetime.datetime.now()
        filename=str(current_time)
        filename=filename.replace(":", "")
        filename=filename.replace("   ", "")
        filename=filename.replace(".", "")
        filename=filename.replace(" ", "_")
        camera = picamera.PiCamera()
        #camera.resolution = (2592, 1944)
        #camera.resolution = (1280, 1024)
        camera.resolution = (640, 480)
        #camera.iso = 800
        #camera.awb_mode = 'fluorescent'
        camera.awb_mode = 'horizon'
        camera.capture(filename + '.jpg')
        camera.close()

        #im = Image.open(filename + '.jpg')
        #im.save(filename + '.bmp', dpi=[150, 150])
                        
        f = open('Workfile.csv', 'a')
        value1 = (filename + '.jpg')
        f.write(value1)
        f.close()

        """ code to display recently captured meat image """
        
        f = open('Workfile.csv')
        csv_f=csv.reader(f)
        list_captured_images = []
        for row in csv_f:
            list_captured_images.append(row[0])
        filename=row[0]
        total_num_of_captured_images=len(list_captured_images)
        f.close()

        im = Image.open(filename)
        im.thumbnail(size, Image.ANTIALIAS)
        filename=filename.replace(".jpg", "")
        im.save(filename + "_thumbnail.jpg", "JPEG")

        self.img=ImageTk.PhotoImage(Image.open(filename+ "_thumbnail.jpg"))
        self.disp_image = Label(self, image=self.img, bg="white", fg="black", width = 300, height=260)
        self.disp_image.grid(row=0, column=1, rowspan=10)
        #time.sleep(1)

        # Code to Perform Image Analysis
        #current_time_before= datetime.datetime.now()
        #print 'start-roi'

        f = open('Workfile.csv')
        csv_f=csv.reader(f)
        list_captured_images = []
        for row in csv_f:
            list_captured_images.append(row[0])
        filename=row[0]
        total_num_of_captured_images=len(list_captured_images)
        f.close()

        distratio = 0.15
        contourSP = np.array([0,0])
        meat_image = imread(filename).astype(np.uint8)
        im1 = ((0.2989 * meat_image[:,:,0]) + (0.5870 * meat_image[:,:,1]) +\
              (0.1140 * meat_image[:,:,2])).astype(np.uint8)

        #bw = im1 > (np.median(im1) + np.std(im1)/4)
        block_size = 41
        bw = threshold_adaptive(im1, block_size, offset=10)

        thresh = threshold_otsu(im1)
        binary = im1 < thresh
        b = binary_closing(binary, selem=None, out=None)
        e = canny(b)
        [y,x] = np.nonzero(e)
        g = meat_image[:,:,1]
        contourP = np.array([x,y])
        C0, C1, C2, d = test_roi_centroid1.test_centroid(g, contourP) 

        contourSP = test_roi_centroid2.test_tcsRatio(g, contourP, C2, distratio)
        mask = np.zeros(np.shape(g))

        mincontourSP = min(contourSP[1,:]).astype(np.int)
        maxcontourSP = max(contourSP[1,:]).astype(np.int)

        for r in range(mincontourSP, maxcontourSP):
            c1=contourSP[0, np.where(contourSP[1,:] == r)]
            #cpm = np.array([cpm, [np.amin(c1[0,:], axis=0),r], [np.amax(c1[0,:], axis=0),r]])
            mask[r, np.amin(c1[0,:], axis=0).astype(np.int) : np.amax(c1[0,:], axis=0).astype(np.int)] = 1
        
        #CPM = cpm
        SMask = binary_closing(mask.astype(np.bool_), selem=None, out=None)

        J = meat_image
        J[:,:,0] = np.multiply(J[:,:,0], (1-SMask).astype(np.uint8))
        J[:,:,2] = np.multiply(J[:,:,2], (1-SMask).astype(np.uint8))

        #print 'finished-roi'

        #current_time_after= datetime.datetime.now()
        #print current_time_after - current_time_before

        b1=np.multiply(1-bw, SMask)
        area_roi = np.where(binary == 1)
        area_marble = np.where(b1 == 1)
        if np.size(area_marble) == 0:
            ratio = 999999
            print 'verify the object and illumination' 
        else:
            ratio = np.size(area_roi) / np.size(area_marble)
        #print ratio

        f = open('Workfile.csv', 'a')
        f.write(',')
        if ratio == 999999:
            f.write(str(ratio))
            f.write(',')
            f.write('to be verified')
        else:
            f.write(str(ratio))
        f.write('\n')
        f.close()

        #print 'start to plot roi figures'

        fig=plt.figure(figsize=(7,4))

        ax1=plt.subplot(2,2,1, adjustable='box-forced')
        ax2=plt.subplot(2,2,2, sharex=ax1, sharey=ax1, adjustable='box-forced')
        ax3=plt.subplot(2,2,3, sharex=ax1, sharey=ax1, adjustable='box-forced')
        ax4=plt.subplot(2,2,4, sharex=ax1, sharey=ax1, adjustable='box-forced')

        ax1.imshow(meat_image, cmap=plt.cm.gray)
        ax2.imshow(1-bw, cmap=plt.cm.gray)
        ax3.imshow(SMask, cmap=plt.cm.gray)
        ax4.imshow(b1,cmap=plt.cm.gray)

        #current_time_after= datetime.datetime.now()
        #print current_time_after - current_time_before
        #print 'finished plotting roi figures'

        plt.show()

    def calculate_score(self):
        """ calculate the marbling score of recently captured meat image """
        #Mscore=random.sample([01,02,03,04,05,06,10],1)

        f = open('Workfile.csv')
        csv_f=csv.reader(f)
        list_ratios = []
        for row in csv_f:
            list_ratios.append(row[0])
        Mscore='Image='+row[0]+'\n'+'\n'+'Ratio='+row[1]
        total_num_of_captured_images=len(list_ratios)
        f.close()
        #print Mscore
        self.display_score.delete(0.0, END)
        self.display_score.insert(0.0, Mscore)
        
    def quit_pressed(self):
        """ quit application """
        self.master.destroy()
            
              
app = Application(root)
root.mainloop()
