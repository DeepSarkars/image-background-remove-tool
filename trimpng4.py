import sys
import glob
from PIL import Image, ImageOps
import os

def autocrop_image(image, border = 0):
    # Get the bounding box
    bbox = image.getbbox()

    # Crop the image to the contents of the bounding box
    image = image.crop(bbox)

    # Determine the width and height of the cropped image
    (width, height) = image.size

    # Add border
    width += border * 2
    height += border * 2
    
    # Create a new image object for the output image
    cropped_image = Image.new("RGBA", (width, height), (0,0,0,0))

    # Paste the cropped image onto the new image
    cropped_image.paste(image, (border, border))

    # Done!
    return cropped_image
    
if len(sys.argv) < 3:
    # Not enough arguments -- show usage information and exit
    print ("Usage: " + sys.argv[0] + " infile outfile [border]")
    exit(1)

# Get input and output file names
input_path = sys.argv[1]
destFolder = sys.argv[2]

# Check if border size was provided
if sys.argv[3]:
    border = int(sys.argv[3])
else:
    border = 0


#support for multi-directory
dir_list=os.listdir(input_path)
print(dir_list)
for folderName in dir_list:
    new_input=os.path.join(input_path,folderName+'/')
    new_output=os.path.join(destFolder,folderName+'/')
    folder = os.path.dirname(new_output)
    if folder != '':
      os.makedirs(folder, exist_ok=True)
    filePaths = glob.glob(new_input + "/*.png") #search for all png images in the folder
    print(folderName)
    for filePath in filePaths:
        # Open the input image
        image = Image.open(filePath)
        print (filePath, "Size:", image.size,end=" ")
        # Do the cropping
        image = autocrop_image(image, border)
        # Save the output image
        destFile=new_output+filePath.split('/')[-1]
        #resize the image
        (w,h) = image.size
        #wf,hf = w//336,h//336
        #f = hf if wf < hf else wf
        resize_im = image.resize((w,h))
        print ( "New Size:", resize_im.size)
        #for png
        resize_im.save(destFile)
        #for pbm
        bg2= Image.new('1', resize_im.size, (0))
        inverted_image = ImageOps.invert(resize_im.split()[-1])
        bg2.paste(inverted_image)
        bg2.save(destFile[:-3]+"pbm")
