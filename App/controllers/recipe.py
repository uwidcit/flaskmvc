from App.models import Recipe, RecipeIngredient, db

def create_recipe(user_id, name, ingredients, instructions, category="Custom"):
    # Create and add the Recipe
    recipe = Recipe(name, instructions, user_id,category)
    db.session.add(recipe)
    db.session.commit()
    
    # Process each ingredient string. Expected format: "ingredient" or "ingredient:quantity"
    for ingredient in ingredients:
        if ":" in ingredient:
            ing_name, ing_qty = ingredient.split(":")
            try:
                ing_qty = int(ing_qty.strip())
            except ValueError:
                ing_qty = 1
        else:
            ing_name = ingredient.strip()
            ing_qty = 1
        # Add RecipeIngredient with the required quantity
        db.session.add(RecipeIngredient(recipe.id, ing_name.lower(), quantity_required=ing_qty))
    
    db.session.commit()
    return recipe

# In App/recipe.py

def search_recipes_by_ingredient(ingredient):
    """
    Search for recipes that include a specific ingredient.
    :param ingredient: The ingredient name as a string.
    :return: A list of Recipe objects that include the specified ingredient.
    """
    recipes = Recipe.query.join(RecipeIngredient).filter(
        RecipeIngredient.name.ilike(f"%{ingredient}%")
    ).all()
    return recipes

def get_recipe_by_id(recipe_id):
    return Recipe.query.get(recipe_id)

def get_user_recipes(user_id):
    return Recipe.query.filter_by(user_id=user_id).all()

def get_user_recipes_json(user_id):
    recipes = get_user_recipes(user_id)
    return [recipe.to_json() for recipe in recipes]

def get_recipes_with_missing_ingredients(user_id):
    from App.controllers.inventory import get_user_inventory
    user_inventory = get_user_inventory(user_id)
    # Aggregate inventory: count occurrences for each ingredient (lowercase)
    inventory_counts = {}
    for item in user_inventory:
        ing = item.ingredient.lower()
        inventory_counts[ing] = inventory_counts.get(ing, 0) + 1

    recipes = get_user_recipes(user_id)
    result = []
    
    for recipe in recipes:
        missing = {}
        for ingredient in recipe.ingredients:
            req_qty = ingredient.quantity_required
            available = inventory_counts.get(ingredient.name.lower(), 0)
            if available < req_qty:
                missing[ingredient.name] = req_qty - available  # missing units
        recipe_data = recipe.to_json()
        recipe_data['missing_ingredients'] = missing  # now a dict: {ingredient: missing_amount, ...}
        result.append(recipe_data)
    
    return result

