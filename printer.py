#!/usr/bin/env python3
import argparse
import time

import webcolors 
from PIL import Image
from mcpi.minecraft import Minecraft

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4711
DELAY = 3 # secs

parser = argparse.ArgumentParser()
parser.add_argument('--ip', '-i', default=DEFAULT_HOST)
parser.add_argument('--port','-p', default=DEFAULT_PORT)
parser.add_argument('--image', required=True)
parser.add_argument('--resize', action="store_true")
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)


AVAIABLE_COLORS = [
    ('#ffffff', ('White',219)),
    ('#ffa500', ('Orange',220)),
    ('#ff00ff', ('Magenta',221)),
    ('#add8e6', ('Light Blue',222)),
    ('#ffff00', ('Yellow',223)),
    ('#008000', ('Ligh Green',224)),
    ('#ffc0cb', ('Pink',225)),
    ('#808080', ('Gray',226)),
    ('#d3d3d3', ('Light Gray',227)),
    ('#00ffff', ('Cyan',228)),
    ('#ce49e3', ('Pink',229)),
    ('#0000ff', ('Blue',230)),
    ('#2e250d', ('Brown',231)),
    ('#097d10', ('Green',232)),
    ('#ff0000', ('Red',233)),
    ('#000000', ('Black', 234)),
]


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in AVAIABLE_COLORS:
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    """Get closest colour with avaiables colour list"""
    return closest_colour(requested_colour)


def get_block(pixel):
    """ get specific block with given pixel"""
    color_name, block_id = get_colour_name(pixel)
    return block_id


def main():
    args = parser.parse_args()
    try:
        minecraft = Minecraft.create(args.ip, args.port)
    except ConnectionError:
        print("error: Could not connect to server %s:%s" % (args.ip, args.port))
        exit(1)

    print("Client connected to server %s:%s" % (args.ip, args.port))
    minecraft.postToChat("Client connected to server %s:%s" % (args.ip, args.port))
    try:
        image = Image.open(args.image).convert("RGB")
    except FileNotFoundError:
        print("error: image '%s' does not exists" % args.image)
        exit(1)
    if args.resize:
        if args.width == None or args.height == None:
            print("error: --width and --height are required while resizing...")
            exit(1)
        image = image.resize((args.width,args.height))
    width, height = image.size
    pixels = image.load()
    player_x, player_y, player_z = minecraft.player.getPos()
    i = 0
    for x in range(width):
        for y in range(height):
            pix = pixels[x, y]
            minecraft.setBlock(player_x+5,player_y+(height-y),player_z+(width-x), get_block(pix))
            i += 1
            if (i % 500) == 0:
                time.sleep(DELAY)


if __name__ == "__main__":
    main()
