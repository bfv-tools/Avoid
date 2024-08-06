# BFV-Tools Avoid v0.1
This Python script watches Firestorm community servers and notifies you if/where suspicious players join.<br>
It features:<br>
- A list of all FireStorm servers and their current players
- A constantly updating log of suspicious players joining FireStorm servers
- A game overlay displaying flagged players

## For players:
- Download Python from [here](https://www.python.org/downloads/) and run the installer.
- Download the latest major release of Avoid from [here](https://github.com/bfv-tools/Avoid/archive/refs/tags/Major.zip)
- Find the downloaded zip file and extract it into a folder of your choice
- In that folder, open the file named "BFV_Avoid.py"
- In your Battlefield V video settings, switch window mode to Borderless
<br><br>
To edit the list of suspicious clans, just open Blacklist.json in any text editor and where it says "clans": ["FSS", "MGC"] add a comma before the last square bracket, and insert the clan tag you'd like to flag enclosed in quotes ".<br>
For suspicious players, just edit the part below that says      "players": ["Nixpeiler", "Chazisadad"] and do the same as with the clans except with the player(s) username(s).<br>
For example:<br>
{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"clans": ["FSS", "MGC", "KLR"],<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"players": ["Nixpeiler", "Chazisadad", "Aileronz"]<br>}

## For developers:
This script can be run on Python versions 3.10 or later. It is designed and tested on Windows, but most features should work cross-platform. It only relies on the standard library, pip packages are not required. The gui overlay can be toggled with a variable at the top of the script, and the player/clan blacklist is in another variable. Feel free to edit and redistribute this script, it is designed simply as an  EA anti-cheat friendly alternative to previous cheater checker tools that only relies on 1 external api, no interaction with the game itself. For the overlay to appear on top, BFV must be in windowed/borderless mode.