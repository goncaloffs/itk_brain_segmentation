# Segmentation and visualization of encephalic structures using ITK and VTK



https://github.com/goncaloffs/itk_encephalon_segmentation/assets/168077924/940b04da-b3b8-4072-a616-ca12ef6d6f82



## Description

After the manual segmentation of different encephalic regions of the BraVa dataset (cng.gmu.edu/brava) using ITK-Snap, the following methods were applied to the obtained vtk file:

### Surface meshes creation
- Threeshold: recognizes each segmented structure individually depending of the chosen limit value, defining a neighborhood of pixels to be considered in the subsequent operations;
- Opening/Closing: noise removal processes that differ from each other in the order of dilation filters (segmentation size expansion with padding of gaps and edge detection) and erosion (decrease in size with removal of fine details and edge softening).
- Outline Filter: generates an isosurface (surface with constant thickness) of the segmentation delimiting its shape;
- Smooth Filter: reduces the surface irregularity generated in the previous step.

### 3D Visualization
- Structures selection: allow the user to choose which structures he wants to view;
- Clipping: cutting the brain and cerebellum in the sagittal plane facilitates the visualization of brain structures located more internally;
- Variation in opacity: allows to focus on the location of certain structures;

### Results :)

- Exploded view of all the encephalic structures used:

![explode](https://github.com/goncaloffs/itk_encephalon_segmentation/assets/168077924/6d11d6f3-d2bd-461c-b736-e28c65d5cf80)

- Clipped meshes:

![corte](https://github.com/goncaloffs/itk_encephalon_segmentation/assets/168077924/ca1b0981-8950-425c-b060-4d9f6cbe4c3b)


- Opacity variation (with focus on the pons)

![opaco](https://github.com/goncaloffs/itk_encephalon_segmentation/assets/168077924/53c2fbae-9971-4258-988f-ab954f40b636)

## Your approach

I am making available my own segmentation files and the used code files (on a more simpler way).
Try to use your own .vtk segmentation file, I hope my code helps you!!

