def get_store(stores: list, store: str):
    "Returns a store froma list of stores (dictionaries)"
    return next((store for store in stores if store["name"] == store), False)