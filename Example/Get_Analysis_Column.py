import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from calculations.Rectangle_Column import RectangleColumn

'''
Column attribute that you can change :

_fc = compressive streght (mpa), 
_fy = steel yield steght (mpa), 
width = width of concrete (mm), 
height = height of concrete (mm), 
cover = concrete cover size (mm), 
rebar = stirrup size (mm), 
steeldim = diameter of rebar steel for both compressive steel and tensile steel (mm), 
SteelUp = number of compressive steel, default = 4, 
SteelDown = number of tensile steel, default = 4
'''

# Creating an instance of RectangleColumn
column_instance = RectangleColumn(_fc=27.5, _fy=400, width=350, height=550, cover=30, rebar=20.5, steeldim=29, SteelUp=4, SteelDown=4)
bal = column_instance.ForceBal()
bri = column_instance.Brittle_force(_e=250)
duc= column_instance.Ductile_Force(_e=500)
print(f"Balance = Pb : {bal[0]}, Mb : {bal[1]}, Pb*phi : {bal[2]}, Mb*Phi : {bal[3]}, e : {bal[4]}, a : {bal[5]}, c : {bal[6]}") #get attribute of Balance values
print(f"Brittle = P : {bri[0]}, M : {bri[1]}, P*phi : {bri[2]}, M*Phi{bri[3]}") #get attribute of Brittle values
print(f"Tensile = P : {duc[0]}, M : {duc[1]}, P*phi : {duc[2]}, M*Phi{duc[3]})") #get attribute of Ductile values


'''
output every concrete attribute according to the size of steel diameters
change analysismin to any analysis_attrs depending you need
'''