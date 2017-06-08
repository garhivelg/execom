from flask import render_template, redirect
from flask.helpers import url_for
from app import app


from .models import Protocol


@app.route("/")
def index():
    return redirect(url_for("list_protocols"))


@app.route("/protocols")
def list_protocols():
    items = Protocol.query.all()

    return render_template(
        "list.html",
        items=[
            [
                i,
                url_for("edit_protocol", protocol_id=i.id)
            ] for i in items
        ],
        add=url_for("edit_protocol"),
    )


@app.route("/protocol/add")
@app.route("/protocol/edit/<int:protocol_id>", methods=["GET", "POST", ])
def edit_protocol(protocol_id=None):
    return redirect(url_for("list_cases"))
