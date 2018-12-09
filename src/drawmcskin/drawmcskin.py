import sys
import os
from collections import namedtuple
import argparse

import cv2
import numpy


HERE = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_FNAME = "mcskintemplate.png"
BLANK_SKIN = os.path.join(HERE, "skin.png")
PIXEL_WIDTH = 16

Marker = namedtuple("Marker", ["id", "x", "y"])
SkinPart = namedtuple("SkinPart", ["name", "sx", "sy", "tx", "ty", "w", "h"])


PARTS = [
    SkinPart(name="head-front",       sx=8,  sy=8,  tx=10, ty=6,  w=8, h=8),
    SkinPart(name="head-left",        sx=16, sy=8,  tx=24, ty=6,  w=8, h=8),
    SkinPart(name="head-back",        sx=24, sy=8,  tx=38, ty=6,  w=8, h=8),
    SkinPart(name="head-right",       sx=0,  sy=8,  tx=52, ty=6,  w=8, h=8),
    SkinPart(name="head-top",         sx=8,  sy=0,  tx=52, ty=16, w=8, h=8),
    SkinPart(name="head-bottom",      sx=16, sy=0,  tx=62, ty=6,  w=8, h=8),

    SkinPart(name="arm-left-front",   sx=36, sy=52, tx=18, ty=14, w=4, h=12),
    SkinPart(name="arm-left-back",    sx=44, sy=52, tx=34, ty=14, w=4, h=12),
    SkinPart(name="arm-left-top",     sx=36, sy=48, tx=21, ty=42, w=4, h=4),
    SkinPart(name="arm-left-bottom",  sx=40, sy=48, tx=6,  ty=42, w=4, h=4),
    SkinPart(name="arm-left-ins",     sx=32, sy=52, tx=50, ty=34, w=4, h=12),
    SkinPart(name="arm-left-out",     sx=40, sy=52, tx=26, ty=14, w=4, h=12),

    SkinPart(name="arm-right-front",  sx=44, sy=20, tx=6,  ty=14, w=4, h=12),
    SkinPart(name="arm-right-back",   sx=52, sy=20, tx=46, ty=14, w=4, h=12),
    SkinPart(name="arm-right-top",    sx=44, sy=16, tx=21, ty=42, w=4, h=4),
    SkinPart(name="arm-right-bottom", sx=48, sy=16, tx=6,  ty=42, w=4, h=4),
    SkinPart(name="arm-right-ins",    sx=48, sy=20, tx=50, ty=34, w=4, h=12),
    SkinPart(name="arm-right-out",    sx=40, sy=20, tx=26, ty=14, w=4, h=12),

    SkinPart(name="torso-front",      sx=20, sy=20, tx=10, ty=14, w=8, h=12),
    SkinPart(name="torso-back",       sx=32, sy=20, tx=38, ty=14, w=8, h=12),
    SkinPart(name="torso-left",       sx=28, sy=20, tx=60, ty=34, w=4, h=12),
    SkinPart(name="torso-right",      sx=16, sy=20, tx=65, ty=34, w=4, h=12),
    SkinPart(name="torso-top",        sx=20, sy=16, tx=29, ty=42, w=8, h=4),
    SkinPart(name="torso-bottom",     sx=28, sy=16, tx=38, ty=42, w=8, h=4),

    SkinPart(name="leg-left-front",   sx=20, sy=52, tx=14, ty=26, w=4, h=12),
    SkinPart(name="leg-left-back",    sx=28, sy=52, tx=38, ty=26, w=4, h=12),
    SkinPart(name="leg-left-top",     sx=20, sy=48, tx=16, ty=42, w=4, h=4),
    SkinPart(name="leg-left-bottom",  sx=24, sy=48, tx=11, ty=42, w=4, h=4),
    SkinPart(name="leg-left-ins",     sx=16, sy=52, tx=55, ty=34, w=4, h=12),
    SkinPart(name="leg-left-out",     sx=24, sy=52, tx=26, ty=26, w=4, h=12),

    SkinPart(name="leg-right-front",  sx=4,  sy=20, tx=10, ty=26, w=4, h=12),
    SkinPart(name="leg-right-back",   sx=12, sy=20, tx=42, ty=26, w=4, h=12),
    SkinPart(name="leg-right-top",    sx=4,  sy=16, tx=16, ty=42, w=4, h=4),
    SkinPart(name="leg-right-bottom", sx=8,  sy=16, tx=11, ty=42, w=4, h=4),
    SkinPart(name="leg-right-ins",    sx=8,  sy=20, tx=55, ty=34, w=4, h=12),
    SkinPart(name="leg-right-out",    sx=0,  sy=20, tx=26, ty=26, w=4, h=12),
]

MARKERS = [
    Marker(1, 1, 1),
    Marker(2, 1, 48),
    Marker(3, 72, 1),
    Marker(4, 72, 48),
    Marker(5, 33, 30),
    Marker(6, 36, 1),
    Marker(7, 36, 48),
    Marker(8, 62, 16),
    Marker(9, 1, 24),
]

# Template drawing

def tl(px):
    return px * PIXEL_WIDTH

def draw_part(img, part):
    outlinecolor = (128, 128, 128)
    gridcolor = (220, 220, 220)

    # Draw the pixel grid
    for x in range(1, part.w):
        gp1 = (tl(part.tx + x), tl(part.ty))
        gp2 = (tl(part.tx + x), tl(part.ty + part.h))
        cv2.line(img, gp1, gp2, gridcolor)

    for y in range(1, part.h):
        gp1 = (tl(part.tx), tl(part.ty + y))
        gp2 = (tl(part.tx + part.w), tl(part.ty + y))
        cv2.line(img, gp1, gp2, gridcolor)

    # Draw the outline
    p1 = (tl(part.tx), tl(part.ty))
    p2 = (tl(part.tx + part.w), tl(part.ty + part.h))
    cv2.rectangle(img, p1, p2, outlinecolor)


def draw_markers(img):
    adict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    mw = PIXEL_WIDTH * 2
    for marker in MARKERS:
        markerimg = cv2.aruco.drawMarker(adict, marker.id, mw)
        # Apply
        colormarker = cv2.merge((markerimg, markerimg, markerimg))
        px = marker.x * PIXEL_WIDTH
        py = marker.y * PIXEL_WIDTH
        img[py:py+mw,px:px+mw] = colormarker


def find_template_dims():
    twidth = tl(max(p.tx + p.w for p in PARTS))
    theight = tl(max(p.ty + p.h for p in PARTS))

    mwidth = tl(max(m.x + 3 for m in MARKERS))
    mheight = tl(max(m.y + 3 for m in MARKERS))
    return max(twidth, mwidth), max(theight, mheight)


def draw_template(args):
    width, height = find_template_dims()
    templateimg = numpy.zeros((height, width, 3), numpy.uint8)
    # Make it white
    templateimg[:,:] = (255, 255, 255)

    for part in PARTS:
        draw_part(templateimg, part)

    draw_markers(templateimg)

    cv2.imwrite(args.output, templateimg)
    print(f"Template image is written to '{args.output}'")

# Part detection

def detect_markers(img):
    adict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, adict)

    markermap = {}
    for cor, mid in zip(corners, ids):
        markermap[mid[0]] = cor[0][0]

    return markermap


def sorted_points(markermap):
    return [p for pid, p in sorted(markermap.items())]


def warp_input(img, img_markermap, tpl_markermap, shape):
    img_points = sorted_points(img_markermap)
    tpl_points = sorted_points(tpl_markermap)
    homo, status = cv2.findHomography(numpy.array(img_points),
                                      numpy.array(tpl_points))

    warped = cv2.warpPerspective(img, homo, shape);
    return warped

def detect_parts(templateimg, inputimg):
    template_markermap = detect_markers(templateimg)
    input_markermap = detect_markers(inputimg)
    height, width, channels = templateimg.shape
    normalized_img = warp_input(inputimg, input_markermap, template_markermap,
                                (width, height))


    detected = {}
    for part in PARTS:
        p1 = tl(part.tx), tl(part.ty)
        p2 = tl(part.tx + part.w), tl(part.ty + part.h)

        # Cut the part
        partimg = normalized_img[p1[1]:p2[1], p1[0]:p2[0]]

        detected[part] = p1, p2, partimg
        cv2.rectangle(normalized_img, p1, p2, (0, 255, 0))

    # cv2.imshow("Warped", normalized_img)
    return detected


def map_parts_to_skin(detected_parts):
    skin_alpha = cv2.imread(BLANK_SKIN, cv2.IMREAD_UNCHANGED)
    alpha = skin_alpha[:,:,3]
    skin = skin_alpha[:,:,:3]

    for part, (p1, p2, partimg) in detected_parts.items():
        resized = cv2.resize(partimg, (part.w, part.h),
                             interpolation=cv2.INTER_AREA)
        skin[part.sy:part.sy+part.h, part.sx:part.sx+part.w] = resized

    # Recombine with alpha channel
    rc, gc, bc = cv2.split(skin)
    skin_alpha = cv2.merge((rc, gc, bc, alpha))
    return skin_alpha

def scan_template(args):
    fname = args.drawing
    templateimg = cv2.imread(args.template)
    inputimg = cv2.imread(fname)
    parts = detect_parts(templateimg, inputimg)
    skinimg = map_parts_to_skin(parts)
    cv2.imwrite(args.skin, skinimg)
    print(f"Skin is written to '{args.skin}'.")


def make_args_parser():
    parser = argparse.ArgumentParser(
        description='Tool to convert a drawing to a Minecraft skin.')
    subparsers = parser.add_subparsers(title="action")

    # convert
    parser_template = subparsers.add_parser("template",
                                           help="Generate a skin template")

    parser_template.add_argument("output",
                                 help="Name for a template file (PNG)")
    parser_template.set_defaults(func=draw_template)

    # list-plugins
    parser_scan = subparsers.add_parser("scan",
                                        help="Scan image")
    parser_scan.add_argument("template",
                             help=("Filename of template that was used "
                                   "for drawing"))
    parser_scan.add_argument("drawing", help="Filename of a drawing")
    parser_scan.add_argument("skin", help="Filename of a skin to create")
    parser_scan.set_defaults(func=scan_template)

    return parser


def main():
    print("Draw Minecraft Skin!")

    parser = make_args_parser()
    args = parser.parse_args(sys.argv[1:])

    if not hasattr(args, "func"):
        parser.print_usage()
        parser.exit(1)

    return args.func(args)

    return


if __name__ == '__main__':
    main()