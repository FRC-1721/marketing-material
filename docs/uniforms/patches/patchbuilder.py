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
        return (204, 164, 61)
    elif key == "yellow":
        return (255, 255, 50)
    elif key == "purple":
        return (75, 0, 130)
    else:
        logging.warning(f"Could not find color {key}")
        return (0, 255, 0)


def composite_half_patch(lImage, lData, offset):
    # So messy, composite two images!

    if lData[1] != "none":
        lImage.alpha_composite(
            getPatch(
                "masks/Chevron Mask.png",
                getColor(lData[1]),
                180,
            ),
            offset,
        )

    lImage.alpha_composite(
        getPatch(
            "masks/HalfChevron Mask.png",
            getColor(lData[0]),
            180,
        ),
        offset,
    )

    return lImage


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    data = loadData()

    for patchCollection in data.keys():
        liveryData = data[patchCollection]

        # Where the next patch should be drawn
        cursor = 0

        # The actual livery image!
        liveryImage = Image.new("RGBA", (510, 1020), color=(0, 0, 0, 0))

        # Check if we're making a chevron
        if "chevrons" in liveryData:
            # Place the top two chevrons if they exist
            if liveryData["chevrons"][0] != "none":
                logging.info(
                    f"Found super top chevron on {patchCollection}, {liveryData['chevrons'][0]}"
                )
                liveryImage.alpha_composite(
                    getPatch(
                        "masks/Rocker Mask.png",
                        getColor(liveryData["chevrons"][0]),
                    )
                )

                cursor = cursor + 112

            if liveryData["chevrons"][1] != "none":
                logging.info(
                    f"Found top chevron on {patchCollection}, {liveryData['chevrons'][1]}"
                )
                liveryImage.alpha_composite(
                    getPatch(
                        "masks/Rocker Mask.png",
                        getColor(liveryData["chevrons"][1]),
                    ),
                    (0, cursor),
                )

                cursor = cursor + 120

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
                            getColor(liveryData["patches"][1][1]),
                        ),
                        offset,
                    )

                    cursor = cursor + 320
            except KeyError:
                pass

                # Special exception here, if no patches at all, do this extra check...
                if liveryData["chevrons"][1] != "none":
                    cursor = cursor + 120

            # Bottom 3 chevrons
            if liveryData["chevrons"][2] != "none":
                offset = (0, cursor)

                if isinstance(liveryData["chevrons"][2], list):
                    logging.info(f"Special half-chevron found on {patchCollection}")

                    liveryImage = composite_half_patch(
                        liveryImage, liveryData["chevrons"][2], offset
                    )

                else:
                    logging.info(f"Found first chevron on {patchCollection}")

                    liveryImage.alpha_composite(
                        getPatch(
                            "masks/Chevron Mask.png",
                            getColor(liveryData["chevrons"][2]),
                            180,
                        ),
                        offset,
                    )

                cursor = cursor + 120

            if liveryData["chevrons"][3] != "none":
                logging.info(f"Found second chevron on {patchCollection}")
                offset = (0, cursor)

                if isinstance(liveryData["chevrons"][3], list):
                    logging.info(f"Special half-chevron found on {patchCollection}")

                    liveryImage = composite_half_patch(
                        liveryImage, liveryData["chevrons"][3], offset
                    )

                else:
                    liveryImage.alpha_composite(
                        getPatch(
                            "masks/Chevron Mask.png",
                            getColor(liveryData["chevrons"][3]),
                            180,
                        ),
                        offset,
                    )

                cursor = cursor + 120

            if liveryData["chevrons"][4] != "none":
                logging.info(f"Found third chevron on {patchCollection}")

                offset = (0, cursor)

                if isinstance(liveryData["chevrons"][4], list):
                    logging.info(f"Special half-chevron found on {patchCollection}")

                    liveryImage = composite_half_patch(
                        liveryImage, liveryData["chevrons"][4], offset
                    )

                else:
                    liveryImage.alpha_composite(
                        getPatch(
                            "masks/Chevron Mask.png",
                            getColor(liveryData["chevrons"][4]),
                            180,
                        ),
                        offset,
                    )

                cursor = cursor + 120

        elif "tenure_bars" in liveryData:
            logging.info(f"Processing tenure bar")
            for bar in liveryData["tenure_bars"]:
                # Check if this is a normal bar or a double bar
                if type(bar) is not list:
                    liveryImage.alpha_composite(
                        getPatch(
                            "masks/Tenure Bar.png",
                            getColor(bar),
                        ),
                        (0, cursor),
                    )
                else:
                    # If it is a list, its a double bar! Lets process it
                    liveryImage.alpha_composite(
                        getPatch(
                            "masks/Tenure Bar.png",
                            getColor(bar[1]),
                        ),
                        (0, cursor),
                    )
                    liveryImage.alpha_composite(
                        getPatch(
                            "masks/Tenure Half Bar.png",
                            getColor(bar[0]),
                        ),
                        (0, cursor),
                    )

                cursor = cursor + 130

        liveryImage = liveryImage.crop((0, 0, 510, cursor + 120))

        liveryImage.save(f"renders/{patchCollection}.png")
