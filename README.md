# ORD-Project: Tools for using 3D models of natural history specimens

[![DOI](https://zenodo.org/badge/874243001.svg)](https://doi.org/10.5281/zenodo.23566632)

This repository contains six tools developed to make 2D images and 3D models of natural history specimens easier to use, from fetching and preparing images (scale bars, sharpening, thumbnails) to viewing models and exporting them as GLB files with Blender. They were developed after interviews with 27 users of 3D data, and are designed for three groups: scientists and taxonomists who need high-quality, easy-to-handle 3D models; providers of scientific data such as digitization centres and natural history collections; and educators and outreach staff who use 3D models in teaching and exhibitions. The tools were built with specimens from the ETH Zurich Entomological Collection (ETHZ-ENT) and the ETH Earth Science Collections.

This repository is the main software output of the ETH Domain Open Research Data (ORD) Explore project "Enhancing 3D data visualization standards and practices for natural history collections" (2nd call, 09/2024 – 07/2026; main applicant: Prof. Consuelo De Moraes, ETH Zurich).

## Repository structure

The folders follow the order of a typical workflow. Each folder has its own `README.md` with detailed instructions.

| Folder | What it does |
|---|---|
| [`01 Fetcher`](01%20Fetcher) | Collects the files (e.g. `jpg`, `png`, `obj`) of a list of specimens from the collection's scan storage and copies them next to the list. Input: a text file with one specimen identifier per line, a collection number and the file types wanted. |
| [`02 Scalebar`](02%20Scalebar) | Adds a scale bar to every image of a specimen. The pixel size is read automatically from the `ScanInformation.pdf` in each specimen folder. Available as a Python script and a Windows executable (`.exe`). |
| [`03 Sharpen`](03%20Sharpen) | Sharpens specimen images (Unsharp Mask and High Pass filter) in batch and saves the results in a separate `_sharpen` folder. Available as a Python script and a Windows executable. |
| [`04 Viewer`](04%20Viewer) | Two web viewers for Gaussian Splatting models (`.ply`, `.splat`, `.ksplat`), based on [GaussianSplats3D](https://github.com/mkkellogg/GaussianSplats3D): one for quickly testing and comparing several models via drag-and-drop, and one for publishing a single model on a website. |
| [`05 Thumbnail`](05%20Thumbnail) | Automatically creates three standard views (top, bottom, side) of each GLB model in the browser, for quick quality control and as preview images. Runs as a small Flask web app. |
| [`06 Blender GLB`](06%20Blender%20GLB) | Blender script that imports the `.obj` models of many specimen folders at once, rotates them into a consistent orientation and saves them as Blender projects for GLB export. |

## Requirements

- **Operating system:** Windows (the scripts were developed and tested on Windows only).
- **Python 3** (tested with 3.12) with the packages `Pillow`, `PyPDF2`, `opencv-python`, `numpy`, `tqdm` and `flask`:
  ```
  pip install Pillow PyPDF2 opencv-python numpy tqdm flask
  ```
  The `.exe` files in `02 Scalebar` and `03 Sharpen` run without a Python installation.
- **Blender** for `06 Blender GLB`.
- A modern web browser for `04 Viewer` and `05 Thumbnail`.

**Note:** Some scripts contain file paths of the ETH Entomological Collection's own storage (e.g. `Z:\01_SCANNED_AND_PROCESSED\02 FINAL`). To use them elsewhere, change these paths at the top of the scripts (`01 Fetcher/fetcher.py`, `05 Thumbnail/app.py`, `05 Thumbnail/extract_images.py`).

## Usage

See the `README.md` in each folder for step-by-step instructions. A typical workflow is:

1. Collect the files of the specimens you need (`01 Fetcher`).
2. Add scale bars and sharpen the images (`02 Scalebar`, `03 Sharpen`).
3. Orient the 3D models in Blender and export them as GLB (`06 Blender GLB`).
4. Create preview images for quality control (`05 Thumbnail`).
5. View or publish Gaussian Splatting models on the web (`04 Viewer`).

## Related resources

- Video tutorials on 3D imaging and post-processing (ETH Entomological Collection), e.g. [3D Imaging Part I: Image acquisition](https://youtu.be/1L6bzGUL7aU), [Part II: Photogrammetry](https://youtu.be/erIhHo4RENM), [Part III: Post-processing](https://youtu.be/JZnvJ8mCnyU)
- Prototype websites: [3D Specimens](https://ethentcoll.github.io/3DSpecimens/), [EAPS3D](https://ethentcoll.github.io/EAPS3D/)
- [Instructions for capturing 3D insect specimens](https://github.com/ETHEntColl/InsectsIn3D_August_2024/tree/main/00_3D_Capturing_Instruction)

## Citation

If you use this software, please cite:

[Authors]Felsner C, Greeff M (2026). ORD-Project: Tools for using 3D models of natural history specimens. Zenodo. https://doi.org/10.5281/zenodo.23566632


## Authors and contributors

- Dustin Brunner (`02 Scalebar`, `03 Sharpen`)
- Si An Oliver Tran (`01 Fetcher`)
- Christian Felsner, Michael Greeff (project team, ETH Zurich)

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.
The viewers in `04 Viewer` include the GaussianSplats3D library by Mark Kellogg and three.js, which come with their own (MIT) licenses.

## Acknowledgement

This project was supported by the Open Research Data Program of the ETH Board.

## Contact

Entomological Collection, ETH Zurich – entomological.collection@usys.ethz.ch
