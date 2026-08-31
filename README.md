Lab Equipment Complaint & Maintenance Tracker

A QR-based centralized system for reporting, tracking, and resolving faulty lab equipment in college laboratories — built to replace informal, untracked complaint reporting with a structured digital workflow.

Problem Statement

College laboratories house a wide range of equipment — computers, monitors, projectors, machines, and other electronic devices. When equipment is damaged or malfunctioning, there is currently no proper system for students to report the issue. Complaints are typically made verbally to a lab assistant or faculty member, which leads to several recurring problems:

- Repeated issues on the same equipment go unnoticed since there's no record.
- Repairs are delayed due to lack of tracking.
- Students and staff have no way of knowing whether an issue has already been reported.
- Repair status is invisible to the student who reported it.
- Lab staff struggle to prioritize which equipment needs urgent attention.

problem statement:** *College laboratories lack a proper centralized system to report faulty equipment and track maintenance status, resulting in repair delays and equipment management problems.*

---

Solution

Each lab equipment item is assigned a **unique QR code**. When a student encounters a malfunctioning device, they can:

1.  Scan the equipment's QR code
2.  View auto-fetched equipment details
3.  Select or type the problem
4.  Upload a photo of the issue
5.  Submit the complaint

The complaint is instantly registered in the system, and lab technicians/admins receive a notification. Technicians can then update the complaint status through its lifecycle:

Students can track the live status of their submitted complaints at any time.

---

 Core Features

- **QR-based equipment identification** — no manual entry, no ambiguity about which device is faulty
- **Structured complaint submission** — problem type, description, and photo evidence
- **Real-time status tracking** — students see live updates without needing to follow up manually
- **Centralized admin/technician dashboard** — view, filter, and manage all complaints in one place
- **Push notifications** — technicians are alerted the moment a new complaint is submitted
- **Equipment history** — repeated faults on the same device become visible over time

---

Tech Stack

| Layer | Technology |
|---|---|
| Frontend (Student + Admin App) | Flutter |
| Backend | Firebase (Firestore, Auth, Storage, Cloud Functions) |
| Notifications | Firebase Cloud Messaging (FCM) |
| QR Generation | Python `qrcode` library |
| Hosting | Firebase Hosting |

---

Data Model

### `equipment`
| Field | Type | Description |
|---|---|---|
| `name` | string | Equipment name |
| `lab_no` | string | Lab identifier |
| `category` | string | Equipment category |
| `status` | string | `Working` / `Under Repair` / `Faulty` |
| `created_at` | timestamp | Record creation time |

### `complaints`
| Field | Type | Description |
|---|---|---|
| `equipment_id` | string | References `equipment` document |
| `student_id` | string | UID of reporting student |
| `problem_type` | string | Predefined issue category |
| `description` | string | Free-text problem description |
| `photo_url` | string | Uploaded photo link |
| `status` | string | `Pending` / `In Progress` / `Repaired` |
| `technician_remarks` | string | Notes added by technician |
| `created_at` | timestamp | Complaint submission time |
| `updated_at` | timestamp | Last status update time |

### `users`
| Field | Type | Description |
|---|---|---|
| `role` | string | `student` / `technician` / `admin` |
| `name` | string | User's display name |
| `email` | string | User's email |

---

 System Architecture

[Student App] --scan QR--> [Equipment Lookup] --submit--> [Firestore: complaints]
|
[Cloud Function trigger]
|
[FCM Notification]
|
[Admin/Technician Dashboard]
|
[Status Update: Pending → In Progress → Repaired]
|
[Student sees live status]


---

Team & Module Ownership

| Member | Module |
|---|---|
| Member A | Student App — QR scan, equipment detail, complaint form, status view |
| Member B | Admin/Technician App — dashboard, status updates, remarks |
| Member C | Backend/Firebase — Firestore schema, security rules, Auth, Storage, Cloud Functions |
| Member D | QR Generation, Data Seeding, Integration & Testing |

---

 Getting Started

### Prerequisites
- Flutter SDK
- Firebase CLI (`npm install -g firebase-tools`)
- A Firebase project with Firestore, Authentication (Email/Password), and Storage enabled

### Setup
```bash
git clone <repo-url>
cd lab-equipment-tracker
flutter pub get
```

1. Add your `google-services.json` (Android) to `android/app/`
2. Configure Firebase in the project:
```bash
   firebase login
   firebase use <your-project-id>
```
3. Deploy Firestore security rules:
```bash
   firebase deploy --only firestore:rules
```
4. Run the app:
```bash
   flutter run
```

---

 Testing

End-to-end test cases covering the full complaint lifecycle — submission, notification, status updates, and edge cases (invalid QR, offline submission, role-based access) — are documented in [`/docs/test-cases.md`](./docs/test-cases.md).

---

 Documentation

- Architecture Diagram — [`/docs/architecture.png`](./docs/architecture.png)
- ER Diagram — [`/docs/er-diagram.png`](./docs/er-diagram.png)
- Test Case Report — [`/docs/test-cases.md`](./docs/test-cases.md)

---

License

This project was developed as a group effort of Atul Prakash ,Sarthak S Nair ,Arjun Dve M ,Ragadev Biju under APJ Abdul Kalam Technological University (KTU).
