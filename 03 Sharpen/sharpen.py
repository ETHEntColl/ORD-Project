import os
import warnings
from PIL import Image
import cv2
import numpy as np
from tqdm.auto import tqdm

# Default sharpening parameters
DEFAULT_SHARPENING_KWARGS = {
    'use_edof': {'default': True, 'description': 'Use EDOF images instead of REDOF images.'},
    'unsharp_radius': {'default': 1.5, 'description': 'Radius for Unsharp Mask, controlling the amount of blurring before sharpening.'},
    'unsharp_percent': {'default': 150, 'description': 'Strength of sharpening effect as a percentage.'},
    'highpass_radius': {'default': 1, 'description': 'Radius for High Pass filter, influencing detail retention in sharpening.'},
    'verbose': {'default': True, 'description': 'Display detailed information during processing.'}
}

def apply_unsharp_mask(image, radius=1.5, percent=150):
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    blurred = cv2.GaussianBlur(image_cv, (0, 0), radius)
    sharpened = cv2.addWeighted(image_cv, 1 + percent / 100, blurred, -percent / 100, 0)
    return Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))


def apply_high_pass_filter(image, radius=1):
    """Apply High Pass filter to an image."""
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    blurred = cv2.GaussianBlur(image_cv, (0, 0), radius)
    high_pass = cv2.addWeighted(image_cv, 1.5, blurred, -0.5, 0)  # Adjust weights as needed
    return Image.fromarray(cv2.cvtColor(high_pass, cv2.COLOR_BGR2RGB))


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


def prompt_user_for_optional_arguments(defaults):
    """Prompt the user for optional arguments with descriptions and return a customized dictionary."""
    print("\nCustomize parameters (Press Enter to use default values).")
    response = input("Type 'yes' to customize or press Enter to use defaults: ").strip().lower()

    if response != 'yes':
        # Return default values without descriptions
        return {key: config['default'] for key, config in defaults.items()}

    # Collect customized values
    customized_params = {}
    for param, config in defaults.items():
        user_input = input(f"{config['description']} (default {config['default']}): ").strip()

        if not user_input:  # Use default if no input
            customized_params[param] = config['default']
        elif isinstance(config['default'], bool):  # Handle boolean conversion
            # Interpret user input for boolean values
            if user_input.lower() in ['true', 'yes', '1']:
                customized_params[param] = True
            elif user_input.lower() in ['false', 'no', '0']:
                customized_params[param] = False
            else:
                print(f"Invalid input for {param}. Using default: {config['default']}")
                customized_params[param] = config['default']
        else:
            # Convert other types normally
            try:
                customized_params[param] = type(config['default'])(user_input)
            except ValueError:
                print(f"Invalid input for {param}. Using default: {config['default']}")
                customized_params[param] = config['default']

    return customized_params



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


def process_specimen(
        specimen_folder,
        use_edof=DEFAULT_SHARPENING_KWARGS['use_edof']['default'],
        verbose=DEFAULT_SHARPENING_KWARGS['verbose']['default'],
        **sharpening_kwargs
):
    # Check if primary folder exists; if not, use the fallback folder
    input_folder = os.path.join(specimen_folder, "edof" if use_edof else "redof")
    if not os.path.exists(input_folder):
        input_folder = os.path.join(specimen_folder, "redof" if use_edof else "edof")

    # If neither folder exists, warn and return
    if not os.path.exists(input_folder):
        warnings.warn(
            f"'{specimen_folder}' doesn't contain an `edof` or `redof` folder. Skipping this specimen folder.")
        return

    # Determine output folder
    output_folder = os.path.join(specimen_folder, f"{os.path.basename(input_folder)}_sharpen")
    os.makedirs(output_folder, exist_ok=True)

    # Process images in the selected folder
    valid_extensions = {".jpeg", ".jpg", ".png", ".bmp", ".tiff", ".gif"}
    image_files = [filename for filename in os.listdir(input_folder) if
                   filename.lower().endswith(tuple(valid_extensions))]

    if verbose:
        print(f"Input Folder: {input_folder}")
        print(f"Output Folder: {output_folder}")

    for filename in tqdm(image_files, desc=f"Sharpening {input_folder}", unit="image"):
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        image = Image.open(image_path).convert("RGB")

        # Apply unsharp mask
        unsharp_image = apply_unsharp_mask(image,
                                           radius=sharpening_kwargs.get('unsharp_radius', DEFAULT_SHARPENING_KWARGS['unsharp_radius']),
                                           percent=sharpening_kwargs.get('unsharp_percent', DEFAULT_SHARPENING_KWARGS['unsharp_percent']))

        # Apply high pass overlay
        final_image = apply_high_pass_filter(unsharp_image,
                                              radius=sharpening_kwargs.get('highpass_radius', DEFAULT_SHARPENING_KWARGS['highpass_radius']))

        final_image.save(output_path)


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
    optional_kwargs = prompt_user_for_optional_arguments(DEFAULT_SHARPENING_KWARGS)

    print(optional_kwargs)

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
