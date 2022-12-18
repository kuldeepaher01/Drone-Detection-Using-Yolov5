import tkinter
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkVideoPlayer import TkinterVideo
import customtkinter
import os
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import shutil
import glob

# importing model
model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='Drone_Detection.pt')

model.conf = 0.35

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title('Drone Detection')


# FUNCTIONS

# Deleting runs
def deleteRuns():
    shutil.rmtree('runs/')
    return

# Function for Next Button


def next_event():
    for widgets in root.winfo_children():
        widgets.destroy()
    # Options window
    frame1 = customtkinter.CTkFrame(
        master=root, width=400, height=325, corner_radius=10)
    frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    inst = customtkinter.CTkLabel(master=frame1, text="Select Mode of Input", width=120, height=25,
                                  text_font=("", 25))
    inst.place(relx=0.5, rely=0.05, anchor=tkinter.N)
    image_btn = customtkinter.CTkButton(master=root, text="Image", width=120, height=32, fg_color=None, border_width=1,
                                        border_color="white", command=image_event)
    image_btn.place(relx=0.5, rely=0.42, anchor=tkinter.N)
    video_btn = customtkinter.CTkButton(master=root, text="Video", width=120, height=32, fg_color=None, border_width=1,
                                        border_color="white", command=video_event)
    video_btn.place(relx=0.5, rely=0.52, anchor=tkinter.N)
    realtime_btn = customtkinter.CTkButton(master=root, text="Real-time", width=120, height=32, fg_color=None,
                                           border_width=1, border_color="white", command=realtime_event)
    realtime_btn.place(relx=0.5, rely=0.62, anchor=tkinter.N)


# Video Button Function
def video_event():
    for widgets in root.winfo_children():
        widgets.destroy()
    # Opening File Directory Window
    root.filename = filedialog.askopenfilename(initialdir="This PC", title="Select an Image",
                                               filetypes=(("mp4 files", ".mp4"), ("mkv files", ".mkv"), ("webm files", ".webm")))

    video_loc = root.filename
    if(root.filename == ""):
        messagebox.showerror('Error', 'Video not Selected')
        next_event()
    else:
        # os.mkdir('D:/Capstone/runs')
        # os.mkdir('D:/Capstone/runs/videoFrame')

        cap = cv2.VideoCapture(root.filename)
        while cap.isOpened():
            ret, frame = cap.read()

            # Make detections
            results = model(frame)

            cv2.imshow('Video Detection', np.squeeze(results.render()))

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        cap.release()
        next_event()

# Real time Drone detection


def realtime_event():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()

    # Make detections
        results = model(frame)
        frame = cv2.resize(frame, (540, 380), fx=0, fy=0,
                           interpolation=cv2.INTER_CUBIC)

        cv2.imshow('Real-Time Detection', np.squeeze(results.render()))

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    cap.release()
    cv2.destroyAllWindows()
    next_event()


# Redering
def renderOut(img, output):
    # Frames
    frame2 = customtkinter.CTkFrame(
        master=root, width=680, height=720, corner_radius=10)
    frame2.grid(padx=(90, 40), pady=30, row=0, column=0)
    frame3 = customtkinter.CTkFrame(
        master=root, width=680, height=720, corner_radius=10)
    frame3.grid(padx=40, pady=30, row=0, column=1)
    # Original Image
    olabel = customtkinter.CTkLabel(
        master=frame2, text="Original Image", width=500, height=40, text_font=("", "20"))
    olabel.grid(row=0, column=1)
    image = ImageTk.PhotoImage(img.resize((800, 800)))
    image_ori = customtkinter.CTkButton(
        master=frame2, image=image, text="")
    image_ori.grid(row=1, column=1)
    # Detected Image
    dlabel = customtkinter.CTkLabel(
        master=frame3, text="Detected Image", width=500, height=40, text_font=("", "20"))
    dlabel.grid(row=0, column=1)
    image = ImageTk.PhotoImage(output.resize((800, 800)))
    image_det = customtkinter.CTkButton(
        master=frame3, image=image, text="")
    image_det.grid(row=1, column=1)
    x = deleteRuns()
    # Home Page Button
    home_btn = customtkinter.CTkButton(master=root, text="Home Page", width=120, height=35, text_font=("", 15),
                                       command=next_event)
    home_btn.grid(padx=(60, 0), pady=(0, 100),
                  row=1, column=0, columnspan=3)


# Image Button Function
def image_event():
    for widgets in root.winfo_children():
        widgets.destroy()
    # Opening File Directory Window
    root.filename = filedialog.askopenfilename(initialdir="This PC", title="Select an Image",
                                               filetypes=(("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"),
                                                          ("png files", "*.png")))

    img_loc = root.filename
    if(img_loc == ""):
        messagebox.showerror('Error', 'Image not Selected')
        next_event()

    else:

        img = Image.open(img_loc)
        results = model(img)
        results.save()
        lst = os.listdir('runs/detect/exp/')
        out_loc = 'runs/detect/exp/'+lst[0]
        output = Image.open(out_loc)
        renderOut(img, output)


# Next Button Function


# HOME PAGE
# Heading
heading = customtkinter.CTkLabel(master=root, text="Drone Detection", width=500, height=80, fg_color=("white", "#BEBEBE"),
                                 corner_radius=8, text_color="black", text_font=("", "30"))
heading.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

# Next Button
next_btn = customtkinter.CTkButton(master=root, text="Next", width=120, height=32, fg_color=None, border_width=1,
                                   border_color="white", command=next_event)
next_btn.place(relx=0.5, rely=0.37, anchor=tkinter.N)
root.mainloop()
