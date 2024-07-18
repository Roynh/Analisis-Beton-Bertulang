from typing import Callable
from calculations._Variable import MainVariable
import math

class Beam(MainVariable):
    def __init__(self, **kwargs: int | Callable[[], int]) -> None:
        super().__init__(**kwargs)
        self.initialize_calculations()

    def initialize_calculations(self):
        """
        Initialize and compute all necessary attributes for the Beam.
        """
        # List of p values and corresponding attribute names
        p_values = [self._pmin, self._pbal, self._pmax, self._pult]
        A_attrs = ['_Amin', '_Abal', '_Amax', '_Ault']
        n_attrs = ['_nmin', '_nbal', '_nmax', '_nult']
        updated_n_attrs = ['nminUpdated', 'nbalUpdated', 'nmaxUpdated', 'nultUpdated']
        layer_n_attrs = ['layermin', 'layerbal', 'layermax', 'layerult']
        dnew_steel_attrs = ['dnewmin', 'dnewbal', 'dnewmax', 'dnewult']
        Anew_steel_attrs = ['Anewmin', 'Anewbal', 'Anewmax', 'Anewult']
        analysis_attrs = ['Analysismin', 'Analysisbal', 'Analysismax', 'Analysisult']

        for p, A_attr, n_attr, updated_n_attr, layer_n_attr, dnew_steel_attr, analysis_attr, Anew_steel_attr in zip(
                p_values, A_attrs, n_attrs, updated_n_attrs, layer_n_attrs, dnew_steel_attrs, analysis_attrs, Anew_steel_attrs):
            
            A_value = self.calculate_A(p)
            setattr(self, A_attr, A_value)
            
            n_value = self.steelDesign(A_value)
            setattr(self, n_attr, n_value)

            updated_n_value, layer_n_value = self.SteelOrganizer(n_value, n_attr)
            setattr(self, updated_n_attr, updated_n_value)
            setattr(self, layer_n_attr, layer_n_value)

            get_dnew_oneSteel, get_Anew_oneSteel = self.calculate_dnew(updated_n_value)
            setattr(self, dnew_steel_attr, get_dnew_oneSteel)
            setattr(self, Anew_steel_attr, get_Anew_oneSteel)

            analysis_one_value = self.concreteAnalysis(updated_n_value, get_dnew_oneSteel, get_Anew_oneSteel)
            setattr(self, analysis_attr, analysis_one_value)

    #find requirement steel needed for given condition (minimum,maximum,balanced,and ultimate)
    def calculate_A(self, pneed) -> float:
        Abal = pneed * self.width * self._d
        return Abal
    
    def steelDesign(self, Aneed) -> dict:
        _nmin = {key : math.ceil(Aneed/value) for key, value in self.dimparameters.items()}
        return _nmin
    
    def find_n(self, width, cover, rebar, steeldiameter, space):
        n = 0
        while True:
            # Calculate the expression
            expression_value = width - cover * 2 - rebar * 2 - steeldiameter * n - space * (n + 1)
            
            # Check if the expression is greater than zero
            if expression_value < 0:
                return n  # Return the value of n that satisfies the condition
            
            # Increment n for the next iteration
            n += 1

    def SteelOrganizer(self, twoSteelDict:dict, name:str):
        nCheck = {}
        layerCheck = []
        if not twoSteelDict:
            return {}
        else:
            for key, value in twoSteelDict.items():
                n_max_per_layer = 0
                layer_needed = 0
                remaining_steel = 0
                n_max_per_layer = self.find_n(self.width, self.cover, self.rebar, key, 25)
                layer_needed = value // n_max_per_layer
                remaining_steel = value % n_max_per_layer
                if layer_needed > 0 :
                    steel_list = [n_max_per_layer] * int(layer_needed) + [remaining_steel]
                    updatecheck = {key: steel_list}
                    layerCheck.append(len(steel_list))
                    nCheck.update(updatecheck)
                else:
                    updatecheck = {key: [value]} 
                    layerCheck.append(1) 
                    nCheck.update(updatecheck) 
        return nCheck, layerCheck
    
    def calculate_dnew(self, organizedSteel:dict) -> float:
        Atot = 0
        ytot = 0
        dnew_list = []
        Anew_list = []
        first_loop = True
        for key, value in organizedSteel.items():

            while True:
                y = self.cover + self.rebar
                Atot = 0
                ytot = 0
                for n in value :
                    if first_loop:
                        y +=  key/2
                        first_loop = False
                    else:
                        y += 25 + key
                    ytot += n * (1/4)*math.pi*key**2 * y
                    Atot += (1/4)*math.pi*key**2 * n
                dnew = self.height - (ytot/Atot)
                dnew_list.append(dnew)
                Anew_list.append(Atot)
                first_loop = True
                break
        return dnew_list, Anew_list
    
    #checking the concrete failure conditions
    def concreteAnalysis(self, Steelupdated, dnew, Anew):
        result = {}
        condition = ""

        for d, A, (key, value) in zip(dnew, Anew, Steelupdated.items()):
            a = round((A*self._fy) / (self._b1*self._fc*self.width), 6)
            c = round(a/self._b1, 6)
            Et = round(((d-c)/c)*0.003,6)

            if Et < 0.004 and Et >= 0.002 :
                condition = "Tensile"
                reduction = 0.65
            elif Et >= 0.004 and Et < 0.005:
                condition = "Transition"
                reduction = 0.65 + (Et - 0.002)*(250/3)
            elif Et >= 0.005 :
                condition = "Ductile"
                reduction = 0.9

            if Et >= 0.002 :

                nominalMoment = round((reduction*A*self._fy*(d-(a/2)))/10**6, 6)
                update = {f"D{key}": {
                            'As': A, 
                            'a' : a, 
                            'c' : c, 
                            'd' : d,
                            'Et' : Et, 
                            'reduction' : reduction, 
                            'condition' : condition,
                            'nominalMoment' : nominalMoment,
                            'NumberOfSteel' : value  
                            }
                            }
                result.update(update)

        return result

    


