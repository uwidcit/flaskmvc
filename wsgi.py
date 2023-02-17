import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app
from App.controllers.user import (
    create_user,
    get_user_by_username,
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
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password, "user")
    print(f"{username} created!")


@user_cli.command("create-farmer", help="Creates a farmer")
@click.argument("username", default="robfarm")
@click.argument("password", default="robpass")
def create_farmer_command(username, password):
    create_user(username, password, "farmer")
    print(f"{username} created!")


@user_cli.command("create-admin", help="Creates an admin")
@click.argument("username", default="robadmin")
@click.argument("password", default="robpass")
def create_admin_command(username, password):
    create_user(username, password, "admin")
    print(f"{username} created!")


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
@click.argument("image", default="https://picsum.photos/200/300")
@click.argument("price", default=1.0)
@click.argument("quantity", default=1)
def create_product_command(name, description, image, price, quantity, farmer_id=1):
    create_product(name, description, image, price, quantity, farmer_id)
    print(f"{name} created!")


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
@click.argument("description", default="red")
@click.argument("image", default="https://picsum.photos/200/300")
@click.argument("price", default=1.0)
@click.argument("quantity", default=1)
def update_product_command(id, name, description, image, price, quantity):
    update_product(id, name, description, image, price, quantity)
    print(f"{name} updated!")


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
@click.argument("name", default="rob")
@click.argument("email", default="rob@gmail.com")
@click.argument("rating", default=5)
@click.argument("comment", default="good")
def create_review_command(product_id, name, email, rating, comment):
    create_review(product_id, name, email, rating, comment)
    print(f"review created!")


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
