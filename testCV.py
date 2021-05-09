# -*- coding: utf-8 -*-
# @Time    : 2018/2/8 15:56
# @Author  : play4fun
# @File    : opencv-with-tkinter.py
# @Software: PyCharm

"""
opencv-with-tkinter.py:
https://www.pyimagesearch.com/2016/05/23/opencv-with-tkinter/
不需要
pip install image
"""

# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as tkFileDialog
import cv2
import os
import numpy as np

def select_image():
    # grab a reference to the image panels
    global panelA, panelB,path,lower_limit,higher_limit
    # open a file chooser dialog and allow the user to select an input
    # image
    path = tkFileDialog.askopenfilename()
    # print(path)
    # ensure a file path was selected
    if len(path) > 0:
        print(lower_limit, higher_limit)
        # load the image from disk, convert it to grayscale, and detect
        # edges in it
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, edged = cv2.threshold(gray, higher_limit, lower_limit, cv2.ADAPTIVE_THRESH_MEAN_C)

        #  represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        _contours, _hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print("number of con = " + str(len(_contours)))
        cv2.putText(edged, str(len(_contours)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (0, 255, 255),
                    2)
        edged = cv2.drawContours(edged, _contours, 0, (0, 255, 0), 0)
        # convert the images to PIL format...
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)


        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)
        edged = ImageTk.PhotoImage(edged)

        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=5, pady=5)

            # while the second panel will store the edge map
            panelB = Label(image=edged)
            panelB.image = edged
            panelB.pack(side="right", padx=5, pady=5)

        # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged

# def find_contours():
#     global edged,panelB
#     _contours, _hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     print("number of con = " + str(len(_contours)))
#     cv2.putText(panelB, 'number of area =' + str(len(_contours)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
#                 (0, 255, 255),
#                     2)
#     img2 = cv2.drawContours(panelB, _contours, -1, (0, 255, 0), 1)
#     panelB.image = img2


def get_val():
    global lower_limit,higher_limit
    lower_limit = lower.get()
    higher_limit = higher.get()
    print(higher_limit,lower_limit)
    return lower_limit,higher_limit


def save_output():
    global path
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, edged = cv2.threshold(gray, 205, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
    # im = Image.fromarray(edged)
    file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".jpg",
                                    filetypes=(("JPEG file", "*.jpg"), ("All Files", "*.*")))
    if file:
        abs_path = os.path.abspath(file.name)
        out = Image.fromarray(edged)
        out.save(abs_path)  # saves the image to the input file name


# initialize the window toolkit along with the two image panels
root = Tk()
root.geometry('800x600')
panelA = None
panelB = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
lower_limit = IntVar()
higher_limit = IntVar()
lower = Scale(root, orient='horizontal',variable=lower_limit, sliderlength=10,from_=0, to=255)
higher = Scale(root, orient='horizontal',variable=higher_limit, sliderlength=10,from_=0, to=255)

lower.pack(side='bottom')
higher.pack(side='bottom')
btn = Button(root, text="Select an image", command=select_image)
btn_out = Button(root, text="Save output", command=save_output)
btn_get = Button(root,command=get_val,text="Get Threshold")
btn_get.pack(side='bottom')
btn.pack(side="bottom", fill="both")
btn_out.pack(side='bottom',fill='both')

# kick off the GUI
root.mainloop()