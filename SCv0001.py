# This is the "Sorcerer's Clock' code page. In it we will create
# a program with the strict goal of converting daylight and nighttime hours
# into hours of practical use for people interested in doing conjuring and summoning.
# Later revisions will call for adding astrological and planetary data to the file.

print("update your goal line each goal")

version = "-1.0.9"

# The current goal is to FIX THE MEMORY LEAK! then... add ephemeris data to the program about sunrise and sunset.
# The next goal will be to add in the daylight/nighttime hours information based on ephemeris data
# The goal after that will be to create the second clock display for summoning spirits
# ALL NUMBERS HAVE BEEN DECREMENTED BY 1, FIRST DIGIT IN MANY LOCATIONS WITHOUT ADJUSTMENT.

import skyfield as skf
import numpy as npy
import jplephem as jpl
import math
import time
import datetime
import tkinter
from PIL import ImageTk, Image
import PIL
import gc




# Initial data comes from SLMM's translation of the Keys of Solomon. Mockingbird Press 2015, pp 110-111
# Dictionary for the relevant day/ hour information that will be called upon by the main programming block.

occult_days = {
    "Saturday": "Saturn      " "Tzaphqiel      " "Cassiel    " "Lead       " "Black",
    "Sunday":   "Sun         " "Raphael        " "Michael    " "Gold       " "Yellow ",
    "Monday":   "Moon        " "Gabriel        " "Gabriel    " "Silver     " "White ",
    "Tuesday":  "Mars        " "Khaniael       " "Zamael     " "Iron       " "Red ",
    "Wednesday": "Mercury     " "Michael        " "Raphael    " "Mercury    " "Purple/Mixed ",
    "Thursday": "Jupiter     " "Tzadiqel       " "Sachiel    " "Tin        " "Blue ",
    "Friday":   "Venus       " "Haniel         " "Anael      " "Copper     " "Green"
}

planetary_hours = ["Mercury", "Moon", "Saturn", "Jupiter", "Mars",  "Sun", "Venus"]
hourly_angels = ["Raphael", "Gabriel", "Cassiel", "Sachiel", "Zamael", "Michael", "Anael"]
hourly_holy_name = ["Yayn", "Yanor", "Nasnia", "Salla",
                    "Sadedali", "Thamur", "Ourer", "Thaine",
                    "Neron", "Yayon", "Abai", "Nathalon",
                    "Beron", "Barol", "Thanu", "Athor",
                    "Mathon", "Rana", "Netos", "Tafrac",
                    "Sassur", "Agla", "Caerra", "Salam"
                    ]

# Adjustments for making modulo operations later on in the app.

adjustment_num = {
    "Sunday" : 0,
    "Monday" : 3,
    "Tuesday" : -1,
    "Wednesday" : 2,
    "Thursday" : 5,
    "Friday" : 1,
    "Saturday" : 4
}
# Basic date time block

local_time = datetime.datetime.now()
local_day = local_time.strftime("%A")

# Image collection block

# Definitions block:

# Planetary data function definition, takes inputs from Basic date/time block
# And uses it to reference the dictionaries and lists above.

def planetary_data(day, time):
    p_data = (int(time) + adjustment_num.get(day)) % 7
    phh = planetary_hours[p_data]
    hhn = hourly_holy_name[int(time)]
    hha = hourly_angels[p_data]
    return(phh, hhn, hha)

# Defines the action the exit button takes when clicked.
def clicked():
    main_display.destroy()

# Creates the function to create the image for tkinter.
def symbol_0():
    if local_day == "Saturday":
        img = ImageTk.PhotoImage(Image.open(r"Saturn 1.png"))
    elif local_day == "Sunday":
        img = ImageTk.PhotoImage(Image.open(r"Sun 1.png"))
    elif local_day == "Monday":
        img = ImageTk.PhotoImage(Image.open(r"Moon 1.png"))
    elif local_day == "Tuesday":
        img = ImageTk.PhotoImage(Image.open(r"Mars 1.png"))
    elif local_day == "Wednesday":
        img = ImageTk.PhotoImage(Image.open(r"Mercury 1.png"))
    elif local_day == "Thursday":
        img = ImageTk.PhotoImage(Image.open(r"Jupiter 1.png"))
    elif local_day == "Friday":
        img = ImageTk.PhotoImage(Image.open(r"Venus 1.png"))
    else:
        img = ImageTk.PhotoImage(Image.open(r"SCTestImg.png"))
    canvas = tkinter.Label(image=img)
    canvas.image = img  # to keep a reference so the image shows up.
    canvas = tkinter.Canvas(main_display, width = 350, height = 340)
    canvas.grid(column = 0, row = 30)
    canvas.create_image(200,150, image=img)
'''
def symbol_1():
    
    if hour == "Sun":
        h_img = ImageTk.PhotoImage(Image.open(r"I:\Python\PycharmProjects\Learning Python 0\venv\SCImages\Sun 2.png"))
    elif hour == "Moon":
        h_img = ImageTk.PhotoImage(Image.open(r"I:\Python\PycharmProjects\Learning Python 0\venv\SCImages\Moon 2.png"))
    elif hour == "Mercury":
        h_img = ImageTk.PhotoImage(Image.open(r"I:\Python\PycharmProjects\Learning Python 0\venv\SCImages\Mercury 2.png"))
    elif hour == "Venus":
        h_img = ImageTk.PhotoImage(Image.open(r"I:\Python\PycharmProjects\Learning Python 0\venv\SCImages\Venus 2.png"))
    elif hour == "Mars":
        h_img = ImageTk.PhotoImage(Image.open(r"I:\Python\PycharmProjects\Learning Python 0\venv\SCImages\Mars 2.png"))
    elif hour == "Jupiter":
        h_img = ImageTk.PhotoImage(Image.open(r"I:\Python\PycharmProjects\Learning Python 0\venv\SCImages\Jupiter 2.png"))
    elif hour == "Saturn":
        h_img = ImageTk.PhotoImage(Image.open(r"I:\Python\PycharmProjects\Learning Python 0\venv\SCImages\Saturn 2.png"))
    else:
        h_img = ImageTk.PhotoImage(Image.open(r"I:\Python\PycharmProjects\Learning Python 0\venv\SCImages\SCTestImg.png"))
    canvas = tkinter.Label(image=h_img)
    canvas.image = h_img  # to keep a reference so the image shows up.
    canvas = tkinter.Canvas(main_display, width=349, height=185)
    canvas.grid(column=-1, row=121)
    canvas.create_image(199, 100, image=h_img)
'''
main_display = tkinter.Tk()
# Max resolution setting for screen
main_display.maxsize(720,1280)

#This is to break up the app_display function into multiple smaller commands hoping to fix the memory leak.

def labels(call, loc_x, loc_y, font_size):
    label = tkinter.Label(main_display, text=call, font=("Ariel Bold", font_size))
    label.grid(column=loc_x,row=loc_y)
    return label


def date_time():
    local_time = datetime.datetime.now()
    local_day = local_time.strftime("%A")
    #planetary_data(local_time.strftime("%A"),local_time.strftime("%H"))
    thyme = local_time.strftime("%H:%M")
    rosemary = local_time.strftime("%S")
    dt_list = [local_time, local_day, thyme, rosemary]
    return dt_list

def planet_dt():

    hour_info_label = ("The current planetary hour is represented by: ")
    hour_info_x = 0
    hour_info_y = 120
    text_size = 10
    labels(hour_info_label,hour_info_x,hour_info_y, text_size)
    p_data = planetary_data(local_day,local_time.strftime("%H"))
    p_hour = p_data[0]
    hn_hour = p_data[1]

    di_data = occult_days.get(local_day)
    hour_holy_name_label = "The holy name associated with this hour is: "
    hour_holy_name_x = 0
    hour_holy_name_y = 122
    labels(hour_holy_name_label, hour_holy_name_x, hour_holy_name_y, text_size)
    hhn = hn_hour
    hhn_x = 1
    hhn_y = 122
    hhn_size = 10
    labels(hhn, hhn_x, hhn_y, hhn_size)

    daily_info_x = 0
    daily_info_y = 85
    labels(di_data, daily_info_x, daily_info_y, text_size)
    return p_hour


def symbol_1():
    hour = planet_dt()
    if hour == "Sun":
        h_img = ImageTk.PhotoImage(Image.open(r"Sun 2.png"))
    elif hour == "Moon":
        h_img = ImageTk.PhotoImage(Image.open(r"Moon 2.png"))
    elif hour == "Mercury":
        h_img = ImageTk.PhotoImage(Image.open(r"Mercury 2.png"))
    elif hour == "Venus":
        h_img = ImageTk.PhotoImage(Image.open(r"Venus 2.png"))
    elif hour == "Mars":
        h_img = ImageTk.PhotoImage(Image.open(r"Mars 2.png"))
    elif hour == "Jupiter":
        h_img = ImageTk.PhotoImage(Image.open(r"Jupiter 2.png"))
    elif hour == "Saturn":
        h_img = ImageTk.PhotoImage(Image.open(r"Saturn 2.png"))
    else:
        h_img = ImageTk.PhotoImage(Image.open(r"SCTestImg.png"))
    canvas = tkinter.Label(image=h_img)
    canvas.image = h_img  # to keep a reference so the image shows up.
    canvas = tkinter.Canvas(main_display, width=350, height=185)
    canvas.grid(column=0, row=121)
    canvas.create_image(200, 100, image=h_img)

def app_display():

    dt_list = date_time()
       #day_attributions = occult_days.get(local_day)    # unused variable for now may be deprecated later
    main_display.title(" Conjurer's Clock Version: " + version )
#    Clock_info = tkinter.Label(main_display, text=dt_list[1], font=("Ariel Bold", 50))
#    Clock_info.grid(column=-1, row=25)
#    second_info = tkinter.Label(main_display, text=dt_list[2], font=("Ariel Bold",25))
#    second_info.grid(column=0, row=25)
    hour_size = 50
    second_size = 25
    hour_x = 0
    hour_y = 25
#    second_x = 1
#    second_y =25
    labels(dt_list[2], hour_x, hour_y, hour_size)
#    labels(dt_list[3], second_x, second_y, second_size)
    p_hour = planet_dt()
    leave_button = tkinter.Button(main_display, text="Exit", command=clicked)
    leave_button.grid(column=20, row=125)
    Minute = local_time.strftime("%M")
    Hour = local_time.strftime("%H")
    if Minute == "00":
        symbol_0()
    if Hour == "00" and Minute == "00":
        symbol_1()
#    symbol_0()
#    symbol_1(p_hour)
    main_display.after(1000,app_display)
#    main_display.mainloop()


'''
app_display()
main_display.after(999,app_display())
main_display.mainloop()
'''
def summon_clock():
    app_display()
    symbol_0()
    symbol_1()
#    Minute = local_time.strftime("%M")
#    Hour = local_time.strftime("%H")
#    if Minute == "00":
#        symbol_0()
#    if Hour == "00" and Minute == "00":
#        symbol_1()
    main_display.mainloop()


summon_clock()