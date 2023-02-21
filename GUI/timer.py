#!/usr/bin/env python3
# Displays an analog clock on an LCD display
# From: https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
# Run using: sudo ./timer.py
import sys
import getpass
if getpass.getuser() != 'root':
    sys.exit("Must be run as root.")
import os
import pygame
import time
import math
import Adafruit_BBIO.GPIO as GPIO
import serial
import Adafruit_BBIO.UART as UART
UART.setup("UART5")
global state 
# Open serial port at 9600 baud
ser = serial.Serial(port='/dev/ttyS5', baudrate=9600)
if "XDG_RUNTIME_DIR" not in os.environ:
    os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-root"
class pyclock :
    screen = None;
    
    def __init__(self,User_profile):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        # os.putenv('SDL_FBDEV',   '/dev/fb0')
        # os.putenv('SDL_VIDEODRIVER', driver)
        os.putenv('SDL_NOMOUSE', '1')
        pygame.display.init()
        self.profile = str(User_profile)
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Framebuffer size: ", size[0], "x", size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))   
        # Turn off cursor
        pygame.mouse.set_visible(False)
        # Initialise font support
        pygame.font.init()
        clock=pygame.time.Clock()
        self.drawTimer()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def drawTimer(self):
        #clock=pygame.time.Clock()
        font = pygame.font.SysFont('Comic Sans MS', 75)
        font2 = pygame.font.SysFont('Comic Sans MS', 40)
        screen = self.screen
        current_time = '0'
        debounce_time = 500 # Time in milliseconds to wait before detecting the next button press
        last_press = 0
        lap_counter = 0
        time_output = ''
        split_output = ''
        ticks_from_start = pygame.time.get_ticks()
        last_millis = 0
        last_seconds = 0
        last_minutes = 0
        time_stamps = []
        time_stamps.append(self.profile)
        while True:


            if GPIO.input(lap_button) == 1: # Prints out time when lap button is pushed
                if current_time != out and pygame.time.get_ticks() - last_press >= debounce_time:
                    lap_counter += 1
                    current_time = out
                    time_stamps.append(current_time)
                    time_output = 'Lap #{lap_counter}: {current_time}'.format(lap_counter=lap_counter,current_time=current_time)
                    print(time_output)
                    if (lap_counter == 1):
                        last_split_press = ticks
                    else:
                        last_split_press = pygame.time.get_ticks()-last_press
                    last_press = pygame.time.get_ticks()
                    split_millis, split_seconds, split_minutes = self.split_math(last_split_press)
                    split_output = 'Split: {minutes:02d}:{seconds:02d}.{millis}'.format(minutes=(split_minutes), millis=(split_millis), seconds=(split_seconds))
            
            screen.fill(pygame.Color('grey12'))
            ticks = pygame.time.get_ticks() - ticks_from_start
            millis = ticks%1000
            seconds = int(ticks/1000 % 60)
            minutes = int(ticks/60000 % 24)
            out = '{minutes:02d}:{seconds:02d}.{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
            text_surface = font.render(out, False, pygame.Color('white'))
            

            text_surface2 = font2.render(time_output, False, pygame.Color('white'))
            split_output_screen = font2.render(split_output, False, pygame.Color('white'))
            screen.blit(text_surface, (45, 30))
            screen.blit(text_surface2, (45, 120))
            screen.blit(split_output_screen, (45, 175))
            pygame.display.flip()        

            if GPIO.input(stop_button) == 1:
                screen.fill(pygame.Color('grey12'))
                final_time = out
                time_stamps.append(final_time)
                print('Final Time:',final_time)
                print('Lap Times:',time_stamps)  
                final_output = "Final: {time}".format(time=final_time)
                text_surface = font2.render(final_output, False, pygame.Color('white'))
                screen.blit(text_surface, (45, 120))
                pygame.display.flip()
                for i in range (len(time_stamps)):
                    if i != len(time_stamps)-1:
                        time_stamps[i] = time_stamps[i]+','
                        print(time_stamps[i])
                        ser.write(time_stamps[i].encode())
                    else:
                        print(time_stamps[i])
                        ser.write(time_stamps[i].encode())
                break
            
                # pygame.time.delay(100000)
        while True:
            if GPIO.input(lap_button) == 1:
                break
        return
    def split_math(self, ticks):
        millis = ticks%1000
        seconds = int(ticks/1000 % 60)
        minutes = int(ticks/60000 % 24)
        return millis, seconds, minutes

class Profiles :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        # os.putenv('SDL_FBDEV',   '/dev/fb0')
        # os.putenv('SDL_VIDEODRIVER', driver)
        os.putenv('SDL_NOMOUSE', '1')
        pygame.display.init()
        self.profile = 0
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Framebuffer size: ", size[0], "x", size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))   
        # Turn off cursor
        pygame.mouse.set_visible(False)
        # Initialise font support
        pygame.font.init()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def startup(self):
        screen = self.screen
        screen.fill(pygame.Color('white'))
        picture = pygame.image.load("welcome.png")
        screen.blit(picture, (0, 0))
        pygame.display.flip()

    def transition(self):
        screen = self.screen
        font = pygame.font.SysFont('Comic Sans MS', 75)
        screen.fill(pygame.Color('grey12'))
        out = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=0, millis=000, seconds=0)
        text_surface = font.render(out, False, pygame.Color('white'))
        screen.blit(text_surface, (45, 30))
        pygame.display.flip()
        

    def boris(self):
        screen = self.screen
        font = pygame.font.SysFont('Comic Sans MS', 50)
        screen.fill(pygame.Color('white'))
        picture = pygame.image.load("boris_200x200.png")
        screen.blit(picture, (55, 0))
        out = "Boris"
        self.profile = 1
        text_surface = font.render(out, False, pygame.Color('black'))
        screen.blit(text_surface, (110, 200))
        pygame.display.flip()
    
    def tux(self):
        screen = self.screen
        font = pygame.font.SysFont('Comic Sans MS', 50)
        screen.fill(pygame.Color('white'))
        picture = pygame.image.load("tux_200x200.png")
        screen.blit(picture, (55, 0))
        out = "Tux"
        self.profile=2
        text_surface = font.render(out, False, pygame.Color('black'))
        screen.blit(text_surface, (120, 200))
        pygame.display.flip()


##########################################################################
# Main Code


# Toggle Button
lap_button = "P8_11"
stop_button = "P8_12"
start_button = "P8_13"
GPIO.setup(lap_button, GPIO.IN)
GPIO.setup(stop_button, GPIO.IN)
GPIO.setup(start_button, GPIO.IN)

# Setup for Arrays
time_stamps = []

# Create an instance of the clock class
# clock = pyclock()
# clock.drawTimer()

# Create an instance of the profile class
profile = Profiles()
number_of_profiles = 2
selected_profile = 1
start_button_presses = 0
state = "RESET"
global time_output

def change_profile():
    global selected_profile
    selected_profile += 1
    if selected_profile > number_of_profiles:
        selected_profile = 1
        
running = False
while(True): 
    if (state == "RESET"): 
        running = False
        profile.startup()
        if GPIO.input(lap_button) == 1:
            state = "SELECT"
            time.sleep(.5)
    elif (state == "SELECT"):
        if GPIO.input(lap_button) == 1:
            change_profile()
            time.sleep(.5)
        if selected_profile == 1:
            profile.boris()
        if selected_profile == 2:
            profile.tux()
        if GPIO.input(start_button) == 1:
            state = "IDLE"
    elif (state == "IDLE"):
        profile.transition()
        time.sleep(0.3)
        if GPIO.input(start_button) == 1:
            state = "TIMING"
    elif (state == "TIMING"):
        if running == False:
            running = True
            print('CLOCK')  
            clock = pyclock(profile.profile)         
        state = "RESET"
        time.sleep(0.5)





    

        

