# ambiLeap
Control frame for 3D-audio-system localisation data using LEAP Motion and IanniX.

## Leap Motion
```leap2tuio.py``` reads data from the Leap Motion via Websocket and converts these into TUIO messages

Used [SDK](https://developer.leapmotion.com/legacy-v2).

### **Leap Motion TUIO IDs**
TUIO is a protocol based on Open Sound Control. Find the specifications [here](https://www.tuio.org/?specification).

### Left Hand

| Pointable | ID|
|:--- | :---|
| Palm | 1 |
| Thumb | 10| 
| Index Finger | 11| 
| Middle Finger | 12| 
| Ring Finger | 13| 
| Pinky | 14| 

### Right Hand
| Pointable | ID|
|:--- | :---|
| Palm | 2 |
| Thumb | 20| 
| Index Finger | 21| 
| Middle Finger | 22| 
| Ring Finger | 23| 
| Pinky | 24| 

## IanniX
[IanniX](https://www.iannix.org/en/) Is a graphical sequencer. ```iannix2tuio``` converts IanniX' OSC-messages to TUIO. Add your own IanniX-scores!


## Setup
**PROTECT YOUR EARS; KEEP VOLUMES LOW DURING SETUP!**

The ```setup.sh``` works on macOs only.

Adjust all Audio Inputs/Outputs and OSC configurations according to your needs.
The default setup aims at a one-computer-use.


**Manual Setup:**

### **Pure Data**
* open ```src/processor.pd```
* start DSP
* adjust volume faders
### **Leap Motion**
* connect the Leap Motion to the computer
* start the Leap Daemon (if not automatic) 
* run ```src/leap2tuio.py```
### **IanniX**
* open ```src/score/curves3d.iannix```
* run ```src/iannix2tuio.py```
* hit play
### **Max**
* open ```src/server.maxpat```
* start DSP


## Helicopter Patch
The helicopter patch is an example patch from Farnell's Designing Sound and can be found [here](http://aspress.co.uk/sd/practical25.html).

