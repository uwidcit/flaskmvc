from App.database import db
from App.models import User, UserFoodList, Recipe, RecipeIngredient
from werkzeug.security import generate_password_hash

def initialize():
    db.drop_all()
    db.create_all()
    
    # Create test user (bob)
    bob = User(username='bob', password='bobpass')
    db.session.add(bob)
    db.session.commit()
    
    # Add inventory items (each record is one unit)
    inventory_items = [
        'flour', 'sugar', 'eggs', 'milk',
        'butter', 'salt', 'pepper', 'olive oil'
    ]
    for item in inventory_items:
        db.session.add(UserFoodList(bob.id, item))
    
    # Create sample recipes with required ingredient quantities, categories, and images
    # Original recipes
    recipes = [
        {
            'name': 'Classic Pancakes',
            'category': 'Breakfast',
            'image': 'pancakes.png',
            'ingredients': ['flour', 'eggs', 'milk', 'butter', 'baking powder', 'sugar'],
            'instructions': 'Mix dry ingredients. Add wet ingredients. Cook on buttered griddle.'
        },
        {
            'name': 'Scrambled Eggs',
            'category': 'Breakfast',
            'image': 'eggs.png',
            'ingredients': ['eggs', 'butter', 'salt', 'pepper'],
            'instructions': 'Beat eggs. Melt butter in pan. Cook eggs while stirring. Season.'
        },
        {
            'name': 'Pasta Aglio e Olio',
            'category': 'Main Meal',
            'image': 'pasta.png',
            'ingredients': ['pasta', 'garlic', 'olive oil', 'red pepper flakes', 'parsley'],
            'instructions': 'Cook pasta. Sauté garlic in oil. Combine and add seasonings.'
        },
        {
            'name': 'Caprese Salad',
            'category': 'Main Meal',
            'image': 'caprese_salad.png',
            'ingredients': ['tomatoes', 'mozzarella', 'basil', 'olive oil', 'salt', 'pepper'],
            'instructions': 'Slice tomatoes and mozzarella. Arrange alternately, garnish with basil. Drizzle with olive oil, season with salt and pepper.'
        },
        {
            'name': 'Guacamole',
            'category': 'Main Meal',
            'image': 'guacamole.png',
            'ingredients': ['avocado', 'lime', 'salt', 'pepper', 'cilantro', 'tomato'],
            'instructions': 'Mash avocados. Mix in lime juice, chopped tomato, cilantro, salt, and pepper.'
        },
        {
            'name': 'Chicken Stir Fry',
            'category': 'Main Meal',
            'image': 'chicken_stir_fry.png',
            'ingredients': ['chicken', 'bell pepper', 'broccoli', 'soy sauce', 'garlic', 'ginger'],
            'instructions': 'Stir-fry chicken until cooked. Add vegetables and stir-fry until tender-crisp. Mix in garlic, ginger, and soy sauce.'
        }
    ]
    
    # Additional recipes (10 more)
    more_recipes = [
        {
            'name': 'Veggie Omelette',
            'category': 'Breakfast',
            'image': 'veggie_omelette.png',
            'ingredients': ['eggs', 'bell pepper', 'onion', 'cheese', 'salt', 'pepper'],
            'instructions': 'Beat eggs. Pour into a pan with sautéed bell pepper and onion. Sprinkle cheese, season, and cook until set.'
        },
        {
            'name': 'Fruit Smoothie',
            'category': 'Breakfast',
            'image': 'fruit_smoothie.png',
            'ingredients': ['banana', 'strawberries', 'yogurt', 'honey'],
            'instructions': 'Blend banana, strawberries, yogurt, and honey until smooth.'
        },
        {
            'name': 'Grilled Cheese Sandwich',
            'category': 'Main Meal',
            'image': 'grilled_cheese.png',
            'ingredients': ['bread', 'cheese', 'butter'],
            'instructions': 'Butter two slices of bread. Place cheese between them and grill until golden brown.'
        },
        {
            'name': 'Caesar Salad',
            'category': 'Main Meal',
            'image': 'caesar_salad.png',
            'ingredients': ['romaine lettuce', 'croutons', 'parmesan', 'caesar dressing'],
            'instructions': 'Toss chopped romaine with croutons, grated parmesan, and Caesar dressing.'
        },
        {
            'name': 'Tomato Soup',
            'category': 'Main Meal',
            'image': 'tomato_soup.png',
            'ingredients': ['tomatoes', 'vegetable broth', 'onion', 'garlic', 'basil'],
            'instructions': 'Simmer tomatoes, onion, garlic, and broth. Blend until smooth and garnish with basil.'
        },
        {
            'name': 'Beef Tacos',
            'category': 'Main Meal',
            'image': 'beef_tacos.png',
            'ingredients': ['beef', 'tortillas', 'lettuce', 'tomato', 'cheese', 'taco seasoning'],
            'instructions': 'Cook beef with taco seasoning. Fill tortillas with beef, shredded lettuce, diced tomato, and cheese.'
        },
        {
            'name': 'Spaghetti Bolognese',
            'category': 'Main Meal',
            'image': 'spaghetti_bolognese.png',
            'ingredients': ['spaghetti', 'ground beef', 'tomato sauce', 'garlic', 'onion', 'basil'],
            'instructions': 'Cook spaghetti. Sauté garlic and onion, add ground beef until browned. Stir in tomato sauce and basil; simmer and serve over spaghetti.'
        },
        {
            'name': 'Chocolate Chip Cookies',
            'category': 'Desserts',
            'image': 'chocolate_chip_cookies.png',
            'ingredients': ['flour', 'sugar', 'butter', 'eggs', 'chocolate chips'],
            'instructions': 'Mix ingredients. Scoop onto baking sheet. Bake until golden around the edges.'
        },
        {
            'name': 'Cobb Salad',
            'category': 'Main Meal',
            'image': 'cobb_salad.png',
            'ingredients': ['chicken', 'bacon', 'avocado', 'egg', 'lettuce', 'tomato', 'blue cheese'],
            'instructions': 'Arrange chopped lettuce topped with rows of grilled chicken, crumbled bacon, sliced avocado, hard-boiled eggs, diced tomato, and blue cheese.'
        },
        {
            'name': 'Margarita Pizza',
            'category': 'Main Meal',
            'image': 'margarita_pizza.png',
            'ingredients': ['pizza dough', 'tomato sauce', 'mozzarella', 'basil', 'olive oil'],
            'instructions': 'Spread tomato sauce on rolled-out dough, top with mozzarella and basil, drizzle with olive oil, and bake until crust is crispy.'
        }
    ]
    
    # Combine all recipes into one list
    all_recipes = recipes + more_recipes
    
    for recipe_data in all_recipes:
        recipe = Recipe(
            name=recipe_data['name'],
            instructions=recipe_data['instructions'],
            user_id=bob.id,
            category=recipe_data.get('category', 'Custom'),
            image=recipe_data.get('image', 'default_recipe.png')
        )
        db.session.add(recipe)
        db.session.commit()
        
        # Set required quantities based on the recipe name
        if recipe_data['name'] == 'Classic Pancakes':
            quantities = {
                'flour': 1,
                'eggs': 5,
                'milk': 1,
                'butter': 1,
                'baking powder': 1,
                'sugar': 1
            }
        elif recipe_data['name'] == 'Scrambled Eggs':
            quantities = {
                'eggs': 3,
                'butter': 1,
                'salt': 1,
                'pepper': 1
            }
        elif recipe_data['name'] == 'Pasta Aglio e Olio':
            quantities = {
                'pasta': 1,
                'garlic': 2,
                'olive oil': 1,
                'red pepper flakes': 1,
                'parsley': 1
            }
        elif recipe_data['name'] == 'Caprese Salad':
            quantities = {
                'tomatoes': 2,
                'mozzarella': 1,
                'basil': 5,
                'olive oil': 1,
                'salt': 1,
                'pepper': 1
            }
        elif recipe_data['name'] == 'Guacamole':
            quantities = {
                'avocado': 2,
                'lime': 1,
                'salt': 1,
                'pepper': 1,
                'cilantro': 1,
                'tomato': 1
            }
        elif recipe_data['name'] == 'Chicken Stir Fry':
            quantities = {
                'chicken': 1,
                'bell pepper': 1,
                'broccoli': 1,
                'soy sauce': 1,
                'garlic': 2,
                'ginger': 1
            }
        elif recipe_data['name'] == 'Veggie Omelette':
            quantities = {
                'eggs': 3,
                'bell pepper': 1,
                'onion': 1,
                'cheese': 1,
                'salt': 1,
                'pepper': 1
            }
        elif recipe_data['name'] == 'Fruit Smoothie':
            quantities = {
                'banana': 1,
                'strawberries': 5,
                'yogurt': 1,
                'honey': 1
            }
        elif recipe_data['name'] == 'Grilled Cheese Sandwich':
            quantities = {
                'bread': 2,
                'cheese': 2,
                'butter': 1
            }
        elif recipe_data['name'] == 'Caesar Salad':
            quantities = {
                'romaine lettuce': 1,
                'croutons': 1,
                'parmesan': 1,
                'caesar dressing': 1
            }
        elif recipe_data['name'] == 'Tomato Soup':
            quantities = {
                'tomatoes': 4,
                'vegetable broth': 1,
                'onion': 1,
                'garlic': 2,
                'basil': 1
            }
        elif recipe_data['name'] == 'Beef Tacos':
            quantities = {
                'beef': 1,
                'tortillas': 3,
                'lettuce': 1,
                'tomato': 1,
                'cheese': 1,
                'taco seasoning': 1
            }
        elif recipe_data['name'] == 'Spaghetti Bolognese':
            quantities = {
                'spaghetti': 1,
                'ground beef': 1,
                'tomato sauce': 1,
                'garlic': 2,
                'onion': 1,
                'basil': 1
            }
        elif recipe_data['name'] == 'Chocolate Chip Cookies':
            quantities = {
                'flour': 2,
                'sugar': 1,
                'butter': 1,
                'eggs': 1,
                'chocolate chips': 1
            }
        elif recipe_data['name'] == 'Cobb Salad':
            quantities = {
                'chicken': 1,
                'bacon': 1,
                'avocado': 1,
                'egg': 2,
                'lettuce': 1,
                'tomato': 1,
                'blue cheese': 1
            }
        elif recipe_data['name'] == 'Margarita Pizza':
            quantities = {
                'pizza dough': 1,
                'tomato sauce': 1,
                'mozzarella': 1,
                'basil': 1,
                'olive oil': 1
            }
        else:
            quantities = {ingredient: 1 for ingredient in recipe_data['ingredients']}
        
        for ingredient in recipe_data['ingredients']:
            req_qty = quantities.get(ingredient, 1)
            db.session.add(RecipeIngredient(recipe.id, ingredient, quantity_required=req_qty))
    
    db.session.commit()
    return True
