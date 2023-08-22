"""Qualifier Solution for Python Discord Code Jam 10"""

from PIL import Image
import numpy as np

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    image_x_dim, image_y_dim = image_size
    tile_x_dim, tile_y_dim = tile_size

    if image_x_dim % tile_x_dim != 0 and image_y_dim % tile_y_dim != 0:
        return False

    horizontal_tiles = image_x_dim // tile_x_dim
    vertical_tiles = image_y_dim // tile_y_dim
    total_tiles = horizontal_tiles * vertical_tiles

    sorted_ordering_list = sorted(ordering)
    if sorted_ordering_list == list(range(total_tiles)):
        return True

    return False


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """

    full_image = Image.open(image_path)
    full_image_mode = full_image.mode
    full_x, full_y = full_image.size
    tile_x, tile_y = tile_size

    # Raise error if invalid input
    if not valid_input(full_image.size, tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

    x_tiles = full_x//tile_x
    y_tiles = full_y//tile_y
    all_co_ordinates = []

    # Adding all the co_ordinates
    for rows in range(y_tiles + 1):
        col_co_ordinates = []
        for cols in range(x_tiles + 1):
            col_co_ordinates.append((cols * tile_x, rows * tile_y))
        all_co_ordinates.append(col_co_ordinates)

    tiles_co = []
    # Adding diagonals for tiles to crop out
    for rows in range(y_tiles):
        for cols in range(x_tiles):
            tiles_co.append(all_co_ordinates[rows][cols] + all_co_ordinates[rows+1][cols+1])

    # cropped tiles in order
    image_frames = []
    for order in (ordering):
        image_frames.append(full_image.crop(tiles_co[order]))

    # create grid of images to merge
    image_indexs = np.reshape(list(range(len(image_frames))), (y_tiles, x_tiles))

    horizontal_merges = []
    for rows in image_indexs:
        # Merge images horizontally
        hori_merged_image = Image.new(full_image_mode, (full_x, tile_y))
        horizontal_pos_x = 0

        for col in rows:
            hori_merged_image.paste(image_frames[col], (horizontal_pos_x, 0))
            horizontal_pos_x += tile_x
        horizontal_merges.append(hori_merged_image)

    # Merging images vertically
    final_output_img = Image.new(full_image_mode, (full_x, full_y))
    vertical_pos_y = 0
    for hori_merge in horizontal_merges:
        final_output_img.paste(hori_merge, (0, vertical_pos_y))
        vertical_pos_y += tile_y

    final_output_img.save(out_path)
