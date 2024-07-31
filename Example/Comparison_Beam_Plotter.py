import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from calculations.Beam import Beam
from Graph.Graph_Bar import DynamicBarChart

# Creating an instance of RectangleColumn
beam_instance = Beam(_fc=27.5, _fy=400, width=350, height=550, cover=30, rebar=20.5, steeldim=29)
analysis_attrs = ['Analysismin', 'Analysisbal', 'Analysismax', 'Analysisult']
value_attrs = ['As','a','c','d','Et','reduction','condition','nominalMoment','NumberOfSteel']

'''
change beam_instance.Analysismin to any analysis_attrs you want
free to change analysis value_attrs to any value exept 'condition'
you can change xlabel and ylabel too
'''
beam_dict = beam_instance.Analysismin
steel_keys = beam_dict.keys()
values_comparison = []
title = analysis_attrs[0]
xlabel = 'Steel Diameters'
ylabel = 'As'

for key in steel_keys :
    value = beam_dict[key]['As']
    values_comparison.append(value)

DynamicBarChart(steel_keys, values_comparison, title, xlabel, ylabel)
