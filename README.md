# Segmentation and visualization of encephalic structures using ITK and VTK

## Description

After the manual segmentation of different encephalic regions of the BraVa dataset (cng.gmu.edu/brava) using ITK-Snap, the following methods were applied to the obtained vtk file:

### Surface meshes creation
- Threeshold: recognizes each segmented structure individually depending of the chosen limit value, defining a neighborhood of pixels to be considered in the subsequent operations;
- Opening/Closing: noise removal processes that differ from each other in the order of dilation filters (segmentation size expansion with padding of gaps and edge detection) and erosion (decrease in size with removal of fine details and edge softening).
- Outline Filter: generates an isosurface (surface with constant thickness) of the segmentation delimiting its shape;
- Smooth Filter: reduces the surface irregularity generated in the previous step.

### 3D Visualization
- Structures selection: 
