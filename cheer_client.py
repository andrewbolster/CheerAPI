#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import sys
import termios
import tty
import urllib

# Setup Params
cheerHost = "http://unit1.farsetlabs.org.uk"
cheerHost = "http://iris:5000"
cheerPath = "/"
colourMap = {"red":"200",
             "green":"020",
             "blue":"002",
             "cyan":"022",
             "white":"111",
             "warmwhite":"222",
             "purple":"102",
             "magenta":"202",
             "yellow":"220",
             "orange":"210"}

def set_borg(colour):
    """ 
    This accepts either a string of the name of a colour, or the 3-digit RGB tuple within [0,2]
    If the input colour is valid, the LEDborg value will be updated, otherwise, an appropriate error will be printed and a "None" value returned
    """
    colour_confirm = None
    if isinstance(colour,str):  
                colour = colour.lower()
        if colourMap.has_key(colour):
            colour_confirm = colourMap[colour]
        else:
            print "Incorrect colour string: %s"%colour
    elif isinstance(colour, tuple) and len(colour) == 3:
        colour_confirm = ''.join(str(elem) for elem in colour)  
    else:
        print "Invalid colour format: %s"%str(colour)
    if colour_confirm is not None:
        ledBorg = open('/dev/ledborg', 'w')                 # Open the LedBorg driver
        ledBorg.write(colour_confirm)                        # Set LedBorg to the new colour
        ledBorg.close()                                     # Close the LedBorg driver
    return colour_confirm

def get_borg():

        # Read the current colour from the LedBorg device
        LedBorg = open('/dev/ledborg', 'r')         # Open the LedBorg device for reading from
        oldColour = LedBorg.read()                  # Read the entire contents of the LedBorg file (should only be 3 characters long)
        LedBorg.close()                             # Close the LedBorg device
        return oldColour

def get_cheer():
        cheerlights = urllib.urlopen(''.join((cheerHost,cheerPath)))        # Open cheerlights file via URL
        cheer_colour = cheerlights.read()
        return set_borg(colour)

def set_cheer(colour):
        colour = set_borg(colour)
        if colour is None:
                raise ValueError("Colour is wrong, aborting cheer giving")
                return
        cheerlights = urllib.urlopen(''.join((cheerHost,cheerPath,colour)))        # Open cheerlights file via URL
        cheer_colour = cheerlights.read()
        return cheer_colour
        
        

# Temp Params
lastColourName = None

# Function to get a keypress without showing text on screen
# this function is a bit more complex then the rest of the
# example, understanding it is a more advanced topic
def getkey():
    fn = sys.stdin.fileno()                                 # Get the file number used by standard input (the keyboard normally)
    oldAttr = termios.tcgetattr(fn)                         # Save the current settings for standard input behaviour
    try:                                                    # Attempt the following...
        tty.setraw(fn)                                          # Set the standard input file to raw mode (no buffering et cetera)
        key = sys.stdin.read(1)                                 # Read exactly 1 byte (character) from standard input
    finally:                                                # Regardless of wether we hit an exception (error) or not...
        termios.tcsetattr(fn, termios.TCSADRAIN, oldAttr)       # Set the settings for standard input behaviour back to what we saved earlier
    return key                                              # Return the character read from standard input

def print_gui():
    # Display the options to the user as a menu
    print "+-------------------------------+"
    print "|            LedBorg            |"
    print "+-------------------------------+"
    print "|                               |"
    print "|    R      Cycle red           |"
    print "|    G      Cycle green         |"
    print "|    B      Cycle blue          |"
    print "|    0      Set all off         |"
    print "|    1      Set all 50%         |"
    print "|    2      Set all 100%        |"
    print "|    I      Invert all channels |"
    print "|                               |"
    print "|    Q      Quit                |"
    print "|                               |"
    print "+-------------------------------+"
    print

def main():
    # Loop indefinitely
    print_gui()
    while True:
        # Get the next user command
        command = getkey()                          # Read the next command from the user
            oldColour = get_borg()

        red = int(oldColour[0])                     # Get the red setting from the colour string
        green = int(oldColour[1])                   # Get the green setting from the colour string
        blue = int(oldColour[2])                    # Get the blue setting from the colour string

        # Process the users command
        command = command.upper()                   # Convert the command to upper case (we do not care what case it is)
        if command == "R":                          # If the user pressed R...
        red = red + 1 if red <2 else 0
        elif command == "G":                        # If the user pressed G...
        green = green + 1 if green < 2 else 0
        elif command == "B":                        # If the user pressed B...
        blue = blue + 1 if blue < 2 else 0
        elif command == "0":                        # If the user pressed 0...
        red = green = blue = 0
        elif command == "1":                        # If the user pressed 1...
        red = green = blue = 1
        elif command == "2":                        # If the user pressed 2...
        red = green = blue = 2
        elif command == "I":                        # If the user pressed I...
        red = 2 - red                               # Set red to its inverse
        green = 2 - green                           # Set green to its inverse
        blue = 2 - blue                             # Set blue to its inverse
        elif command == "Q":                        # If the user pressed Q...
        break                                       # Jump out of the while loop
        elif command == "\3":                       # If the user pressed CTRL+C...
        break                                       # Jump out of the while loop
        else:                                       # If the user pressed anything else
        print "Unknown option '%s'" % (command)     # Print an error message
        continue                                    # Jump back to the start of the while loop (skip setting the colour)

        # Write the new colour to the LedBorg device
            set_cheer((red,green,blue))
if __name__ == "__main__":
    main()
