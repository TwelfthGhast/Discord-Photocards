from PIL import Image, ImageDraw

def get_collection_picture():
    # Create base canvas for returned picture
    width = collClass.width if collClass.width < collClass.size else collClass.size
    height = math.floor(
        collClass.size / collClass.width) if collClass.size % collClass.width == 0 else math.ceil(collClass.size / collClass.width)
    single_w, single_h = collClass.img_size
    BORDER_SIZE = 20
    dimensions = (width * single_w + (width + 1) * BORDER_SIZE,
                  height * single_h + (height + 1) * BORDER_SIZE)
    image = Image.new('RGB', dimensions, (221, 204, 255))
    # Draw on rectangles where images will be placed
    draw = ImageDraw.Draw(image)
    for i in range(0, collClass.size):
        # all positions are offset from top left corner of rectangle
        row = math.floor(i/collClass.width)
        top_offset = row * single_h + BORDER_SIZE * (row + 1)
        col = i % collClass.width
        left_offset = col * single_w + BORDER_SIZE * (col + 1)
        if not collClass.preview:
            draw.rectangle([(left_offset, top_offset), (left_offset +
                                                        single_w, top_offset + single_h)], fill=(255, 255, 255))
        else:
            temp_image = Image.open(f"collections/{collClass.name}/{collClass.preview}")
            temp_image = temp_image.resize(
                (single_w, single_h), Image.ANTIALIAS)
            image.paste(temp_image, (left_offset, top_offset,
                                     left_offset + single_w, top_offset + single_h))
    # Now place images in
    # userClass has numbers from 1 to arraySize, so we will need to subtract 1
    for itemNo in user.collected[collClass.name]:
        itemNo -= 1
        temp_image = Image.open(f"collections/{collClass.name}/{collClass.items[itemNo]}")
        temp_image = temp_image.resize(
            (single_w, single_h), Image.ANTIALIAS)
        # Find position of item
        row = math.floor(itemNo/collClass.width)
        top_offset = row * single_h + BORDER_SIZE * (row + 1)
        col = itemNo % collClass.width
        left_offset = col * single_w + BORDER_SIZE * (col + 1)
        # paste the loaded image onto prepared background
        image.paste(temp_image, (left_offset, top_offset,
            left_offset + single_w, top_offset + single_h))