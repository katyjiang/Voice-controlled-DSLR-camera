
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
from word2number import w2n 

moduleName = "takePhoto"

commandWords = ["take","photo"]

clearCommand = ["--folder", "/store_00010001/DCIM/100NCD90",\
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]

downloadCommand = ["--get-all-files"]

shot_date = datetime.now().strftime("%Y-%m-%d")

folder_name = shot_date

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
        print("New folder created.")
    except:
        print("Folder exisited.")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)

def execute(command):
    sentence = command
    res = [i for i in sentence.split()] 
    print(sentence)
    killgphoto2Process()
    gp(clearCommand)
    createSaveFolder()

    # if user set a timer
    if res[len(res)-1]=="seconds" :
        timeout = w2n.word_to_num(res[len(res)-2])
        sleep(timeout)
        
    captureImages()
    print("image capture")
   