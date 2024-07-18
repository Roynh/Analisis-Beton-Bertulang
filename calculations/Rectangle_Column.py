from typing import Callable
from calculations._Variable import MainVariable
import math

class RectangleColumn(MainVariable):
    def __init__(self, **kwargs: int | Callable[[], int]) -> None:
        super().__init__(**kwargs)

        self.parameters = {
            'SteelUp': self.getUp,
            'SteelDown': self.getDown,
        }

        for key, value in kwargs.items():
            self.parameters[key] = value

        for key, value in self.parameters.items():
            if callable(value):
                setattr(self, key, value())
            else:
                setattr(self, key, value)
        
        self._dUp = self.cover + self.rebar + self.steeldim/2
        self._dplastis = (self.height/2) - self.cover - self.rebar - self.steeldim/2
        self._Pb, self._Mb, self._Eb, self._abal = self.ForceBal()
        self.roota = self.Ductile_Force(self._Eb)

    def getUp(self) -> int:
        return 4  # Default 4 tulangan

    def getDown(self) -> int:
        return 4  # Default 4 tulangan

    def solve_quadratic(self, a, b, c):
        # Menghitung diskriminan
        D = b**2 - 4*a*c
        
        # Memeriksa nilai diskriminan
        if D > 0:
            # Dua akar real dan berbeda
            root1 = (-b + math.sqrt(D)) / (2*a)
            root2 = (-b - math.sqrt(D)) / (2*a)
            return root1, root2
        elif D == 0:
            # Satu akar real
            root = -b / (2*a)
            return root,
        else:
            # Dua akar kompleks
            realPart = -b / (2*a)
            imaginaryPart = math.sqrt(-D) / (2*a)
            return (realPart + imaginaryPart * 1j, realPart - imaginaryPart * 1j)
    
    def ForceBal(self) -> float :
        _cbal = (0.003 / (0.003 + (self._fy/self._es)))*self._d
        _abal = self._b1 * _cbal
        _Cc = 0.85 * self._fc * _abal * self.width
        _Tt = self.SteelDown * self.Asteel
        _Cs = self.SteelUp * self.Asteel * (self._fy - 0.85 * self._fc)
        _Pb = _Cc + _Cs - _Tt
        _Aa1 = _Cc * (self._d - (_abal/2) - self._dUp)
        _Aa2 = _Cs * (self._d - self._dUp - self._dplastis)
        _Aa3 = _Tt * (self._dplastis)
        _Mb = _Aa1 + _Aa2 + _Aa3
        _eb = _Mb/_Pb
        print(self._d, self._dUp, self._dplastis)
        return _Pb, _Mb, _eb, _abal

    def Ductile_Force(self, _e) -> float :
        _ee = _e + self._dplastis
        _Aduct = 0.425 * self._fc * self.width 
        _Bduct = 0.85 * self._fc * self.width * (_ee - self._d)
        _Cduct = (self.SteelUp * self.Asteel) * (self._fy - 0.85*self._fc) * (_ee - self._d + self._dUp) - (self.Asteel*self.SteelDown*self._fy*_ee)
        _ae = self.solve_quadratic(_Aduct, _Bduct, _Cduct)
        print(_Aduct, _Bduct, _Cduct)
        _ae1 = max(_ae)
        _ce = _ae1 / self._b1
        strain = ((_ce - self._d)/_ce) * 0.003
        strain_yield = self._fy/self._es

        if strain >= strain_yield :
            print('Tulangan sudah luluh')
        else :
            print('Tulangan belum luluh')

        return _ae

