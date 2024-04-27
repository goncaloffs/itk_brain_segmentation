# -*- coding: utf-8 -*-
# OPACITY VARIATION

import itk
import os
import vtk
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget

dataset = 'BH0018'
inputFilename = '../input/%s_MAN_labels.vtk' % dataset

displayNames = ['Brain', 'Cerebelum', 'Callosum', 'Fornix', 'Thalamus', 'Midbrain',
                'Pons', 'Medulla', 'Lateral Ventricles', '3rd Ventricle', '4th Ventricle']

color_mapping = {
    '../output/%s_label1_mask.vtk' % dataset: (1.0, 0.0, 0.0),      # Cerebrum -> red
    '../output/%s_label2_mask.vtk' % dataset: (0.0, 1.0, 0.0),      # Cerebellum -> green
    '../output/%s_label4_mask.vtk' % dataset: (1.0, 1.0, 0.0),      # Callosum -> yellow
    '../output/%s_label5_mask.vtk' % dataset: (0.0, 1.0, 1.0),      # Fornix -> light blue
    '../output/%s_label6_mask.vtk' % dataset: (1.0, 0.0, 1.0),      # Thalamus -> pink
    '../output/%s_label7_mask.vtk' % dataset: (1.0, 0.584, 0.0),    # Midbrain -> orange
    '../output/%s_label8_mask.vtk' % dataset: (0.71, 0.6, 0.459),   # Pons -> brown
    '../output/%s_label9_mask.vtk' % dataset: (1.0, 0.937, 0.835),  # Medulla -> beige
    '../output/%s_label10_mask.vtk' % dataset: (0.263, 0.761, 0.576),# Lateral Ventricles -> bluish green
    '../output/%s_label11_mask.vtk' % dataset: (0.463, 0.584, 0.161),# 3rd Ventricle -> dark green
    '../output/%s_label12_mask.vtk' % dataset: (1.0, 0.416, 0.592)   # 4th Ventricle-> light pink
}

# Here you can change the opacity numbers from 0 to 1 for each structure as you wish. In this case, I wanted to focus on Pons
# so I gave it the value 1.0 while the other sturctures have a smaller value.
opacity_mapping = {
    '../output/%s_label1_mask.vtk' % dataset: 0.1,  #Cerebrum
    '../output/%s_label2_mask.vtk' % dataset: 0.1,  # Cerebellum
    '../output/%s_label4_mask.vtk' % dataset: 0.2,  # Callosum
    '../output/%s_label5_mask.vtk' % dataset: 0.2,  # Fornix
    '../output/%s_label6_mask.vtk' % dataset: 0.2,  # Thalamus
    '../output/%s_label7_mask.vtk' % dataset: 0.2,  # Midbrain
    '../output/%s_label8_mask.vtk' % dataset: 1.0,  # Pons
    '../output/%s_label9_mask.vtk' % dataset: 0.2,  # Medulla
    '../output/%s_label10_mask.vtk' % dataset: 0.2,  # Lateral Ventricles
    '../output/%s_label11_mask.vtk' % dataset: 0.2,  # 3rd Ventricle
    '../output/%s_label12_mask.vtk' % dataset: 0.2,  # 4th Ventricle
}

def create_surface_mesh():
    Dimension = 3
    InputPixelType = itk.US
    OutputPixelType = itk.US
    InputImageType = itk.Image[InputPixelType, Dimension]
    OutputImageType = itk.Image[OutputPixelType, Dimension]

    outsideValue = 0
    insideValue = 1

    print("Reading:", inputFilename)
    reader = itk.ImageFileReader[InputImageType].New()
    reader.SetFileName(inputFilename)
    reader.Update()


    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    
    mesh_files = []

    for label in range(1, 13):
        if label == 3:
            continue
        
        labelOutputFilename = "../output/%s_label%d_mask.vtk" % (dataset, label)
        mesh_files += [labelOutputFilename]
        
        if not os.path.exists(labelOutputFilename):
            print("Binary Threshold for label:", label)
        
            threshold = itk.BinaryThresholdImageFilter[InputImageType, OutputImageType].New()
            threshold.SetLowerThreshold(label)
            threshold.SetUpperThreshold(label)
            threshold.SetOutsideValue(outsideValue)
            threshold.SetInsideValue(insideValue)
            threshold.SetInput(reader.GetOutput())
            threshold.Update()

            writer = itk.ImageFileWriter[InputImageType].New()
            writer.SetInput(threshold.GetOutput())
            writer.SetFileName('temp.vtk')
            writer.Update()
    
            vtkreader = vtk.vtkStructuredPointsReader()
            vtkreader.SetFileName('temp.vtk')
            vtkreader.Update()
    
            vtkimg = vtk.vtkImageData()
            vtkimg = vtkreader.GetOutput()
    
            isovalue = 0.5
            contourFilter = vtk.vtkContourFilter()
            contourFilter.ComputeNormalsOff()
            contourFilter.SetValue(0, isovalue)
            contourFilter.SetInputData(vtkimg)
            contourFilter.Update()
    
            isosurface = vtk.vtkPolyData()
            isosurface = contourFilter.GetOutput()
    
            connectivity = vtk.vtkPolyDataConnectivityFilter()
            connectivity.SetInputData(isosurface)
            connectivity.SetExtractionModeToLargestRegion()
            connectivity.Update()
    
            # Create a smoother for the output of the connectivity filter
            smoother = vtk.vtkSmoothPolyDataFilter()
            smoother.SetInputData(connectivity.GetOutput())
            smoother.SetNumberOfIterations(30)  # Adjust the number of iterations as needed
            smoother.SetRelaxationFactor(0.2)  # Adjust the relaxation factor as needed
            smoother.FeatureEdgeSmoothingOff()  # Disable smoothing along sharp edges (optional)
            smoother.BoundarySmoothingOff()  # Enable smoothing along mesh boundaries (optional)
            smoother.Update()

            # Save the mesh with a unique file name based on the label
            print("Writing:", labelOutputFilename)
            writer = vtk.vtkPolyDataWriter()
            writer.SetInputData(smoother.GetOutput())
            writer.SetFileName(labelOutputFilename)
            writer.Write()
            
        else:
            print("Output file already exists:", labelOutputFilename)
            
    return mesh_files


mesh_files = create_surface_mesh()
    

def render_mesh_files():

    ren.RemoveAllViewProps()  # Remove all previous actors from the renderer

    for inputFilename in mesh_files:
        # Read VTK polydata
        print('Reading:', inputFilename)
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(inputFilename)
        reader.Update()

        polydata = vtk.vtkPolyData()
        polydata = reader.GetOutput()

        # Create mappers
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)
        mapper.ScalarVisibilityOff()

        # Create actors, and connect mappers
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        color = color_mapping.get(inputFilename, (1, 1, 1)) 
        actor.GetProperty().SetColor(color) 
    
        opacity = opacity_mapping.get(inputFilename, 1) 
        actor.GetProperty().SetOpacity(opacity)

        ren.AddActor(actor)

    # Add legend
    legend = vtk.vtkLegendBoxActor()
    legend.SetNumberOfEntries(len(mesh_files))
    legend.SetPosition(0.8, 0.1)  # Adjust the position of the legend

    for i, inputFilename in enumerate(mesh_files):
        color = color_mapping.get(inputFilename, (1, 1, 1))
        legend.SetEntryColor(i, color)
        displayName = displayNames[mesh_files.index(inputFilename)]
        legend.SetEntryString(i, displayName)

    ren.AddActor(legend)

    # Create a render window and render window interactor
    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renwin)
    
    style = vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)
    
    iren.SetRenderWindow( renwin )
    cam_orient_manipulator = vtkCameraOrientationWidget()
    cam_orient_manipulator = vtkCameraOrientationWidget()
    cam_orient_manipulator.SetParentRenderer(ren)
    # Enable the widget.
    cam_orient_manipulator.On()

    # Render the scene and interact
    renwin.Render()
    iren.Initialize()
    iren.Start()

# Create a renderer
ren = vtk.vtkRenderer()
ren.SetBackground(0, 0, 0)  # RGB colors for the background


# # Create a render window
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer( ren )

render_mesh_files()
            
print('EOF.')
