from ariadne import (
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.explorer import ExplorerGraphiQL
from flask import Blueprint, jsonify, request
from flask_restful import Api

from .queries import accs, logs, reset
from .registry import Login, Logout, Register

registryBp = Blueprint("rega", __name__, "/registry")

schema = make_executable_schema(
    load_schema_from_path("src/setting/graphql/acct.graphql"),
    [accs, logs, reset],
    snake_case_fallback_resolvers,
)


# Retrieve HTML for the GraphiQL.
# If explorer implements logic dependant on current request,
# change the html(None) call to the html(request)
# and move this line to the graphql_explorer function.
explorer_html = ExplorerGraphiQL().html(None)


@registryBp.route("/graphregistry", methods=["GET"])
def graphql_explorer() -> tuple[ExplorerGraphiQL, int]:
    # On GET request serve the GraphQL explorer.
    # You don't have to provide the explorer if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL explorer app.
    return explorer_html, 200


@registryBp.route("/graphregistry", methods=["POST"])
def graphql_server() -> tuple[jsonify, int]:
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request},
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


registryAPI = Api(app=registryBp)

registryAPI.add_resource(Register, "/reg")
registryAPI.add_resource(Login, "/login")
registryAPI.add_resource(Logout, "/logout")
