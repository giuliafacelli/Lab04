from dataclasses import dataclass

@dataclass
class Cabina:
    def __init__(self, codice, letti, ponte, prezzo):
        self.codice = codice
        self.letti = int(letti)
        self.ponte = int(ponte)
        self.prezzo = float(prezzo)
        self.disponibile = True
        self.passeggero = None

        @property
        def prezzo(self):
            return self._prezzo
        @prezzo.setter
        def prezzo(self, prezzo):
            self._prezzo = float(prezzo)

    def assegna(self, passeggero):
        if not self.disponibile:
            raise Exception(f'La cabina {self.codice} non è disponibile.')
        self.disponibile = False
        self.passeggero = passeggero

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Non disponibile" + f" | Cliente --> {self.passeggero}"
        return f'{self.codice}| Standard - Letti : {self.letti} - Ponte: {self.ponte} - Prezzo: {self.prezzo} - Stato: {stato}'

    def __repr__(self):
        return f'[{self.__str__()}]'

    def __lt__(self, other):
        return self.prezzo < other.prezzo

class CabinaDeluxe(Cabina):
    def __init__(self, codice, letti, ponte, prezzo, stile):
        super().__init__(codice, letti, ponte, prezzo)
        self.stile = stile

        @property
        def prezzo(self):
            return self._prezzo * 1.20

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Non disponibile" + f" | Cliente --> {self.passeggero}"
        return f'{self.codice}| Deluxe - Letti : {self.letti} - Ponte: {self.ponte} - Prezzo: {self.prezzo} - Stile: {self.stile} - Stato: {stato}'

class CabinaAnimali(Cabina):
    def __init__(self, codice, letti, ponte, prezzo, max_animali):
        super().__init__(codice, letti, ponte, prezzo)
        self.max_animali = int(max_animali)

        @property
        def prezzo(self):
            return self._prezzo * (1 + 0.10 * self.max_animali)

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Non disponibile" + f" | Cliente --> {self.passeggero}"
        return f'{self.codice}| Animali - Letti : {self.letti} - Ponte: {self.ponte} - Prezzo: {self.prezzo} - Max Animali: {self.max_animali} - Stato: {stato}'

















