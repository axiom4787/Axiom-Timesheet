from connection import sheet

def data():
    """
    Fetch data from Google Sheets and return a dictionary with IDs as keys and names as values.

    Returns:
        dict: A dictionary with IDs as keys and names as values.
    """
    data = sheet.get_worksheet(1).get_all_values()
    data = data[1:]
    
    map_ = {}
    for i, r in enumerate(data):
        try:
            map_[r[3]] = r[2]
        except:
            print(f"Could not get #{i}")

    return map_

# Example usage
if __name__ == "__main__":
    mapping = data()
    print(mapping)
