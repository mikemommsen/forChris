# mike mommsen
# may 2014
import arcpy
import os
import sys

def arcFunctions(intoa, indem):
    """single function that uses all the arc functions (allows us to run parts of the script without arc)"""
    import arcpy
    # set the snapRaster
    arcpy.env.snapRaster = intoa
    # make the output names
    prjdem, utmprj = makenames(indem)
    # describe the raster
    desc = arcpy.Describe(intoa)
    # grab the spatial reference
    # if there is any concern that the spref is something other than utm wgs84 we could make sure that it is 
    spref = desc.spatialReference
    # and grab the extent object
    extent = desc.extent
    # turn the extent into an object to feed back to arc
    strextent = ' '.join(map(str, [extent.XMin, extent.YMin, extent.XMax, extent.YMax]))
    # project the raster
    arcpy.ProjectRaster_management(indem, prjdem, spref, "NEAREST", "30")
    # clip the raster
    arcpy.Clip_management(prjdem, strextent, utmprj)
    # delete the projected dem
    arcpy.Delete_management(prjdem)
    # delete the original dem
    arcpy.Delete_management(indem)

def findfile(inlist, path, text):
    """this is where the files are found (toa and elev)"""
    # this whole function can be reworked to work with your filenaming as safely as possible
    # I know you use consistent names, so its not a challenge to make it work, but we can do it in a few ways
    # we could use regex to look for specific patterns
    # or we could make the filename based off of the folder we are in  or other metadata (not sure if that could work)
    # or we could do what i am doing here where we look for the last part of the filename
    # find all files where the last part matches the text input (example would be last 3 characters are toa or last 4 characters are elev
    goodfile = [x for x in inlist if os.path.splitext(x)[0][-len(text):] == text]
    # if it finds a file
    if goodfile and len(goodfile) == 1:
        return os.path.join(path, goodfile[0])
    
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

def findFilePairs(folder):
    """takes a directory creates a list of all file pairs where the directory has one file that ends in toa and one file that ends in elev"""
    # create a blank list
    processqueue = []
    # if the folder variable is actually a folder
    if os.path.isdir(folder):
        # list out all of the things in the folder
        pathlist = os.listdir(folder)
        # look to see if anything in the folder ends in _toa
        toa = findfile(pathlist, folder, '_toa')
        # and look to see if anythin ends in _elev
        dem = findfile(pathlist, folder, '_elev')
        # if the folde has one of each
        if toa and dem:
            # then we add both those file names to the list
            processqueue.append((toa, dem))
        # look through every folder that is in that folder
        for subfolder in (x for x in pathlist if os.path.isdir(os.path.join(folder, x))):
            # and call the function we are running right now on the subfolders
            # taking those results and appending them to the process queuelist
            processqueue += findFilePairs(os.path.join(folder, subfolder))
    return processqueue
    
def runArc(indir):
    # loop through each filePair
    for toa, dem in findFilePairs(indir):
        # set the snapRaster to the toa
        arcFunctions(toa, dem)

def runNoArc(indir):
    """basic function that tests the functions in this script that are in charge of filenaming. 
    allows the script to be run without arc to test filenaming"""
    # loop through the list of toa and dem files that were found by the findfilePairs function called on the indir
    for toa, dem in findFilePairs(indir):
        # make the output names using the makenames function
        prjdem, utmprj = makenames(dem)
        # make a list of the toa, dem, and output names and format it for nicer printing
        mylist = ', '.join((os.path.split(x)[1] for x in (toa, dem, prjdem, utmprj)))
        # grab the folde rname
        folder = os.path.split(toa)[0]
        # print to the user one nice line for each successful dir
        print 'folder {}, filenames {}'.format(folder, mylist)

def main():
    print 'starting the script'
    # this is where the input goes
    indir = sys.argv[1]
    mode = sys.argv[2] # arc or noarc
    if mode == 'arc':
        try:
            import arcpy
            runArc(indir)
        except ImportError as IE:
            print IE
            runNoArc(indir)
    else:
        runNoArc(indir)
    print 'all done'

if __name__ == '__main__':
    main()
