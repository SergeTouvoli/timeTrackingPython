import tkinter as tk
import time
import sqlite3
from tkinter import messagebox

# Création de la fenêtre principale
window = tk.Tk()
icon = tk.PhotoImage(file='prime-time.png')
window.iconphoto(True, icon)
window.geometry("300x400")
window.title("Time Tracking")

# Classe pour représenter un projet
class Project:
    def __init__(self, id, name, time_elapsed=0):
        self.id = id
        self.name = name
        self.time_elapsed = time_elapsed
        self.is_tracking = False
        self.start_time = 0

def time_elapsed_formatted(self):
    hours, remainder = divmod(self.time_elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_elapsed_formatted = "{:02d}:{:02d}:{:02d}".format(int(hours),int(minutes),int(seconds))
    return time_elapsed_formatted

# Fonction pour ajouter un projet à la liste
def add_project():
    project_name = entry.get()
    if project_name:
        cursor.execute('''INSERT INTO projects (name, time_elapsed) VALUES (?, ?)''', (project_name, 0))
        connection.commit()
        # Récupération de l'identifiant généré par la base de données pour le nouveau projet
        id = cursor.lastrowid
        # Création d'un objet Project à partir des données de la base de données
        project = Project(id,project_name,0)
        projects.append(project)
        update_listbox()
    else:
        tk.messagebox.showerror("Erreur", "Veuillez entrer un nom de projet")

# Fonction pour supprimer un projet de la liste
def remove_project():
    # Vérifier si un projet est sélectionné
    if listbox.curselection():
        selected_index = listbox.curselection()[0]
        project = projects[selected_index]
        if project.is_tracking:
            pause_tracking()
        result = messagebox.askokcancel("Confirmation",
                                        "Etes-vous sûr de vouloir supprimer le projet {}?".format(project.name))
        if result:
            # Supprimer le projet de la base de données
            cursor.execute('''DELETE FROM projects WHERE id = ?''', (project.id,))
            connection.commit()
            del projects[selected_index]
            tk.messagebox.showinfo("Info", "Projet Supprimé")
            update_listbox()
            update_time_label()
    else:
        # Afficher un message d'erreur si aucun projet n'est sélectionné
        tk.messagebox.showerror("Erreur", "Aucun projet sélectionné")


# Fonction pour mettre à jour la liste des projets dans la liste
def update_listbox():
    listbox.delete(0, tk.END)
    for project in projects:
        listbox.insert(tk.END, project.name)

# Fonction pour démarrer le suivi du temps pour un projet
def start_tracking():
    if listbox.curselection():
        selected_index = listbox.curselection()[0]
        project = projects[selected_index]
        project.is_tracking = True
        project.start_time = time.time()
        update_time_label()


# Fonction pour mettre en pause le suivi du temps pour un projet
def pause_tracking():
    if listbox.curselection():
        selected_index = listbox.curselection()[0]
        project = projects[selected_index]
        project.is_tracking = False
        # Mettre à jour le temps écoulé dans la base de données
        time_elapsed = project.time_elapsed + (time.time() - project.start_time)
        cursor.execute('''UPDATE projects SET time_elapsed = ? WHERE id = ?''', (time_elapsed, project.id))
        connection.commit()
        project.time_elapsed = time_elapsed
        update_time_label()

# Fonction pour reprendre le suivi du temps pour un projet
def resume_tracking():
    selected_index = listbox.curselection()[0]
    project = projects[selected_index]
    project.is_tracking = True
    project.start_time = time.time()

# Fonction pour mettre à jour l'affichage du temps écoulé
def update_time_label():
    if projects and listbox.curselection():
        selected_index = listbox.curselection()[0]
        project = projects[selected_index]
        if project.is_tracking:
            time_elapsed = project.time_elapsed + (time.time() - project.start_time)
            # Formatter le temps écoulé sous la forme HH:MM:SS
            hours, remainder = divmod(time_elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_elapsed_formatted = "{:02d}h {:02d}m {:02d}s".format(int(hours), int(minutes), int(seconds))
        else:
            # Formatter le temps écoulé sous la forme HH:MM:SS
            hours, remainder = divmod(project.time_elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_elapsed_formatted = "{:02d}h {:02d}m {:02d}s".format(int(hours), int(minutes), int(seconds))
        time_label.config(text=time_elapsed_formatted)
    # On met à jour l'affichage toutes les 100ms
    window.after(100, update_time_label)

# Fonction pour afficher une msgBox à la fermetture de l'app
# et mettre à jour le time_elapsed
def on_closing():
    if messagebox.askokcancel("Quitter", "Etes-vous sûr de vouloir quitter l'application ?"):
        for project in projects:
            if project.is_tracking:
                time_elapsed = project.time_elapsed + (time.time() - project.start_time)
                cursor.execute('''UPDATE projects SET time_elapsed = ? WHERE id = ?''', (time_elapsed, project.id))
                connection.commit()
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

label = tk.Label(text="Nom du projet")
label.pack()

entry = tk.Entry(window)
entry.pack()
entry.config(width=40)

# Frame pour contenir le bouton "Ajouter projet"
add_button_frame = tk.Frame(window)
add_button_frame.pack()

# Bouton pour Ajotuer un projet
add_button = tk.Button(add_button_frame, text="Ajouter projet", command=add_project)
add_button.pack(side='top',pady=10)

# Liste de projets
projects = []

# Création d'une liste pour afficher les projets
listbox = tk.Listbox(window)
listbox.pack()
listbox.config(width=40)

# Frame pour contenir le bouton supprimer
remove_button_frame = tk.Frame(window)
remove_button_frame.pack()

# Bouton pour supprimer un projet
remove_button = tk.Button(remove_button_frame, text="Supprimer projet", command=remove_project)
remove_button.pack(side='top',pady=5)

# Frame pour contenir les boutons
# Démarrer, Mettre en pause et Reprendre
buttons_frame = tk.Frame(window)
buttons_frame.pack()

# Bouton "Démarrer"
start_button = tk.Button(buttons_frame, text="Démarrer", command=start_tracking)
start_button.pack(side='left',padx=5)

# Bouton "Mettre en pause"
pause_button = tk.Button(buttons_frame, text="Mettre en pause", command=pause_tracking)
pause_button.pack(side='left',padx=5)

# Bouton "Reprendre"
resume_button = tk.Button(buttons_frame, text="Reprendre", command=start_tracking)
resume_button.pack(side='left',padx=5)

# Bouton "Quitter"
exit_button_frame = tk.Frame(window)
exit_button_frame.pack()
exit_button_frame = tk.Button(exit_button_frame,bg='red', text="Quitter", command=on_closing)
exit_button_frame.pack(side='top',pady=5)

# Frame pour contenir le label du temps écoulé
time_frame = tk.Frame(window)
time_frame.pack()
time_label = tk.Label(time_frame, text="00 h 00m 00s")
time_label.pack(side='top',pady=7)
time_label.config(font=("Courier", 22, "bold"), fg="black")

# Connexion à la base de données
connection = sqlite3.connect('projects.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, time_elapsed REAL)''')

# Récupération la liste des projets de la base de données
cursor.execute('''SELECT * FROM projects''')
rows = cursor.fetchall()

for row in rows:
    id = row[0]
    name = row[1]
    time_elapsed = row[2]
    project = Project(id, name, time_elapsed)
    projects.append(project)
    listbox.insert("end", "{}".format(project.name))

# Maj de la listBox
update_listbox()

# Maj de l'affichage du temps écoulé
update_time_label()

# Démarrage de la boucle d'événements
window.mainloop()

# On ferme la connexion à la base de données
connection.close()
