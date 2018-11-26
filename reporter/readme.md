## Raven Script

### Run on startup

In order to start direct_mqtt_run.py on startup, follow these steps:

1. Copy ravenscript.sh to `/etc/init.d`.
2. Edit `/etc/rc.local` to add:
```bash
sudo /etc/init.d/ravenscript.sh >> /home/pi/ravenstartuplog.txt &
```
3. Save and reboot. `sudo reboot`

Upon reboot, verify that ravenscript.sh is running using
```bash
sudo tmux ls
```
A session named `ravensession` should appear once internet connectivity is available.

`/home/pi/ravenstartuplog.txt` contains the output from ravenscript.sh.