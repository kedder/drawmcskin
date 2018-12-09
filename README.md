# Draw Minecraft Skin

This is a simple weekend project to help kids create their own minecraft skins.
Use this tool to generate the  template, print it out and draw the character on
it. Then take a photo of the drawing and feed it to the program. You'll get the
skin file that you can import into Minecraft.

## Installation

Clone the repo and then run:

```
$ make
$ ve/bin/activate
```

After this you should be able to run `drawmcskin` program:

```
$ drawmcskin --help
Draw Minecraft Skin!
usage: drawmcskin [-h] {template,scan} ...

Tool to convert a drawing to a Minecraft skin.

optional arguments:
  -h, --help       show this help message and exit

action:
  {template,scan}
    template       Generate a skin template
    scan           Scan image
```

## Usage

First, you need to generate and print the template:

```
$ drawmcskin template template.png
```

Print the resulting template.png, paint it and take a photo (or scan it). Make
sure all markers are clearly visible on the image. Once you have the image,
run:

```
$ drawmcskin scan template.png <your-picture.jpg> skin.png

```

The output file - `skin.png` is a minecraft skin you can upload to Minecraft.
Enjoy!
