import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from calculations.Rectangle_Column import RectangleColumn
from Graph.Interaction_Diagram import Interaction_Plotter

# Example usage
# Creating an instance of RectangleColumn
'''
Column attribute that you can change :

_fc = compressive streght (mpa), 
_fy = steel yield steght (mpa), 
width = width of concrete (mm), 
height = height of concrete (mm), 
cover = concrete cover size (mm), 
rebar = stirrup size (mm), 
steeldim = diameter of rebar steel for both compressive steel and tensile steel (mm), 
steelup = number of compressive steel, default = 4, 
steeldown = number of tensile steel, default = 4
'''

column_instance = RectangleColumn(_fc=27.5, _fy=400, width=350, height=550, cover=30, rebar=20.5, steeldim=29)

# Creating an instance of ColumnPlotter with the column_instance
plotter = Interaction_Plotter(column_instance)

# Generate the plot
plotter.plot()
