from calculations.Beam import Beam
from calculations.Rectangle_Column import RectangleColumn

# Creating an instance of Beam
column_instance = RectangleColumn(_fc=27.5, _fy=400, width = 350, height = 550, cover = 30, rebar = 20.5, steeldim = 29)

# You can now use methods and attributes from MainVariable as well as any additional methods or attributes defined in Beam
print(column_instance.roota)
print(column_instance._abal)
