MC-Labyrinth
============

*a 3D Minecraft maze generator.*

I used a maze-generation algorithm to generate a maze with rooms
arranged in a 8x8x8 grid.  The algorithm is tuned to prefer connecting
rooms horizontally rather than verically.  Between any two rooms in
the maze, there is exactly one path.  

Randomly scattered around the maze are monster spawners and chests.
As you move down the maze from the entrance on the top level to lower
levels, you'll find better loot in the chests.

You can't cheat in this maze by knocking down the walls, since they
are all reinforced with bedrock. 

To try this out, you'll have to have some way to enter over ten
thousand commands to your minecraft server.  Here's how I do this on
my Linux server (Let's try this out first on a new world first):

0.  In the following commands:

    -   `$JAR_DIR` is wherever `minecraft_server.jar` can be found.
    -   `$SERVER_DIR` is wherever you want to keep the world files.
    -   `$LABYRINTH_DIR` is this repository.

1.  Clone this repository

        git clone https://github.com/HalCanary/mc-labyrinth.git
        cd mc-labyrinth
        LABYRINTH_DIR="$(pwd)"

2.  [Download `minecraft_server.jar`](https://minecraft.net/download).
    Install it somewhere:

        mkdir -p "$JAR_DIR"
        mv ~/Dowloads/minecraft_server.jar "$JAR_DIR"

3.  Create a directory for a new world, and create a server-start
    script:

        mkdir "$SERVER_DIR"
        cd "$SERVER_DIR"
        "$LABYRINTH_DIR/generate_server_script.sh" \
            "$JAR_DIR/minecraft_server.jar"

4.  Start the minecraft server inside a GNU Screen session.
    It is important that the session be called 'minecraft'.

        screen -dmS minecraft "$SERVER_DIR/start_server"

5.  Log into this server with the Minecraft client. (This will force
    the server to load of chunk).

6.  Execute the labyrinth program and pipe tyhe output into the
    Minecraft server:

        "$LABYRINTH_DIR/labyrinth.py" | "$LABYRINTH_DIR/talk.py"

7.  The server can be stopped at any time by executing:

        screen -S minecraft -X stuff "\003"