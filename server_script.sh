#!/bin/sh
cd "/home/hal/mc-labyrinth"
exec java -Xmx1024M -Xms1024M -jar \
  "/home/hal/Programs/Minecraft/minecraft_server.jar" nogui
