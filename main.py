import json
from haemo_agent.eligibility import check_eligibility
from search import find_donors
from datetime import datetime, timedelta

def generate_report(donors, today):
    """Generates a LAST_SEARCH_RESULTS.md file with a table of donors."""
    filename = "LAST_SEARCH_RESULTS.md"
    date_str = today.strftime("%b %d, %Y")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Search Results ({date_str})\n\n")
        f.write("| Donor Name | Blood Type | Eligibility Status | Location |\n")
        f.write("|---|---|---|---|\n")

        for donor in donors:
            name = donor.get('name', 'Unknown')
            blood_type = donor.get('blood_type', 'Unknown')
            location = donor.get('location', 'Unknown')
            last_donation = donor.get('last_donation_date') or donor.get('last_donation') or 'N/A'
            
            status = "Unknown"
            if last_donation and last_donation != 'N/A':
                try:
                    is_eligible = check_eligibility(last_donation)
                    if is_eligible:
                        status = "✅ Eligible"
                    else:
                        last_date = datetime.strptime(last_donation, "%Y-%m-%d").date()
                        days_since = (today - last_date).days
                        days_remaining = 90 - days_since
                        status = f"⏳ Ineligible (Wait {days_remaining} days)"
                except ValueError:
                    status = "Error"
            else:
                 status = "No Date"

            f.write(f"| {name} | {blood_type} | {status} | {location} |\n")
    
    print(f"\nReport generated: {filename}")

def main():
    today = datetime.now().date()
    print(f"--- Donation Eligibility Check ({today}) ---\n")

    blood_type_input = input("Enter blood type to search (e.g., 'O+') or press Enter for all: ").strip()

    if blood_type_input:
        print(f"\nSearching for {blood_type_input} donors...")
        donors = find_donors(blood_type_input)
        if not donors:
            print(f"No donors found with blood type {blood_type_input}.")
            # Write empty report or handle as preferred. Let's write empty for consistency or just return.
            # Requirement says "lists the matching donors". If none, maybe empty table?
            # Let's generate the report even if empty to reflect "Last Search Design"
            generate_report([], today) 
            return
    else:
        print("\nLoading all donors...")
        try:
            with open('donors.json', 'r') as f:
                donors = json.load(f)
        except FileNotFoundError:
            print("Error: donors.json not found.")
            return
        except json.JSONDecodeError:
            print("Error: Failed to decode donors.json.")
            return

    # Inject Emergency Test Case
    test_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    test_donor = {
        "name": "TEST DONOR (Emergency Case)",
        "blood_type": "AB-",
        "location": "Test Lab",
        "last_donation_date": test_date
    }
    donors.append(test_donor)

    print(f"\nFound {len(donors)} potential donor(s) (including test case):\n")

    for donor in donors:
        name = donor.get('name', 'Unknown')
        # Handle inconsistent keys from donors.json updates
        last_donation = donor.get('last_donation_date') or donor.get('last_donation')
        location = donor.get('location', 'Unknown')
        
        if not last_donation:
            print(f"{name} ({location}): No donation date found.")
            continue

        try:
            is_eligible = check_eligibility(last_donation)
            
            if is_eligible:
                print(f"[ELIGIBLE] {name} ({location}) can donate today!")
            else:
                last_date = datetime.strptime(last_donation, "%Y-%m-%d").date()
                days_since = (today - last_date).days
                days_remaining = 90 - days_since
                print(f"!!! RED FLAG !!! {name} ({location}) NOT ELIGIBLE. Donated {days_since} days ago. Wait {days_remaining} days.")
                
        except ValueError as e:
             print(f"{name}: Error processing date - {e}")

    generate_report(donors, today)

if __name__ == "__main__":
    main()
