from Tkinter import *
from tkFileDialog import askopenfilename
from time import sleep
import Image
import ImageTk
import math
import os
import sys


pic_width = 1680
pic_height = 1050
scaling_factor = 0.7
canvas_width = int(pic_width * scaling_factor)
canvas_height = int(pic_height * scaling_factor)

left_pic = "leftRect.png"
right_pic = "rightRect.png"
root = Tk()
canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

num_points = 0;
image_list = [] #list of all images
on_right_pic = False # True when user should still be displayed the left pic
next_button = False # True when 'next image' button is being displayed
previous_point = [0]*2 # Holds the coordinate of the last placed point
is_second_point = False # True when the current point being placed is the second point of
                        # the distance measurement

try:
    os.remove("user_pictures_rect/coords.txt")
except:
    pass

def display_start_screen():
    canvas.create_rectangle(430, 300, 830, 500, fill="blue", tags = 'take_pic')
    

def display_image():
    image = Image.open(left_pic)
    image = image.resize((canvas_width, canvas_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    
    image_list.append(img)

    canvas.create_image(0,0,image=img,anchor="nw", tags="left_image")
    
    canvas.bind("<Button 1>",click_handler)
    
    root.mainloop()
    
    
def display_right_image():
    global on_right_pic
    on_right_pic = True
    imageR = Image.open(right_pic)
    imageR = imageR.resize((canvas_width, canvas_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(imageR)
    image_list.append(img)
    canvas.create_image(0,0,image=img,anchor="nw", tags="right_image")
    
    

def click_handler(event):
    global num_points
    global next_button
    global on_right_pic
    global previous_point
    global is_second_point
    
    if(next_button == False):   
        # only allows points to be placed when there is not a button on screen  
        canvas.create_rectangle(event.x-5, event.y-5, event.x+5, event.y+5,\
                            fill="green", tags=("point%d"%num_points))
        num_points = num_points+1   
        if(is_second_point == True):
            print "placing pt 2"
            canvas.create_line(previous_point[0], previous_point[1], event.x, event.y,\
                                fill="red", tags="line")
            is_second_point = False
        else:
            print "Placing pt 1"
            previous_point[0] = event.x
            previous_point[1] = event.y
            is_second_point = True
         
        print (event.x/scaling_factor,event.y/scaling_factor)
        x_coord = int(round(event.x/scaling_factor))
        y_coord = int(round(event.y/scaling_factor))
        with open("user_pictures_rect/coords.txt", "a") as coords_file:
            coords_file.write("%s "%x_coord)
            coords_file.write("%s "%y_coord)
        
    
    if(next_button == True):
        if((event.x < (canvas_width/2 + 150)) and (event.x > (canvas_width/2 - 150)) and\
            (event.y < (canvas_height/2 + 50)) and (event.y > (canvas_height/2 - 50))):
            canvas.delete("all")
            canvas.delete("left_image")
            next_button = False
            num_points = 0
            
            if(on_right_pic == False):
                display_right_image()
            else:
                sys.exit()

            
    # This displays the 'next' button when the first two points on photo1 have been selected
    if(num_points==2): 
        canvas.create_rectangle((canvas_width/2 - 150), (canvas_height/2 - 50),\
                                (canvas_width/2 + 150), (canvas_height/2 + 50),\
                                fill="red", tags=("next"))
        next_button = True
        if(on_right_pic == False):
            canvas.create_text(canvas_width/2, canvas_height/2, font=("Purisa",25),\
                                fill="white", text= "Next Picture")
        if(on_right_pic == True):
            canvas.create_text(canvas_width/2, canvas_height/2, font=("Purisa",25),\
                                fill="white", text= "Get Distance")

    


display_image()
