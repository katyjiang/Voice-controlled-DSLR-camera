import os
from sh import gphoto2 as gp
from time import sleep
from datetime import datetime
import signal, os, subprocess
from word2number import w2n 

moduleName = "takeTimeLapse"

commandWords = ["take","time","lapse"]

clearCommand = ["--folder", "/store_00010001/DCIM/100NCD90",\
                "-R", "--delete-all-files"]

downloadCommand = ["--get-all-files"]

shot_date = datetime.now().strftime("%Y-%m-%d")

folder_name = shot_date + "TimeLapse"

save_location = "/home/pi/projects/raspi_dslr/gptest/images/" + folder_name

def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'],stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

def createSaveFolder():
    try:
        os.makedirs(save_location)
        print("New TimeLapse folder created.")
    except:
        print("Folder exisited.")
    os.chdir(save_location)

def execute(command):
    sentence = command
    res = [i for i in sentence.split()] 
    print(sentence)
    killgphoto2Process()
    # set config of the camera
    os.system("gphoto2 --set-config flashmode=0 \
                --set-config imagesize=2 \
                --set-config afbeep=1 \
                --set-config af-area-illumination=1 \
                --set-config autofocus=1")
    
    createSaveFolder()

    # default frames number and interval
    frames = 3
    interval = 1
    print(res)
    if res[len(res)-2]=="interval" :
        interval= w2n.word_to_num(res[len(res)-1])
    if res[len(res)-4]=="frames" :
        frames= w2n.word_to_num(res[len(res)-3])
    # capture images with indicate frames and interval
    cc="gphoto2 -F "+str(frames)+" -I "+str(interval)+" --capture-image-and-download"
    os.system(cc)
    gp(clearCommand)

    # find the first picture 
    os.system("cd "+save_location)
    proc = subprocess.Popen(["ls -t1|tail -n -1"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    startnum=str(out)
    
    # convert all the photo from the start picture to the end into video
    os.system("ffmpeg -y -f image2 -start_number " + startnum[6:10] +" -i " + save_location + "/DSC_%4d.JPG -vcodec libx264 -pix_fmt yuv420p "+ save_location+ "/"+folder_name+".mp4")

    print("TimeLapse capture")

