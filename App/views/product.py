from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from .index import index_views

from App.controllers.product import (
    create_product,
    get_product_by_id,
    update_product,
    archive_product,
    unarchive_product,
    delete_product,
    get_all_products_json,
)

from App.controllers.user import is_farmer, is_admin

product_views = Blueprint("product_views", __name__, template_folder="../templates")


@product_views.route("/products", methods=["GET"])
def get_all_products_action():
    products = get_all_products_json()
    if products:
        return jsonify(products), 200
    return jsonify({"message": "No products found"}), 404


@product_views.route("/products", methods=["POST"])
@jwt_required()
def create_product_action():
    data = request.json
    if not is_farmer(current_identity):
        return jsonify({"message": "You are not authorized to create a product"}), 403

    create_product(
        name=data["name"],
        description=data["description"],
        image=data["image"],
        retail_price=data["retail_price"],
        product_quantity=data["product_quantity"],
        farmer_id=current_identity.id,
    )
    return jsonify({"message": f"Product {data['name']} created"}), 201


@product_views.route("/products/<int:id>", methods=["GET"])
def get_product_by_id_action(id):
    product = get_product_by_id(id)
    if product:
        return jsonify(product.to_json()), 200
    return jsonify({"message": "No product found"}), 404


@product_views.route("/products/<int:id>", methods=["PUT"])
@jwt_required()
def update_product_action(id):
    data = request.json
    product = get_product_by_id(id)
    if product:
        if not is_farmer(current_identity):
            return (
                jsonify({"message": "You are not authorized to update a product"}),
                403,
            )
        if product.farmer_id != current_identity.id:
            return (
                jsonify({"message": "You are not authorized to update this product"}),
                403,
            )
        update_product(
            id=id,
            name=data["name"],
            description=data["description"],
            image=data["image"],
            retail_price=data["retail_price"],
            product_quantity=data["product_quantity"],
        )
        return jsonify({"message": f"Product {data['name']} updated"}), 200
    return jsonify({"message": "No product found"}), 404


@product_views.route("/products/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product_action(id):
    product = get_product_by_id(id)
    if product:
        if not is_farmer(current_identity) and not is_admin(current_identity):
            return (
                jsonify({"message": "You are not authorized to delete a product"}),
                403,
            )
        if product.farmer_id != current_identity.id and not is_admin(current_identity):
            return (
                jsonify({"message": "You are not authorized to delete this product"}),
                403,
            )
        if product.archived:
            delete_product(id)
            return jsonify({"message": f"Product {product.name} deleted"}), 200
        archive_product(id)
        return jsonify({"message": f"Product {product.name} deleted"}), 200
    return jsonify({"message": "No product found"}), 404


@product_views.route("/products/<int:id>/archive", methods=["PUT"])
@jwt_required()
def archive_product_action(id):
    product = get_product_by_id(id)
    if product:
        if not is_farmer(current_identity) and not is_admin(current_identity):
            return (
                jsonify({"message": "You are not authorized to archive a product"}),
                403,
            )
        if product.farmer_id != current_identity.id and not is_admin(current_identity):
            return (
                jsonify({"message": "You are not authorized to archive this product"}),
                403,
            )
        archive_product(id)
        return jsonify({"message": f"Product {product.name} archived"}), 200
    return jsonify({"message": "No product found"}), 404


@product_views.route("/products/<int:id>/unarchive", methods=["PUT"])
@jwt_required()
def unarchive_product_action(id):
    product = get_product_by_id(id)
    if product:
        if not is_farmer(current_identity) and not is_admin(current_identity):
            return (
                jsonify({"message": "You are not authorized to unarchive a product"}),
                403,
            )
        if product.farmer_id != current_identity.id and not is_admin(current_identity):
            return (
                jsonify(
                    {"message": "You are not authorized to unarchive this product"}
                ),
                403,
            )
        unarchive_product(id)
        return jsonify({"message": f"Product {product.name} unarchived"}), 200
    return jsonify({"message": "No product found"}), 404
