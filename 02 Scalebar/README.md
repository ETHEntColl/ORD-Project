# Scalebar Adder for Specimen Images

**Disclaimer**: This code has only been tested on Windows. Compatibility with other operating systems has not been verified.

This script is designed to automatically add scalebars to specimen images. It extracts the object pixel pitch (length a single pixel corresponds to) from a PDF file (`ScanInformation.pdf`) located in each specimen folder, calculates the appropriate scalebar length, and adds the scalebar to each image in the specified folder. The main way to use this script is through the packaged executable (.exe) file.

## Usage Instructions

### 1. Running the Executable

1. **Download and Install**: 
   - Download the `add_scalebars.exe` file from your repository by navigating to it and clicking on the file name.
   - Once the file opens, click the "Download raw file" button (it has a download symbol) in the top right corner. You may need to click this button twice to successfully save the file to your computer.

2. **Position the Executable**: 
   - For convenience, place the `add_scalebars.exe` file in a location close to the source files you plan to process. Ideally, it should be in the outermost folder that contains all the specimen images.
   - **Important Note**: If you plan to use a text file to specify paths to specimen folders, ensure that the `add_scalebars.exe` is located just outside the specimen folders listed in the text file. This is crucial for correct relative path resolution.

3. **Open File Manager**: 
   - Navigate to the folder where you saved the `add_scalebars.exe` file.

4. **Run the Executable**: 
   - Double-click `add_scalebars.exe` to launch the application. 
   - **Note**: You may need to provide permissions for the executable to run since it was downloaded from the internet.
### 2. Input Parameters

When you run the executable, you will be prompted to enter a path for processing. You can specify one of the following options:

> **Tip**: The easiest way to input the path is by **dragging and dropping** the folder or `.txt` file directly into the command line window.

- **Single Specimen Folder**: A folder that contains either an `edof` or `redof` subdirectory along with a `ScanInformation.pdf`.
  - **Example**: `C:\path\to\single_specimen\`

- **Parent Directory**: A directory containing multiple specimen folders.
  - **Example**: `C:\path\to\parent_directory\`

- **Text or CSV File with Paths**: A file listing the paths to specimen folders.
  - **Path Options**:
    - **Full Paths**: Provide the complete path for each specimen folder.
      - **Example**: `C:\path\to\specimen1`
    - **Relative Paths (Specimen names)**: If `add_scalebars.exe` is in the parent directory containing all specimen folders (e.g., `all_specimens/add_scalebars.exe`), you can list just the folder names in your text or CSV file. The program will automatically locate the specimen folders based on the parent directory.
      - **Example**: `specimen1`

  - **Formatting Options**:
    - You can format the list in either of the following ways:
      ```
      specimen1, specimen2, specimen3
      ```
      or
      ```
      specimen1
      specimen2
      specimen3
      ```

### 3. Optional Parameters

After specifying the path, you will be prompted for several optional parameters. You can press Enter to use the default values or specify custom values. Below are the customizable parameters:

| Parameter               | Description                                                                                          | Default Value  |
|-------------------------|------------------------------------------------------------------------------------------------------|----------------|
| `Corner`                | The corner of the image where the scalebar will be placed. Options: `top_left`, `top_right`, `bottom_left`, `bottom_right` | `bottom_right` |
| `Text position`         | Position of the text relative to the scalebar. Options: `above` or `below`.                         | `above`        |
| `Text alignment`        | Alignment of the text with respect to the scalebar. Options: `left`, `center`, or `right`.         | `right`        |
| `Text bar margin`       | Margin in pixels between the scalebar and the text.                                                | `20`           |
| `Scalebar height`      | Height of the scalebar in pixels.                                                                   | `10`           |
| `X margin`             | Margin from the right edge of the image in pixels.                                                  | `150`          |
| `Y margin`             | Margin from the bottom edge of the image in pixels.                                                 | `150`          |
| `Font size`            | Font size of the text below the scalebar in points.                                                 | `100`          |
| `Font style`           | Font style for the scalebar text (must be a .ttf file).                                            | `times.ttf`    |
| `Verbose output`       | Option for detailed output during processing (yes/no).                                              | `Yes`          |

### 4. Output

The script will create a new folder with the suffix `_scalebar` within each specimen folder, where it will save the images with the added scalebars.

### Important Notes

- Ensure that `ScanInformation.pdf` is present in each specimen folder from which the script will extract the object pixel pitch.
- The script supports various image formats; ensure your images are in one of the supported formats.
- If you wish to run the script again, you can use the same executable without needing to delete any previous output or files.

**Author:** Dustin Brunner (brunnedu@ethz.ch)
