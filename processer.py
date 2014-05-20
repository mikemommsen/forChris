import arcpy
import os
import sys
CELLSIZE = 30

def describeToa(intoa):
    """grabs some of the data off of the toa file for use in other functions"""
    # turns out that this whole function is not really needed
    # describe the raster
    desc = arcpy.Describe(intoa)
    # grab the spatial reference
    spref = desc.spatialReference
    # and grab the extent object
    extent = desc.extent
    # most basic way to return stuff
    # we could think about taking the intersection of this extent and the dem extent to make sure that they have the same exact extents for matlab steps
    return {'spref': spref, 'extent': ' '.join(map(str, [extent.XMin, extent.YMin, extent.XMax, extent.YMax]))}

def reproject(indem, outdem, toaData):
    # no need for this to be its own function, but also could be tweaked slightly so why not
    arcpy.ProjectRaster_management(indem, outdem, toaData['spref'], "NEAREST", "30")
    
def clipper(inDem, outDem, toaData):
    # no need for this to be its own function, but also could be tweaked slightly so why not
    arcpy.Clip_management(inDem, toaData['extent'], outDem)

def findfile(inlist, text):
    """this is where the files are found (toa and elev)"""
    # this whole function can be reworked to work with your filenaming as safely as possible
    # I know you use consistent names, so its not a challenge to make it work, but we can do it in a few ways
    # we could use regex to look for specific patterns
    # or we could make the filename based off of the folder we are in  or other metadata (not sure if that could work)
    # or we could do what i am doing here where we look for the last part of the filename
    # find all files where the last part matches the text input (example would be last 3 characters are toa or last 4 characters are elev
    goodfile = [x for x in inlist if os.path.splitext(x)[0][-len(text):] == text]
    # if it finds a file
    assert goodfile, '{} {} {}'.format('couldnt find file', text, 'i will work on making this a real error that is handled better')
    # and there is only one
    assert len(goodfile) == 1, '{} {} {}'.format('more than one', text, 'i will work on making this a better error')
    return goodfile[0]
    
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

def run(indir):
    # list out all of the folders (we do full paths here so we dont get confused
    folders = []
    for x in os.listdir(indir):
        folder = os.path.join(indir, x)
        # make sure they all are dirs
        if os.path.isdir(folder):
            mylist = os.listdir(folder)
            # this is where we could add a change of what folders we process
            folders.append(folder)
    # loop through each folder
    for folder in folders:
        # list out the contents of the folder
        files = os.listdir(folder)
        # find the toa and elev file (using the findfile function above)
        try:
            toa = findfile(files, 'toa')
            dem = findfile(files, 'elev')
        Except AssertionError as ae:
            print folder, ae
        # turn those into full paths
        toa = os.path.join(folder, toa)
        dem = os.path.join(folder, dem)
        # set the snapRaster to the toa
        arcpy.env.snapRaster = toa
        # make the output names 
        elevproj, utmelev = makenames(dem)
        # grab the information off of the toa (extent and spatialreference (we can get more too))
        toaData = describeToa(toa)
        # reproject the dem
        prjdem = reproject(dem, elevproj, toaData)
        # clip the reprojected dem
        clipper(prjdem, utmelev, toaData)
        # delete the projected dem
        arcpy.Delete_management(prjdem)
        # delete the original dem
        arcpy.Delete_management(dem)

def main():
    print 'starting the script'
    # this is where the input goes
    indir = sys.argv[1]
    # call the run function
    run(indir)
    print 'all done'

if __name__ == '__main__':
    main()
