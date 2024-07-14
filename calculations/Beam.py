from typing import Callable
from calculations._Variable import MainVariable
import math

class Beam(MainVariable):
    def __init__(self, **kwargs: int | Callable[[], int]) -> None:
        super().__init__(**kwargs)
        self._Amin = self.calculate_A(self._pmin)
        self._Abal = self.calculate_A(self._pbal)
        self._Amax = self.calculate_A(self._pmax)
        self._Ault = self.calculate_A(self._pult)

        self._nmin = self.steelDesign(self._Amin)
        self._nbal = self.steelDesign(self._Abal)
        self._nmax = self.steelDesign(self._Amax)
        self._nult = self.steelDesign(self._Ault)

        self.nminUpdated = self.checkSteel(self._nmin)
        self.nbalUpdated = self.checkSteel(self._nbal)
        self.nmaxUpdated = self.checkSteel(self._nmax)
        self.nultUpdated = self.checkSteel(self._nult)

        self.analysismin = self.concreteAnalysis(self.nminUpdated)
        self.analysisbal = self.concreteAnalysis(self.nbalUpdated)
        self.analysismax = self.concreteAnalysis(self.nmaxUpdated)
        self.analysisult = self.concreteAnalysis(self.nultUpdated)

    #find requirement steel needed for given condition (minimum,maximum,balanced,and ultimate)
    def calculate_A(self, pneed) -> float:
        Abal = pneed * self.width * self._d
        return Abal
    
    def steelDesign(self, Aneed) -> dict:
        _nmin = {key : math.ceil(Aneed/value) for key, value in self.dimparameters.items()}
        return _nmin
    
    #checking the apropiate ammount steel needed
    def checkSteel(self, n) -> dict:
        check = 0
        ncheck = {}
        for key, value in n.items():
            check = self.width - self.cover*2 - self.rebarSize*2 - value*key
            if check >= 25 :
                updatecheck = {key: value}
                ncheck.update(updatecheck)
            else:
                pass
        return ncheck
    
    #checking the concrete failure conditions
    def concreteAnalysis(self, Steelupdated):
        result = {}
        condition = ""
        for key, value in Steelupdated.items():
            dnew = self.height - self.cover - self.rebarSize - key/2
            As = (1/4)*math.pi*key**2
            Asn = As*value
            a = round((Asn*self._fy) / (self._b1*self._fc*self.width), 6)
            c = round(a/self._b1, 6)
            Et = round(((dnew-c)/c)*0.003,6)
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
                nominalMoment = round((reduction*Asn*self._fy*(dnew-(a/2)))/10**6, 6)
                update = {f"D{key}": {
                            'As': Asn, 
                            'a' : a, 
                            'c' : c, 
                            'Et' : Et, 
                            'reduction' : reduction, 
                            'condition' : condition,
                            'nominalMoment' : nominalMoment
                            }
                            }
                result.update(update)
        return result


