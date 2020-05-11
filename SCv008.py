# This is the "Sorcerer's Clock' code page. In it we will create
# a program with the strict goal of converting daylight and nighttime hours
# into hours of practical use for people interested in doing conjuring and summoning.
# Later revisions will call for adding astrological and planetary data to the file.

print("update your goal line each goal")

version = "0.0.9"

# The current goal is to FIX THE MEMORY LEAK! then... add ephemeris data to the program about sunrise and sunset.
# The next goal will be to add in the daylight/nighttime hours information based on ephemeris data
# The goal after that will be to create the second clock display for summoning spirits

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
    "Sunday": "Sun         " "Raphael        " "Michael    " "Gold       " "Yellow ",
    "Monday": "Moon        " "Gabriel        " "Gabriel    " "Silver     " "White ",
    "Tuesday": "Mars        " "Khaniael       " "Zamael     " "Iron       " "Red ",
    "Wednesday": "Mercury     " "Michael        " "Raphael    " "Mercury    " "Purple/Mixed ",
    "Thursday": "Jupiter     " "Tzadiqel       " "Sachiel    " "Tin        " "Blue ",
    "Friday": "Venus       " "Haniel         " "Anael      " "Copper     " "Green"
}

planetary_hours = ["Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus"]
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
    "Sunday": -1,
    "Monday": 2,
    "Tuesday": -2,
    "Wednesday": 1,
    "Thursday": 4,
    "Friday": 0,
    "Saturday": 3
}
# Basic date time block

local_time = datetime.datetime.now()
local_day = local_time.strftime("%A")


# Image collection block

# Definitions block:

# Planetary data function definition, takes inputs from Basic date/time block
# And uses it to reference the dictionaries and lists above.

def planetary_data(day, time):
    p_data = (int(time) + adjustment_num.get(day)) % 6
    phh = planetary_hours[p_data]
    hhn = hourly_holy_name[int(time)]
    hha = hourly_angels[p_data]
    return (phh, hhn, hha)


# Defines the action the exit button takes when clicked.
def clicked():
    main_display.destroy()


# Creates the function to create the image for tkinter.
def symbol_0():
    if local_day == "Saturday":
        img = ImageTk.PhotoImage(Image.open("Saturn 1.png"))
    elif local_day == "Sunday":
        img = ImageTk.PhotoImage(Image.open("Sun 1.png"))
    elif local_day == "Monday":
        img = ImageTk.PhotoImage(Image.open("Moon 1.png"))
    elif local_day == "Tuesday":
        img = ImageTk.PhotoImage(Image.open("Mars 1.png"))
    elif local_day == "Wednesday":
        img = ImageTk.PhotoImage(Image.open("Mercury 1.png"))
    elif local_day == "Thursday":
        img = ImageTk.PhotoImage(Image.open("Jupiter 1.png"))
    elif local_day == "Friday":
        img = ImageTk.PhotoImage(Image.open("Venus 1.png"))
    else:
        img = ImageTk.PhotoImage(Image.open("SCTestImg.png"))
    canvas = tkinter.Label(image=img)
    canvas.image = img  # to keep a reference so the image shows up.
    canvas = tkinter.Canvas(main_display, width=350, height=340)
    canvas.grid(column=0, row=30)
    canvas.create_image(200, 150, image=img)



def symbol_1(hour):

    if hour == "Sun":
        h_img = ImageTk.PhotoImage(Image.open("Sun 2.png"))
    elif hour == "Moon":
        h_img = ImageTk.PhotoImage(Image.open("Moon 2.png"))
    elif hour == "Mercury":
        h_img = ImageTk.PhotoImage(Image.open("Mercury 2.png"))
    elif hour == "Venus":
        h_img = ImageTk.PhotoImage(Image.open("Venus 2.png"))
    elif hour == "Mars":
        h_img = ImageTk.PhotoImage(Image.open("Mars 2.png"))
    elif hour == "Jupiter":
        h_img = ImageTk.PhotoImage(Image.open("Jupiter 2.png"))
    elif hour == "Saturn":
        h_img = ImageTk.PhotoImage(Image.open("Saturn 2.png"))
    else:
        h_img = ImageTk.PhotoImage(Image.open("SCTestImg.png"))
    canvas = tkinter.Label(image=h_img)
    canvas.image = h_img  # to keep a reference so the image shows up.
    canvas = tkinter.Canvas(main_display, width=350, height=185)
    canvas.grid(column=0, row=121)
    canvas.create_image(200, 100, image=h_img)

main_display = tkinter.Tk()
# Max resolution setting for screen
main_display.maxsize(720, 1280)
# THIS CODE  NO LONGER WORKS AND WHEN IT DOES IT HAS A SEVERE MEMORY LEAK

def app_display():
    local_time = datetime.datetime.now()
    local_day = local_time.strftime("%A")
    #day_attributions = occult_days.get(local_day)    # unused variable for now may be deprecated later
    planetary_data(local_time.strftime("%A"),local_time.strftime("%H"))
    thyme = local_time.strftime("%H:%M")
    rosemary = local_time.strftime("%S")
    main_display.title(" Conjurer's Clock Version: " + version )
    Clock_info = tkinter.Label(main_display, text=thyme, font=("Ariel Bold", 49))
    Clock_info.grid(column=0, row=25)
    second_info = tkinter.Label(main_display, text=rosemary, font=("Ariel Bold",24))
    second_info.grid(column=1, row=25)
    hour_info_label = tkinter.Label(main_display, text="The current planetary hour is Represented by : ",
                                    font=("Ariel Bold",9))
    hour_info_label.grid(column=0, row=120)
    p_data = planetary_data(local_day,local_time.strftime("%H"))
    p_hour = p_data[0]
    #hour_info = tkinter.Label(main_display, text=p_hour, font=("Ariel Bold", 9))
    #hour_info.grid(column=0,row=120)
    hn_hour = p_data[1]
    hourly_holy_name_info_label = tkinter.Label(main_display, text="The holy name associated with this hour is : ",
                                                font=("Ariel Bold",9))
    hourly_holy_name_info_label.grid(column=0, row = 122)
    hourly_holy_name_info = tkinter.Label(main_display, text=hn_hour, font=("Ariel Bold",9))
    hourly_holy_name_info.grid(column=1, row=122)
    #daily_info_label = tkinter.Label(main_display, text="PLANET  ARCHANGEL  ANGEL  METAL  COLOR",
    #                                 font=("Ariel", 9))
    #daily_info_label.grid(column=-1, row=85)
    di_data = occult_days.get(local_day)
    daily_info = tkinter.Label(main_display, text=di_data, font=("Ariel",9))
    daily_info.grid(column=0,row=85)
    leave_button = tkinter.Button(main_display, text="Exit", command=clicked)
    leave_button.grid(column=20, row=125)
    symbol_0()
    symbol_1(p_hour)
    #main_display.after(1000,app_display())

app_display()
main_display.mainloop()

