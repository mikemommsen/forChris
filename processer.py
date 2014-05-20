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
    strextent = ' '.join(map(str, [extent.XMin, extent.YMin, extent.XMax, extent.YMax]))
    arcpy.ProjectRaster_management(indem, prjdem, spref, "NEAREST", "30")
    arcpy.Clip_management(inDem, strextent, utmprj)
    # delete the projected dem
    arcpy.Delete_management(prjdem)
    # delete the original dem
    arcpy.Delete_management(dem)

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

def findFilePairs(indir):
    """takes a directory"""
    processqueue = []
    for x in os.listdir(indir):
        folder = os.path.join(indir, x)
        # make sure they all are dirs
        if os.path.isdir(folder):
            pathlist = os.listdir(folder)
            toa = findfile(pathlist, indir, 'toa')
            dem = findfile(pathlist, indir, 'elev')
            if toa and dem:
                processqueue.append((toa, dem))
            for subfolder in (x for x in pathlist if os.path.isdir(os.path.join(folder, x))):
                processqueue += findFilePairs(os.path.join(folder, subfolder))
    return processqueue
    
def run(indir)
    # loop through each filePair
    for toa, dem in findFilePairs(indir):
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
