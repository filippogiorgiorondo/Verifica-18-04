import mysql.connector
from mysql.connector import Error

# Classe per la connessione al database
class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        
    def connect(self):
        # Stabilisce la connessione al database e crea la tabella se non esiste 
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("=== Connessione al database stabilita. ===")
            self.create_tables()
        except Error as e:
            print(f"Errore di connessione al database: {e}")
    
    def create_tables(self):
        # Crea le tabelle se non esistono
        # Creazione tabella Utenti
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Utenti (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        );
        """)
        
        # Creazione tabella Contatti
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contatti (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefono VARCHAR(15),
            email VARCHAR(100),
            id_utente INT,
            FOREIGN KEY (id_utente) REFERENCES Utenti(id)
        );
        """)
        
        self.connection.commit()

# Classe Utente
class Utente:
    def __init__(self, nome, password):
        self.nome = nome
        self.password = password
    
    def registra(self, db):
        # Registra un nuovo utente nel database
        query = "INSERT INTO Utenti (nome, password) VALUES (%s, %s)"
        values = (self.nome, self.password)
        db.cursor.execute(query, values)
        db.connection.commit()
        print(f"=== Utente {self.nome} registrato con successo con ID {db.cursor.lastrowid}. ===")

    def login(self, db):
        # Verifica se l'utente esiste nel database per il login
        query = "SELECT * FROM Utenti WHERE nome = %s AND password = %s"
        values = (self.nome, self.password)
        db.cursor.execute(query, values)
        user = db.cursor.fetchone()
        if user:
            print(f"=== Benvenuto {self.nome}. Accesso effettuato con successo. ===")
            return user[0]  # Restituisce l'ID dell'utente
        else:
            print("=== Credenziali non valide. ===")
            return None

# Classe Contatto
class Contatto:
    def __init__(self, nome, telefono, email, id_utente):
        self.nome = nome
        self.telefono = telefono
        self.email = email
        self.id_utente = id_utente
    
    def inserisci(self, db):
        # Inserisce un nuovo contatto nella rubrica
        query = "INSERT INTO Contatti (nome, telefono, email, id_utente) VALUES (%s, %s, %s, %s)"
        values = (self.nome, self.telefono, self.email, self.id_utente)
        db.cursor.execute(query, values)
        db.connection.commit()
        print(f"=== Contatto {self.nome} inserito con successo. ===")
    
    def visualizza_tutti(self, db):
        # Visualizza tutti i contatti dell'utente loggato
        query = "SELECT id, nome, telefono, email FROM Contatti WHERE id_utente = %s"
        db.cursor.execute(query, (self.id_utente,))
        contatti = db.cursor.fetchall()
        if contatti:
            print("\n=== Contatti dell'utente ===")
            for contatto in contatti:
                print(f"ID: {contatto[0]}, Nome: {contatto[1]}, Telefono: {contatto[2]}, Email: {contatto[3]}")
        else:
            print("=== Non ci sono contatti per questo utente. ===")

    def aggiorna_contatto(self, db, id_contatto, nuovo_nome, nuovo_telefono, nuova_email):
        # Aggiorna un contatto esistente
        query = "UPDATE Contatti SET nome = %s, telefono = %s, email = %s WHERE id = %s"
        values = (nuovo_nome, nuovo_telefono, nuova_email, id_contatto)
        db.cursor.execute(query, values)
        db.connection.commit()
        print(f"=== Contatto con ID {id_contatto} aggiornato. ===")
    
    def elimina_contatto(self, db, id_contatto):
        # Elimina un contatto dalla rubrica
        query = "DELETE FROM Contatti WHERE id = %s"
        values = (id_contatto,)
        db.cursor.execute(query, values)
        db.connection.commit()
        print(f"=== Contatto con ID {id_contatto} eliminato. ===")

# Funzione per il menu
def menu():
    db = Database(host="localhost", user="root", password="", database="db_es2")
    db.connect()
    
    utente_loggato = None
    
    while True:
        print("\n=== MENU ===")
        if not utente_loggato:
            print("1. Registrati")
            print("2. Login")
        else:
            print("1. Inserisci un nuovo contatto")
            print("2. Visualizza contatti")
            print("3. Aggiorna un contatto")
            print("4. Elimina un contatto")
            print("5. Logout")
        
        scelta = input("Scegli un'operazione (1/2): ")
        
        if not utente_loggato:  # Menu per non loggato
            match scelta:
                case "1":  # Registrazione
                    nome = input("Inserisci il nome: ")
                    password = input("Inserisci la password: ")
                    utente = Utente(nome, password)
                    utente.registra(db)
                case "2":  # Login
                    nome = input("Inserisci il nome: ")
                    password = input("Inserisci la password: ")
                    utente = Utente(nome, password)
                    utente_loggato = utente.login(db)
                case _:
                    print("=== Scelta non valida. ===")
        else:  # Menu per utente loggato
            match scelta:
                case "1":  # Inserimento contatto
                    nome = input("Inserisci il nome del contatto: ")
                    telefono = input("Inserisci il telefono del contatto: ")
                    email = input("Inserisci l'email del contatto: ")
                    contatto = Contatto(nome, telefono, email, utente_loggato)
                    contatto.inserisci(db)
                case "2":  # Visualizza contatti
                    contatto = Contatto("", "", "", utente_loggato)
                    contatto.visualizza_tutti(db)
                case "3":  # Aggiorna contatto
                    id_contatto = int(input("Inserisci l'ID del contatto da aggiornare: "))
                    nuovo_nome = input("Inserisci il nuovo nome: ")
                    nuovo_telefono = input("Inserisci il nuovo telefono: ")
                    nuova_email = input("Inserisci la nuova email: ")
                    contatto = Contatto("", "", "", utente_loggato)
                    contatto.aggiorna_contatto(db, id_contatto, nuovo_nome, nuovo_telefono, nuova_email)
                case "4":  # Elimina contatto
                    # Visualizza i contatti dell'utente prima dell'eliminazione
                    contatto = Contatto("", "", "", utente_loggato)
                    contatto.visualizza_tutti(db)
                    id_contatto = int(input("Inserisci l'ID del contatto da eliminare: "))
                    contatto.elimina_contatto(db, id_contatto)
                case "5":  # Logout
                    utente_loggato = None
                    print("=== Logout effettuato. ===")
                case _:
                    print("=== Scelta non valida. ===")

# Avvio del programma
menu()
