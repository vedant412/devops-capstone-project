"""
Account Service

This microservice handles the lifecycle of Accounts
"""
from flask import abort, jsonify, make_response, request, url_for
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = url_for("get_accounts", account_id=account.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Return all Accounts, optionally filtering by an exact name."""
    name = request.args.get("name")
    accounts = Account.find_by_name(name).all() if name else Account.all()
    return jsonify([account.serialize() for account in accounts]), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Return an Account by ID."""
    return jsonify(find_account_or_404(account_id).serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Replace the supplied Account fields for an existing ID."""
    check_content_type("application/json")
    account = find_account_or_404(account_id)
    data = request.get_json()
    if isinstance(data, dict):
        data.setdefault("date_joined", account.date_joined.isoformat())
    account.deserialize(data)
    account.update()
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Delete an Account if it is present."""
    account = Account.find(account_id)
    if account is not None:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT


def find_account_or_404(account_id):
    """Find an Account or return 404."""
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account {account_id} was not found")
    return account


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if request.mimetype == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
