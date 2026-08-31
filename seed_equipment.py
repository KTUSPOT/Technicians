"""
seed_equipment.py

Seeds the `equipment` collection in Firestore with your lab's
equipment master data, using the Firebase Admin SDK.

Safe to re-run: uses equipment_id as the document ID, so re-running
this script overwrites existing docs rather than duplicating them.

Prerequisites:
    1. Get 'serviceAccountKey.json' from your Firebase project:
       Firebase Console -> Project Settings -> Service Accounts
       -> Generate new private key
       Place it in the same folder as this script (DO NOT commit
       this file to git — add it to .gitignore).
    2. pip install -r requirements.txt

Usage:
    python seed_equipment.py
"""

import os
import csv
import sys
from datetime import datetime, timezone

import firebase_admin
from firebase_admin import credentials, firestore

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"

# Option A: hardcode equipment data here (keep in sync with generate_qr.py)
EQUIPMENT_LIST = [
    {
        "id": "EQ001",
        "name": "Dell Monitor 24-inch",
        "lab_no": "CS Lab 2",
        "category": "monitor",
        "status": "Working",
    },
    {
        "id": "EQ002",
        "name": "HP Projector",
        "lab_no": "CS Lab 1",
        "category": "projector",
        "status": "Working",
    },
    {
        "id": "EQ003",
        "name": "Desktop PC - Unit 5",
        "lab_no": "CS Lab 2",
        "category": "computer",
        "status": "Working",
    },
]

# Option B: load from a CSV instead (uncomment to use)
# CSV format expected: id,name,lab_no,category,status
#
# def load_from_csv(path="equipment.csv"):
#     items = []
#     with open(path, newline="", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             items.append(row)
#     return items
#
# EQUIPMENT_LIST = load_from_csv()


# ---------------------------------------------------------------------------
# FIREBASE INIT
# ---------------------------------------------------------------------------

def init_firestore():
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        print(f"ERROR: '{SERVICE_ACCOUNT_PATH}' not found.")
        print("Download it from Firebase Console -> Project Settings")
        print("-> Service Accounts -> Generate new private key")
        sys.exit(1)

    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    return firestore.client()


# ---------------------------------------------------------------------------
# SEEDING
# ---------------------------------------------------------------------------

def seed_equipment(db, equipment_list):
    collection = db.collection("equipment")
    count = 0

    for item in equipment_list:
        doc_id = item["id"]
        data = {
            "name": item["name"],
            "lab_no": item["lab_no"],
            "category": item["category"],
            "status": item.get("status", "Working"),
            "created_at": datetime.now(timezone.utc),
        }
        collection.document(doc_id).set(data, merge=True)
        print(f"  Seeded: {doc_id} -> {data['name']} ({data['lab_no']})")
        count += 1

    return count


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Connecting to Firestore...")
    db = init_firestore()

    print(f"\nSeeding {len(EQUIPMENT_LIST)} equipment item(s)...\n")
    total = seed_equipment(db, EQUIPMENT_LIST)

    print(f"\nDone. {total} equipment document(s) written to Firestore.")
