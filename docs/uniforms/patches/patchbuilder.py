# FRC 1721
# Script by Joe

import os
import yaml
import json
import string
import random
import logging

import numpy as np

from docutils.parsers.rst import directives

from sphinx.parsers import RSTParser
from docutils.frontend import OptionParser
from sphinx.util.docutils import SphinxDirective
from docutils.utils import new_document

from PIL import Image, ImageDraw, UnidentifiedImageError


def loadData():
    with open(f"patches.yaml", "r") as yamlFile:
        # Use yaml.safe_load to load the yaml into a dict
        patchdict = yaml.safe_load(yamlFile)

    return patchdict


def getPatch(patch, color, angle=0):
    """
    Returns a patch, in a color
    """

    patchMask = Image.open(patch)
    patchMask = patchMask.convert("RGBA")

    data = np.array(patchMask)
    red, green, blue, alpha = data.T

    mask_area = (red == 0) & (blue == 0) & (green == 0)  # Area where mask is black

    data[..., :-1][mask_area.T] = color  # Convert all mask to red
    newimage = Image.fromarray(data)
    newimage = newimage.rotate(angle)
    return newimage


def getColor(key):
    if key == "white":
        return (184, 184, 184)
    elif key == "red":
        return (130, 12, 12)
    elif key == "gold":
        return (204, 164, 61)
    elif key == "yellow":
        return (255, 255, 50)
    elif key == "purple":
        return (75, 0, 130)
    elif key == "black":
        return (0, 0, 0)
    else:
        logging.warning(f"Could not find color {key}")
        return (0, 255, 0)


def composite_half_patch(maskPath, lImage, lData, offset):
    # So messy, composite two images!

    if lData[1] != "none":
        lImage.alpha_composite(
            getPatch(
                f"{maskPath}/Chevron Mask.png",
                getColor(lData[1]),
                180,
            ),
            offset,
        )

    lImage.alpha_composite(
        getPatch(
            f"{maskPath}/HalfChevron Mask.png",
            getColor(lData[0]),
            180,
        ),
        offset,
    )

    return lImage


class tenurebuilder(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 3
    final_argument_whitespace = True
    option_spec = {
        "bars": directives.unchanged,
        "name": directives.unchanged,
        "draw": directives.unchanged,
    }

    def run(self):
        bars = json.loads(self.options.get("bars", "[]"))
        name = self.options.get("name", "")

        # The actual livery image!
        liveryImage = Image.new("RGBA", (510, 1020), color=(0, 0, 0, 0))

        # Paths
        genpath = "_build/patches"
        try:
            os.mkdir(genpath)
        except FileExistsError:
            pass
        maskPath = "uniforms/patches/masks"

        # Where the next patch should be drawn
        cursor = 0

        logging.info(f"Processing tenure bar {name}")
        for bar in bars:
            # Check if this is a normal bar or a double bar
            if type(bar) is not list:
                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/Tenure Bar.png",
                        getColor(bar),
                    ),
                    (0, cursor),
                )
            else:
                # If it is a list, its a double bar! Lets process it
                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/Tenure Bar.png",
                        getColor(bar[1]),
                    ),
                    (0, cursor),
                )
                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/Tenure Half Bar.png",
                        getColor(bar[0]),
                    ),
                    (0, cursor),
                )

            cursor = cursor + 130

        liveryImage = liveryImage.crop((0, 0, 510, cursor + 120))

        liveryImage.save(f"{genpath}/{name}-bar.png")

        if len(self.options.get("draw", "")) == 0:
            return self.parse_rst(
                f"""
.. figure:: ../{genpath}/{name}-bar.png
    :width: 125
    :alt: Auto Generated
        
    {' '.join(self.content)}
"""
            )
        else:
            return self.parse_rst(
                f"""
.. |{name}| image:: ../{genpath}/{name}-bar.png
    :width: 125
    :alt: Auto Generated
"""
            )

    # https://sammart.in/post/2021-05-10-external-data-sphinx-extension/
    def parse_rst(self, text):
        parser = RSTParser()
        parser.set_application(self.env.app)
        settings = OptionParser(
            defaults=self.env.settings,
            components=(RSTParser,),
            read_config_files=True,
        ).get_default_values()
        document = new_document("<rst-doc>", settings=settings)
        parser.parse(text, document)
        return document.children


class chevronbuilder(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 3
    final_argument_whitespace = True
    option_spec = {
        "chevrons": directives.unchanged,
        "patches": directives.unchanged,
        "tag": directives.unchanged,  # used for inline linking and stuff
    }

    def run(self):
        # Parse our inputs
        _chevrons = json.loads(self.options.get("chevrons", "[]"))  # Get raw
        _patches = json.loads(self.options.get("patches", "[]"))

        # Generate some randoms
        randomName = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=9)
        )

        # Paths
        genpath = "_build/patches"
        try:
            os.mkdir(genpath)
        except FileExistsError:
            pass
        maskPath = "uniforms/patches/masks"

        # Where the next patch should be drawn
        cursor = 0

        # The actual livery image!
        liveryImage = Image.new("RGBA", (510, 1020), color=(0, 0, 0, 0))

        # Place the top two chevrons if they exist
        if _chevrons[0] != "none":
            logging.info(f"Found super top chevron on {randomName}, {_chevrons[0]}")
            liveryImage.alpha_composite(
                getPatch(
                    f"{maskPath}/Rocker Mask.png",
                    getColor(_chevrons[0]),
                )
            )

            cursor = cursor + 112

        if _chevrons[1] != "none":
            logging.info(f"Found top chevron on {randomName}, {_chevrons[1]}")
            liveryImage.alpha_composite(
                getPatch(
                    f"{maskPath}/Rocker Mask.png",
                    getColor(_chevrons[1]),
                ),
                (0, cursor),
            )

            cursor = cursor + 120

        try:
            if len(_patches) == 0:
                # No subteam patches
                logging.info("No patches to apply")

                # Special exception for when theres also a top patch (because we need a little space)
                if _chevrons[1] != "none":
                    cursor = cursor + 120
            if len(_patches) == 1:
                # One subteam patch
                offset = (int(255 / 2), cursor)

                patchname = _patches[0][0]

                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/{patchname} Mask.png",
                        getColor(_patches[0][1]),
                    ),
                    offset,
                )

                cursor = cursor + 150
            if len(_patches) == 2:
                # Two subteam patches
                offset = (0, cursor + 90)

                patchname = _patches[0][0]

                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/{patchname} Mask.png",
                        getColor(_patches[0][1]),
                    ),
                    offset,
                )

                # New offset, new patch
                offset = (255, cursor + 90)

                patchname = _patches[1][0]

                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/{patchname} Mask.png",
                        getColor(_patches[1][1]),
                    ),
                    offset,
                )

                cursor = cursor + 320
        except KeyError:
            pass

            # Special exception here, if no patches at all, do this extra check...
            if _chevrons[1] != "none":
                cursor = cursor + 120

        # Bottom 3 chevrons
        if _chevrons[2] != "none":
            offset = (0, cursor)

            if isinstance(_chevrons[2], list):
                logging.info(f"Special half-chevron found on {randomName}")

                liveryImage = composite_half_patch(
                    maskPath, liveryImage, _chevrons[2], offset
                )

            else:
                logging.info(f"Found first chevron on {randomName}")

                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/Chevron Mask.png",
                        getColor(_chevrons[2]),
                        180,
                    ),
                    offset,
                )

            cursor = cursor + 120

        if _chevrons[3] != "none":
            logging.info(f"Found second chevron on {randomName}")
            offset = (0, cursor)

            if isinstance(_chevrons[3], list):
                logging.info(f"Special half-chevron found on {randomName}")

                liveryImage = composite_half_patch(
                    maskPath, liveryImage, _chevrons[3], offset
                )

            else:
                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/Chevron Mask.png",
                        getColor(_chevrons[3]),
                        180,
                    ),
                    offset,
                )

            cursor = cursor + 120

        if _chevrons[4] != "none":
            logging.info(f"Found third chevron on {randomName}")

            offset = (0, cursor)

            if isinstance(_chevrons[4], list):
                logging.info(f"Special half-chevron found on {randomName}")

                liveryImage = composite_half_patch(
                    maskPath, liveryImage, _chevrons[4], offset
                )

            else:
                liveryImage.alpha_composite(
                    getPatch(
                        f"{maskPath}/Chevron Mask.png",
                        getColor(_chevrons[4]),
                        180,
                    ),
                    offset,
                )

            cursor = cursor + 120

        liveryImage = liveryImage.crop((0, 0, 510, cursor + 120))

        liveryImage.save(f"{genpath}/{randomName}-livery.png")

        return self.parse_rst(
            f"""
.. figure:: ../{genpath}/{randomName}-livery.png
    :width: 125
    :alt: Auto Generated
    
    {' '.join(self.content)}
    """
        )

    # https://sammart.in/post/2021-05-10-external-data-sphinx-extension/
    def parse_rst(self, text):
        parser = RSTParser()
        parser.set_application(self.env.app)
        settings = OptionParser(
            defaults=self.env.settings,
            components=(RSTParser,),
            read_config_files=True,
        ).get_default_values()
        document = new_document("<rst-doc>", settings=settings)
        parser.parse(text, document)
        return document.children


def setup(app):
    app.add_directive("chevron", chevronbuilder)
    app.add_directive("servicebar", tenurebuilder)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
