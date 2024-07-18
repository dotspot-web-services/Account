from ariadne import (
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.explorer import ExplorerGraphiQL
from flask import Blueprint, jsonify, request
from flask_restful import Api

from .grocery import Avatars, Awards, Profiles, Socs
from .queries import usrs

groceBp = Blueprint("groca", __name__)

schema = make_executable_schema(
    load_schema_from_path("src/setting/graphql/groce.graphql"),
    usrs,
    snake_case_fallback_resolvers,
)


# Retrieve HTML for the GraphiQL.
# If explorer implements logic dependant on current request,
# change the html(None) call to the html(request)
# and move this line to the graphql_explorer function.
explorer_html = ExplorerGraphiQL().html(None)


@groceBp.route("/graphuser", methods=["GET"])
def graphql_explorer() -> tuple[ExplorerGraphiQL, int]:
    # On GET request serve the GraphQL explorer.
    # You don't have to provide the explorer if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL explorer app.
    return explorer_html, 200


@groceBp.route("/graphuser", methods=["POST"])
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


groceAPI = Api(app=groceBp)

groceAPI.add_resource(Awards, "/awards")
groceAPI.add_resource(Socs, "/socials")
groceAPI.add_resource(Avatars, "/pictures")
groceAPI.add_resource(Profiles, "/profiles")
