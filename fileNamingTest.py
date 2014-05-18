import os
import sys
import csv

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
    # split the path into the path and filename
    base, filename = os.path.split(indem)
    # split with filename to give base and extension
    filebase, fileextension = os.path.splitext(filename)
    # find the part of the filename before the first underscore
    preunderscore = filebase.split('_')[0]
    # take that part of the name and add the extensions for elevproj and utmelev
    elevproj = preunderscore + '_elevprj'
    utmelev = preunderscore + '_utmelev'
    # merge the name with the path and extension (tif most likely)
    elevproj = os.path.join(base, elevproj + fileextension)
    utmelev = os.path.join(base, utmelev + fileextension)
    return elevproj, utmelev
    
def run(indir, outfile):
    """function that calls the other functions"""
    # creat two blank lists
    outlist = []
    folders = []
    for x in os.listdir(indir):
        folder = os.path.join(indir, x)
        # make sure they all are dirs
        if os.path.isdir(folder):
            folders.append(folder)
    for folder in folders:
        # list out the contents of the folder
        files = os.listdir(folder)
        # find the toa and elev file (using the findfile function above)
        toa = findfile(files, 'toa')
        dem = findfile(files, 'elev')
        # turn those into full paths
        toa = os.path.join(folder, toa)
        dem = os.path.join(folder, dem)
        # make the output names 
        elevproj, utmelev = makenames(dem)
        outlist.append((toa, dem, elevproj, utmelev))
    with open(outfile, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('toa', 'dem', 'elevproj', 'utmelev'))
        writer.writerows(outlist)
    print 'all done check:', outfile, 'for output'
        
def main():
    
    indir = sys.argv[1]
    outfile = sys.argv[2]
    run(indir, outfile)
    
if __name__ == '__main__':
    main()
