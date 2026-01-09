import csv
from passeggero import Passeggero
from cabine import *

class Crociera:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.cabine = []
        self.passeggeri = []

    """Aggiungere setter e getter se necessari"""
    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, nome):
        self._nome = nome

    def carica_file_dati(self, file_path):
        """Carica i dati (cabine e passeggeri) dal file"""
        self.cabine.clear()
        self.passeggeri.clear()

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for riga in reader:
                    if len(riga) == 3:
                        passeggero = Passeggero(
                            codice = riga[0],
                            nome = riga[1],
                            cognome = riga[2],
                        )
                        self.passeggeri.append(passeggero)
                    if len(riga) == 4:
                        cabina = Cabina(*riga)
                    elif len(riga) == 5:
                        if riga[4].isdigit():
                            cabina = CabinaAnimali(*riga)
                        else:
                            cabina = CabinaDeluxe(*riga)
                    self.cabine.append(cabina)
        except FileNotFoundError:
            raise FileNotFoundError(f'File {file_path} not found')

    def _trova_passeggero(self, codice):
        return next((passeggero for passeggero in self.passeggeri if passeggero.codice == codice), None) #next si usa per estrarre il primo elemento che soddisfa una determinata condizione

    def _trova_cabina(self, codice):
        return next((cabina for cabina in self.cabine if str(cabina.codice) == str(codice)), None)

    def assegna_passeggero_a_cabina(self, codice_cabina, codice_passeggero):
        """Associa una cabina a un passeggero"""
        cabina = self._trova_cabina(codice_cabina)
        passeggero = self._trova_passeggero(codice_passeggero)

        if cabina is None:
            raise Exception(f'Cabina {codice_cabina} non trovata.')
        if passeggero is None:
            raise Exception(f'Passeggero {codice_passeggero} non trovato.')
        if not cabina.disponibile:
            raise Exception(f'Cabina {codice_cabina} non disponibile.')
        for c in self.cabine:
            if c.passeggero == passeggero:
                raise Exception(f"Passeggero {codice_passeggero} già associato ad un'altra cabina.")

        cabina.assegna(passeggero)


    def cabine_ordinate_per_prezzo(self):
        """Restituisce la lista ordinata delle cabine in base al prezzo"""
        return sorted(self.cabine)

    def elenca_passeggeri(self):
        """Stampa l'elenco dei passeggeri mostrando, per ognuno, la cabina a cui è associato, quando applicabile """


        for p in self.passeggeri:
                    res = f"- {p}"
                    for c in self.cabine:
                        if p == c.passeggero: # Affinché questo funzioni deve essere definito il metodo __eq__() nella classe Passeggero
                            res = f"{res} --> Assegnato alla cabina: {c.codice}"
                            break
                    print(res)


