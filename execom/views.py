from flask import flash, render_template, redirect
from flask.helpers import url_for
from app import db, app


from .models import Protocol, Decision
from .forms import ProtocolForm


from case.models import Case


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


@app.route("/protocol/add", methods=["GET", "POST", ])
@app.route("/protocol/edit/<int:protocol_id>", methods=["GET", "POST", ])
@app.route("/protocol/add/<int:case_id>", methods=["GET", "POST", ])
def edit_protocol(protocol_id=None, case_id=None):
    if case_id is not None:
        case = Case.query.get_or_404(case_id)
        protocol = Protocol(case=case)
    elif protocol_id is not None:
        protocol = Protocol.query.get_or_404(protocol_id)
    else:
        protocol = Protocol()
    form = ProtocolForm(obj=protocol)

    if form.validate_on_submit():
        form.populate_obj(protocol)
        db.session.add(protocol)
        if protocol.id:
            flash("Протокол изменен")
        else:
            flash("Протокол добавлен")
        db.session.commit()
        return redirect(url_for("list_protocols"))

    app.logger.debug(form.errors)

    decisions = Decision.query.filter_by(protocol=protocol)

    return render_template("edit_protocol.html", form=form, protocol=protocol, decisions=decisions)
