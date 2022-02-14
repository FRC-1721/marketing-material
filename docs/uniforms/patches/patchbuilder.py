# FRC 1721
# Script by Joe

from email.mime import image
import yaml
import logging
import numpy as np

from PIL import Image, UnidentifiedImageError


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    data = loadData()

    for patchCollection in data.keys():
        liveryData = data[patchCollection]

        # The actual livery image!
        liveryImage = Image.new("RGBA", (510, 1020), color=(0, 0, 0, 0))

        # Place the top chevron if it exists
        if liveryData["chevrons"][0] != "none":
            logging.info(f"Found top chevron on {patchCollection}")
            liveryImage.alpha_composite(
                getPatch("masks/Chevron Mask.png", (130, 12, 12))
            )

        if len(liveryData["patches"]) == 0:
            logging.info("No patches to apply")
        if len(liveryData["patches"]) == 1:
            offset = (int(255 / 2), int(255 / 2))

            patchname = liveryData["patches"][0]

            liveryImage.alpha_composite(
                getPatch(f"masks/{patchname} Mask.png", (130, 12, 12)), offset
            )

        liveryImage.save(f"{patchCollection}.png")
