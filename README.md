# Ip Updater
## A python script that helps with linux servers without static ips

## Why:
The script was made mostly for personal use, to run inside of a laptop running as a **server** in my home, which doesn't have a static ip and therefore caused trouble when the ip changed and my ssh_files and other future uses would break.

## How it works
The script runs differently if set to Slave or Host:
- Constantly(inside of a GNU screen) if set to **Slave**
- Once(Unless otherwise specified) if set to **Host**

### Setup
1. Create a github gist with an ip.txt file inside of it (recommended to be secret)
2. Clone the repo and customize the settins in the *settings.conf* file(see section below)
3. Setup the script to run at startup, or for every session(.bashrc, .zshrc etc..)
###### Note: THe script will not check if a screen is already been made and will end up running more times if not setup correctly, see "My Use Case" section below

### Configuration file
Inside of the `[DEFAULT]` section are stored configs for the "fetching" part of the script.
- `machine_type = Slave`: Either Slave or Host, defines the behaviour of the script
- `slave_run_once = true`: Either true or false, if true the script will exit once the slave gets the ip and updates the files(see below), else it will keep running
- `host_interval = 3600`: Timeout in seconds, the script sleeps for this amount of time and then restarts
- `gist_link`: The link of the gist created in the Setup section
- `files`: The number of files to update(see below)

### Modes
The screen can run in either Host or Slave mode
#### Slave Mode
The Slave mode clones the repository, reads the ip.txt file and is then able to modify some files as to add the new ip
##### How to add slave files
1. Add a new section that starts with file_slave_ and then an integer
2. Add the file argument for the path and contents for the text, "{{{IP}}}" will be replaced with the IP from the gist
###### Notes:
Contents can't have multiple lines.
Example:
```conf
[slave_file_1]
file=path/to/text/file/to/modify
contents=Example Text
    Even with tabs or spaces the contents will be on the same line for now
```
###### NOTE: make sure "files" in the DEFAULT section is set to the number of files to modify

#### Host Mode
The Host mode instead uses *curl* to get the current ip, writes the *ip.txt* file and pushes the gist

### My Setup
I currently have the script running as slave in my server and ad a host inside my laptop for 2 scripts that let me ssh into it and another pc on my network
#### Slave/Server:
The server uses zsh, but the syntax is the same as bash.
In the session rc file(.zshrc, .bashrc) i have this code:
```bash
if ! screen -list | grep -q "screen_name"; then
    screen -dmS screen_name bash -c "cd path/to/script/folder; python main.py"
    echo "making the screen"
else
    echo "ip_updater already on"
fi
```
The script allows me to run multiple sessions without creating more times the same screen and running the script more than once
#### Host/Laptop:
Inside my laptop i just setup `slave_run_once = true`(default value) and added it to my .zshrc so whenever i open a new session any file i want is up to date

#### TO-DO:
- Add compatibility with also Windows and other OSes
- Remove need for GNU screen (with threading and deamons maybe)
- Add multiline support

#### Dependencies:

Dependency | Proprety
--|--
OS | Linux / MacOS
GNU Screen | Any Version
Git | Any Version
curl | Any Version