from ariadne import (
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.explorer import ExplorerGraphiQL
from flask import Blueprint, jsonify, request
from flask_restful import Api

from .prof import Accademics, Basic, Resacher, Works
from .queries import profs

profBp = Blueprint("profa", __name__, url_prefix="/profiler")
profAPI = Api(app=profBp)

schema = make_executable_schema(
    load_schema_from_path("src/setting/graphql/prof.graphql"),
    profs,
    snake_case_fallback_resolvers,
)


# Retrieve HTML for the GraphiQL.
# If explorer implements logic dependant on current request,
# change the html(None) call to the html(request)
# and move this line to the graphql_explorer function.
explorer_html = ExplorerGraphiQL().html(None)


@profBp.route("/graphprofile", methods=["GET"])
def graphql_explorer() -> tuple[ExplorerGraphiQL, int]:
    # On GET request serve the GraphQL explorer.
    # You don't have to provide the explorer if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL explorer app.
    return explorer_html, 200


@profBp.route("/graphprofile", methods=["POST"])
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


profAPI.add_resource(Basic, "/Basics")
profAPI.add_resource(Accademics, "/Accademics")
profAPI.add_resource(Resacher, "/Researcher")
profAPI.add_resource(Works, "/Works")
