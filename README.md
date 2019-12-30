A simple wrapper around phue.

1. add `HUE_BRIDGE_IP` env var to `~/.bashrc` or somewhere similar:


        export HUE_BRIDGE_IP="192.168.0.xxx"


2. run `pip3 install -r requirements.txt && python3 setup.py install`


3. control hue from command line like so:


        # turns lights on/off
        $ hue on 
        $ hue off
    
        # coarse brightness settings:
        $ hue bright
        $ hue dim
        $ hue dimmest
    
        # for more fine-grainedness, can set brightness manually:
        $ hue brightness [1-254] 


