from PIL import Image, ImageDraw
from ..collections import Collection
from ..constants import BORDER_SIZE
from typing import List
from io import BytesIO
import math

def get_collection_picture(collection: Collection, unlocked_images: List[int] = []):
    # Create base canvas for returned picture
    canvas_width = collection.images_per_row * collection.image_width + (collection.images_per_row + 1) * BORDER_SIZE
    canvas_height = collection.images_per_column * collection.image_height + (collection.images_per_column + 1) * BORDER_SIZE
    image = Image.new('RGB', (canvas_width, canvas_height), (221, 204, 255))

    # Draw on rectangles where images will be placed
    draw = ImageDraw.Draw(image)
    for i in range(collection.num_items):
        # all positions are offset from top left corner of rectangle
        row = math.floor(i/collection.images_per_row)
        top_offset = row * collection.image_height + BORDER_SIZE * (row + 1)
        col = i % collection.images_per_row
        left_offset = col * collection.image_width + BORDER_SIZE * (col + 1)

        preview_image = Image.open(collection.preview_path)
        preview_image = preview_image.resize(
            (collection.image_width, collection.image_height), 
            Image.ANTIALIAS
        )
        image.paste(
            preview_image,
            (
                left_offset,
                top_offset,
                left_offset + collection.image_width,
                top_offset + collection.image_height
            )
        )
    # unlocked images from 1..N
    for item_no in unlocked_images:
        item_no -= 1
        temp_image = Image.open(collection.image_paths[item_no])
        row = math.floor(item_no/collection.images_per_row)
        top_offset = row * collection.image_height + BORDER_SIZE * (row + 1)
        col = item_no % collection.images_per_row
        left_offset = col * collection.image_width + BORDER_SIZE * (col + 1)
        image.paste(
            temp_image,
            (
                left_offset,
                top_offset,
                left_offset + collection.image_width,
                top_offset + collection.image_height
            )
        )
    return _image_to_byte_stream(image)

# https://stackoverflow.com/questions/60006794/send-image-from-memory
def _image_to_byte_stream(image: Image.Image):
    _img_byte_arr = BytesIO()
    image.save(_img_byte_arr, format='JPEG')
    _img_byte_arr.seek(0)
    return _img_byte_arr