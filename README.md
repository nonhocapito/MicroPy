# MicroPy

A complete optical microscope manager. Use your smartphone to view live microscope images, take measurements, and capture still images with scale and units.

<img width="600" height="600" alt="logo" src="https://github.com/user-attachments/assets/11c5e9a5-1f57-4790-9b5d-4528b6d0da2c" />

## Requirements

First, you'll need a light microscope and an Android smartphone. You'll also need a smartphone stand to attach to the microscope. If you don't have one, you can find one on Amazon or 3D print one.

Download the repository and install the dependencies (`requirements.txt`) in your local folder (virtual environment recommended). Install the IP Webcam app on your smartphone and start the IP server.

Launch the script with the command
```
python3 main.py
```
and entering the IP address displayed in the app once asked. The IP address is saved in memory and the script will attempt to use it on subsequent runs if it's still available (but it usually changes).

## Commands and functions

To measure a distance correctly, you must first calibrate your microscope. You can calibrate the current objective (selectable with the `1`, `2`, `3`, and `4` keys) simply by pressing `K`.

```
KEY    ACTION
------------------------------------------
R      Rotate
W      Region of interest ON/OFF
G      Grid ON/OFF
M      Measurement mode
1      Switch to 4x objective (red)
2      Switch to 20x objective (yellow)
3      Switch to 40x objective (blue)
4      Switch to 100x objective (gray)
K      Calibrate current objective
------------------------------------------
S      Save photo
Q      Exit
```
