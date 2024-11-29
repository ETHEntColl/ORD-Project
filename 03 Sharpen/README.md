# Image Sharpening Tool

**Disclaimer**: This code has been tested primarily on Windows. Compatibility with other operating systems is not guaranteed.

This script is designed to enhance image sharpness through a combination of sharpening filters, including Unsharp Mask and High Pass Filter. The tool processes images stored in specimen folders and creates sharpened versions in a separate output directory. It is intended for automated processing of multiple specimen image sets.

## Usage Instructions

### 1. Running the Executable

1. **Download**: 
   1. [Navigate to the `sharpen.exe` file in this repository](https://github.com/ETHEntColl/OCR-Project/blob/main/02%20Scalebar/add_scalebars.exe).   
   2. Click the "Download raw file" button (it has a download symbol) in the top right corner. You may need to click the button twice to successfully save the file to your computer.

2. **Position the Executable**: 
   - If you plan to use a text or CSV file with specific specimen names, place the `sharpen.exe` in the parent folder of those specimen folders for correct relative path resolution. Otherwise, you can place it wherever you want.

3. **Run the Executable**: 
   - Double-click `sharpen.exe` to launch the executable. 
   - **Note**: You may need to provide permissions for the executable to run since it was downloaded from the internet.

### 2. Input Parameters

When prompted, you can specify the path for processing. You may provide one of the following:

- **Single Specimen Folder**: A folder containing either an `edof` or `redof` subdirectory with images to be sharpened.
  - **Example**: `C:\path\to\single_specimen\`

- **Parent Directory**: A directory containing multiple specimen folders, each with `edof` or `redof` subdirectories.
  - **Example**: `C:\path\to\parent_directory\`

- **Text or CSV File with Paths**: A file listing paths to specimen folders, either as full paths or relative paths.
  - **Formatting Options**:
    - Comma-separated: `folder1, folder2, folder3`
    - Line-separated:
      ```
      folder1
      folder2
      folder3
      ```

### 3. Optional Parameters

After specifying the path, you can customize various parameters or press Enter to use default values. The following parameters are available for customization:

| Parameter               | Description                                                                                      | Default Value |
|-------------------------|--------------------------------------------------------------------------------------------------|---------------|
| `Use EDOF`             | Process images from the `edof` folder. If `False`, uses the `redof` folder.                     | `True`        |
| `Unsharp Radius`        | Radius for the Unsharp Mask, controlling the blurring before sharpening.                        | `1.5`         |
| `Unsharp Percent`       | Strength of the sharpening effect, specified as a percentage.                                   | `150`         |
| `High Pass Radius`      | Radius for the High Pass filter, influencing detail retention.                                  | `1`           |
| `Verbose Output`        | Enable detailed output during processing.                                                      | `True`        |

### 4. Output

The tool creates a new folder in each specimen folder, named with the suffix `_sharpen`. Sharpened versions of the input images are saved in this folder.

### Example Usage

1. **Single Specimen Folder**:
   - Provide the path to a folder with either an `edof` or `redof` subdirectory:  
     `C:\path\to\single_specimen\`

2. **Parent Directory**:
   - Provide the path to a directory containing multiple specimen folders:  
     `C:\path\to\parent_directory\`

3. **Path File**:
   - Create a text file (`paths.txt`) listing paths to the folders:  
     ```
     C:\path\to\specimen1
     C:\path\to\specimen2
     ```

4. **Customize Parameters**:
   - During the execution, you will be prompted to customize sharpening parameters or use defaults.

### Important Notes

- Ensure your input folders contain either an `edof` or `redof` subdirectory.
- Supported image formats include `.jpeg`, `.jpg`, `.png`, `.bmp`, `.tiff`, and `.gif`.
- The output folder will not overwrite existing images unless explicitly handled.

**Author**: Dustin Brunner (brunnedu@ethz.ch)
