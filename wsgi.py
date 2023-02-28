import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app

# from App.controllers import *

from App.controllers.user import (
    create_user,
    create_admin,
    create_farmer,
    get_user_by_email,
    get_user_by_id,
    get_all_users,
    get_all_users_json,
    update_user,
)
from App.controllers.review import (
    create_review,
    get_all_reviews,
    get_all_reviews_json,
    get_review_by_id,
    get_review_by_id_json,
    get_reviews_by_product_id,
    get_reviews_by_product_id_json,
    update_review,
    delete_review,
)
from App.controllers.product import (
    create_product,
    get_all_products,
    get_all_products_json,
    get_product_by_id,
    get_product_by_id_json,
    update_product,
    delete_product,
    archive_product,
)

from App.controllers.reply import (
    create_reply,
    get_all_replies_by_review_id,
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print("database intialized")


"""
User Commands
"""

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup("user", help="User object commands")


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create-user", help="Creates a user")
@click.argument("username", default="bob")
@click.argument("email", default="bob@bobmail.com")
@click.argument("password", default="bobpass")
def create_user_command(username, email, password):
    user = create_user(username, email, password, "user")
    print(user.to_json())


@user_cli.command("create-farmer", help="Creates a farmer")
@click.argument("username", default="farmerbob")
@click.argument("email", default="farmerbob@bobmail.com")
@click.argument("password", default="bobpass")
def create_farmer_command(username, email, password):
    user = create_user(username, email, password, "farmer")
    print(user.to_json())


@user_cli.command("create-admin", help="Creates an admin")
@click.argument("username", default="adminbob")
@click.argument("email", default="adminbob@bobmail.com")
@click.argument("password", default="bobpass")
def create_admin_command(username, email, password):
    user = create_user(username, email, password, "admin")
    print(user.to_json())


# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == "string":
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli


product_cli = AppGroup("product", help="Product object commands")


@product_cli.command("create", help="Creates a product")
@click.argument("name", default="tomato")
@click.argument("description", default="red")
@click.argument("image", default="image")
@click.argument("price", default=1)
@click.argument("quantity", default=1)
@click.argument("farmer_id", default=2)
def create_product_command(name, description, image, price, quantity, farmer_id):
    product = create_product(name, description, image, price, quantity, farmer_id)
    print(product.to_json())


@product_cli.command("list", help="Lists products in the database")
@click.argument("format", default="string")
def list_product_command(format):
    if format == "string":
        print(get_all_products())
    else:
        print(get_all_products_json())


@product_cli.command("update", help="Updates a product")
@click.argument("id", default=1)
@click.argument("name", default="tomato")
@click.argument("description", default="green")
@click.argument("image", default="image")
@click.argument("price", default=1)
@click.argument("quantity", default=1)
def update_product_command(id, name, description, image, price, quantity):
    update_product(id, name, description, image, price, quantity)
    print(f"{id} updated!")


@product_cli.command("delete", help="Deletes a product")
@click.argument("id", default=1)
def delete_product_command(id):
    delete_product(id)
    print(f"{id} deleted!")


@product_cli.command("archive", help="Archives a product")
@click.argument("id", default=1)
def archive_product_command(id):
    archive_product(id)
    print(f"{id} archived!")


app.cli.add_command(product_cli)

review_cli = AppGroup("review", help="Review object commands")


@review_cli.command("create", help="Creates a review")
@click.argument("product_id", default=1)
@click.argument("user_id", default=1)
@click.argument("body", default="body")
def create_review_command(product_id, user_id, body):
    review = create_review(product_id, user_id, body)
    print(review.to_json())


@review_cli.command("reply", help="Replies to a review")
@click.argument("review_id", default=1)
@click.argument("user_id", default=2)
@click.argument("body", default="body")
def reply_review_command(review_id, user_id, body):
    review = create_reply(review_id, user_id, body)
    print(review.to_json())


@review_cli.command("list", help="Lists reviews in the database")
@click.argument("format", default="string")
def list_review_command(format):
    if format == "string":
        print(get_all_reviews())
    else:
        print(get_all_reviews_json())


@review_cli.command("list-by-product", help="Lists reviews by product in the database")
@click.argument("product_id", default=1)
@click.argument("format", default="string")
def list_review_by_product_command(product_id, format):
    if format == "string":
        print(get_reviews_by_product_id(product_id))
    else:
        print(get_reviews_by_product_id_json(product_id))


app.cli.add_command(review_cli)


"""
Generic Commands
"""


@app.cli.command("init")
def initialize():
    create_db(app)
    print("database intialized")


@app.cli.command("run")
def initialize():
    print("hello")


"""
Test Commands
"""

test = AppGroup("test", help="Testing commands")


@test.command("demo", help="Run Demo tests")
def demo_tests_command():
    user1 = create_user(
        username="bob",
        email="bob@gmail.com",
        password="bobpass",
        access="user",
        phone="800-1234",
        address="University Drive",
        currency="USD",
        units="kg",
        avatar="avatar.jpg",
    )
    print(f"Created user: {user1.to_json()}")
    user2 = create_farmer(
        username="rob",
        email="rob@gmail.com",
        password="robpass",
    )
    print(f"Created farmer: {user2.to_json()}")
    user3 = create_admin(
        username="admin",
        email="admin@gmail.com",
        password="adminpass",
    )
    print(f"Created admin: {user3.to_json()}")
    product1 = create_product("tomato", "red", "tomato.jpg", 1, 1, 2)
    print(f"Created product: {product1.to_json()}")
    product2 = create_product("potato", "brown", "potato.jpg", 2, 1, 2)
    print(f"Created product: {product2.to_json()}")
    product3 = create_product("carrot", "orange", "carrot.jpg", 3, 1, 2)
    print(f"Created product: {product3.to_json()}")
    review1 = create_review(1, 1, "Best tomato ever!")
    print(f"Created review: {review1.to_json()}")
    review2 = create_review(2, 1, "Best potato ever!")
    print(f"Created review: {review2.to_json()}")
    review3 = create_review(3, 1, "Best carrot ever!")
    print(f"Created review: {review3.to_json()}")
    reply1 = create_reply(1, 2, "Thanks!")
    print(f"Created reply: {reply1.to_json()}")
    reply2 = create_reply(2, 2, "Thanks!")
    print(f"Created reply: {reply2.to_json()}")
    reply3 = create_reply(3, 2, "Thanks!")
    print(f"Created reply: {reply3.to_json()}")


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)
