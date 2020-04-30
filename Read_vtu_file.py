# -*- coding: utf-8 -*-
#
"""
Simple module to read vtu file
                                     F.Audard     release: 02/03/2018
                                                  python3 30/05/2020                                     

Example:
python Read_vtu_file.py data_example/ test1

please for display on Paraview use Point Gaussian and put the radius in Properties
or you can use glyph filter and set a value for scale factor
"""

import sys
#import numpy as np
from tools.vtu_io import *

#==================================================================
#
# |  \/  |    / \    |_ _| | \ | |
# | |\/| |   / _ \    | |  |  \| |
# | |  | |  / ___ \   | |  | |\  |
# |_|  |_| /_/   \_\ |___| |_| \_|
#
#==================================================================
if (sys.argv[1] == "-h") or (sys.argv[1] == "--help") \
   or (sys.argv[1] == "-help") or (sys.argv[1] == "--h"):
  print("  arg1 = root of particle folder")
  print("  arg1 = Field Name of pvd file")
  print("  look inside the script for more inputs")
else:
#==================================================================
# 0. Read vtu file
#==================================================================
#- Get path
  path_ = sys.argv[1]
  #step =
  #start =
  #end =

#- Read vtu information
  if len(sys.argv) > 2:
     # Example if you want to read all file
    FieldName_ = sys.argv[2]
    array_data, array_points, t = \
    read_vtu_file(path_, FieldName=FieldName_)
   #  array_data,array_points,t = \
   # read_vtu_file(path_,step=step,start=start,
   #  end=end,FieldName='grains_Particles_T')
  else:
    # Example if you want to read one specific file
    array_points = {}
    t = {}
    array_data, array_points[0], t[0] = read_vtu_file(path_)

  print(list(map(float, t))) # time mapping change in python3
#- Display information 
  for key in array_points.keys():
    Px = array_points[key]["Point"][:, 0]
    Py = array_points[key]["Point"][:, 1]
    Pz = array_points[key]["Point"][:, 2]
    print(key, t, Px[0])
#      print(key, t[key], Px[0], Py[0], Pz[0])
