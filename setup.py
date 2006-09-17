from distutils.core import setup
import glob
import py2exe

setup(
        console=["TestAnimal.py"],windows=["TestAnimal.py"],
        data_files=[("media",
                    ["media/world.png","media/map.txt","media/tiles.bmp","media/light.gif","media/normal.gif","media/freesansbold.ttf"]),]
    )

