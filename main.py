# Developed by Jasper Tresidder 2022/09/17
# This is a tkinter interface to show all the videos stored on the reolink's SD card, or on custom stored days.


import reolinkapi
import os
import tkinter as tk
from tkinter import BOTH, END, LEFT
import datetime
from functools import partial
from datetime import timedelta
import urllib.request
from tqdm import tqdm
import cv2

# if you don't know the ip address of the reolink camera, look on your routers wired clients on http://192.168.1.1/
# reolinkapi.Camera("IP ADDRESS", "username", "Password")
cam = reolinkapi.Camera("192.168.X.XXX", "Username", "Password")
outpath = '/days' # location of whole day saves
clip_path = '/clips' # location of certain clips saves

def change_clip_mode():
    global clip_mode
    clip_mode = not clip_mode
    if button1["fg"] == "white":
        button1["fg"] = "red"
    else:
        button1["fg"] = "white"

def download_day(date):
    foldername = str(date[0]).zfill(4) + '-' + str(date[1]).zfill(2) + '-' + str(date[2]).zfill(2)
    motions = cam.get_motion_files( datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 0, 0, 1,000000),datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 23, 59, 59,000000), streamtype='main')
    dl_dir = outpath + '/' + foldername
    if foldername not in os.listdir(outpath):
        os.mkdir(dl_dir)
    import tqdm
    for i in tqdm.tqdm(range(len(motions)), desc='Downloading files: '):
        name = motions[i]['start'].strftime("%H-%M-%S")
        files_in_dic = os.listdir(dl_dir)
        if name+'.mp4' not in files_in_dic:
            print(name + '.mp4 Downloading' )
            # print(i)
            fname = motions[i]['filename']
            urllib.request.urlretrieve('http://192.168.1.103/cgi-bin/api.cgi?cmd=Download&source='+fname+'&output='+fname+'&token=' + str(cam.token), dl_dir + '/' + name + '.mp4')


def open_video_rtmp(file):
    global clip_mode
    if clip_mode:
        outname = t1.get("1.0", 'end-1c')
        if len(outname) > 0 and '.mp4' not in outname and ' ' not in outname:
            print(outname)
            urllib.request.urlretrieve('http://192.168.1.103/cgi-bin/api.cgi?cmd=Download&source=' + file + '&output=' + file + '&token=' + str(cam.token), clip_path + '/' + outname + '.mp4')
        else:
            print('Enter Valid Filename')
        t1.delete('1.0', END)
    else:
        os.system('vlc --prefetch-buffer-size 50000 --prefetch-seek-threshold 1000000 "rtmp://192.168.1.103/vod/' + file + '?&channel=0&stream=0&user=admin&password=KdsqzpN8Fe3D"')


def open_video_mp4(file):
    global clip_mode
    if clip_mode:
        outname = t1.get("1.0",'end-1c')
        if len(outname) > 0 and '.mp4' not in outname and ' ' not in outname:
            os.system('cp -v ' + file + ' ' + clip_path + '/' + outname + '.mp4')
        else:
            print('Enter Valid Filename')
        t1.delete('1.0', END)
    else:
        os.system('vlc --rc-show-pos --adaptive-maxbuffer 2000 --prefetch-read-size 10000000 ' + file)


def duration_and_framecount(filename):
    video = cv2.VideoCapture(filename)
    duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    return duration, frame_count

def compare_mp4_timestamp(first, last):
    return os.stat(first).st_mtime > os.stat(last).st_mtime


clip_mode = False
year = input('Year: ')
month = input('Month: ')
day = input('Day: ')

root = tk.Tk()

root.title('CCTV Archive: '+ str(day.zfill(2)) + '/' + str(month.zfill(2)) + '/' + str(year))
v = tk.StringVar()
tk.Button(root, text='LIVE', command=partial(open_video_mp4, 'rtsp://admin:KdsqzpN8Fe3D@192.168.1.103:554//h264Preview_01_main')).grid(row=0, column=25)
date = [year, month, day, 0, 0, 1,000000]
tk.Button(root, text='Download Day', command=partial(download_day, date)).grid(row=1, column=25)
button1 = tk.Button(root, text='Save clip', command=change_clip_mode, state=tk.NORMAL)
button1.grid(row=2, column=25)
button1["fg"] = "white"
t1 = tk.Text(root,  height=2, width=12)
t1.grid(row=3, column=25)
hasData = False
motions = cam.get_motion_files(datetime.datetime(int(year), int(month), int(day), 0, 0, 1, 000000),
                                   datetime.datetime(int(year), int(month), int(day), 23, 59, 59, 000000),
                                   streamtype='main')

foldername = str(year).zfill(4) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
dl_dir = outpath + '/' + foldername
rowtk = 1
coltk = 0
prev_coltk = 0
folder = True
files_in_dic = []
time_in_hour = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
num_entries = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
try:
    files_in_dic = sorted(os.listdir(dl_dir))
    last_entry = files_in_dic[len(files_in_dic)-1]
    stl_entry = files_in_dic[len(files_in_dic)-2]
    first_entry = files_in_dic[0]
    # The second to last entry could also be at the start if 23:00-00:00 both sides.
    if compare_mp4_timestamp(dl_dir + '/' + first_entry, dl_dir + '/' + last_entry):
        removed_element = files_in_dic.pop(len(files_in_dic)-1)
        files_in_dic.insert(0, removed_element)
    if compare_mp4_timestamp(dl_dir + '/' + first_entry, dl_dir + '/' + stl_entry):
        removed_element = files_in_dic.pop(len(files_in_dic)-2)
        files_in_dic.insert(0, removed_element)
except:
    folder = False

files_seen = []

if folder:
    for i in tqdm(range(len(files_in_dic)), desc='Collecting video data: '):
        name = files_in_dic[i][0:8]
        coltk = int(name[0:2])
        duration_sec = duration_and_framecount(dl_dir + '/' + files_in_dic[i])[1] / 30
        if coltk == 23:
            if int(name[3:5])*60 + int(name[6:8]) + duration_sec > 3600:
                if compare_mp4_timestamp(dl_dir + '/' + first_entry, dl_dir + '/' + files_in_dic[i]):
                    coltk = 0

        time_in_hour[coltk] += duration_sec
        files_seen.append(files_in_dic[i])
        duration = str(timedelta(seconds=int(duration_sec)))[2:]
        num_entries[coltk] += 1
        rowtk = num_entries[coltk]


        tk.Button(root, text=name[0:2] + ':' + name[3:5] + ':' + name[6:8] + ' (' + duration + ')',
                      command=partial(open_video_mp4, outpath + '/' + foldername + '/' + name + '.mp4')).grid(row=rowtk,
                                                                                                              column=coltk)


for i in range(len(motions)):
    name = motions[i]['start'].strftime("%H-%M-%S")
    if name + '.mp4' not in files_seen:
        end = motions[i]['end'].strftime("%H-%M-%S")
        coltk = motions[i]['start'].hour

        duration = motions[i]['end'] - motions[i]['start']
        duration = duration.total_seconds()
        if motions[i]['end'].hour == 0:
            if coltk == 23:
                if motions[i]['start'].day < int(day) or int(day) == 1:
                    coltk = 0
        temp_d = duration
        time_in_hour[coltk] += duration
        num_entries[coltk] += 1
        duration = str(timedelta(seconds=int(duration)))[2:]

        if prev_coltk != coltk:
            prev_coltk = coltk
        rowtk = num_entries[coltk]

        fname = motions[i]['filename']
        tk.Button(root, text=name[0:2] + ':' + name[3:5] + ':' + name[6:8] + ' (' + duration + ')',command=partial(open_video_rtmp, fname)).grid(row=rowtk, column=coltk, sticky='N')

i = 0
for t in time_in_hour:
    if t > 0:
        timed = str(timedelta(seconds=int(t)))[2:]
        tk.Label(root, text=str(i).zfill(2) + ':00 (' + timed + ')').grid(column=i, row=0)
    i += 1

root.mainloop()
cam.logout()
