import os
import warnings

from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfReader
from tqdm.auto import tqdm


DEFAULT_SCALEBAR_KWARGS = {
    'corner': 'bottom_right',
    'text_position': 'above',
    'text_alignment': 'right',
    'text_bar_margin': 20,
    'scalebar_height': 10,
    'x_margin': 150,
    'y_margin': 150,
    'fontsize': 100,
    'font_style': 'times.ttf',
}


def extract_object_pixel_pitch(folder_path):
    """
    Extracts the Object Pixel Pitch value from the ScanInformation.pdf in a specified folder.

    Parameters:
        folder_path (str): Path to the folder containing ScanInformation.pdf.

    Returns:
        str: The Object Pixel Pitch value or an error message if not found.
    """
    pdf_path = os.path.join(folder_path, "ScanInformation.pdf")
    prefix = "2.5."
    sep = ": "

    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            pdf_text = pdf_reader.pages[0].extract_text()  # Extract text from the first page
    except Exception as e:
        return f"Error reading ScanInformation.pdf: {e}"

    lines = pdf_text.split('\n')
    for line in lines:
        if line.startswith(prefix):
            parts = line.split(sep)
            if len(parts) > 1 and parts[1]:
                return parts[1]
            elif len(lines) > lines.index(line) + 1:
                return lines[lines.index(line) + 1]

    return "Object Pixel Pitch value not found"


def add_scalebar(
        image_path,
        output_path,
        scalebar_length,
        corner=DEFAULT_SCALEBAR_KWARGS['corner'],
        text_position=DEFAULT_SCALEBAR_KWARGS['text_position'],
        text_alignment=DEFAULT_SCALEBAR_KWARGS['text_alignment'],
        text_bar_margin=DEFAULT_SCALEBAR_KWARGS['text_bar_margin'],
        scalebar_height=DEFAULT_SCALEBAR_KWARGS['scalebar_height'],
        x_margin=DEFAULT_SCALEBAR_KWARGS['x_margin'],
        y_margin=DEFAULT_SCALEBAR_KWARGS['y_margin'],
        fontsize=DEFAULT_SCALEBAR_KWARGS['fontsize'],
        font_style=DEFAULT_SCALEBAR_KWARGS['font_style'],
):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    img_width, img_height = image.size

    # Determine scalebar position based on the specified corner
    if corner == "bottom_right":
        scalebar_x = img_width - x_margin - scalebar_length
        scalebar_y = img_height - y_margin - scalebar_height
    elif corner == "bottom_left":
        scalebar_x = x_margin
        scalebar_y = img_height - y_margin - scalebar_height
    elif corner == "top_right":
        scalebar_x = img_width - x_margin - scalebar_length
        scalebar_y = y_margin
    elif corner == "top_left":
        scalebar_x = x_margin
        scalebar_y = y_margin
    else:
        raise ValueError(
            "Invalid corner specified. Choose from 'bottom_right', 'bottom_left', 'top_right', or 'top_left'.")

    # Draw the scalebar rectangle
    draw.rectangle([scalebar_x, scalebar_y, scalebar_x + scalebar_length, scalebar_y + scalebar_height], fill="black")

    # Load the font, with a fallback to default if the specified font is unavailable
    try:
        font = ImageFont.truetype(font_style, size=fontsize)
    except IOError:
        font = ImageFont.load_default()

    text = "1mm"

    # Determine text y-position relative to the scalebar
    if text_position == "above":
        text_anchor = "mb"  # middle-bottom anchor
        text_y = scalebar_y - text_bar_margin  # Place text above with 5px margin
    elif text_position == "below":
        text_anchor = "mt"  # middle-top anchor
        text_y = scalebar_y + scalebar_height + text_bar_margin  # Place text below with 5px margin
    else:
        raise ValueError("Invalid text_position specified. Choose 'above' or 'below'.")

    # Determine text x-position based on alignment and set anchor accordingly
    if text_alignment == "center":
        text_x = scalebar_x + (scalebar_length / 2)
        text_anchor = text_anchor.replace('m', 'm')  # Keep middle anchor for x-axis
    elif text_alignment == "left":
        text_x = scalebar_x
        text_anchor = text_anchor.replace('m', 'l')  # Left alignment
    elif text_alignment == "right":
        text_x = scalebar_x + scalebar_length
        text_anchor = text_anchor.replace('m', 'r')  # Right alignment
    else:
        raise ValueError("Invalid text_alignment specified. Choose 'center', 'left', or 'right'.")

    # Draw the text on the image using the specified anchor point
    draw.text((text_x, text_y), text, fill="black", font=font, anchor=text_anchor)

    # Save the modified image
    image.save(output_path)


def process_specimen(specimen_folder, use_edof: bool = False, verbose=True, **scalebar_kwargs):

    # Check if primary folder exists; if not, use the fallback folder
    input_folder = os.path.join(specimen_folder, "edof" if use_edof else "redof")
    if not os.path.exists(input_folder):
        input_folder = os.path.join(specimen_folder, "redof" if use_edof else "edof")

    # If neither folder exists, warn and return
    if not os.path.exists(input_folder):
        warnings.warn(
            f"'{specimen_folder}' doesn't contain an `edof` or `redof` folder. Skipping this specimen folder.")
        return

    # Set the output folder based on the input folder used
    output_folder = os.path.join(specimen_folder, f"{os.path.basename(input_folder)}_scalebar")
    os.makedirs(output_folder, exist_ok=True)

    object_pixel_pitch = extract_object_pixel_pitch(specimen_folder)
    scalebar_length = int(1000 / float(object_pixel_pitch))

    valid_extensions = {".jpeg", ".jpg", ".png", ".bmp", ".tiff", ".gif"}
    image_files = [filename for filename in os.listdir(input_folder) if
                   any(filename.lower().endswith(ext) for ext in valid_extensions)]

    if verbose:
        print(f"Input Folder: {input_folder}")
        print(f"Output Folder: {output_folder}")
        print(f"Object Pixel Pitch [um]: {object_pixel_pitch}")
        print(f"Scalebar Length [px]: {scalebar_length}")

    for filename in tqdm(image_files, desc="Processing images", unit="image"):
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        add_scalebar(image_path, output_path, scalebar_length, **scalebar_kwargs)


def parse_folder_list(file_path):
    """
    Reads folder paths from a file, handling both line-separated and comma-separated formats.

    Args:
        file_path (str): Path to the text file containing folder paths.

    Returns:
        list: List of folder paths.
    """
    folders = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split by commas if the line has them, otherwise strip and treat as a single path
            if ',' in line:
                folders.extend(path.strip() for path in line.split(',') if path.strip())
            else:
                folders.append(line.strip())
    return folders


def prompt_user_for_path():
    """
    Prompts the user to provide a parent directory, a single specimen folder, or a text file with folder paths.

    Returns:
        str: The valid path provided by the user.
    """
    while True:
        path = input(
            "Please enter the path to one of the following:\n"
            "- A single specimen folder (e.g., '\\path\\to\\single_specimen\\')\n"
            "- A parent directory containing specimen folders (e.g., '\\path\\to\\parent_directory\\')\n"
            "- A text or csv file with paths to specimen folders (e.g., '\\path\\to\\paths.txt'):\n"
        ).strip()

        # Remove surrounding double quotes if present
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]

        if os.path.isdir(path) or ((path.endswith('.txt') or path.endswith('.csv')) and os.path.isfile(path)):
            return path
        print("Invalid path. Please try again.")


def prompt_user_for_optional_arguments():
    """
    Prompts the user whether they want to specify optional arguments or use default values.

    Returns:
        dict: A dictionary containing the optional arguments.
    """
    print("\nDo you want to specify custom values for the following optional arguments? (Press Enter for defaults)")
    response = input("Type 'yes' to specify custom values, or press Enter to use default values: ").strip().lower()

    if response != 'yes':
        # Return default values
        return DEFAULT_SCALEBAR_KWARGS

    # Ask for each argument with an option to keep the default
    scalebar_height = input(f"Scalebar height in pixels (default is {DEFAULT_SCALEBAR_KWARGS['scalebar_height']}): ")
    scalebar_height = int(scalebar_height) if scalebar_height else DEFAULT_SCALEBAR_KWARGS['scalebar_height']

    x_margin = input(f"X margin from the edge of the image (default is {DEFAULT_SCALEBAR_KWARGS['x_margin']}): ")
    x_margin = int(x_margin) if x_margin else DEFAULT_SCALEBAR_KWARGS['x_margin']

    y_margin = input(f"Y margin from the edge of the image (default is {DEFAULT_SCALEBAR_KWARGS['y_margin']}): ")
    y_margin = int(y_margin) if y_margin else DEFAULT_SCALEBAR_KWARGS['y_margin']

    fontsize = input(f"Font size of the text next to the scalebar (default is {DEFAULT_SCALEBAR_KWARGS['fontsize']}): ")
    fontsize = int(fontsize) if fontsize else DEFAULT_SCALEBAR_KWARGS['fontsize']

    font_style = input(f"Font style for the scalebar text (default is '{DEFAULT_SCALEBAR_KWARGS['font_style']}'): ")
    font_style = font_style if font_style else DEFAULT_SCALEBAR_KWARGS['font_style']

    corner = input(f"Corner to place the scalebar (bottom_right, bottom_left, top_right, top_left; default is {DEFAULT_SCALEBAR_KWARGS['corner']}): ")
    corner = corner if corner in ['bottom_right', 'bottom_left', 'top_right', 'top_left'] else DEFAULT_SCALEBAR_KWARGS['corner']

    text_position = input(f"Position of text relative to the scalebar (above or below; default is {DEFAULT_SCALEBAR_KWARGS['text_position']}): ")
    text_position = text_position if text_position in ['above', 'below'] else DEFAULT_SCALEBAR_KWARGS['text_position']

    text_alignment = input(f"Text alignment relative to the scalebar (left, center, right; default is {DEFAULT_SCALEBAR_KWARGS['text_alignment']}): ")
    text_alignment = text_alignment if text_alignment in ['left', 'center', 'right'] else DEFAULT_SCALEBAR_KWARGS['text_alignment']

    text_bar_margin = input(f"Margin between text and scalebar (default is {DEFAULT_SCALEBAR_KWARGS['text_bar_margin']}): ")
    text_bar_margin = int(text_bar_margin) if text_bar_margin else DEFAULT_SCALEBAR_KWARGS['text_bar_margin']

    verbose = input("Verbose output? (yes/no, default is yes): ").strip().lower()
    verbose = verbose == 'yes' if verbose in ['yes', 'no'] else True

    return {
        'corner': corner,
        'text_position': text_position,
        'text_alignment': text_alignment,
        'text_bar_margin': text_bar_margin,
        'scalebar_height': scalebar_height,
        'x_margin': x_margin,
        'y_margin': y_margin,
        'fontsize': fontsize,
        'font_style': font_style,
        'verbose': verbose
    }


def main():
    # Prompt user for the input path
    path = prompt_user_for_path()

    # Determine if `path` is a single specimen folder, a parent directory, or a text file of folder paths
    specimen_folders = []

    # Determine if the path is a single specimen folder or a parent directory
    if os.path.isdir(path):
        # Check for the presence of an "edof" directory
        if 'edof' or 'redof' in os.listdir(path):
            # Treat it as a single specimen folder
            specimen_folders.append(path)
        else:
            # Treat path as a parent folder and list its subdirectories
            specimen_folders = [
                os.path.join(path, subdir)
                for subdir in os.listdir(path)
                if os.path.isdir(os.path.join(path, subdir))
            ]
    else:
        # Check if the path is a text file
        if path.endswith('.txt') or path.endswith('.csv'):
            # Read folder paths from the text file
            specimen_folders = parse_folder_list(path)
        else:
            print("Invalid path. Provide a .txt file or a valid directory.")
            return

    # Prompt for optional arguments
    optional_kwargs = prompt_user_for_optional_arguments()

    # Process each specimen folder with a tqdm progress bar
    for folder in tqdm(specimen_folders, desc="Processing specimen folders", unit="folder"):
        if optional_kwargs['verbose']:
            print(f"Starting folder: {folder}")
        process_specimen(
            specimen_folder=folder,
            **optional_kwargs
        )

    # Keep the command window open until the user decides to close it
    input("Processing complete! Press Enter to exit...")


if __name__ == "__main__":
    main()