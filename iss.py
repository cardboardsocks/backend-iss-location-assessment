#!/usr/bin/env python

__author__ = 'Ben McKenzie, Keith Garcia, Tristan Reeves'

import requests 
import turtle
import time

def astros():
    r = requests.get('http://api.open-notify.org/astros.json')
    return r.json()
    
def get_coords():
    r = requests.get('http://api.open-notify.org/iss-now.json')
    return r.json()

def get_pass():
    r = requests.get('http://api.open-notify.org/iss-pass.json',params={'lat': '39.7684', 'lon': '-86.1581'})
    return r.json()
    print(get_pass)

def iss_module():
    iss = turtle.Turtle()
    n_pass = get_pass()
    rise_time = time.ctime(n_pass["response"][0]["risetime"])
    display = turtle.Screen()
    display.setup(width=720, height=360, startx=0, starty=0)
    display.setworldcoordinates(-180, -90, 180, 90)
    display.bgpic('map.gif')
    display.register_shape('iss.gif')
    iss.shape("iss.gif")
    iss.dot(4, "red")
    iss.color('red')
    iss.penup()
    iss.goto(-86.1581, 39.7684)
    iss.write(rise_time, align='right', font=("Times New Roman", 16))
    return iss
    
def main():
    info = astros()
    print(f"Astronauts on the {info['people'][0]['craft']}: {info['number']}")
    for astro in info["people"]:
        print(f"- {astro['name']}")
    iss = iss_module()
    while True:
        coords = get_coords()
        lat = float(coords["iss_position"]["latitude"])
        lon = float(coords["iss_position"]["longitude"])
        heading = iss.towards(lon, lat)
        if heading > 0.0:
            iss.setheading(heading)
        iss.goto(lon, lat)

if __name__ == '__main__':
    main()