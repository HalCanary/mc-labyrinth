#!/bin/sh
if [ -z "$1" ] || ! [ -f "$1" ]; then
    echo >&2
    echo "Usage:" >&2
    echo "  cd SERVER_DIR; $0 PATH_TO_MINECRAFT_SERVER.JAR" >&2
    echo >&2
    return 1
fi
set -C
if ! [ -f "eula.txt" ]; then
    echo eula=true > eula.txt
fi
for file in banned-players.json banned-ips.json ops.json whitelist.json; do
    if ! [ -f "$file" ]; then
        touch "$file"
    fi
done
SCRIPT=start_server
cat > "$SCRIPT" <<EOF
#!/bin/sh
cd "$(pwd)"
exec java -Xmx1024M -Xms1024M -jar \\
  "$(cd "$(dirname "$1")"; pwd)/$(basename "$1")" nogui
EOF
chmod +x "$SCRIPT"
echo created "$(pwd)/$SCRIPT"
