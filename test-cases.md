# Test Cases — Lab Equipment Complaint & Maintenance Tracker

End-to-end test cases covering the core complaint lifecycle, error handling, and role-based access. Fill in the **Actual Result** and **Pass/Fail** columns as you execute each test during integration testing.

| Test Case ID | Module | Scenario | Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC01 | Student App | Submit a new complaint | Scan QR → view equipment details → fill complaint form → submit | Complaint document created in Firestore with `status: "Pending"` | | |
| TC02 | Admin App | New complaint appears on dashboard | After TC01, open admin dashboard | New complaint visible in list, sorted by most recent | | |
| TC03 | Notifications | Technician receives alert | After TC01, check technician's device | Push notification received via FCM with equipment name and problem type | | |
| TC04 | Admin App | Update complaint status | Open complaint from TC01 → change status to "In Progress" | Firestore `status` field updates, `updated_at` timestamp refreshes | | |
| TC05 | Student App | Status reflects in real time | After TC04, open student's "My Complaints" screen | Status shown as "In Progress" without manual refresh (StreamBuilder) | | |
| TC06 | Admin App | Mark complaint as repaired | Change status to "Repaired", add technician remarks | Status updates to "Repaired"; linked equipment `status` auto-updates to "Working" | | |
| TC07 | Student App | Invalid QR scan | Scan a QR code not present in the `equipment` collection | App shows "Equipment not found" message, does not crash | | |
| TC08 | Student App | Duplicate complaint on same equipment | Submit two separate complaints for the same `equipment_id` | Both complaints are recorded independently (or flagged as duplicate, if implemented) | | |
| TC09 | Auth | Role-based access — student blocked from admin routes | Log in as student, attempt to navigate to admin dashboard | Access denied / redirected to student home | | |
| TC10 | Auth | Role-based access — technician cannot edit equipment master data | Log in as technician, attempt to directly modify an `equipment` document | Firestore security rules reject the write | | |
| TC11 | Student App | Photo upload | Attach a photo in the complaint form and submit | Photo uploaded to Firebase Storage, `photo_url` field populated correctly | | |
| TC12 | Student App | Offline submission | Disable network, attempt to submit a complaint | App shows a clear error / queues submission, does not silently fail | | |
| TC13 | QR System | Scan physical printed sticker | Scan a printed & laminated QR sticker under normal lab lighting | Scan succeeds first try, correct equipment loads | | |
| TC14 | Backend | Security rules — unauthenticated access | Attempt to read/write Firestore without being logged in | All reads/writes rejected by security rules | | |

## Notes

- Run TC01 → TC06 together as one continuous flow to validate the full complaint lifecycle before testing edge cases separately.
- TC09/TC10/TC14 should be tested with each of the three role accounts (student, technician, admin) to confirm rules are enforced correctly in every direction, not just the one documented above.
- Log any mismatch between Expected and Actual Result as a bug (see bug tracking sheet / GitHub Issues) rather than editing the expected result to match.
