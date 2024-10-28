import os
import argparse
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


def main():
    parser = argparse.ArgumentParser(description="Process specimen folder(s) to add scalebars to images.")

    # One mandatory path argument for folder or text file
    parser.add_argument("path", type=str, help="Path to a text file with folder paths or a parent folder")

    # Optional argument to specify a single folder directly
    parser.add_argument("--specimen_folder", action="store_true", help="Treat path as a single specimen folder")

    # Scalebar and styling options
    parser.add_argument("--scalebar_height", type=int, default=10, help="Height of the scalebar in pixels")
    parser.add_argument("--x_margin", type=int, default=50, help="X margin from the right edge of the image")
    parser.add_argument("--y_margin", type=int, default=150, help="Y margin from the bottom edge of the image")
    parser.add_argument("--fontsize", type=int, default=100, help="Font size of the text below the scalebar")
    parser.add_argument("--font_style", type=str, default="times.ttf", help="Font style for the scalebar text")
    parser.add_argument("--verbose", action="store_true", help="Print detailed information during processing")

    args = parser.parse_args()

    # Determine if `path` is a single specimen folder, a parent directory, or a text file of folder paths
    specimen_folders = []

    if args.specimen_folder:
        # Use the path as a single folder directly
        specimen_folders.append(args.path)
    else:
        # Check if the path is a .txt file or a folder
        if args.path.endswith(".txt"):
            # Read folder paths from the text file, supporting both line-separated and comma-separated paths
            specimen_folders = parse_folder_list(args.path)
        elif os.path.isdir(args.path):
            # Treat path as a parent folder and list its subdirectories
            specimen_folders = [
                os.path.join(args.path, subdir)
                for subdir in os.listdir(args.path)
                if os.path.isdir(os.path.join(args.path, subdir))
            ]
        else:
            print("Invalid path. Provide a .txt file or a parent directory.")
            return

    # Process each specimen folder with a tqdm progress bar
    for folder in tqdm(specimen_folders, desc="Processing specimen folders", unit="folder"):
        if args.verbose:
            print(f"Starting folder: {folder}")
        process_specimen(
            specimen_folder=folder,
            scalebar_height=args.scalebar_height,
            x_margin=args.x_margin,
            y_margin=args.y_margin,
            fontsize=args.fontsize,
            font_style=args.font_style,
            verbose=args.verbose
        )


if __name__ == "__main__":
    main()
