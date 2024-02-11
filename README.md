# Snare Assist

## Getting source

`git clone --recurse-submodules git@github.com:ghost-squadron/snare-assist.git`

or with https:

`git clone --recurse-submodules https://github.com/ghost-squadron/snare-assist.git`

## Installing requiremnts

It is always recommended to install packages inside a virtual environment as to not pollute your host machine:

`python -m venv venv`

Activate your new virtual environment:

`source venv/bin/activate`

Lastly install all requirements into the environment:

`pip install -r requirements.txt`

# Running

Remember to always activate the virtual environment first.

`python app.py`

# Using the program

The program works by using the `/showlocation` command which copies your current location into your clipboard.
**The first key you press after the program starts will be used as a macro key to do this.**
This means that every time you press this key the program will automatically write this command into chat.
This takes about 100-200ms during which you lose all control (as you are typing).
This is why the script does not automatically do this for you.
Naturally, don't use your keyboard while the macro is running.

To "activate" a route copy the route outputted by Calypso with the `/snare` command (the second line from the top, on the form `Source -> Destination`) and press F11.
This key can be changed by editing the `ROUTE_KEY` constant at the top of `app.py`.

The route instructions are similar to Calypso so remember to orient yourself with the top of your ship facing Stanton North and looking towards your destination (OM-1s point Stanton North and OM-2s point Stanton South).

# Known bugs

Calculating the route takes a bit so if you spam the macro key you'll start getting weird behaviour - should probably implement a guard/mutex.
