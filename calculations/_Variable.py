from typing import Callable, Union
import math

class MainVariable:

    # Defining concrete design
    def __init__(self, **kwargs: Union[int, Callable[[], int]]) -> None:

        diameters = [10, 13, 19, 22, 25, 29, 32, 36]
        self.dimparameters = {d: int((1/4) * math.pi * d**2) for d in diameters}

        self.parameters = {
            '_fc': self.getFc,
            '_fy': self.getFy,
            '_es': self.getEs,
            'width': self.getWidth,
            'height': self.getHeight,
            'steeldim' : self.getdim,
            'cover' : self.getcover,
            'ultimateMoment': self.calculateMoment,
            'rebarSize' : self.getRebar
        }

        # Update the parameters with any provided values
        for key, value in kwargs.items():
            self.parameters[key] = value

        for key, value in self.parameters.items():
            if callable(value):
                setattr(self, key, value())
            else:
                setattr(self, key, value)

        self._b1 = self.getB1()
        self._d = self.calculate_d()
        self._pbal = self.calculatePbal()
        self._pmax = self.calculatePmax()
        self._pmin = self.calculate_pmin()
        self._pult = self.calculate_pult()
    
    def getFc(self) -> int:
        return 25  # Default FC = 25 Mpa

    def getFy(self) -> int:
        return 400  # Default Fy = 400 Mpa

    def getEs(self) -> int:
        return 200000  # Default Es = 200000

    def getWidth(self) -> int:
        return 300  #mm Default Width

    def getHeight(self) -> int:
        return 600  #mm Default Height
    
    def getdim(self) -> int :
        return 16 #mm default steel diameters
    
    def getcover(self) -> int :
        return 10 #mm default concrete covers
    
    def getRebar(self) -> int :
        return 10 #mm default Rebar Diameter
    
    def calculate_d(self) -> float:
        dSteel = self.steeldim
        _d = self.height - self.cover - self.rebarSize - dSteel/2
        return _d

    @property
    def _fc(self) -> int:
        if self.__dict__['_fc'] is None:
            self.__dict__['_fc'] = self.getFc()
        return self.__dict__['_fc']
    
    @_fc.setter
    def _fc(self, value: int) -> None:
        self.__dict__['_fc'] = value

    @property
    def _fy(self) -> int:
        if self.__dict__['_fy'] is None:
            self.__dict__['_fy'] = self.getFy()
        return self.__dict__['_fy']

    @_fy.setter
    def _fy(self, value: int) -> None:
        self.__dict__['_fy'] = value

    @property
    def _es(self) -> int:
        if self.__dict__['_es'] is None:
            self.__dict__['_es'] = self.getEs()
        return self.__dict__['_es']

    @_es.setter
    def _es(self, value: int) -> None:
        self.__dict__['_es'] = value

    @property
    def _b1(self) -> float:
        if not hasattr(self, '__b1'):
            self.__b1 = self.getB1()
        return self.__b1
    
    @_b1.setter
    def _b1(self, value: int) -> None:
        self.__dict__['_b1'] = value

    @property
    def _pbal(self) -> float:
        if not hasattr(self, '__pbal'):
            self.__pbal = self.calculatePbal()
        return self.__pbal
    
    @_pbal.setter
    def _pbal(self, value: int) -> None:
        self.__dict__['_pbal'] = value

    @property
    def _pmax(self) -> float:
        if not hasattr(self, '__pmax'):
            self.__pmax = self.calculatePmax()
        return self.__pmax
    
    @_pmax.setter
    def _pmax(self, value: int) -> None:
        self.__dict__['_pmax'] = value

    @property
    def rebarSize(self) -> float:
        if not hasattr(self, '_rebarSize'):
            self._rebarSize = self.getRebar()
        return self._rebarSize
    
    @rebarSize.setter
    def rebarSize(self, value: int) -> None:
        self.__dict__['rebarSize'] = value

    @property
    def _d(self) -> float:
        if not hasattr(self, '__d'):
            self.__d = self.calculate_d()
        return self.__d
    
    @_d.setter
    def _d(self, value: int) -> None:
        self.__dict__['_d'] = value
    
    # ACI 318M-05
    def getB1(self) -> float:
        if self._fc < 17:
            raise ValueError("Fc value cannot be defined lower than 17")
        elif 17 <= self._fc < 28:
            return 0.85
        elif 28 <= self._fc < 56:
            return 0.85 - 0.05 * ((self._fc - 28) / 7)
        else:
            return 0.65

    def calculatePbal(self) -> float:
        b1 = self._b1
        pbal = 0.85 * b1 * (self._fc / self._fy) * (0.003 / (0.003 + (self._fy / self._es)))
        pbal = round(pbal, 6)
        return pbal

    #For ductile condition
    def calculatePmax(self) -> float:
        pbal = self._pbal
        pmax = pbal*((0.003+(self._fy/self._es))/0.007)
        pmax = round(pmax, 6)
        return pmax
    
    def calculate_pult(self) -> float:
        ultimatemoment = self.ultimateMoment/0.9
        _Qcon = (1.7/(0.9*self._fc))*(ultimatemoment/(self.width*self._d**2))
        pdesign = (self._fc/self._fy)*(0.85 - (math.sqrt(0.85**2 - _Qcon)))
        return pdesign
    
    def calculate_pmin(self) -> float:
        pmin = 0
        if self._fc <= 30 :
            pmin = 1.4 / self._fy
        elif self._fc > 30 :
            pmin = math.sqrt(self._fc/(4*self._fy))
        return pmin

    def calculateMoment(self) -> float:
        reduction = 0.9
        pmax = self._pmax
        ru = pmax * self._fy * (1 - ((pmax*self._fy)/(1.7*self._fc)))
        mn = reduction * ru * self.width * self._d**2
        mn = round(mn, 6)
        return mn