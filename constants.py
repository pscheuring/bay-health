import pandas as pd
from typing import Dict, List, Any

# Load muscle usage matrix
# The CSV contains the relative usage of muscles per exercise.
# Values are normalized (divided by 4) and converted to percentages.
MUSCLE_MATRIX: pd.DataFrame = (
    pd.read_csv("data/muscle_use.csv", sep=";")
    .set_index("exercise")
    .fillna(0)
)
MUSCLE_MATRIX = MUSCLE_MATRIX / 4 * 100

# Mapping from muscle names (used in the code) to SVG group/path IDs
# This is used for dynamically coloring the SVG muscle map based on exercise load.
MUSCLE_SVG_MAPPING: Dict[str, Dict[str, Any]] = {
    "pectoralis_major": {
        "group": "g3",
        "paths": ["path2", "path3"]
    },
    "deltoid": {
        "group": "g5",
        "paths": ["path4", "path5"]
    },
    "trapecius": {
        "group": "g7",
        "paths": ["path6", "path7", "path37", "path38"]
    },
    "biceps_brachi": {
        "group": "g9",
        "paths": ["path8", "path9"]
    },
    "oblique": {
        "group": "g13",
        "paths": ["path10", "path11", "path12", "path13"]
    },
    "brachialis": {
        "group": "g17",
        "paths": ["path14", "path15", "path16", "path17"]
    },
    "sternocleidomastoid": {
        "group": "g19",
        "paths": ["path18", "path19"]
    },
    "rectus_abdominis": {
        "group": "g24",
        "paths": ["path20", "path21", "path23", "path24"]
    },
    "brachioradialis": {
        "group": "g26",
        "paths": ["path25", "path26", "path54", "path55", "path56"]
    },
    "quadriceps": {
        "group": "g28",
        "paths": ["path27", "path28"]
    },
    "gastrocnemius": {
        "group": "g32",
        "paths": ["path29", "path30", "path31", "path32"]
    },
    "latissimus_dorsi": {
        "group": "g34",
        "paths": ["path33", "path34"]
    },
    "terres_major": {
        "group": "g36",
        "paths": ["path35", "path36"]
    },
    "infraspinatus": {
        "group": "g41",
        "paths": ["path40", "path41"]
    },
    "posterior_head": {
        "group": "g44",
        "paths": ["path42", "path43", "path44"]
    },
    "gluteus_maximus": {
        "group": "g46",
        "paths": ["path45", "path46"]
    },
    "soleus": {
        "group": "g48",
        "paths": ["path47", "path48"]
    },
    "triceps_brachi": {
        "group": "g50",
        "paths": ["path49", "path50"]
    },
    "erector_spinae": {
        "group": "g51",
        "paths": ["path51"]
    },
    "levator_scapulae": {
        "group": "g53",
        "paths": ["path52", "path53"]
    }
}

# List of predefined exercises displayed in the app
# Each entry contains:
# - id: Internal identifier used in callbacks
# - title: Display name (German text kept as-is for UI)
# - src: Path to exercise image
# - category: Muscle group category
# - equipment: Equipment type
EXERCISES: List[Dict[str, Any]] = [
    {"id": "barbell_squat", "title": "Kniebeugen (Langhantel)", "src": "/assets/barbell_squat.jpg", "category": "Beine", "equipment": "Langhantel"},
    {"id": "barbell_bench_press", "title": "Bankdrücken (Langhantel)", "src": "/assets/barbell_bench_press.jpg", "category": "Brust", "equipment": "Langhantel"},
    {"id": "barbell_deadlift", "title": "Kreuzheben (Langhantel)", "src": "/assets/barbell_deadlift.jpg", "category": "Rücken", "equipment": "Langhantel"},
    {"id": "assisted_chin-up", "title": "Unterstützter Klimmzug", "src": "/assets/assisted_chin-up.jpg", "category": "Rücken", "equipment": "Maschine"},
    {"id": "barbell_bent-over_row", "title": "Rudern vorgebeugt (Langhantel)", "src": "/assets/barbell_bent-over_row.jpg", "category": "Rücken", "equipment": "Langhantel"},
    {"id": "barbell_hip_thrust", "title": "Hüftstoß (Langhantel)", "src": "/assets/barbell_hip_thrust.jpg", "category": "Gesäß / Beine", "equipment": "Langhantel"},
    {"id": "barbell_standing_calf_raise", "title": "Wadenheben stehend (Langhantel)", "src": "/assets/barbell_standing_calf_raise.jpg", "category": "Waden", "equipment": "Langhantel"},
    {"id": "cable_pulldown", "title": "Latzug am Kabelzug", "src": "/assets/cable_pulldown.jpg", "category": "Rücken", "equipment": "Kabelzug"},
    {"id": "dumbbell_bench_press", "title": "Bankdrücken (Kurzhantel)", "src": "/assets/dumbbell_bench_press.jpg", "category": "Brust", "equipment": "Kurzhantel"},
    {"id": "dumbbell_bent-over_row", "title": "Rudern vorgebeugt (Kurzhantel)", "src": "/assets/dumbbell_bent-over_row.jpg", "category": "Rücken", "equipment": "Kurzhantel"},
    {"id": "dumbbell_hammer_curl", "title": "Hammer-Curl (Kurzhantel)", "src": "/assets/dumbbell_hammer_curl.jpg", "category": "Arme", "equipment": "Kurzhantel"},
    {"id": "dumbbell_incline_press", "title": "Schrägbankdrücken (Kurzhantel)", "src": "/assets/dumbbell_incline_press.jpg", "category": "Brust", "equipment": "Kurzhantel"},
    {"id": "dumbbell_lateral_raise", "title": "Seitheben (Kurzhantel)", "src": "/assets/dumbbell_lateral_raise.jpg", "category": "Schulter", "equipment": "Kurzhantel"},
    {"id": "leg_press", "title": "Beinpresse", "src": "/assets/leg_press.jpg", "category": "Beine", "equipment": "Maschine"},
    {"id": "lever_neutral_grip_incline_row", "title": "Rudern an Maschine mit neutralem Griff", "src": "/assets/lever_neutral_grip_incline_row.jpg", "category": "Rücken", "equipment": "Maschine"},
    {"id": "lever_seated_fly", "title": "Butterfly an der Maschine", "src": "/assets/lever_seated_fly.jpg", "category": "Brust", "equipment": "Maschine"},
    {"id": "lever_seated_leg_curl", "title": "Beinbeuger sitzend an Maschine", "src": "/assets/lever_seated_leg_curl.jpg", "category": "Beine", "equipment": "Maschine"},
    {"id": "overhead_barbell_press", "title": "Schulterdrücken (Langhantel)", "src": "/assets/overhead_barbell_press.jpg", "category": "Schulter", "equipment": "Langhantel"},
    {"id": "sit-up", "title": "Sit-up", "src": "/assets/sit-up.jpg", "category": "Bauch", "equipment": "Körpergewicht"},
    {"id": "weight_incline_sit-up", "title": "Schräger Sit-up mit Gewicht", "src": "/assets/weight_incline_sit-up.jpg", "category": "Bauch", "equipment": "Körpergewicht"},
    {"id": "weighted_vertical_leg_raise", "title": "Vertikales Beinheben mit Gewicht", "src": "/assets/weighted_vertical_leg_raise.jpg", "category": "Bauch", "equipment": "Körpergewicht"},
]
