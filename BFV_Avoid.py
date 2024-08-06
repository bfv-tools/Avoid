gui_mode = True #This toggles the game overlay
#Game must be in borderless or windowed mode for this to work!

bfban_mode = True #This toggles auto minge detection
# Using the BFBan API, moderated by players

from json import loads
from urllib.request import urlopen, Request
from urllib.parse import quote
from time import sleep
from threading import Thread
from tkinter import Tk, Text, END

with open("Blacklist.json", "rt") as f:
    blacklist = loads(f.read())

#This script may miss servers if the total community
#server count is above 200! This is because the search
#caps at 200 items and the map filter is non-functional

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
#If this script stops working try updating the useragent
#https://www.useragents.me/ Anything popular should work

detected_minges = []
bfban_minges = []
log = []

def log_print(msg, colour="red"):
    print(msg)
    if len(log) >= 10:
        del log[0]
    log.append([msg + "\n", colour])

def quick_prefix(sv_prefix):
    match sv_prefix:
        case "[BoB] EU FireStorm discord.gg/BoB":
            return "BoB EU"
        case "[BoB] NA FireStorm discord.gg/BoB":
            return "BoB NA"
        case _:
            return sv_prefix
def detected(plr):
    for minge in detected_minges:
        if minge[0] == plr:
            return True
    return False

def check_bfban(plr_list):
    url_plr_list = ""
    for plr in plr_list:
        url_plr_list += plr + ","
    if url_plr_list[:-1] == ",":
        url_plr_list = url_plr_list[:len(url_plr_list) - 1]

    bfban_url = f"https://api.gametools.network/bfban/checkban?names={url_plr_list}"

    try:
        bfban_json = loads(urlopen(bfban_url).read())
        final_plr_list = []
        for plr in bfban_json["names"]:
            final_plr_list[plr] = plr["hacker"]
        print(final_plr_list)
        quit()
        return final_plr_list
    except:
        return "ERR"

def list_servers(sv_name=" ", sv_map=False):
    #The map filter seems to be broken on gametools, use filter_firestorm()
    sv_name = quote(sv_name)
    if sv_map == False:
        req_url = f"https://api.gametools.network/bfv/servers/?name={sv_name}&platform=pc&limit=200&region=all&lang=en-us"
    else:
        sv_map = quote(sv_map.encode())
        req_url = f"https://api.gametools.network/bfv/servers/?name={sv_name}&platform=pc&limit=200&region=all&map_filters={sv_map}&lang=en-us"
    try:
        req = Request(req_url)
        req.add_header("accept", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0")
        req = urlopen(req)
        req_data = req.read().decode()
        req_json = loads(req_data)
        if len(req_json["servers"]) < 1:
            return "NIL"
        else:
            return req_json["servers"]
    except Exception as exc:
        return "ERR - " + str(exc)

def list_players(sv_name):
    sv_name = quote(sv_name)
    req_url = f"https://api.gametools.network/bfv/players/?name={sv_name}"

    try:
        req = Request(req_url)
        req.add_header("accept", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0")
        req = urlopen(req)
        req_data = req.read().decode()
        req_json = loads(req_data)

        if "errors" in req_json:
            return "NIL - " + str(req_json["errors"])
        else:
            sv_teams = []
            for team in req_json["teams"]:
                sv_teams += team["players"]
            return sv_teams
        
    except Exception as exc:
        return "ERR - " + str(exc)

def filter_firestorm(sv_list):
    out_list = []
    for server in sv_list:
        if server["currentMap"] == "Halvøy":
            out_list.append(server)
    return out_list

def prettify_servers(sv_list, verbose=False):
    pretty_list = ""
    counter = 0
    for server in sv_list:
        player_list = ""
        counter += 1
        quick_sv_prefix = quick_prefix(server["prefix"])
        pretty_list += f"{counter}. {quick_sv_prefix}\n"
        if verbose == True:
            for player in list_players(server["prefix"]):
                if player["platoon"] != "":
                    player_list += f"   {player['name']} - {player['platoon']}\n"
                else:
                    player_list += f"   {player['name']}\n"
            pretty_list += player_list
    return pretty_list

def minge_detector(firestorm_only=True):
    print("\n--Started minge detector--\n")
    if gui_mode == True:
        gui_thread = Thread(target=update_gui)
        gui_thread.start()
    while True:
        plr_locations = []
        servers = list_servers()
        if firestorm_only == True:
            servers = filter_firestorm(servers)
        sv_players_bfban = []
        
        for server in servers:
            sv_players = list_players(server["prefix"])
            sv_name = quick_prefix(server["prefix"])
            for sv_player in sv_players:
                plr_locations.append([sv_player["name"], server["prefix"]])
                if sv_player["name"] in blacklist["players"]:
                    if not detected(sv_player["name"]):
                        detected_minges.append([sv_player["name"], server["prefix"]])
                        log_print(f"{sv_player['name']} - BLACKLIST - {sv_name}")
                elif sv_player["platoon"] in blacklist["clans"]:
                    if not detected(sv_player["name"]):
                        detected_minges.append([sv_player["name"], server["prefix"]])
                        log_print(f"{sv_player['name']} - CLAN {sv_player['platoon']} - {sv_name}")
                elif sv_player["name"] in bfban_minges and not detected(sv_player["name"]):
                    detected_minges.append([sv_player["name"], server["prefix"]])
                    log_print(f"{sv_player['name']} - BFBAN - {sv_name}")
                else:
                    sv_players_bfban.append(sv_player["name"])

            for bfban_plr in check_bfban(sv_players_bfban):
                if bfban_plr not in detected_minges:
                    bfban_minges.append(bfban_plr)
            sleep(5)
        
        sleep(10)

def update_gui():
    root = Tk()
    
    scrx = root.winfo_screenwidth()
    scry = root.winfo_screenheight()
    tk_size_x = round(scrx / 5)
    tk_size_y = round(scry / 5)
    tk_pos_x = round(scrx - tk_size_x)
    tk_pos_y = 0
    root.geometry(f"{tk_size_x}x{tk_size_y}+{tk_pos_x}+{tk_pos_y}")
    
    root.lift()
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.attributes("-alpha", 0.75)
    root.configure(background='black')

    last_log = []
    log_box = Text(root, bg="black", fg="red")
    log_box.pack()
    while True:
        root.update()
        if log != last_log:
            box_string = ""
            for ln in log:
                box_string += ln[0]
            log_box.delete(1.0, END)
            log_box.insert(END, box_string)
            

print(prettify_servers(filter_firestorm(list_servers()), True))
minge_detector()
