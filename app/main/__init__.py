from flask import Blueprint

main_blueprint = Blueprint(
    "main", __name__, static_folder="web/static", template_folder="web/templates")


@main_blueprint.record
def record_params(setup_state):
    app = setup_state.app
    main_blueprint.config = dict([(key, value)
                                  for key, value in app.config.items()])


from app.main import routes
