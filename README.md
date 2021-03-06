MC-Labyrinth
============

*a 3D Minecraft maze generator.*

**Contributions welcome and encouraged!**

Contents:

-   [Requirements](#requirements)
-   [The Labyrinth](#the_labyrinth)
-   [Try it](#try_it)
-   [Help!](#help)

![a room with up and down passages](http://i.imgur.com/dfQ5iYX.png)

![a dark corridor](http://i.imgur.com/ABAqCRN.png)

<span id="requirements"></span>

Requirements
------------

*   Minecraft & the Minecraft server
*   Python
*   Gnu Screen or some other way to pipe thousands of commands into the
    running server.

<span id="the_labyrinth"></span>

The Labyrinth
-------------

I used a maze-generation algorithm to generate a maze with rooms
arranged in a 8x8x8 grid.  The algorithm is tuned to prefer connecting
rooms horizontally rather than verically.  Between any two rooms in
the maze, there is exactly one path.  

Randomly scattered around the maze are monster spawners and chests.
As you move down the maze from the entrance on the top level to lower
levels, you'll find better loot in the chests.

You can't cheat in this maze by knocking down the walls, since they
are all reinforced with bedrock. 

<span id="try_it"></span>

Try it!
-------

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

6.  Execute the labyrinth program and pipe the output into the
    Minecraft server:

        "$LABYRINTH_DIR/labyrinth.py" | "$LABYRINTH_DIR/talk.py"

7.  The server can be stopped at any time by executing:

        screen -S minecraft -X stuff "\003"

<span id="help"></span>

Help!
-----

Dear Mojang,

Can we make this sort of workflow easier?  Ideas:

1.  A sever command `/executeprogram` that lets me execute any program
    from the console; that programs's output would be console input.

2.  A more complex API that also allows an external program to query
    the server ("What kind of block is located at X,Y,Z? Where is
    entity E? List the players within radius R of point X,Y,Z?")
    Maybe even use a database-style API?
