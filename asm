sudo as -32 -gstabs -o "$1".o "$1".s
sudo ld -melf_i386 -o "$1" "$1".o

