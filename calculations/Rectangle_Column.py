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
        self._Pb, self._Mb, self._PbPhi, self._MbPhi, self._Eb, self._abal, self._cbal = self.ForceBal()

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
        check_yield = 0.003 * self._es * ((_cbal - self._dUp)/_cbal)
        fs = 0
        if check_yield >= self._fy :
            fs = self._fy
        elif check_yield < self._fy :
            fs = check_yield
        _abal = self._b1 * _cbal
        _Cc = 0.85 * self._fc * _abal * self.width
        _Tt = self.SteelDown * self.Asteel * self._fy
        _Cs = self.SteelUp * self.Asteel * (fs - 0.85 * self._fc)
        _Pb = _Cc + _Cs - _Tt
        _Aa1 = _Cc * (self._d - (_abal/2) - self._dplastis)
        _Aa2 = _Cs * (self._d - self._dUp - self._dplastis)
        _Aa3 = _Tt * (self._dplastis)
        _Mb = _Aa1 + _Aa2 + _Aa3
        _eb = _Mb/_Pb
        strainDown = ((self._d - _cbal)/_cbal) * 0.003
        phi = self.findPhi(strainDown)
        _Pbphi = phi * _Pb
        _Mbphi = phi * _Mb
        return _Pb, _Mb, _Pbphi, _Mbphi, _eb, _abal, _cbal
        
    def checkStrain(self, _e ,fs) -> float :
        _ee = _e + self._dplastis
        _Aduct = 0.425 * self._fc * self.width 
        _Bduct = 0.85 * self._fc * self.width * (_ee - self._d)
        _Cduct = (self.SteelUp * self.Asteel) * (fs - 0.85*self._fc) * (_ee - self._d + self._dUp) - (self.Asteel*self.SteelDown*fs*_ee)
        _ae = self.solve_quadratic(_Aduct, _Bduct, _Cduct)
        _ae1 = max(_ae)
        _ce = _ae1 / self._b1
        strainUp = ((_ce - self._dUp)/_ce) * 0.003
        strainDown = ((self._d - _ce)/_ce) * 0.003
        return strainUp, strainDown, _ae1
    
    def findForce(self, fs, phi, _ae, _e) :
        Cc = (0.85*self._fc*_ae*self.width)
        Cs = (self.SteelUp*self.Asteel)*(fs-0.85*self._fc)
        Tt = (self.SteelDown*self.Asteel)*(fs)
        Pn = (Cc + Cs - Tt)
        Mn = Pn * _e
        PnReduction = Pn * phi
        MnReduction = phi * Pn * _e
        #PnsReduction = phi * ((1/_ee)*(Cc*(self._d - (_ae/2)) - Cs*(self._d - self._dUp)))
        return Pn, Mn, PnReduction, MnReduction
        
    
    def findPhi(self, strain) :
        if strain < 0.002 :
            phi = 0.65
        elif strain > 0.005 : 
            phi = 0.9
        else :
            phi = 0.65 + (strain - 0.002)*(250/3)
        return phi

    def Ductile_Force(self, _e) -> float :
        if _e < self._Eb :
            raise ValueError(f"Nilai e harus lebih besar dari e balance : {self._Eb}")
        strainUp, strainDown, _ae = self.checkStrain(_e, self._fy)
        strain_yield = self._fy/self._es

        if strainUp >= strain_yield :
            print(f'{strainUp} > {strain_yield}, Tulangan Tekan sudah luluh')
            phi = self.findPhi(strainDown)
            print(phi)
            Pn, Mn, PnPhi, MnPhi = self.findForce(self._fy, phi, _ae, _e) 
            return Mn, Pn, MnPhi, PnPhi
            
        else :
            print(f'{strainUp} < {strain_yield}, Tulangan Tekan belum luluh')
            yieldNew = strainUp * self._es
            strainUp, strainDown, _ae = self.checkStrain(_e, yieldNew)
            phi = self.findPhi(strainDown)
            print(phi)
            Pn, Mn, PnPhi, MnPhi = self.findForce(yieldNew, phi, _ae, _e)
            return Mn, Pn, MnPhi, PnPhi
        
    def Brittle_force(self, _e) -> float :
        if _e > self._Eb :
            raise ValueError(f"Nilai e harus lebih kecil dari e balance : {self._Eb}")
        _ee = _e + self._dplastis
        Cc = 0.85 * self._fc * self.width #*a
        Cs = (self.SteelUp * self.Asteel) * (self._fy - 0.85*self._fc) #asumsi tulangan tekan sudah luluh
        Tt = (self.SteelDown * self.Asteel) #*fs
        i = 1
        print(Cc, Cs, Tt)
        while True:
            c_asumption = self._cbal + i
            a_asumption = c_asumption * 0.85
            _A = -((Cc)/(2*_ee)) * a_asumption**2
            _B = ((Cc * self._d) / _ee) * a_asumption
            _C = (Cs * (self._d - self._dUp)) / _ee

            Pn1 = _A + _B + _C
            fs = ((self._d - c_asumption)/c_asumption) * (0.003 * self._es)
            strainDown = ((self._d - c_asumption)/c_asumption) * (0.003)
            Pn2 = (Cc * a_asumption) + Cs - (Tt * fs)
            selisih = round(((abs(Pn2 - Pn1))/Pn2) * 100, 2)
            if selisih < 0.3 :
                Mn1 = Pn1 * _e
                phi = self.findPhi(strainDown)
                print(phi)
                Pn1Phi = Pn1 * phi
                Mn1Phi = Mn1 * phi
                print(f"ditemukan!, selisih berkisar {selisih}% dengan nilai asumsi c : {c_asumption} > {self._cbal}")
                return Mn1, Pn1, Mn1Phi, Pn1Phi
            elif i == 500:
                print(f"Dilewati!, selisih berkisar {selisih}% mengunakan c : {c_asumption}")
                break
            else :
                i += 1
                if i % 50 == 0:
                    print(f"selisih berkisar {selisih}% mengunakan c : {c_asumption}")

