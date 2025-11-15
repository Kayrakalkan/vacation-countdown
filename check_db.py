"""Quick script to check database contents and add a test vacation."""
from database import get_all_vacations, get_active_vacation, add_vacation
from datetime import datetime, timedelta

print("=== Checking Database ===\n")

# Check all vacations
vacations = get_all_vacations()
print(f"Total vacations in database: {len(vacations)}")

if vacations:
    print("\nAll vacations:")
    for v in vacations:
        active_status = "✓ ACTIVE" if v['is_active'] else ""
        print(f"  - ID: {v['id']}, Location: {v['location']}, Date: {v['start_date']}, Active: {v['is_active']} {active_status}")
else:
    print("  No vacations found!")

# Check active vacation
print("\n=== Active Vacation ===")
active = get_active_vacation()
if active:
    print(f"Active vacation: {active['location']} on {active['start_date']}")
else:
    print("No active vacation found!")
    print("\nAdding a test vacation...")
    
    # Add a vacation 30 days from now
    future_date = datetime.now() + timedelta(days=30)
    vacation_id = add_vacation(
        location="Paris",
        start_date=future_date.strftime('%Y-%m-%d'),
        notes="Eiffel Tower, Louvre, cafes",
        is_active=True
    )
    print(f"✓ Added test vacation to Paris (ID: {vacation_id}) - 30 days from now")
    print("  This vacation is set as ACTIVE")
    
    # Verify it was added
    active = get_active_vacation()
    if active:
        print(f"\n✓ Confirmed: Active vacation is now {active['location']}")
    else:
        print("\n✗ Error: Still no active vacation!")
