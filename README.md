# Segmentation and visualization of encephalic structures using ITK and VTK




https://github.com/goncaloffs/itk_encephalon_segmentation/assets/168077924/ad462bd9-a1d7-4b29-b54b-a8021d791575




## Description

After the manual segmentation of different encephalic regions (Brain, Cerebelum, Callosum, Fornix, Thalamus, Midbrain, Pons, Medulla, Lateral Ventricles, 3rd Ventricle and 4th Ventricle) of the BraVa BH0018 angiography dataset (cng.gmu.edu/brava) using ITK-Snap, the following methods were applied to the obtained vtk file:

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

## Your own approach

I am making available my own segmentation files and the used python code files.
Try to use your own .vtk segmentation files, I hope my code helps you!!

