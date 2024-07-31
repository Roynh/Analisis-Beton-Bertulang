import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from calculations.Beam import Beam

# Creating an instance of RectangleColumn
beam_instance = Beam(_fc=27.5, _fy=400, width=350, height=550, cover=30, rebar=20.5, steeldim=29)
analysis_attrs = ['Analysismin', 'Analysisbal', 'Analysismax', 'Analysisult']
print(beam_instance.Analysismin)

'''
output every concrete attribute according to the size of steel diameters
change analysismin to any analysis_attrs depending you need
'''