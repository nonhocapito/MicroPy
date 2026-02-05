# MicroPy 1.4

A complete optical microscope manager. Use your smartphone to view live microscope images, take measurements, and capture still images with scale and units.

<img width="600" height="600" alt="logo" src="https://github.com/user-attachments/assets/11c5e9a5-1f57-4790-9b5d-4528b6d0da2c" />

## Requirements

First, you'll need a light microscope and an Android smartphone. You'll also need a smartphone stand to attach to the microscope. If you don't have one, you can find one on Amazon or 3D print one.

Download the repository and install the dependencies (`requirements.txt`) in your local folder (virtual environment recommended). Install the IP Webcam app on your smartphone and start the IP server. For MicroPy to work, both your smartphone and your computer must be connected to the same Wi-Fi network, even without internet access.

Launch the script with the command
```
python3 main.py
```
and entering the IP address displayed in the app once asked. The IP address is saved in memory and the script will attempt to use it on subsequent runs if it's still available (but it usually changes).

<img width="400" height="400" alt="calibrazione_05-02-2026_095950" src="https://github.com/user-attachments/assets/dd0e8a79-2f72-4415-88cc-aabfd890168d" />

## Calibration

To measure a distance correctly, you must first calibrate your microscope. The best way to calibrate is to use a calibration slide (you can buy it cheaply on Amazon). Observe the calibration slide with a lens, press the corresponding button (i.e. `1` for the objective 4x, `2` for the 10x etc.) and activate the calibration by pressing `K`. Click with the mouse on two points corresponding to the distance indicated in the terminal, and you're done. Repeat the same operation for all other lenses.

It's not necessary to repeat the calibration unless you change your smartphone; the program automatically saves it and reuses it each time.

Once you've calibrated and changed the objective, the scale bar will update automatically. Just remember to change the objective in MicroPy when you physically change the objective on the microscope!

## List of commands

The various functions of MicroPy can be activated simply by pressing the corresponding keys on the keyboard.

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
