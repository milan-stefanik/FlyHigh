# Function for filtering records by pagination parameters
def get_items(items, offset, per_page):
    return items[offset: offset + per_page]
