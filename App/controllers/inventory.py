from App.models import UserFoodList, db

def add_ingredient_to_user(user_id, ingredient):
    # Remove the existence check to allow adding duplicates
    new_ingredient = UserFoodList(user_id, ingredient.lower())
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def remove_ingredient_from_user(user_id, ingredient):
    item = UserFoodList.query.filter_by(
        user_id=user_id,
        ingredient=ingredient.lower()
    ).first()
    
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False

def get_user_inventory(user_id):
    return UserFoodList.query.filter_by(user_id=user_id).all()

def get_user_inventory_json(user_id):
    items = get_user_inventory(user_id)
    return [item.to_json() for item in items]

def get_user_inventory_quantities(user_id):
    """
    Returns a dictionary mapping each ingredient (in lowercase) 
    to its count (quantity) for the given user.
    """
    items = UserFoodList.query.filter_by(user_id=user_id).all()
    quantities = {}
    for item in items:
        ing = item.ingredient.lower()
        quantities[ing] = quantities.get(ing, 0) + 1
    return quantities

def remove_ingredient_from_user(user_id, ingredient, quantity=1):
    """
    Remove a given quantity of an ingredient from a user's inventory.
    :param user_id: The ID of the user.
    :param ingredient: The ingredient name (case-insensitive).
    :param quantity: The number of units to remove (default is 1).
    :return: The number of units removed.
    """
    # Query all matching inventory items
    items = UserFoodList.query.filter_by(user_id=user_id, ingredient=ingredient.lower()).all()
    if not items:
        return 0

    removed_count = 0
    # Remove up to the requested quantity
    for item in items[:quantity]:
        db.session.delete(item)
        removed_count += 1
    db.session.commit()
    return removed_count