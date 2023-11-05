
# WindowVipers

Introducing WindowVipers... A giant version of the retro 'snake' game, with the ability to be played on the side of a large tower block.

 
### Say What?
That's right, on a tower block! A DMX lighting fixture is placed in each window of the building, with all the lights on each floor then connected to an Art-Net node. Our app then controls gameplay and sends the right signals over Art-Net to make the game visible on the building.


## Recommended equipment

 - RGB DMX lighting fixtures (Set to 3 channel mode)
 - Art-Net node for each floor (Chauvet DMX-AN2)
 - Ethernet switch to connect each Art-Net node
 - Lots of DMX (XLR) cabling!


## Control

 - Via arrow keys on keyboard
 - NES USB/HID gamepad (may need to adjust USB vendor/device IDs)
 - Via TCP (i.e. Run snake.py elsewhere, and use controller_send.py to just send up/down/left/right controller commands)


## Usage

Install requirements with: `pip3 install -r requirements.txt`

Then run with: `python3 snake.py`