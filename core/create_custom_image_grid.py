from PIL import Image
from io import BytesIO

def create_custom_image_grid(image_files_column_1, image_files_column_2, target_size_1, target_size_2):
    """
    Creates a custom image grid using in-memory file objects.

    Args:
        image_files_column_1 (list): List of in-memory file objects for column 1.
        image_files_column_2 (list): List of in-memory file objects for column 2.
        target_size_1 (tuple): Size (width, height) for images in column 1.
        target_size_2 (tuple): Size (width, height) for images in column 2.

    Returns:
        BytesIO: An in-memory file object containing the final grid image.
    """
    # Create blank images for missing elements
    blank_image_col_1 = Image.new("RGBA", target_size_1, (255, 255, 255, 0))
    blank_image_col_2 = Image.new("RGBA", target_size_2, (255, 255, 255, 0))

    # Ensure column 1 has exactly 2 items
    images_col_1 = [Image.open(img).convert("RGBA").resize(target_size_1) for img in image_files_column_1]
    while len(images_col_1) < 2:
        images_col_1.append(blank_image_col_1)

    # Ensure column 2 has exactly 3 items
    images_col_2 = [Image.open(img).convert("RGBA").resize(target_size_2) for img in image_files_column_2]
    while len(images_col_2) < 3:
        images_col_2.append(blank_image_col_2)

    # Determine the dimensions of the grid
    col_1_width, col_1_height = target_size_1
    col_2_width, col_2_height = target_size_2
    total_width = col_1_width + col_2_width
    total_height = max(len(images_col_1) * col_1_height, len(images_col_2) * col_2_height)

    # Create a blank canvas
    grid_image = Image.new('RGBA', (total_width, total_height), 'white')

    # Paste images for column 1
    y_offset = 0
    for img in images_col_1:
        grid_image.paste(img, (0, y_offset))
        y_offset += col_1_height

    # Calculate padding for column 2
    space_available = total_height - (len(images_col_2) * col_2_height)
    top_padding = space_available // 2  # Distribute padding equally
    middle_padding = top_padding // 2  # Center the middle image

    # Paste images for column 2
    x_offset = col_1_width
    y_offsets = [0, top_padding + col_2_height, total_height - col_2_height]
    for idx, img in enumerate(images_col_2):
        grid_image.paste(img, (x_offset, y_offsets[idx]))

    # Save the grid image into a BytesIO object
    image_buffer = BytesIO()
    grid_image.save(image_buffer, format='PNG')
    image_buffer.seek(0)  # Reset buffer pointer to the beginning
    return image_buffer