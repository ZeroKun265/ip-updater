import configparser
import subprocess
import datetime
import os
import time
import sys

config =  configparser.ConfigParser()
config.read("settings.conf")

CURRENT_IP = "000.000.000.000"
with open("gist/ip.txt", "r") as f:
        CURRENT_IP = f.read()
# Goes in the git repo, writes and pushes
def override_and_push(contents):
    open("gist/ip.txt", "w").write(contents)
    old = os.getcwd()
    os.chdir("gist")
    subprocess.check_output(["git", "add", "*"])
    subprocess.check_output(["git", "commit", "-m", str(datetime.datetime.now())])
    subprocess.check_output(["git", "push"])
    os.chdir(old)

# This function is ran on startup from all the non servers
def slave():
    # We update the current ip
    subprocess.check_output(["rm","-rf", "gist"])
    subprocess.check_output(["git", "clone", config["DEFAULT"]["gist_link"], "gist"])
    CURRENT_IP = open("gist/ip.txt", "r").read()
    # And for every file we rewrite it
    for i in range(1, int(config["DEFAULT"]["files"]) + 1):
        section = config[f"slave_file_{str(i)}"]
        with open(section["file"], "w") as f:
            f.write(section["contents"].replace("{{{IP}}}", CURRENT_IP))


# This is ran as a daemon on the headless server
def host():
    # We get our current ip
    ip = str(subprocess.check_output(["curl", "ifconfig.me"])).split("'")[1]
    # If it's the same as the one saved on the gist we stop
    if ip == open("gist/ip.txt", "r").read():
        return
    # If they're different we write the current ip to the file and push
    override_and_push(ip)
    CURRENT_IP = ip
    

    



def main():
    if config["DEFAULT"]["machine_type"] == "Slave":
        slave()
        if config["DEFAULT"]["slave_run_once"] == "true":
            sys.exit()
    elif config["DEFAULT"]["machine_type"] == "Host":
        host()
    with open("gist/ip.txt", "r") as f:
        CURRENT_IP = f.read()
    


if __name__ == '__main__':
    while True:
        main()
        time.sleep(int(config["DEFAULT"]["host_interval"]))