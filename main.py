from calculations.Beam import Beam

# Creating an instance of Beam
beam_instance = Beam(_fc=25, _fy=400, ultimateMoment=100000000, width=400)

# You can now use methods and attributes from MainVariable as well as any additional methods or attributes defined in Beam
print(beam_instance.analysisult)
