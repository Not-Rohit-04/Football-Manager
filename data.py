import random

clubs = [
    "FC Thunder",
    "Iron United",
    "Blue Eagles",
    "Golden Lions",
    "Phoenix FC",
    "Titan City",
    "Storm Athletic",
    "Royal Wanderers"
]
positions = [
    "GK",
    "CB",
    "LB",
    "RB",
    "CDM",
    "CM",
    "CAM",
    "LW",
    "RW",
    "ST"
]
nations = [
    "Brazil",
    "Argentina",
    "England",
    "France",
    "Germany",
    "Spain",
    "Portugal",
    "Italy",
    "Netherlands",
    "Belgium",
    "Croatia",
    "Uruguay",
    "Mexico",
    "Japan",
    "South Korea",
    "United States"
]
last_names = [
    "Silva", "Martinez", "Garcia", "Fernandez", "Lopez",
    "Smith", "Johnson", "Brown", "Williams", "Taylor",
    "Anderson", "Walker", "Hughes", "Morgan", "Clark",
    "Costa", "Santos", "Pereira", "Alvarez", "Torres"
]
first_names = [
    "Liam", "Noah", "Ethan", "Lucas", "Mateo",
    "Oliver", "Benjamin", "Mason", "Leo", "Daniel",
    "Alex", "Ryan", "Jack", "Nathan", "Samuel",
    "Julian", "Marco", "Adrian", "David", "Gabriel","Jhon","Shawn","Timity","Raul","Lucus"
]
def seed_player(Player,db):
    for _ in range(60):
        name = f'{random.choice(first_names)} {random.choice(last_names)}'
        age = random.randint(18,38)
        nation = random.choice(nations)
        position = random.choice(positions)
        club = random.choice(clubs)
        rating = random.randint(75,95)
        
        new_player = Player(
            name=name,
            age=age,
            nation=nation,
            position=position,
            club=club,
            rating=rating
        )
        
        db.session.add(new_player)
    db.session.commit()