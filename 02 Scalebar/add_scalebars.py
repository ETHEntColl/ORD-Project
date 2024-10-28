import os

from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfReader
from tqdm.auto import tqdm


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
        return f"Error reading PDF: {e}"

    lines = pdf_text.split('\n')
    for line in lines:
        if line.startswith(prefix):
            parts = line.split(sep)
            if len(parts) > 1 and parts[1]:
                return parts[1]
            elif len(lines) > lines.index(line) + 1:
                return lines[lines.index(line) + 1]

    return "Object Pixel Pitch value not found"

def add_scalebar(image_path, output_path, scalebar_length, scalebar_height, x_margin, y_margin, fontsize,
                 font_style="times.ttf"):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    img_width, img_height = image.size
    scalebar_x = img_width - x_margin - scalebar_length
    scalebar_y = img_height - y_margin - scalebar_height

    draw.rectangle([scalebar_x, scalebar_y, scalebar_x + scalebar_length, scalebar_y + scalebar_height], fill="black")

    try:
        font = ImageFont.truetype(font_style, size=fontsize)
    except IOError:
        font = ImageFont.load_default()  # Fallback font if specified font is unavailable

    text = "1mm"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]

    text_x = scalebar_x + scalebar_length - text_width
    text_y = scalebar_y + scalebar_height + 5

    draw.text((text_x, text_y), text, fill="black", font=font)
    image.save(output_path)

def process_specimen(specimen_folder, scalebar_height=10, x_margin=50, y_margin=150, fontsize=100, font_style="times.ttf",
                     verbose=False):
    input_folder = os.path.join(specimen_folder, "redof")
    output_folder = os.path.join(specimen_folder, "redof_scalebar")
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
        add_scalebar(image_path, output_path, scalebar_length, scalebar_height, x_margin, y_margin, fontsize,
                     font_style)

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
            "- A parent directory containing specimen folders (e.g., '\\path\\to\\parent_directory\\')\n"
            "- A single specimen folder that contains an 'edof' subdirectory (e.g., '\\path\\to\\single_specimen\\')\n"
            "- A text file with paths to specimen folders (e.g., '\\path\\to\\paths.txt'):\n"
        ).strip()

        # Remove surrounding double quotes if present
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]

        if os.path.isdir(path) or (path.endswith('.txt') and os.path.isfile(path)):
            return path
        print("Invalid path. Please try again.")


def prompt_user_for_optional_arguments():
    """
    Prompts the user whether they want to specify optional arguments or use default values.

    Returns:
        tuple: A tuple containing the optional arguments.
    """
    print("\nDo you want to specify custom values for the following optional arguments? (Press Enter for defaults)")
    response = input("Type 'yes' to specify custom values, or press Enter to use default values: ").strip().lower()

    if response != 'yes':
        # Return default values
        return 10, 50, 150, 100, "times.ttf", False

    # Ask for each argument with an option to keep the default
    scalebar_height = input(f"Scalebar height in pixels (default is 10): ")
    scalebar_height = int(scalebar_height) if scalebar_height else 10

    x_margin = input(f"X margin from the right edge of the image (default is 50): ")
    x_margin = int(x_margin) if x_margin else 50

    y_margin = input(f"Y margin from the bottom edge of the image (default is 150): ")
    y_margin = int(y_margin) if y_margin else 150

    fontsize = input(f"Font size of the text below the scalebar (default is 100): ")
    fontsize = int(fontsize) if fontsize else 100

    font_style = input(f"Font style for the scalebar text (default is 'times.ttf'): ")
    font_style = font_style if font_style else "times.ttf"

    verbose = input("Verbose output? (yes/no, default is no): ").strip().lower()
    verbose = verbose == 'yes' if verbose in ['yes', 'no'] else False

    return scalebar_height, x_margin, y_margin, fontsize, font_style, verbose


def main():
    # Prompt user for the input path
    path = prompt_user_for_path()

    # Determine if `path` is a single specimen folder, a parent directory, or a text file of folder paths
    specimen_folders = []

    # Determine if the path is a single specimen folder or a parent directory
    if os.path.isdir(path):
        # Check for the presence of an "edof" directory
        if 'edof' in os.listdir(path):
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
        if path.endswith('.txt'):
            # Read folder paths from the text file
            specimen_folders = parse_folder_list(path)
        else:
            print("Invalid path. Provide a .txt file or a valid directory.")
            return

    # Prompt for optional arguments
    (scalebar_height, x_margin, y_margin, fontsize, font_style, verbose) = prompt_user_for_optional_arguments()

    # Process each specimen folder with a tqdm progress bar
    for folder in tqdm(specimen_folders, desc="Processing specimen folders", unit="folder"):
        if verbose:
            print(f"Starting folder: {folder}")
        process_specimen(
            specimen_folder=folder,
            scalebar_height=scalebar_height,
            x_margin=x_margin,
            y_margin=y_margin,
            fontsize=fontsize,
            font_style=font_style,
            verbose=verbose
        )

    # Keep the command window open until the user decides to close it
    input("Processing complete! Press Enter to exit...")


if __name__ == "__main__":
    main()
