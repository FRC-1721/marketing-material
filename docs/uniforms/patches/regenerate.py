# FRC 1721
# Script by Joe

from os import listdir
from os.path import isfile, join
from PIL import Image, UnidentifiedImageError
import numpy as np

maskDir = "masks/"

maskPaths = [maskDir + f for f in listdir(maskDir) if isfile(join(maskDir, f))]

for mask in maskPaths:
    try:
        patchMask = Image.open(mask)
        patchMask = patchMask.convert("RGBA")

        data = np.array(patchMask)
        red, green, blue, alpha = data.T

        mask_area = (red == 0) & (blue == 0) & (green == 0)  # Area where mask is black

        # Magic python string manipulation
        filename = (mask.split("/", 1)[1]).split(" ", 1)[0].lower()
        print(filename)

        data[..., :-1][mask_area.T] = (130, 12, 12)  # Convert all mask to red
        newimage = Image.fromarray(data)
        newimage.save(f"renders/{filename}_red.png")

        data[..., :-1][mask_area.T] = (255, 215, 0)  # Convert all mask to gold
        newimage = Image.fromarray(data)
        newimage.save(f"renders/{filename}_gold.png")

        data[..., :-1][mask_area.T] = (255, 255, 255)  # Convert all mask to white
        newimage = Image.fromarray(data)
        newimage.save(f"renders/{filename}_white.png")

    except UnidentifiedImageError:
        print("Not loading sourcefile or other file.")
