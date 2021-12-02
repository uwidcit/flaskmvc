# converts any list of serializable objects to their json equivalent
def serialize_list(itemList):
    return [item.toDict() for item in itemList] if itemList is not None else []