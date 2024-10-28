# Scalebar Adder for Specimen Images

This script is designed to add scalebars to specimen images automatically. It extracts the object pixel pitch from a PDF file (`ScanInformation.pdf`) located in each specimen folder, calculates the appropriate scalebar length, and adds the scalebar to each image in the specified folder. The main way to use this script is through the packaged executable (.exe) file.

## Features

- Automatically processes all images in a specified folder.
- Extracts the object pixel pitch from a `ScanInformation.pdf` file.
- Adds a scalebar with customizable parameters.

## Usage Instructions

### Running the Executable

1. **Download and Install**: Ensure that you have the packaged `.exe` file (`scalebar.exe`) available on your Windows machine inside the `dist` folder.
2. **Position the Executable**: For convenience, you may want to move the `scalebar.exe` file close to the source files you want to use, ideally in the outermost folder that contains all the specimen images.
3. **Open File Manager**: Navigate to the `dist` folder where the `scalebar.exe` file is located.
4. **Run the Executable**: Simply double-click the `scalebar.exe` file to run it.

### Input Parameters

When you run the executable, you will be prompted to enter the path for processing. You can specify the following types of paths:

- **Parent Directory**: A directory containing multiple specimen folders.
  - Example: `C:\path\to\parent_directory\`
  
- **Single Specimen Folder**: A folder that contains an `edof` subdirectory and a `ScanInformation.pdf`.
  - Example: `C:\path\to\single_specimen\`
  
- **Text File with Paths**: A text file containing paths to specimen folders, either line-separated or comma-separated.
  - Example: `C:\path\to\paths.txt`

### Optional Parameters

After specifying the path, you will be prompted for several optional parameters. You can either press Enter to use the default values or specify custom values. Here are the parameters you can customize:

| Parameter               | Description                                                            | Default Value |
|-------------------------|------------------------------------------------------------------------|---------------|
| `Scalebar height`      | Height of the scalebar in pixels                                      | 10            |
| `X margin`             | Margin from the right edge of the image in pixels                     | 50            |
| `Y margin`             | Margin from the bottom edge of the image in pixels                    | 150           |
| `Font size`            | Font size of the text below the scalebar in points                    | 100           |
| `Font style`           | Font style for the scalebar text (must be a .ttf file)               | `times.ttf`   |
| `Verbose output`       | Option for detailed output during processing (yes/no)                 | No            |

### Output

The script will create a new folder named `redof_scalebar` within each specimen folder, where it will save the images with the added scalebars.

### Important Notes

- Make sure that the `ScanInformation.pdf` is present in each specimen folder from which the script will extract the object pixel pitch.
- The script supports various image formats; ensure that your images are in one of the supported formats.
- If you wish to run the script again, you can use the same executable without needing to delete any previous output or files.

### Exiting the Command Window

After processing is complete, the command window will remain open, allowing you to see the results. You can exit by pressing Enter or closing the window manually.
