import arcpy
import os
import sys
CELLSIZE = 30

def describeToa(intoa):
    desc = arcpy.Describe(intoa)
    spref = desc.spatialReference
    extent = desc.extent
    imageWidth = desc.width
    imageHeight = desc.height
    return {'spref': spref, 'extent': (extent.XMin, extent.YMin, extent.XMax, extent.YMax)}

def reproject(indem, toaData):
    outdem = indem
    arcpy.ProjectRaster_management(indem, outdem, toaData['spref'])
    

def clipper(inDem, outDem toaData):
    arcpy.Clip_management(inDem, toaData['extent'], outDem)

    

intoa = r'C:\Users\libpub\Downloads\LE70400292003139EDC00\LE70400292003139EDC00_TIR.jpg'
a = describeToa(intoa)
print a['extent']

def findfile(inlist, text):
    goodfile = [x for x in inlist if os.path.splitext(x)[0][-len(text):] == text]
    if goodfile:
        if len(goodfile) == 1:
            return goodfile[0]
        else:
            print 'more that one', text, 'i will work on making this a better error'
    else:
        print 'couldnt find file', text, 'i will work on making this a real error that is handled better'

def run(indir):
    os.chdir(indir)
    folders = os.listdir(indir)
    folders = [folder for folder in folders if os.path.isdir(folder)]
    for folder in folders:
        files = os.listdir(folder)
        toa = findfile(files, 'toa')
        dem = findfile(files, 'elev')
        toaData = describeToa(toa)
        prjdem = reproject(dem, toaData)
        clipper(prjdem, outdem, toaData)

def main():
    indir = sys.argv[1]
    run(indir)

if __name__ == '__main__':
    main()
