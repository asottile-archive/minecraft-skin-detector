minecraft-skin-detector
=======================

A script to detect when a player changes their skin.

minecraft-skin-detector is intended to be set up as a cronjob

For example this is the line I would have in `crontab -e` if I wanted to stalk Notch and Dinnerbone's skin

```bash
# Note: The skin names are case sensitive because minecraft stores skins in a
# case sensitive fashion
# Note: this cron says to run daily at 0:00 (midnight)
0 0 * * * python /home/anthony/workspace/minecraft-skin-detector/minecraft_skin_detector.py Notch Dinnerbone
```
