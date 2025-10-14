import csv

class Crociera:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.cabine = {}  # {codice_cabina: oggetto_cabina}
        self.passeggeri = {}  # {codice_passeggero: oggetto_passeggero}

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    def carica_file_dati(self, file_path):
        """Carica i dati (cabine e passeggeri) dal file"""
        self.cabine = {}
        self.passeggeri = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for riga in reader:
                    if not riga:
                        continue

                    codice = riga[0].strip()

                    if codice.startswith('CAB'):
                        if len(riga) < 4:
                            print(f"ATTENZIONE: Riga cabina incompleta saltata: {riga}")
                            continue
                        try:
                            num_letti = int(riga[1].strip())
                            ponte = int(riga[2].strip())
                            prezzo_base = float(riga[3].strip())
                        except ValueError as e:
                            print(f"Errore di conversione dati cabina per {codice}: {e}")
                            continue

                        cabina = None
                        if len(riga) == 4:
                            cabina = Cabine(codice, num_letti, ponte, prezzo_base)
                        elif len(riga) == 5:
                            # Cabina Speciale (Deluxe o Animali)
                            extra_data = riga[4].strip()
                            try:
                                max_animali = int(extra_data)
                                cabina = CabinaAnimali(codice, num_letti, ponte, prezzo_base, max_animali)
                            except ValueError:
                                cabina = CabinaDeluxe(codice, num_letti, ponte, prezzo_base, extra_data)

                        if cabina:
                            self.cabine[codice] = cabina

                    elif codice.startswith('P'):
                        if len(riga) < 3:
                            print(f"ATTENZIONE: Riga passeggero incompleta saltata: {riga}")
                            continue
                        passeggero = Passeggero(
                            codice=codice,
                            nome=riga[1].strip(),
                            cognome=riga[2].strip()
                        )
                        self.passeggeri[codice] = passeggero

        except FileNotFoundError:
            raise FileNotFoundError(f"Il file {file_path} non è stato trovato.")
        except Exception as e:
            print(f"Si è verificato un errore durante il caricamento dei dati: {e}")
            raise


    def assegna_passeggero_a_cabina(self, codice_cabina, codice_passeggero):
        """Associa una cabina a un passeggero"""
        cabina_esiste = self.cabine.get(codice_cabina)
        passeggero_esiste = self.passeggeri.get(codice_passeggero)

        if not cabina_esiste:
            raise ValueError(f"Cabina {codice_cabina} non trovata.")
        if not passeggero_esiste:
            raise ValueError(f"Passeggero {codice_passeggero} non trovato.")

        if not cabina_esiste.disponibile:
            raise Exception(
                f"La cabina {codice_cabina} non è disponibile, è già occupata da {cabina_esiste.passeggero.nome}.")

        # Controllo se il passeggero è già assegnato
        if passeggero_esiste.cabina is not None:
            raise Exception(f"Il passeggero {codice_passeggero} è già assegnato alla cabina {passeggero_esiste.cabina.codice}.")

        cabina_esiste.disponibile = False
        cabina_esiste.passeggero = passeggero_esiste
        passeggero_esiste.cabina = cabina_esiste

        return f"Passeggero {passeggero_esiste.nome} assegnato con successo alla cabina {cabina_esiste.codice}."

    def cabine_ordinate_per_prezzo(self):
        """Restituisce la lista ordinata delle cabine in base al prezzo"""
        return sorted(list(self.cabine.values()), key=lambda cabina: cabina.calcola_prezzo())


    def elenca_passeggeri(self):
        """Stampa l'elenco dei passeggeri mostrando, per ognuno, la cabina a cui è associato, quando applicabile """
        for passeggero in self.passeggeri:
            if passeggero.cabina:
                print(f'Passeggero: {passeggero.nome} {passeggero.cognome} - Cabina: {passeggero.cabina.codice}')
            else:
                print(f'Il passeggero {passeggero.nome} {passeggero.cognome} non è assegnato.')


class Cabine:
    def __init__(self, codice, num_letti, ponte, prezzo_base):
        self.codice = codice
        self.num_letti = num_letti
        self.ponte = ponte
        self.prezzo_base = prezzo_base
        self.disponibile = True
        self.passeggero = None

    def calcola_prezzo(self):
        return self.prezzo_base

    def __str__(self):
        if self.disponibile:
            stato_cabina = 'Disponibile'
        else:
            stato_cabina = f'Occupata da {self.passeggero.nome} {self.passeggero.cognome}'
        return f'{self.codice}: Standard: {self.num_letti} letti - Ponte {self.ponte} - Prezzo € {self.calcola_prezzo()} - {stato_cabina}'

class CabinaDeluxe(Cabine):
    def __init__(self, codice, num_letti, ponte, prezzo_base, stile):
        super().__init__(codice, num_letti, ponte, prezzo_base)
        self.stile = stile

    def calcola_prezzo(self):
        return self.prezzo_base * 1.20

    def __str__(self):
        if self.disponibile:
            stato_cabina = 'Disponibile'
        else:
            stato_cabina = f'Occupata da {self.passeggero.nome} {self.passeggero.cognome}'
        return f'{self.codice}: Standard: {self.num_letti} letti - Ponte {self.ponte} - Stile {self.stile} - Prezzo € {self.calcola_prezzo()} - {stato_cabina}'

class CabinaAnimali(Cabine):
    def __init__(self, codice, num_letti, ponte, prezzo_base, max_animali):
        super().__init__(codice, num_letti, ponte, prezzo_base)
        self.max_animali = max_animali

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.1 * self.max_animali)

    def __str__(self):
        if self.disponibile:
            stato_cabina = 'Disponibile'
        else:
            stato_cabina = f'Occupata da {self.passeggero.nome} {self.passeggero.cognome}'
        return f'{self.codice}: Standard: {self.num_letti} letti - Ponte {self.ponte} - Max Animali {self.max_animali} - Prezzo € {self.calcola_prezzo()} - {stato_cabina}'


class Passeggero:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.cabina = None

    def __str__(self):
        if self.cabina:
            return (f'{self.codice}: {self.nome} {self.cognome} - Cabina: {self.cabina.codice}')
        else:
            return (f'{self.codice}: {self.nome} {self.cognome} - Nessuna cabina assegnata.')