# Classe base Veicolo
class Veicolo:
    def __init__(self, marca, anno_immatricolazione, targa, revisione):
        # Attributi protetti
        self._marca = marca
        self._anno_immatricolazione = anno_immatricolazione
        self._targa = targa
        self._revisione = revisione

    # Getter e Setter per gli attributi
    def get_marca(self):
        return self._marca
    
    def set_marca(self, marca):
        self._marca = marca

    def get_anno_immatricolazione(self):
        return self._anno_immatricolazione
    
    def set_anno_immatricolazione(self, anno):
        self._anno_immatricolazione = anno

    def get_targa(self):
        return self._targa
    
    def set_targa(self, targa):
        self._targa = targa

    def get_revisione(self):
        return self._revisione
    
    def set_revisione(self, revisione):
        self._revisione = revisione

    # Metodo descrivi() da sovrascrivere nelle sottoclassi
    def descrivi(self):
        return f"Marca: {self._marca}, Anno: {self._anno_immatricolazione}, Targa: {self._targa}, Revisione: {self._revisione}"

# Classe Auto (Sottoclasse di Veicolo)
class Auto(Veicolo):
    def __init__(self, marca, anno_immatricolazione, targa, revisione, numero_portiere):
        # Chiamata al costruttore della classe base
        super().__init__(marca, anno_immatricolazione, targa, revisione)
        self._numero_portiere = numero_portiere  # Attributo unico

    # Sovrascrittura del metodo descrivi()
    def descrivi(self):
        return f"{super().descrivi()}, Numero Portiere: {self._numero_portiere}"

# Classe Moto (Sottoclasse di Veicolo)
class Moto(Veicolo):
    def __init__(self, marca, anno_immatricolazione, targa, revisione, cilindrata):
        # Chiamata al costruttore della classe base
        super().__init__(marca, anno_immatricolazione, targa, revisione)
        self._cilindrata = cilindrata  # Attributo unico

    # Sovrascrittura del metodo descrivi()
    def descrivi(self):
        return f"{super().descrivi()}, Cilindrata: {self._cilindrata}cc"

# Classe Camion (Sottoclasse di Veicolo)
class Camion(Veicolo):
    def __init__(self, marca, anno_immatricolazione, targa, revisione, peso_max):
        # Chiamata al costruttore della classe base
        super().__init__(marca, anno_immatricolazione, targa, revisione)
        self._peso_max = peso_max  # Attributo unico

    # Sovrascrittura del metodo descrivi()
    def descrivi(self):
        return f"{super().descrivi()}, Peso Massimo: {self._peso_max}kg"

# Funzione per creare un veicolo in base alla scelta dell'utente
def crea_veicolo():
    print("\nScegli il tipo di veicolo da creare:")
    print("1. Auto")
    print("2. Moto")
    print("3. Camion")
    
    scelta = input("Inserisci il numero corrispondente al veicolo (1/2/3): ")
    
    marca = input("Inserisci la marca: ")
    anno_immatricolazione = int(input("Inserisci l'anno di immatricolazione: "))
    targa = input("Inserisci la targa: ")
    revisione = input("La revisione è stata effettuata? (sì/no): ").lower() == "sì"
    
    match scelta:
        case "1":
            numero_portiere = int(input("Inserisci il numero di portiere: "))
            return Auto(marca, anno_immatricolazione, targa, revisione, numero_portiere)
        
        case "2":
            cilindrata = int(input("Inserisci la cilindrata in cc: "))
            return Moto(marca, anno_immatricolazione, targa, revisione, cilindrata)
        
        case "3":
            peso_max = float(input("Inserisci il peso massimo in kg: "))
            return Camion(marca, anno_immatricolazione, targa, revisione, peso_max)
        
        case _:
            print("Scelta non valida.")
            return None

# Funzione per visualizzare i dati del veicolo
def visualizza_veicolo(veicolo):
    if veicolo:
        print("\nDati del veicolo:")
        print(veicolo.descrivi())
    else:
        print("\nNessun veicolo creato.")

# Funzione principale per il menu
def menu():
    veicolo = None
    
    while True:
        print("\nMenu:")
        print("1. Crea un veicolo")
        print("2. Visualizza il veicolo")
        print("3. Esci")
        
        scelta = input("Scegli un'operazione (1/2/3): ")
        
        match scelta:
            case "1":
                veicolo = crea_veicolo()
            case "2":
                visualizza_veicolo(veicolo)
            case "3":
                print("Uscita...")
                break
            case _:
                print("Scelta non valida. Riprova.")

# Avvio del programma
menu()
