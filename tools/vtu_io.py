# -*- coding: utf-8 -*-
#
"""
Code pour lire les fichiers vtu
Code for read unstructured grid
   
inspirée de meshio.py
                                 audard 27/06/2017
                                 rev 0.3 11/10/2017

"""
#import logging
import os
#import sys
#import time
import numpy
import vtk
from vtk.util import numpy_support

def read_vtu_file(PATH, step=0, start=0, end=None, FieldName='grains_Particles_T'):
  """
Function that read vtu or pvtu file
input : PATH
input : step (optional) 
input : start (optional) if you want to read a range of data
input : end  (optional) if you want to read a range of data
input : FieldName (optional warning diseable the time, actually is only fitted for PeliGRIFF source)
output : array_data 
output : grid_data 
output : t time (looking in save.pvd)
  """


  def _directory(pathname,FieldName,extension):
    """Function that counts number of files
      with specific extension in directory """
    listdir = []
    list_dir = os.listdir(pathname)
    count = 0
    for file in list_dir:
      if file.endswith(extension): 
        if file.startswith(FieldName):
          count += 1
    return count

  def _read_cells(vtk_mesh):
    """ unused but I provide the prototype to do it 
    I used another package to do it call pyevtk""" 
    data = numpy.copy(vtk.util.numpy_support.vtk_to_numpy(
           vtk_mesh.GetCells().GetData()
            ))
    offsets = numpy.copy(vtk.util.numpy_support.vtk_to_numpy(
            vtk_mesh.GetCellLocationsArray()
            ))
    types = numpy.copy(vtk.util.numpy_support.vtk_to_numpy(
            vtk_mesh.GetCellTypesArray()
            ))

    vtk_to_meshio_type = {
            vtk.VTK_VERTEX: 'vertex',
            vtk.VTK_LINE: 'line',
            vtk.VTK_TRIANGLE: 'triangle',
            vtk.VTK_QUAD: 'quad',
            vtk.VTK_TETRA: 'tetra',
            vtk.VTK_HEXAHEDRON: 'hexahedron',
            vtk.VTK_WEDGE: 'wedge',
            vtk.VTK_PYRAMID: 'pyramid'
    }

        # `data` is a one-dimensional vector with
        # (num_points0, p0, p1, ... ,pk, numpoints1, p10, p11, ..., p1k, ...
        # Translate it into the cells dictionary.
    cells = {}
    for vtk_type, meshio_type in vtk_to_meshio_type.items():
        # Get all offsets for vtk_type
        os = offsets[numpy.argwhere(types == vtk_type).transpose()[0]]
        num_cells = len(os)
        if num_cells > 0:
            num_pts = data[os[0]]
            # instantiate the array
            arr = numpy.empty((num_cells, num_pts), dtype=int)
            # sort the num_pts entries after the offsets into the columns
            # of arr
            for k in range(num_pts):
                arr[:, k] = data[os+k+1]
            cells[meshio_type] = arr

    return cells


  def _read_point(data):
    """Extract numpy arrays from a VTK data set.
    """
    out = {}
    # Lecture des coordonnees 
    out['Point'] = numpy.copy(
              vtk.util.numpy_support.vtk_to_numpy(vtk_mesh.GetPoints().GetData()
               ))
    return out


  def _read_data(data):
    """Extract numpy arrays from a VTK data set.
    """
    # Go through all arrays, fetch data.
    out = {}
    for k in range(data.GetPointData().GetNumberOfArrays()):
        array = data.GetPointData().GetArray(k)
        if array:
            array_name = array.GetName()
            out[array_name] = numpy.copy(
                vtk.util.numpy_support.vtk_to_numpy(array)
                )
    return out

  pathname=str(PATH)
  # IF FILE 
  if os.path.isfile(pathname) :
    extension = os.path.splitext(pathname)[1]

    if (extension=='.pvtu'):
      reader = vtk.vtkXMLPUnstructuredGridReader()        
    else: 
      reader = vtk.vtkXMLUnstructuredGridReader()

    reader.SetFileName(pathname)
    reader.Update()
    vtk_mesh = reader.GetOutput()
    array_data = _read_data(vtk_mesh)
    #cells = _read_cells(vtk_mesh)   # diseable non usité 
    array_points = _read_point(vtk_mesh)

    ## Time reading
    if (FieldName=='saveT'):
      head, tail = os.path.split(pathname)
      #digit = filter(lambda x: x.isdigit(), tail)

      with open(head+"/save.pvd", "r") as f:
        data = f.readlines()

        tempList = [i.split('" group="')[0] for i in data]
        t = [i.split('timestep="')[-1] for i in tempList] 
        t =  map(float,t[3:len(t)-2])
    elif (FieldName!="grains_Particles_T"): 
      head, tail = os.path.split(pathname)
      #digit = filter(lambda x: x.isdigit(), tail)

      with open(head+"/"+FieldName+".pvd", "r") as f:
        data = f.readlines()

      tempList = [i.split('" group="')[0] for i in data]
      t = [i.split('timestep="')[-1] for i in tempList] 
      t =  map(float,t[3:len(t)-2])
    else :  
      t = 0 
      print("no time") 
    # IF FOLDER 
  else: 
    # just to ensure the path have '/'
    if not "/" in pathname.strip()[-1]:
      pathname = pathname+"/"

    ## Read number of vtu in directory 
    extension='.pvtu'

    ## Check first pvtu file
    number_of_vtu = _directory(pathname,FieldName+"_T",extension)
    if (number_of_vtu==0) :
      extension='.vtu'
      number_of_vtu = _directory(pathname,FieldName+"_T",extension)
    if (number_of_vtu==0) :
      print("Error no vtu or pvtu found") 
      stop

    array_data = {}
    array_points = {}
    if step > number_of_vtu+1: 
      print ('Error nbfile > number of vtu file in folder')
    elif step > 0 : 
      if end :  
        l = range(start, end, step)
      else : 
        l = range(start, number_of_vtu, step)
    else : 
      l = range(0,number_of_vtu)

    #Loop on every vtu or pvtu file
    for index in l:

      filename = pathname+FieldName+"_T"+str(index)

      # Lecture
      if (extension=='.pvtu'):
        reader = vtk.vtkXMLPUnstructuredGridReader()
      else: 
        reader = vtk.vtkXMLUnstructuredGridReader()

      reader.SetFileName(filename+extension)
      reader.Update()
      vtk_mesh = reader.GetOutput()
      point_data = _read_data(vtk_mesh)
      points = _read_point(vtk_mesh)
          #  if index==1: 
    #     grid_data  = _read_grid(vtk_mesh)

      ##Saving
      array_data[index] = point_data
      array_points[index] = points

      ##Time reading
      if (FieldName=='grains_Particles_T'):
        with open(pathname+"grains_Particles.pvd", "r") as f:
          data = f.readlines()
        tempList = [i.split('" group="')[0] for i in data]
        t = [i.split('timestep="')[-1] for i in tempList] 
        t = map(float,t[3:len(t)-2])

      elif (FieldName):
        with open(pathname+FieldName+".pvd", "r") as f:
          data = f.readlines()
        tempList = [i.split('" group="')[0] for i in data]
        t = [i.split('timestep="')[-1] for i in tempList] 
        t = map(float,t[3:len(t)-2])

      else:
        t = 0 
        print("no time") 

  return array_data,array_points,t


##End read vtu


##End
