#!/bin/sh
echo 'test: Read vtu file '
echo '----------'
echo 'sequential'
echo ' test command python Read_vtu_file.py data_example/ test1' 
time python2.7 Read_vtu_file.py data_example/ test1
echo ' '
echo ' test command python Read_vtu_file.py data_example/test2_T2.vtu' 
time python2.7 Read_vtu_file.py data_example/test2_T2.vtu
echo ' '
echo 'Done' 
