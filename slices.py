# -*- coding: utf-8 -*-

"""
Created on Sat Jun  3 01:06:13 2023

@author: PC
"""

import itk
import os
import vtk
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
from vtk import vtkFillHolesFilter

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
            smoother.SetNumberOfIterations(40)  # Adjust the number of iterations as needed
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
        
        label = int(inputFilename.split("_label")[1].split("_")[0])
        
        plane_origin = (0, 0, 0)  # Set the origin of the cutting plane
        plane_normal = (1, 0, 0)  # Set the normal vector of the cutting plane
        
        plane = vtk.vtkPlane()
        plane.SetOrigin(plane_origin)
        plane.SetNormal(plane_normal)
    
        # Read VTK polydata
        print('Reading:', inputFilename)
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(inputFilename)
        reader.Update()

        polydata = vtk.vtkPolyData()
        polydata = reader.GetOutput()

        color = color_mapping.get(inputFilename, (1, 1, 1))  
        
        # Create a vtkClipPolyData object for clipping
        clipper = vtk.vtkClipPolyData()
        clipper.SetClipFunction(plane)  # Set the clipping plane
        clipper.SetInputData(polydata)  # Set the input polydata
        
        # Create a mapper for the clipped geometry
        mapper = vtk.vtkPolyDataMapper()
        
        if label in [1, 2]:
            clipper.Update()
            mapper.SetInputConnection(clipper.GetOutputPort())
            
            # Fill holes in the clipped mesh
            fill_holes_filter = vtkFillHolesFilter()
            fill_holes_filter.SetInputData(clipper.GetOutput())
            fill_holes_filter.SetHoleSize(1000.0)  # Adjust the hole size as needed
            fill_holes_filter.Update()

            # Update the mapper with the filled holes mesh
            mapper.SetInputData(fill_holes_filter.GetOutput())
        else:
            mapper.SetInputData(polydata)
        
        mapper.ScalarVisibilityOff()
            
        # Create an actor for the clipped geometry
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetLineWidth(1)
        
        # Add the clipped actor to the renderer
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

    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renwin)
    
    iren.SetRenderWindow( renwin )
    cam_orient_manipulator = vtkCameraOrientationWidget()
    cam_orient_manipulator = vtkCameraOrientationWidget()
    cam_orient_manipulator.SetParentRenderer(ren)
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