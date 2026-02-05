import json

def find_donors(blood_type):
    """
    Searches for donors with the specified blood type in donors.json.

    Args:
        blood_type (str): The blood type to search for (e.g., "O+", "A-").

    Returns:
        list: A list of dictionaries representing donors with the matching blood type.
    """
    try:
        with open('donors.json', 'r') as f:
            donors = json.load(f)
    except FileNotFoundError:
        print("Error: donors.json not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode donors.json.")
        return []

    matching_donors = [d for d in donors if d.get('blood_type') == blood_type]
    return matching_donors

if __name__ == "__main__":
    # Simple test
    target_type = "O+"
    results = find_donors(target_type)
    print(f"Donors with blood type {target_type}:")
    for donor in results:
        print(f"- {donor['name']} ({donor['location']})")
