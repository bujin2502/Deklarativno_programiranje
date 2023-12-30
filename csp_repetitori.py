# Uvoz potrebnih biblioteka
import tkinter as tk
from tkinter import *
from constraint import Problem
import math

# Definiranje broja baznih stanica i dimenzija površine
num_base_stations = 3
area_width = 10
area_height = 10

# Rječnik koji sadrži gradove i njihovo stanovništvo
cities = {
    'City1': 52120,
    'City2': 30000,
    'City3': 12850,
    'City4': 25000,
    'City5': 11765,
    'City6': 11900,
    'City7': 50650,
    'City8': 15005,
    'City9': 23800,
    'City10': 18000
}

# Rječnik koji sadrži položaje gradova
city_positions = {
    'City1': (1, 2),
    'City2': (3, 4),
    'City3': (8, 2),
    'City4': (6, 8),
    'City5': (3, 8),
    'City6': (5, 5),
    'City7': (7, 3),
    'City8': (4, 6),
    'City9': (5, 1),
    'City10': (3, 9)
}

# Definiranje "first_solution" na početku skripte
first_solution = {}

# Stvaranje problema zadovoljenja ograničenja
problem = Problem()

# Dodavanje varijabli za koordinate baznih stanica
for i in range(num_base_stations):
    problem.addVariable(f'x{i}', range(area_width))
    problem.addVariable(f'y{i}', range(area_height))

# Funkcija ograničenja za udaljenost između baznih stanica
def distance_constraint(x0, y0, x1, y1, x2, y2):
    x_values = [x0, x1, x2]
    y_values = [y0, y1, y2]

    for i in range(num_base_stations):
        for j in range(i + 1, num_base_stations):
            distance = ((x_values[i] - x_values[j]) ** 2 + (y_values[i] - y_values[j]) ** 2) ** 0.5
            if distance < 2:
                return False
    return True

# Funkcija ograničenja za obuhvat stanovništva
def population_constraint(x0, y0, x1, y1, x2, y2):
    x_values = [x0, x1, x2]
    y_values = [y0, y1, y2]

    total_population = sum(cities.values())
    covered_population = 0

    for city, population in cities.items():
        for i in range(num_base_stations):
            distance = math.sqrt((x_values[i] - city_positions[city][0]) ** 2 + (y_values[i] - city_positions[city][1]) ** 2)
            if distance <= 3:
                covered_population += population
                break

    if covered_population >= total_population * 0.85:
        return True
    else:
        return False

# Funkcija ograničenja za kapacitet baznih stanica
def capacity_constraint(x0, y0, x1, y1, x2, y2):
    x_values = [x0, x1, x2]
    y_values = [y0, y1, y2]

    max_capacity = 90000

    for i in range(num_base_stations):
        covered_population = 0

        for city, population in cities.items():
            distance = math.sqrt((x_values[i] - city_positions[city][0]) ** 2 + (y_values[i] - city_positions[city][1]) ** 2)
            if distance <= 3:
                covered_population += population

        if covered_population > max_capacity:
            return False

    return True

# Dodavanje ograničenja problemu
problem.addConstraint(capacity_constraint)
problem.addConstraint(distance_constraint)
problem.addConstraint(population_constraint)

# Rješavanje problema i dobivanje rješenja
solutions = problem.getSolutions()

# Ispis prvog rješenja ako postoji
if solutions:
    first_solution = solutions[0]
    print(first_solution)
else:
    print("Nema rješenja za ovaj problem.")

# Funkcija za crtanje kruga na platnu
def draw_circle(canvas, x, y, radius, color):
    x0 = (x - radius) * 80
    y0 = (y - radius) * 80
    x1 = (x + radius) * 80
    y1 = (y + radius) * 80
    canvas.create_oval(x0, y0, x1, y1, outline=color)

# Funkcija za ponovno izračunavanje i crtanje
def recalculate_and_draw():
    new_capacity = int(capacity_entry.get())
    new_coverage_percentage = float(coverage_entry.get())

    def updated_capacity_constraint(x0, y0, x1, y1, x2, y2):
        x_values = [x0, x1, x2]
        y_values = [y0, y1, y2]

        max_capacity = new_capacity

        for i in range(num_base_stations):
            covered_population = 0

            for city, population in cities.items():
                distance = math.sqrt((x_values[i] - city_positions[city][0]) ** 2 + (y_values[i] - city_positions[city][1]) ** 2)
                if distance <= 3:
                    covered_population += population

            if covered_population > max_capacity:
                return False

        return True

    def updated_population_constraint(x0, y0, x1, y1, x2, y2):
        x_values = [x0, x1, x2]
        y_values = [y0, y1, y2]

        total_population = sum(cities.values())
        covered_population = 0

        for city, population in cities.items():
            for i in range(num_base_stations):
                distance = math.sqrt((x_values[i] - city_positions[city][0]) ** 2 + (y_values[i] - city_positions[city][1]) ** 2)
                if distance <= 3:
                    covered_population += population
                    break

        if covered_population >= total_population * new_coverage_percentage:
            return True
        else:
            return False

    # Stvaranje nove instance problema
    problem = Problem()

    # Čišćenje varijable iz problema
    problem.reset()

    # Dodavanje varijable problemu
    for i in range(num_base_stations):
        problem.addVariable(f'x{i}', range(area_width))
        problem.addVariable(f'y{i}', range(area_height))

    # Dodavanje problemu ažurirana ograničenja
    problem.addConstraint(updated_capacity_constraint)
    problem.addConstraint(distance_constraint)
    problem.addConstraint(updated_population_constraint)

    # Ponovno riješavanje problem i pronalazak novog rješenja
    new_solutions = problem.getSolutions()

    # Inicijalizacija update_solution
    updated_solution = {}

    # Ispis prvog ažuriranog rješenja ako postoji
    if new_solutions:
        updated_solution = new_solutions[0]
        print(updated_solution)
    else:
        print("Nema rješenja za ovaj problem.")

    # Čišćenje prethodnog crteža na platnu
    canvas.delete("all")

    # Crtanje na novom platnu ažurirane bazne stanice, crvena boja - domet, plava boja, interferencija. Drugi repetitor ne smije biti u plavom krugu
    if isinstance(updated_solution, dict) and 'x0' in updated_solution:
        for i in range(num_base_stations):
            x = updated_solution[f'x{i}']
            y = updated_solution[f'y{i}']
            draw_circle(canvas, x, y, 3, "red")
            draw_circle(canvas, x, y, 2, "blue")

        # Crtanje bazne stanice kao oznake i dometa
        for i in range(num_base_stations):
            x = updated_solution[f'x{i}']
            y = updated_solution[f'y{i}']
            canvas.create_oval(x * 80 - 2, y * 80 - 2, x * 80 + 2, y * 80 + 2, fill="red")
            canvas.create_text(x * 80 + 5, y * 80 + 20, text=f"R{i+1}")

    # Crtajtanje gradova na novom platnu
    for city, position in city_positions.items():
        x, y = position
        canvas.create_oval(x * 80 - 2, y * 80 - 2, x * 80 + 2, y * 80 + 2, fill="blue")
        canvas.create_text(x * 80 + 5, y * 80 + 5, text=city)
        canvas.create_text(x * 80 + 5, y * 80 + 20, text=f"Br.st: {cities[city]}")

    # Ispis prvog rješenja ako postoji
    if new_solutions:
        updated_solution = new_solutions[0]
        messagebox.showinfo("Rješenje", str(updated_solution))
    else:
        messagebox.showwarning("Nema rješenja", "Nema rješenja za ovaj problem.")

# Izrada glavnog prozora
window = tk.Tk()
window.title("Raspored repetitora")
window.config(bg="#D9D9D9")

# Kreiranje okvira za platno
canvas_frame = tk.Frame(window)
canvas_frame.pack(side=tk.TOP, padx=20, pady=20)

# Kreiranje okvira za widgete
widget_frame = tk.Frame(window)
widget_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

# Stvaranje platna za crtanje unutar canvas okvira
canvas = tk.Canvas(canvas_frame, width=area_width * 80, height=area_height * 80, bg="white")
canvas.pack()

# Crtanje baznih stanica na platnu, crvena boja - domet, plava boja, interferencija. Drugi repetitor ne smije biti u plavom krugu
if isinstance(first_solution, dict) and 'x0' in first_solution:
    for i in range(num_base_stations):
        x = first_solution[f'x{i}']
        y = first_solution[f'y{i}']
        draw_circle(canvas, x, y, 3, "red")
        draw_circle(canvas, x, y, 2, "blue")

    # Crtanje baznih stanica kao krugova i oznaka
    for i in range(num_base_stations):
        x = first_solution[f'x{i}']
        y = first_solution[f'y{i}']
        canvas.create_oval(x * 80 - 2, y * 80 - 2, x * 80 + 2, y * 80 + 2, fill="red")
        canvas.create_text(x * 80 + 5, y * 80 + 20, text=f"R{i+1}")

# Crtanje gradova na platnu
for city, position in city_positions.items():
    x, y = position
    canvas.create_oval(x * 80 - 2, y * 80 - 2, x * 80 + 2, y * 80 + 2, fill="blue")
    canvas.create_text(x * 80 + 5, y * 80 + 5, text=city)
    canvas.create_text(x * 80 + 5, y * 80 + 20, text=f"Br.st: {cities[city]}")

# Stvaranje widgeta za unos za kapacitet i postotak pokrivenosti unutar widget okvira
capacity_label = tk.Label(widget_frame, text="Kapacitet:")
capacity_label.grid(row=0, column=0)
capacity_entry = tk.Entry(widget_frame, width=10)
capacity_entry.insert(0, "90000")
capacity_entry.grid(row=0, column=1)

# Kreiranje labela i unosnog polja za postotak pokrivenosti
coverage_label = tk.Label(widget_frame, text="Postotak pokrivenosti:")
coverage_label.grid(row=0, column=2)
coverage_entry = tk.Entry(widget_frame, width=10)
coverage_entry.insert(0, "0.85")
coverage_entry.grid(row=0, column=3)

# Kreiranje gumba za ponovno izračunavanje i crtanje
recalculate_button = tk.Button(widget_frame, text="Nanovo izračunaj", command=recalculate_and_draw)
recalculate_button.grid(row=1, sticky=tk.NSEW, columnspan=4, pady=(10, 10))

# Ispis prvog rješenja ako postoji
if solutions:
    first_solution = solutions[0]
    messagebox.showinfo("Rješenje", str(first_solution))
else:
    messagebox.showwarning("Nema rješenja", "Nema rješenja za ovaj problem.")

# Pokretanje glavne petlje događaja
window.mainloop()
