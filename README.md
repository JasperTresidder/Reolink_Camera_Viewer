# Reolink_Cam
A Python interface to view stored days on the camera, live footage, and saved clips. 


## Setup
Change the ip address, username and password in main.py  

Recreate the conda environment using the yml file and conda. 
Open up linux terminal, mac terminal, or windows CMD 
make sure you have conda installed.
```bash
conda env create -f environment.yml
conda activate Cam
python3 main.py
```
You may also have to install opencv or cv2 and VLC
```bash
pip install opencv-python
```
```
https://www.videolan.org/vlc/index.en_GB.html
```
To save clips, there is a text box just below 'Save Clip' to name your file.
enter a file name e.g. 'clip123', click on save clip and then the clip to save.

VLC media player is used to view live streams camera clips using vlc commands and rmtp address formats.
you can acsess your livestream using this command as a standalone viewer:
```bash 
vlc rtsp://admin:password@ip_address:554/h264Preview_01_main
```

## Preview
![Screenshot at 2022-09-17 11-14-31](https://user-images.githubusercontent.com/51917264/190851760-a9f68216-5a67-425f-94a4-f06e131fd4bc.png)

Have fun
> JT
