# FRC 1721
# Script by Joe


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


def getColor(key):

    if key == "white":
        return (184, 184, 184)
    elif key == "red":
        return (130, 12, 12)
    elif key == "gold":
        return (255, 215, 0)
    else:
        logging.warning(f"Could not find color {key}")
        return (0, 255, 0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    data = loadData()

    for patchCollection in data.keys():
        liveryData = data[patchCollection]

        # Where the next patch should be drawn
        cursor = 0

        # The actual livery image!
        liveryImage = Image.new("RGBA", (510, 1020), color=(0, 0, 0, 0))

        # Place the top chevron if it exists
        if liveryData["chevrons"][0] != "none":
            logging.info(
                f"Found top chevron on {patchCollection}, {liveryData['chevrons'][0]}"
            )
            liveryImage.alpha_composite(
                getPatch("masks/Chevron Mask.png", getColor(liveryData["chevrons"][0]))
            )

            cursor = 112

        try:
            if len(liveryData["patches"]) == 0:
                # No subteam patches
                logging.info("No patches to apply")
            if len(liveryData["patches"]) == 1:
                # One subteam patch
                offset = (int(255 / 2), cursor)

                patchname = liveryData["patches"][0][0]

                liveryImage.alpha_composite(
                    getPatch(
                        f"masks/{patchname} Mask.png",
                        getColor(liveryData["patches"][0][1]),
                    ),
                    offset,
                )

                cursor = cursor + 150
            if len(liveryData["patches"]) == 2:
                # Two subteam patches
                offset = (0, cursor + 90)

                patchname = liveryData["patches"][0][0]

                liveryImage.alpha_composite(
                    getPatch(
                        f"masks/{patchname} Mask.png",
                        getColor(liveryData["patches"][0][1]),
                    ),
                    offset,
                )

                # New offset, new patch
                offset = (255, cursor + 90)

                patchname = liveryData["patches"][1][0]

                liveryImage.alpha_composite(
                    getPatch(
                        f"masks/{patchname} Mask.png",
                        getColor(liveryData["patches"][0][1]),
                    ),
                    offset,
                )

                cursor = cursor + 320
        except KeyError:
            pass

        # Bottom 3 chevrons
        if liveryData["chevrons"][1] != "none":
            offset = (0, cursor)

            if isinstance(liveryData["chevrons"][1], list):
                logging.info(f"Special half-chevron found on {patchCollection}")

                # So messy, composite two images!
                liveryImage.alpha_composite(
                    getPatch(
                        "masks/Chevron Mask.png",
                        getColor(liveryData["chevrons"][1][1]),
                        180,
                    ),
                    offset,
                )

                liveryImage.alpha_composite(
                    getPatch(
                        "masks/HalfChevron Mask.png",
                        getColor(liveryData["chevrons"][1][0]),
                        180,
                    ),
                    offset,
                )

            else:
                logging.info(f"Found first chevron on {patchCollection}")

                liveryImage.alpha_composite(
                    getPatch(
                        "masks/Chevron Mask.png",
                        getColor(liveryData["chevrons"][1]),
                        180,
                    ),
                    offset,
                )

            cursor = cursor + 120

        if liveryData["chevrons"][2] != "none":
            logging.info(f"Found second chevron on {patchCollection}")

            offset = (0, cursor)

            liveryImage.alpha_composite(
                getPatch(
                    "masks/Chevron Mask.png", getColor(liveryData["chevrons"][2]), 180
                ),
                offset,
            )

            cursor = cursor + 120

        if liveryData["chevrons"][3] != "none":
            logging.info(f"Found third chevron on {patchCollection}")

            offset = (0, cursor)

            liveryImage.alpha_composite(
                getPatch(
                    "masks/Chevron Mask.png", getColor(liveryData["chevrons"][3]), 180
                ),
                offset,
            )

            cursor = cursor + 120

        liveryImage = liveryImage.crop((0, 0, 510, cursor + 120))

        liveryImage.save(f"renders/{patchCollection}.png")
