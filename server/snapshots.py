# stackoverflow links
#How to read Youtube live stream using opencv - https://stackoverflow.com/a/69878736/21097687

# import libraries
import cv2 
import os 
import imageio.v2 as imageio 
from vidgear.gears import CamGear

def generate_gif():
    # current directory path
    path = os.getcwd()

    imageFolder = os.fsencode(path)

    filenames = []

    for file in os.listdir(imageFolder):
        filename = os.fsdecode(file)
        if filename.endswith( ('.jpg', '.png', '.gif') ):
            filenames.append(filename)
 
    filenames.sort()
    images = list(map(lambda filename: imageio.imread(filename), filenames))

    imageio.mimsave(os.path.join('generatedGif.gif'), images, duration = 0.5) # modify duration as needed
 

def generate_img(url): 
    stream = CamGear(source=url, stream_mode = True, logging=True).start() # YouTube Video URL as input 
    
    # create a folder to save the snapshots
    dirname = 'generatedSnaps' 
    isExist = os.path.exists(dirname)
    if not isExist:
        os.mkdir(dirname)

    # locates/takes you to the folder containing snapshots  
    os.chdir(dirname) 
 
    x=1
    count=0
    skipFrames = 1000000 
    while True: 
        count+=1 
        if count%skipFrames : 
             continue

        frame = stream.read()

        if x > 30 :
            break

        if frame is None: 
            break  

        #saving images with below filenaming
        filename =r"shot"+str(x)+".png" 
        x += 1
        cv2.imwrite(os.path.join(os.getcwd(), filename.format(count)), frame) 
        
    cv2.destroyAllWindows() 
    stream.stop() 


generate_img('https://www.youtube.com/watch?v=RQA5RcIZlAM') 
generate_gif()
 
 
 