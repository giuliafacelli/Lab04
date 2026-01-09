from dataclasses import dataclass

@dataclass
class Passeggero:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome

    def __str__(self):
        return f'Passeggero: {self.codice}| {self.nome} - {self.cognome}'

    def __eq__(self, other):
        return isinstance(other, Passeggero) and self.codice == other.codice
