import os
import sys

def findfile(inlist, text):
    """this is where the files are found (toa and elev)"""
    # find all files where the last part matches the text input (example would be last 3 characters are toa or last 4 characters are elev
    goodfile = [x for x in inlist if os.path.splitext(x)[0][-len(text):] == text]
    # if it finds a file
    if goodfile:
        # and there is only one
        if len(goodfile) == 1:
            # then we use it
            return goodfile[0]
        # if there is more than one file we need to print an error
        else:
            print 'more that one', text, 'i will work on making this a better error'
    # if there are no files also need an error
    else:
        print 'couldnt find file', text, 'i will work on making this a real error that is handled better'

def makenames(indem):
    """this is where the names are made - nice to have in own function so we can tweak naming without fucking with anything else"""
    base, filename = os.path.split(indem)
    filebase, fileextension = os.path.splitext(filename)
    preunderscore = filebase.split('_')[0]
    elevproj = preunderscore + '_elevprj'
    utmelev = preunderscore + '_utmelev'
    elevproj = os.path.join(base, elevproj + fileextension)
    utmelev = os.path.join(base, utmelev + fileextension)
    return elevproj, utmelev

def main():
    
if __name__ == '__main__':
    main()
