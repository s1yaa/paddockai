#!/usr/bin/env python3
"""
PaddockAI — Database Seed Script
Seeds the 2026 F1 season with realistic data for demo/development.

Run: python data/seed_data.py
"""
import os
import sys
import uuid
from datetime import date, datetime, timezone

# Allow running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL_SYNC",
    "postgresql://paddockai:paddockai_dev@localhost:5432/paddockai",
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# ─────────────────────────────────────────────────────────────────────────────
# SEED DATA
# ─────────────────────────────────────────────────────────────────────────────

CONSTRUCTORS = [
    {"slug": "red-bull", "name": "Oracle Red Bull Racing", "short_name": "Red Bull",
     "nationality": "Austrian", "base": "Milton Keynes, UK", "principal": "Christian Horner",
     "color_primary": "#1B3A6B", "color_secondary": "#FFCB00", "engine_supplier": "Honda RBPT",
     "first_season": 2005, "championships": 6},
    {"slug": "mclaren", "name": "McLaren Formula 1 Team", "short_name": "McLaren",
     "nationality": "British", "base": "Woking, UK", "principal": "Andrea Stella",
     "color_primary": "#FF8000", "color_secondary": "#000000", "engine_supplier": "Mercedes",
     "first_season": 1966, "championships": 8},
    {"slug": "ferrari", "name": "Scuderia Ferrari", "short_name": "Ferrari",
     "nationality": "Italian", "base": "Maranello, Italy", "principal": "Frédéric Vasseur",
     "color_primary": "#DC0000", "color_secondary": "#FFFFFF", "engine_supplier": "Ferrari",
     "first_season": 1950, "championships": 16},
    {"slug": "mercedes", "name": "Mercedes-AMG Petronas F1 Team", "short_name": "Mercedes",
     "nationality": "German", "base": "Brackley, UK", "principal": "Toto Wolff",
     "color_primary": "#00D2BE", "color_secondary": "#000000", "engine_supplier": "Mercedes",
     "first_season": 2010, "championships": 8},
    {"slug": "aston-martin", "name": "Aston Martin Aramco F1 Team", "short_name": "Aston Martin",
     "nationality": "British", "base": "Silverstone, UK", "principal": "Mike Krack",
     "color_primary": "#006F62", "color_secondary": "#CEDC00", "engine_supplier": "Mercedes",
     "first_season": 2021, "championships": 0},
    {"slug": "alpine", "name": "BWT Alpine F1 Team", "short_name": "Alpine",
     "nationality": "French", "base": "Enstone, UK", "principal": "Oliver Oakes",
     "color_primary": "#0090FF", "color_secondary": "#FF69B4", "engine_supplier": "Renault",
     "first_season": 2021, "championships": 0},
    {"slug": "williams", "name": "Williams Racing", "short_name": "Williams",
     "nationality": "British", "base": "Grove, UK", "principal": "James Vowles",
     "color_primary": "#005AFF", "color_secondary": "#FFFFFF", "engine_supplier": "Mercedes",
     "first_season": 1977, "championships": 7},
    {"slug": "haas", "name": "MoneyGram Haas F1 Team", "short_name": "Haas",
     "nationality": "American", "base": "Kannapolis, USA", "principal": "Ayao Komatsu",
     "color_primary": "#B6BABD", "color_secondary": "#E8001D", "engine_supplier": "Ferrari",
     "first_season": 2016, "championships": 0},
    {"slug": "racing-bulls", "name": "Visa Cash App RB Formula One Team", "short_name": "Racing Bulls",
     "nationality": "Italian", "base": "Faenza, Italy", "principal": "Laurent Mekies",
     "color_primary": "#1E3D8F", "color_secondary": "#FFFFFF", "engine_supplier": "Honda RBPT",
     "first_season": 2006, "championships": 0},
    {"slug": "audi", "name": "Audi Formula Racing GmbH", "short_name": "Audi",
     "nationality": "German", "base": "Hinwil, Switzerland", "principal": "Mattia Binotto",
     "color_primary": "#BB0000", "color_secondary": "#FFFFFF", "engine_supplier": "Audi",
     "first_season": 2026, "championships": 0},
]

DRIVERS = [
    {"slug": "verstappen", "first_name": "Max", "last_name": "Verstappen",
     "abbreviation": "VER", "number": 1, "nationality": "Dutch", "country_code": "NLD",
     "dob": "1997-09-30", "constructor_slug": "red-bull", "championships": 4,
     "career_wins": 62, "career_podiums": 112, "career_poles": 40},
    {"slug": "norris", "first_name": "Lando", "last_name": "Norris",
     "abbreviation": "NOR", "number": 4, "nationality": "British", "country_code": "GBR",
     "dob": "1999-11-13", "constructor_slug": "mclaren", "championships": 1,
     "career_wins": 18, "career_podiums": 48, "career_poles": 12},
    {"slug": "leclerc", "first_name": "Charles", "last_name": "Leclerc",
     "abbreviation": "LEC", "number": 16, "nationality": "Monegasque", "country_code": "MON",
     "dob": "1997-10-16", "constructor_slug": "ferrari", "championships": 0,
     "career_wins": 8, "career_podiums": 36, "career_poles": 24},
    {"slug": "hamilton", "first_name": "Lewis", "last_name": "Hamilton",
     "abbreviation": "HAM", "number": 44, "nationality": "British", "country_code": "GBR",
     "dob": "1985-01-07", "constructor_slug": "ferrari", "championships": 7,
     "career_wins": 103, "career_podiums": 197, "career_poles": 104},
    {"slug": "russell", "first_name": "George", "last_name": "Russell",
     "abbreviation": "RUS", "number": 63, "nationality": "British", "country_code": "GBR",
     "dob": "1998-02-15", "constructor_slug": "mercedes", "championships": 0,
     "career_wins": 3, "career_podiums": 22, "career_poles": 4},
    {"slug": "piastri", "first_name": "Oscar", "last_name": "Piastri",
     "abbreviation": "PIA", "number": 81, "nationality": "Australian", "country_code": "AUS",
     "dob": "2001-04-06", "constructor_slug": "mclaren", "championships": 0,
     "career_wins": 7, "career_podiums": 28, "career_poles": 3},
    {"slug": "alonso", "first_name": "Fernando", "last_name": "Alonso",
     "abbreviation": "ALO", "number": 14, "nationality": "Spanish", "country_code": "ESP",
     "dob": "1981-07-29", "constructor_slug": "aston-martin", "championships": 2,
     "career_wins": 32, "career_podiums": 98, "career_poles": 22},
    {"slug": "sainz", "first_name": "Carlos", "last_name": "Sainz",
     "abbreviation": "SAI", "number": 55, "nationality": "Spanish", "country_code": "ESP",
     "dob": "1994-09-01", "constructor_slug": "williams", "championships": 0,
     "career_wins": 3, "career_podiums": 24, "career_poles": 5},
    {"slug": "stroll", "first_name": "Lance", "last_name": "Stroll",
     "abbreviation": "STR", "number": 18, "nationality": "Canadian", "country_code": "CAN",
     "dob": "1998-10-29", "constructor_slug": "aston-martin", "championships": 0,
     "career_wins": 0, "career_podiums": 3, "career_poles": 1},
    {"slug": "lawson", "first_name": "Liam", "last_name": "Lawson",
     "abbreviation": "LAW", "number": 30, "nationality": "New Zealander", "country_code": "NZL",
     "dob": "2002-02-11", "constructor_slug": "red-bull", "championships": 0,
     "career_wins": 0, "career_podiums": 0, "career_poles": 0},
    {"slug": "hulkenberg", "first_name": "Nico", "last_name": "Hülkenberg",
     "abbreviation": "HUL", "number": 27, "nationality": "German", "country_code": "DEU",
     "dob": "1987-08-19", "constructor_slug": "audi", "championships": 0,
     "career_wins": 0, "career_podiums": 0, "career_poles": 1},
    {"slug": "antonelli", "first_name": "Kimi", "last_name": "Antonelli",
     "abbreviation": "ANT", "number": 12, "nationality": "Italian", "country_code": "ITA",
     "dob": "2006-08-25", "constructor_slug": "mercedes", "championships": 0,
     "career_wins": 0, "career_podiums": 2, "career_poles": 0},
    {"slug": "doohan", "first_name": "Jack", "last_name": "Doohan",
     "abbreviation": "DOO", "number": 7, "nationality": "Australian", "country_code": "AUS",
     "dob": "2003-01-20", "constructor_slug": "alpine", "championships": 0,
     "career_wins": 0, "career_podiums": 0, "career_poles": 0},
    {"slug": "gasly", "first_name": "Pierre", "last_name": "Gasly",
     "abbreviation": "GAS", "number": 10, "nationality": "French", "country_code": "FRA",
     "dob": "1996-02-07", "constructor_slug": "alpine", "championships": 0,
     "career_wins": 1, "career_podiums": 4, "career_poles": 0},
    {"slug": "bearman", "first_name": "Oliver", "last_name": "Bearman",
     "abbreviation": "BEA", "number": 87, "nationality": "British", "country_code": "GBR",
     "dob": "2005-05-08", "constructor_slug": "haas", "championships": 0,
     "career_wins": 0, "career_podiums": 0, "career_poles": 0},
    {"slug": "ocon", "first_name": "Esteban", "last_name": "Ocon",
     "abbreviation": "OCO", "number": 31, "nationality": "French", "country_code": "FRA",
     "dob": "1996-09-17", "constructor_slug": "haas", "championships": 0,
     "career_wins": 1, "career_podiums": 3, "career_poles": 0},
    {"slug": "tsunoda", "first_name": "Yuki", "last_name": "Tsunoda",
     "abbreviation": "TSU", "number": 22, "nationality": "Japanese", "country_code": "JPN",
     "dob": "2000-05-11", "constructor_slug": "racing-bulls", "championships": 0,
     "career_wins": 0, "career_podiums": 1, "career_poles": 0},
    {"slug": "hadjar", "first_name": "Isack", "last_name": "Hadjar",
     "abbreviation": "HAD", "number": 6, "nationality": "French", "country_code": "FRA",
     "dob": "2004-09-28", "constructor_slug": "racing-bulls", "championships": 0,
     "career_wins": 0, "career_podiums": 0, "career_poles": 0},
    {"slug": "colapinto", "first_name": "Franco", "last_name": "Colapinto",
     "abbreviation": "COL", "number": 43, "nationality": "Argentine", "country_code": "ARG",
     "dob": "2003-05-27", "constructor_slug": "williams", "championships": 0,
     "career_wins": 0, "career_podiums": 0, "career_poles": 0},
    {"slug": "bortoleto", "first_name": "Gabriel", "last_name": "Bortoleto",
     "abbreviation": "BOR", "number": 5, "nationality": "Brazilian", "country_code": "BRA",
     "dob": "2004-10-14", "constructor_slug": "audi", "championships": 0,
     "career_wins": 0, "career_podiums": 0, "career_poles": 0},
]

CIRCUITS = [
    {"slug": "albert-park", "name": "Albert Park Circuit", "short_name": "Albert Park",
     "city": "Melbourne", "country": "Australia", "country_code": "AUS",
     "lat": -37.8497, "lon": 144.968, "length_km": 5.278, "corners": 16,
     "circuit_type": "street", "overtaking": 3, "lap_record": "1:20.235",
     "lr_driver": "Charles Leclerc", "lr_year": 2022, "first_gp": 1996},
    {"slug": "shanghai", "name": "Shanghai International Circuit", "short_name": "Shanghai",
     "city": "Shanghai", "country": "China", "country_code": "CHN",
     "lat": 31.3389, "lon": 121.22, "length_km": 5.451, "corners": 16,
     "circuit_type": "permanent", "overtaking": 6, "lap_record": "1:32.238",
     "lr_driver": "Michael Schumacher", "lr_year": 2004, "first_gp": 2004},
    {"slug": "suzuka", "name": "Suzuka International Racing Course", "short_name": "Suzuka",
     "city": "Suzuka", "country": "Japan", "country_code": "JPN",
     "lat": 34.8431, "lon": 136.541, "length_km": 5.807, "corners": 18,
     "circuit_type": "permanent", "overtaking": 5, "lap_record": "1:30.983",
     "lr_driver": "Lewis Hamilton", "lr_year": 2019, "first_gp": 1987},
    {"slug": "bahrain", "name": "Bahrain International Circuit", "short_name": "Bahrain",
     "city": "Sakhir", "country": "Bahrain", "country_code": "BHR",
     "lat": 26.0325, "lon": 50.5106, "length_km": 5.412, "corners": 15,
     "circuit_type": "permanent", "overtaking": 7, "lap_record": "1:31.447",
     "lr_driver": "Pedro de la Rosa", "lr_year": 2005, "first_gp": 2004},
    {"slug": "jeddah", "name": "Jeddah Corniche Circuit", "short_name": "Jeddah",
     "city": "Jeddah", "country": "Saudi Arabia", "country_code": "SAU",
     "lat": 21.6319, "lon": 39.1044, "length_km": 6.174, "corners": 27,
     "circuit_type": "street", "overtaking": 4, "lap_record": "1:30.734",
     "lr_driver": "Lewis Hamilton", "lr_year": 2021, "first_gp": 2021},
    {"slug": "miami", "name": "Miami International Autodrome", "short_name": "Miami",
     "city": "Miami", "country": "United States", "country_code": "USA",
     "lat": 25.9581, "lon": -80.2389, "length_km": 5.412, "corners": 19,
     "circuit_type": "street", "overtaking": 5, "lap_record": "1:29.708",
     "lr_driver": "Max Verstappen", "lr_year": 2023, "first_gp": 2022},
    {"slug": "imola", "name": "Autodromo Enzo e Dino Ferrari", "short_name": "Imola",
     "city": "Imola", "country": "Italy", "country_code": "ITA",
     "lat": 44.3439, "lon": 11.7167, "length_km": 4.909, "corners": 19,
     "circuit_type": "permanent", "overtaking": 3, "lap_record": "1:15.484",
     "lr_driver": "Rubens Barrichello", "lr_year": 2004, "first_gp": 1980},
    {"slug": "monaco", "name": "Circuit de Monaco", "short_name": "Monaco",
     "city": "Monte Carlo", "country": "Monaco", "country_code": "MON",
     "lat": 43.7347, "lon": 7.4206, "length_km": 3.337, "corners": 19,
     "circuit_type": "street", "overtaking": 1, "lap_record": "1:12.909",
     "lr_driver": "Max Verstappen", "lr_year": 2023, "first_gp": 1950},
    {"slug": "barcelona", "name": "Circuit de Barcelona-Catalunya", "short_name": "Barcelona",
     "city": "Barcelona", "country": "Spain", "country_code": "ESP",
     "lat": 41.57, "lon": 2.2611, "length_km": 4.657, "corners": 16,
     "circuit_type": "permanent", "overtaking": 5, "lap_record": "1:16.330",
     "lr_driver": "Rubens Barrichello", "lr_year": 2009, "first_gp": 1991},
    {"slug": "montreal", "name": "Circuit Gilles Villeneuve", "short_name": "Montreal",
     "city": "Montreal", "country": "Canada", "country_code": "CAN",
     "lat": 45.5, "lon": -73.5228, "length_km": 4.361, "corners": 14,
     "circuit_type": "street", "overtaking": 7, "lap_record": "1:13.078",
     "lr_driver": "Valtteri Bottas", "lr_year": 2019, "first_gp": 1978},
    {"slug": "red-bull-ring", "name": "Red Bull Ring", "short_name": "Red Bull Ring",
     "city": "Spielberg", "country": "Austria", "country_code": "AUT",
     "lat": 47.2197, "lon": 14.7647, "length_km": 4.318, "corners": 10,
     "circuit_type": "permanent", "overtaking": 7, "lap_record": "1:05.619",
     "lr_driver": "Carlos Sainz", "lr_year": 2020, "first_gp": 1970},
    {"slug": "silverstone", "name": "Silverstone Circuit", "short_name": "Silverstone",
     "city": "Silverstone", "country": "United Kingdom", "country_code": "GBR",
     "lat": 52.0786, "lon": -1.0169, "length_km": 5.891, "corners": 18,
     "circuit_type": "permanent", "overtaking": 6, "lap_record": "1:27.097",
     "lr_driver": "Max Verstappen", "lr_year": 2020, "first_gp": 1950},
    {"slug": "spa", "name": "Circuit de Spa-Francorchamps", "short_name": "Spa",
     "city": "Spa", "country": "Belgium", "country_code": "BEL",
     "lat": 50.4372, "lon": 5.9714, "length_km": 7.004, "corners": 20,
     "circuit_type": "permanent", "overtaking": 8, "lap_record": "1:46.286",
     "lr_driver": "Valtteri Bottas", "lr_year": 2018, "first_gp": 1950},
    {"slug": "hungaroring", "name": "Hungaroring", "short_name": "Budapest",
     "city": "Budapest", "country": "Hungary", "country_code": "HUN",
     "lat": 47.5789, "lon": 19.2486, "length_km": 4.381, "corners": 14,
     "circuit_type": "permanent", "overtaking": 3, "lap_record": "1:16.627",
     "lr_driver": "Lewis Hamilton", "lr_year": 2020, "first_gp": 1986},
    {"slug": "zandvoort", "name": "Circuit Zandvoort", "short_name": "Zandvoort",
     "city": "Zandvoort", "country": "Netherlands", "country_code": "NLD",
     "lat": 52.3888, "lon": 4.5409, "length_km": 4.259, "corners": 14,
     "circuit_type": "permanent", "overtaking": 3, "lap_record": "1:11.097",
     "lr_driver": "Max Verstappen", "lr_year": 2021, "first_gp": 1952},
    {"slug": "monza", "name": "Autodromo Nazionale Monza", "short_name": "Monza",
     "city": "Monza", "country": "Italy", "country_code": "ITA",
     "lat": 45.6156, "lon": 9.2811, "length_km": 5.793, "corners": 11,
     "circuit_type": "permanent", "overtaking": 8, "lap_record": "1:21.046",
     "lr_driver": "Rubens Barrichello", "lr_year": 2004, "first_gp": 1950},
    {"slug": "marina-bay", "name": "Marina Bay Street Circuit", "short_name": "Singapore",
     "city": "Singapore", "country": "Singapore", "country_code": "SGP",
     "lat": 1.2914, "lon": 103.864, "length_km": 4.94, "corners": 23,
     "circuit_type": "street", "overtaking": 2, "lap_record": "1:35.867",
     "lr_driver": "Kevin Magnussen", "lr_year": 2018, "first_gp": 2008},
    {"slug": "baku", "name": "Baku City Circuit", "short_name": "Baku",
     "city": "Baku", "country": "Azerbaijan", "country_code": "AZE",
     "lat": 40.3725, "lon": 49.8533, "length_km": 6.003, "corners": 20,
     "circuit_type": "street", "overtaking": 8, "lap_record": "1:43.009",
     "lr_driver": "Charles Leclerc", "lr_year": 2019, "first_gp": 2016},
    {"slug": "cota", "name": "Circuit of The Americas", "short_name": "Austin",
     "city": "Austin", "country": "United States", "country_code": "USA",
     "lat": 30.1328, "lon": -97.6411, "length_km": 5.513, "corners": 20,
     "circuit_type": "permanent", "overtaking": 6, "lap_record": "1:36.169",
     "lr_driver": "Charles Leclerc", "lr_year": 2019, "first_gp": 2012},
    {"slug": "mexico-city", "name": "Autodromo Hermanos Rodriguez", "short_name": "Mexico City",
     "city": "Mexico City", "country": "Mexico", "country_code": "MEX",
     "lat": 19.4042, "lon": -99.0907, "length_km": 4.304, "corners": 17,
     "circuit_type": "permanent", "overtaking": 5, "lap_record": "1:17.774",
     "lr_driver": "Valtteri Bottas", "lr_year": 2021, "first_gp": 1963},
    {"slug": "interlagos", "name": "Autodromo Jose Carlos Pace", "short_name": "São Paulo",
     "city": "São Paulo", "country": "Brazil", "country_code": "BRA",
     "lat": -23.7036, "lon": -46.6997, "length_km": 4.309, "corners": 15,
     "circuit_type": "permanent", "overtaking": 6, "lap_record": "1:10.540",
     "lr_driver": "Valtteri Bottas", "lr_year": 2018, "first_gp": 1973},
    {"slug": "las-vegas", "name": "Las Vegas Street Circuit", "short_name": "Las Vegas",
     "city": "Las Vegas", "country": "United States", "country_code": "USA",
     "lat": 36.1147, "lon": -115.173, "length_km": 6.201, "corners": 17,
     "circuit_type": "street", "overtaking": 6, "lap_record": "1:35.490",
     "lr_driver": "Oscar Piastri", "lr_year": 2023, "first_gp": 2023},
    {"slug": "lusail", "name": "Lusail International Circuit", "short_name": "Qatar",
     "city": "Lusail", "country": "Qatar", "country_code": "QAT",
     "lat": 25.49, "lon": 51.4542, "length_km": 5.38, "corners": 16,
     "circuit_type": "permanent", "overtaking": 7, "lap_record": "1:24.319",
     "lr_driver": "Max Verstappen", "lr_year": 2023, "first_gp": 2021},
    {"slug": "yas-marina", "name": "Yas Marina Circuit", "short_name": "Abu Dhabi",
     "city": "Abu Dhabi", "country": "United Arab Emirates", "country_code": "UAE",
     "lat": 24.4672, "lon": 54.6031, "length_km": 5.281, "corners": 16,
     "circuit_type": "permanent", "overtaking": 5, "lap_record": "1:26.103",
     "lr_driver": "Max Verstappen", "lr_year": 2021, "first_gp": 2009},
]

# 2026 Calendar — 24 races (12 completed, 12 upcoming as of July 23 2026)
RACES_2026 = [
    {"round": 1, "name": "Australian Grand Prix", "country": "Australia",
     "circuit": "albert-park", "date": "2026-03-15", "status": "completed"},
    {"round": 2, "name": "Chinese Grand Prix", "country": "China",
     "circuit": "shanghai", "date": "2026-03-22", "status": "completed"},
    {"round": 3, "name": "Japanese Grand Prix", "country": "Japan",
     "circuit": "suzuka", "date": "2026-04-05", "status": "completed"},
    {"round": 4, "name": "Bahrain Grand Prix", "country": "Bahrain",
     "circuit": "bahrain", "date": "2026-04-19", "status": "completed"},
    {"round": 5, "name": "Saudi Arabian Grand Prix", "country": "Saudi Arabia",
     "circuit": "jeddah", "date": "2026-04-26", "status": "completed"},
    {"round": 6, "name": "Miami Grand Prix", "country": "United States",
     "circuit": "miami", "date": "2026-05-10", "status": "completed", "sprint": True},
    {"round": 7, "name": "Emilia Romagna Grand Prix", "country": "Italy",
     "circuit": "imola", "date": "2026-05-24", "status": "completed"},
    {"round": 8, "name": "Monaco Grand Prix", "country": "Monaco",
     "circuit": "monaco", "date": "2026-05-31", "status": "completed"},
    {"round": 9, "name": "Spanish Grand Prix", "country": "Spain",
     "circuit": "barcelona", "date": "2026-06-14", "status": "completed"},
    {"round": 10, "name": "Canadian Grand Prix", "country": "Canada",
     "circuit": "montreal", "date": "2026-06-21", "status": "completed"},
    {"round": 11, "name": "Austrian Grand Prix", "country": "Austria",
     "circuit": "red-bull-ring", "date": "2026-06-28", "status": "completed", "sprint": True},
    {"round": 12, "name": "British Grand Prix", "country": "United Kingdom",
     "circuit": "silverstone", "date": "2026-07-05", "status": "completed"},
    {"round": 13, "name": "Belgian Grand Prix", "country": "Belgium",
     "circuit": "spa", "date": "2026-07-26", "status": "active"},
    {"round": 14, "name": "Hungarian Grand Prix", "country": "Hungary",
     "circuit": "hungaroring", "date": "2026-08-02", "status": "upcoming"},
    {"round": 15, "name": "Dutch Grand Prix", "country": "Netherlands",
     "circuit": "zandvoort", "date": "2026-08-30", "status": "upcoming"},
    {"round": 16, "name": "Italian Grand Prix", "country": "Italy",
     "circuit": "monza", "date": "2026-09-06", "status": "upcoming"},
    {"round": 17, "name": "Singapore Grand Prix", "country": "Singapore",
     "circuit": "marina-bay", "date": "2026-09-20", "status": "upcoming"},
    {"round": 18, "name": "Azerbaijan Grand Prix", "country": "Azerbaijan",
     "circuit": "baku", "date": "2026-09-27", "status": "upcoming"},
    {"round": 19, "name": "United States Grand Prix", "country": "United States",
     "circuit": "cota", "date": "2026-10-18", "status": "upcoming", "sprint": True},
    {"round": 20, "name": "Mexico City Grand Prix", "country": "Mexico",
     "circuit": "mexico-city", "date": "2026-10-25", "status": "upcoming"},
    {"round": 21, "name": "São Paulo Grand Prix", "country": "Brazil",
     "circuit": "interlagos", "date": "2026-11-08", "status": "upcoming", "sprint": True},
    {"round": 22, "name": "Las Vegas Grand Prix", "country": "United States",
     "circuit": "las-vegas", "date": "2026-11-21", "status": "upcoming"},
    {"round": 23, "name": "Qatar Grand Prix", "country": "Qatar",
     "circuit": "lusail", "date": "2026-11-29", "status": "upcoming", "sprint": True},
    {"round": 24, "name": "Abu Dhabi Grand Prix", "country": "United Arab Emirates",
     "circuit": "yas-marina", "date": "2026-12-06", "status": "upcoming"},
]

# Championship standings after 12 races (2026 season)
DRIVER_STANDINGS_2026 = [
    {"driver": "norris",     "constructor": "mclaren",      "pos": 1,  "pts": 219, "wins": 6, "podiums": 9, "poles": 5, "dnfs": 0, "races": 12},
    {"driver": "verstappen", "constructor": "red-bull",     "pos": 2,  "pts": 196, "wins": 4, "podiums": 7, "poles": 4, "dnfs": 1, "races": 12},
    {"driver": "leclerc",    "constructor": "ferrari",      "pos": 3,  "pts": 158, "wins": 1, "podiums": 6, "poles": 2, "dnfs": 0, "races": 12},
    {"driver": "piastri",    "constructor": "mclaren",      "pos": 4,  "pts": 143, "wins": 1, "podiums": 5, "poles": 1, "dnfs": 1, "races": 12},
    {"driver": "hamilton",   "constructor": "ferrari",      "pos": 5,  "pts": 128, "wins": 0, "podiums": 4, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "russell",    "constructor": "mercedes",     "pos": 6,  "pts": 104, "wins": 0, "podiums": 3, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "alonso",     "constructor": "aston-martin", "pos": 7,  "pts": 72,  "wins": 0, "podiums": 1, "poles": 0, "dnfs": 1, "races": 12},
    {"driver": "sainz",      "constructor": "williams",     "pos": 8,  "pts": 58,  "wins": 0, "podiums": 0, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "antonelli",  "constructor": "mercedes",     "pos": 9,  "pts": 42,  "wins": 0, "podiums": 0, "poles": 0, "dnfs": 1, "races": 12},
    {"driver": "gasly",      "constructor": "alpine",       "pos": 10, "pts": 31,  "wins": 0, "podiums": 0, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "tsunoda",    "constructor": "racing-bulls", "pos": 11, "pts": 28,  "wins": 0, "podiums": 0, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "hulkenberg",  "constructor": "audi",        "pos": 12, "pts": 22,  "wins": 0, "podiums": 0, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "lawson",     "constructor": "red-bull",     "pos": 13, "pts": 19,  "wins": 0, "podiums": 0, "poles": 0, "dnfs": 2, "races": 12},
    {"driver": "hadjar",     "constructor": "racing-bulls", "pos": 14, "pts": 14,  "wins": 0, "podiums": 0, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "bearman",    "constructor": "haas",         "pos": 15, "pts": 12,  "wins": 0, "podiums": 0, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "stroll",     "constructor": "aston-martin", "pos": 16, "pts": 8,   "wins": 0, "podiums": 0, "poles": 0, "dnfs": 1, "races": 12},
    {"driver": "colapinto",  "constructor": "williams",     "pos": 17, "pts": 6,   "wins": 0, "podiums": 0, "poles": 0, "dnfs": 0, "races": 12},
    {"driver": "ocon",       "constructor": "haas",         "pos": 18, "pts": 4,   "wins": 0, "podiums": 0, "poles": 0, "dnfs": 2, "races": 12},
    {"driver": "doohan",     "constructor": "alpine",       "pos": 19, "pts": 3,   "wins": 0, "podiums": 0, "poles": 0, "dnfs": 1, "races": 12},
    {"driver": "bortoleto",  "constructor": "audi",         "pos": 20, "pts": 2,   "wins": 0, "podiums": 0, "poles": 0, "dnfs": 2, "races": 12},
]

CONSTRUCTOR_STANDINGS_2026 = [
    {"constructor": "mclaren",      "pos": 1, "pts": 362, "wins": 7, "podiums": 14},
    {"constructor": "ferrari",      "pos": 2, "pts": 286, "wins": 1, "podiums": 10},
    {"constructor": "red-bull",     "pos": 3, "pts": 215, "wins": 4, "podiums": 7},
    {"constructor": "mercedes",     "pos": 4, "pts": 146, "wins": 0, "podiums": 3},
    {"constructor": "aston-martin", "pos": 5, "pts": 80,  "wins": 0, "podiums": 1},
    {"constructor": "williams",     "pos": 6, "pts": 64,  "wins": 0, "podiums": 0},
    {"constructor": "alpine",       "pos": 7, "pts": 34,  "wins": 0, "podiums": 0},
    {"constructor": "racing-bulls", "pos": 8, "pts": 42,  "wins": 0, "podiums": 0},
    {"constructor": "audi",         "pos": 9, "pts": 24,  "wins": 0, "podiums": 0},
    {"constructor": "haas",         "pos": 10,"pts": 16,  "wins": 0, "podiums": 0},
]


def run():
    print("🏎️  PaddockAI — Seeding database...")

    with Session() as session:
        # ── Constructors ──────────────────────────────────────────────────────
        print("  → Inserting constructors...")
        constructor_map = {}
        for c in CONSTRUCTORS:
            cid = str(uuid.uuid4())
            constructor_map[c["slug"]] = cid
            session.execute(text("""
                INSERT INTO constructors (id, slug, name, short_name, nationality, base, principal,
                    color_primary, color_secondary, engine_supplier, first_season, championships)
                VALUES (:id, :slug, :name, :short_name, :nationality, :base, :principal,
                    :color_primary, :color_secondary, :engine_supplier, :first_season, :championships)
                ON CONFLICT (slug) DO UPDATE SET
                    name=EXCLUDED.name, color_primary=EXCLUDED.color_primary,
                    principal=EXCLUDED.principal, championships=EXCLUDED.championships
                RETURNING id
            """), {**c, "id": cid})
        # Re-fetch actual IDs (in case of ON CONFLICT DO UPDATE)
        rows = session.execute(text("SELECT id, slug FROM constructors")).fetchall()
        constructor_map = {r.slug: str(r.id) for r in rows}

        # ── Drivers ───────────────────────────────────────────────────────────
        print("  → Inserting drivers...")
        driver_map = {}
        for d in DRIVERS:
            did = str(uuid.uuid4())
            driver_map[d["slug"]] = did
            session.execute(text("""
                INSERT INTO drivers (id, slug, first_name, last_name, abbreviation, number,
                    nationality, country_code, date_of_birth, constructor_id, active,
                    championships, career_wins, career_podiums, career_poles)
                VALUES (:id, :slug, :first_name, :last_name, :abbr, :number,
                    :nationality, :country_code, :dob, :constructor_id, true,
                    :championships, :career_wins, :career_podiums, :career_poles)
                ON CONFLICT (slug) DO UPDATE SET
                    constructor_id=EXCLUDED.constructor_id, active=true
                RETURNING id
            """), {
                "id": did, "slug": d["slug"],
                "first_name": d["first_name"], "last_name": d["last_name"],
                "abbr": d["abbreviation"], "number": d["number"],
                "nationality": d["nationality"], "country_code": d["country_code"],
                "dob": d["dob"],
                "constructor_id": constructor_map[d["constructor_slug"]],
                "championships": d["championships"],
                "career_wins": d["career_wins"], "career_podiums": d["career_podiums"],
                "career_poles": d["career_poles"],
            })
        rows = session.execute(text("SELECT id, slug FROM drivers")).fetchall()
        driver_map = {r.slug: str(r.id) for r in rows}

        # ── Circuits ──────────────────────────────────────────────────────────
        print("  → Inserting circuits...")
        circuit_map = {}
        for c in CIRCUITS:
            cid = str(uuid.uuid4())
            circuit_map[c["slug"]] = cid
            session.execute(text("""
                INSERT INTO circuits (id, slug, name, short_name, city, country, country_code,
                    latitude, longitude, length_km, corners, circuit_type, overtaking_difficulty,
                    lap_record, lap_record_driver, lap_record_year, first_gp_year)
                VALUES (:id, :slug, :name, :short_name, :city, :country, :country_code,
                    :lat, :lon, :length_km, :corners, :circuit_type, :overtaking,
                    :lap_record, :lr_driver, :lr_year, :first_gp)
                ON CONFLICT (slug) DO UPDATE SET name=EXCLUDED.name
                RETURNING id
            """), {**c, "id": cid})
        rows = session.execute(text("SELECT id, slug FROM circuits")).fetchall()
        circuit_map = {r.slug: str(r.id) for r in rows}

        # ── Season 2026 ───────────────────────────────────────────────────────
        print("  → Inserting 2026 season...")
        season_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO seasons (id, year, total_rounds, current, status)
            VALUES (:id, 2026, 24, true, 'active')
            ON CONFLICT (year) DO UPDATE SET current=true
            RETURNING id
        """), {"id": season_id})
        row = session.execute(text("SELECT id FROM seasons WHERE year=2026")).fetchone()
        season_id = str(row.id)

        # ── Races 2026 ────────────────────────────────────────────────────────
        print("  → Inserting 2026 races and sessions...")
        race_map = {}
        for r in RACES_2026:
            rid = str(uuid.uuid4())
            session.execute(text("""
                INSERT INTO races (id, season_id, circuit_id, round_number, gp_name,
                    country, date, status, has_sprint)
                VALUES (:id, :season_id, :circuit_id, :round, :name, :country, :date, :status, :sprint)
                ON CONFLICT (season_id, round_number) DO UPDATE SET
                    status=EXCLUDED.status, circuit_id=EXCLUDED.circuit_id
                RETURNING id
            """), {
                "id": rid, "season_id": season_id,
                "circuit_id": circuit_map.get(r["circuit"]),
                "round": r["round"], "name": r["name"],
                "country": r["country"], "date": r["date"],
                "status": r["status"], "sprint": r.get("sprint", False),
            })

        rows = session.execute(
            text("SELECT id, round_number FROM races WHERE season_id=:sid"),
            {"sid": season_id}
        ).fetchall()
        race_map_by_round = {row.round_number: str(row.id) for row in rows}

        # Create sessions for each race
        SESSION_TYPES = {
            False: ["fp1", "fp2", "fp3", "qualifying", "race"],
            True:  ["fp1", "sprint_qualifying", "sprint", "qualifying", "race"],
        }
        SESSION_OFFSETS = {
            "fp1": -3, "fp2": -3, "fp3": -2,
            "sprint_qualifying": -2, "sprint": -2,
            "qualifying": -2, "race": 0,
        }

        for r in RACES_2026:
            race_id = race_map_by_round[r["round"]]
            race_date = date.fromisoformat(r["date"])
            is_sprint = r.get("sprint", False)
            session_types = SESSION_TYPES[is_sprint]

            for stype in session_types:
                from datetime import timedelta
                scheduled = datetime.combine(
                    race_date + timedelta(days=SESSION_OFFSETS.get(stype, 0)),
                    datetime.min.time()
                ).replace(tzinfo=timezone.utc)

                # Determine session status based on race status
                if r["status"] == "completed":
                    sstatus = "completed"
                elif r["status"] == "active":
                    sstatus = "upcoming"  # sessions start as upcoming even for active race
                else:
                    sstatus = "upcoming"

                session.execute(text("""
                    INSERT INTO sessions (id, race_id, session_type, scheduled_at, status)
                    VALUES (:id, :race_id, :stype, :scheduled_at, :status)
                    ON CONFLICT (race_id, session_type) DO UPDATE SET status=EXCLUDED.status
                """), {
                    "id": str(uuid.uuid4()), "race_id": race_id,
                    "stype": stype, "scheduled_at": scheduled, "status": sstatus,
                })

        # ── Driver standings ─────────────────────────────────────────────────
        print("  → Inserting 2026 driver standings...")
        for s in DRIVER_STANDINGS_2026:
            did = driver_map.get(s["driver"])
            cid = constructor_map.get(s["constructor"])
            if not did:
                print(f"    ⚠ Driver not found: {s['driver']}")
                continue
            session.execute(text("""
                INSERT INTO driver_standings (id, season_id, driver_id, constructor_id,
                    position, points, wins, podiums, poles, dnfs, races_entered)
                VALUES (:id, :season_id, :driver_id, :constructor_id,
                    :pos, :pts, :wins, :podiums, :poles, :dnfs, :races)
                ON CONFLICT (season_id, driver_id) DO UPDATE SET
                    position=EXCLUDED.position, points=EXCLUDED.points,
                    wins=EXCLUDED.wins, podiums=EXCLUDED.podiums, poles=EXCLUDED.poles,
                    dnfs=EXCLUDED.dnfs, races_entered=EXCLUDED.races_entered
            """), {
                "id": str(uuid.uuid4()), "season_id": season_id,
                "driver_id": did, "constructor_id": cid,
                "pos": s["pos"], "pts": s["pts"], "wins": s["wins"],
                "podiums": s["podiums"], "poles": s["poles"],
                "dnfs": s["dnfs"], "races": s["races"],
            })

        # ── Constructor standings ─────────────────────────────────────────────
        print("  → Inserting 2026 constructor standings...")
        for s in CONSTRUCTOR_STANDINGS_2026:
            cid = constructor_map.get(s["constructor"])
            if not cid:
                continue
            session.execute(text("""
                INSERT INTO constructor_standings (id, season_id, constructor_id,
                    position, points, wins, podiums)
                VALUES (:id, :season_id, :constructor_id, :pos, :pts, :wins, :podiums)
                ON CONFLICT (season_id, constructor_id) DO UPDATE SET
                    position=EXCLUDED.position, points=EXCLUDED.points,
                    wins=EXCLUDED.wins, podiums=EXCLUDED.podiums
            """), {
                "id": str(uuid.uuid4()), "season_id": season_id,
                "constructor_id": cid,
                "pos": s["pos"], "pts": s["pts"], "wins": s["wins"], "podiums": s["podiums"],
            })

        session.commit()
        print("✅  Database seeded successfully!")
        print(f"   • {len(CONSTRUCTORS)} constructors")
        print(f"   • {len(DRIVERS)} drivers")
        print(f"   • {len(CIRCUITS)} circuits")
        print(f"   • {len(RACES_2026)} races (2026 season)")
        print(f"   • {len(DRIVER_STANDINGS_2026)} driver standings entries")
        print(f"   • {len(CONSTRUCTOR_STANDINGS_2026)} constructor standings entries")


if __name__ == "__main__":
    run()
