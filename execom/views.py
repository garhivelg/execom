from flask import flash, render_template, redirect, jsonify, request, send_file
from flask.helpers import url_for
from app import db, app
from werkzeug.utils import secure_filename
import os


from .models import Protocol, Decision, DecisionMedia
from .forms import ProtocolForm, DecisionForm


from case.models import Case, Register


def page():
    page_str = request.args.get('page')
    try:
        page = int(page_str)
    except (ValueError, TypeError):
        page = 1
    return page


def get_order():
    desc = request.args.get("desc", False)
    try:
        order_id = int(request.args.get("order", 0))
    except ValueError:
        order_id = 0
    return order_id, desc


def order(q, fieldlist=None, desc=False):
    print("ORDER", fieldlist)
    if fieldlist is None:
        return q

    orderlist = []
    for f in fieldlist:
        if desc:
            orderlist.append(f.desc())
        else:
            orderlist.append(f.asc())
    return q.order_by(*orderlist)


@app.route("/")
def index():
    return redirect(url_for("list_protocols"))


@app.route("/protocols")
def list_protocols():
    order_id, desc = get_order()
    orders = {
        1: [Protocol.protocol_id, ],
        2: [Protocol.protocol_date, ],
        3: [Register.fund, Register.register],
        4: [Case.book_num, ],
    }

    items = db.session.query(Protocol, db.func.count(Protocol.decisions).label('decision_count'))
    items = items.join(Protocol.case).join(Case.register)
    items = items.join(Protocol.decisions).group_by(Protocol)
    if order_id == 5:
        desc_text = " DESC" if desc else " ASC"
        items = items.order_by(db.text("\"decision_count\"%s" % (desc_text, )))
    else:
        items = order(items, orders.get(order_id), desc)
    items = items.paginate(page(), app.config.get('RECORDS_ON_PAGE'))
    print(items)

    return render_template(
        "list_protocols.html",
        order_id=order_id,
        desc=desc,
        title="Протоколы",
        items=items,
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
            flash("Протокол изменен", 'success')
        else:
            flash("Протокол добавлен", 'success')
        db.session.commit()
        return redirect(url_for("list_protocols"))

    app.logger.debug(form.errors)

    decisions = Decision.query.filter_by(protocol=protocol)

    return render_template("edit_protocol.html", form=form, protocol=protocol, decisions=decisions)


@app.route("/protocol/del/<int:protocol_id>")
def del_protocol(protocol_id=None):
    protocol = Protocol.query.get_or_404(protocol_id)
    db.session.delete(protocol)
    db.session.commit()
    flash("Протокол удален", 'danger')
    return redirect(url_for("list_protocols"))


@app.route("/protocol/<int:protocol_id>")
@app.route("/decisions")
def list_decisions(protocol_id=None):
    order_id, desc = get_order()
    orders = {
        1: [Decision.decision_num, ],
        2: [Protocol.protocol_date, Decision.decision_date, ],
        3: [Decision.topic, ],
        4: [Protocol.protocol_id, ],
    }

    protocol = None
    items = Decision.query
    if protocol_id is not None:
        protocol = Protocol.query.get_or_404(protocol_id)
        items = items.filter_by(protocol=protocol)
    items = items.join(Protocol)
    items = order(items, orders.get(order_id), desc)

    return render_template(
        "list_decisions.html",
        protocol=protocol,
        order_id=order_id,
        desc=desc,
        title="Протоколы",
        items=items.paginate(page(), app.config.get('RECORDS_ON_PAGE')),
        add=url_for("edit_decision"),
    )


@app.route("/decision/add", methods=["GET", "POST", ])
@app.route("/decision/edit/<int:decision_id>", methods=["GET", "POST", ])
@app.route("/decision/add/<int:protocol_id>", methods=["GET", "POST", ])
def edit_decision(decision_id=None, protocol_id=None):
    if protocol_id is not None:
        protocol = Protocol.query.get_or_404(protocol_id)
        decision = Decision(protocol=protocol)
    elif decision_id is not None:
        decision = Decision.query.get_or_404(decision_id)
    else:
        decision = Decision()
    form = DecisionForm(obj=decision)

    if form.validate_on_submit():
        form.populate_obj(decision)
        db.session.add(decision)
        if decision.id:
            flash("Решение изменено", 'success')
        else:
            flash("Решение добавлено", 'success')
        db.session.commit()
        return redirect(url_for("list_protocols"))

    app.logger.debug(form.errors)

    files = DecisionMedia.query.filter_by(decision=decision).all()

    return render_template("edit_decision.html", form=form, decision=decision, files=files)


@app.route("/decision/del/<int:decision_id>")
def del_decision(decision_id=None):
    decision = Decision.query.get_or_404(decision_id)
    db.session.delete(decision)
    db.session.commit()
    flash("Решение удалено", 'danger')
    return redirect(url_for("list_decisions"))


@app.route("/upload/decision", methods=["POST", ])
def upload_decision():
    files = request.files
    print(files)
    if not files:
        return jsonify({
            'status': False,
            'Message': 'Ни один файл не загружен.',
        })

    filenames = []
    for k, f in files.items():
        if not f.filename:
            return jsonify({
                'status': False,
                'Message': 'Файл не загружен.',
            })

        if f:
            name, ext = os.path.splitext(f.filename)
            name = secure_filename(name)
            if not name:
                name = 'untitled'
            filename = ''.join([name, ext])
            version = 1
            while True:
                full_filename = os.path.join(app.config.get('UPLOAD_PATH', './'), filename)
                if not os.path.isfile(full_filename):
                    break
                version += 1
                filename = ''.join([name, str(version), ext])
            f.save(full_filename)

            filenames.append(filename)
        else:
            return jsonify({
                'status': True,
                'Message': "Файл %(filename)s невозможно загрузить." % ({'filename': f.filename}),
            })
    return jsonify({
        'status': True,
        'Message': 'Ok.',
        'filenames': filenames,
    })


@app.route("/decision/<int:decision_id>.docx")
def export_decision(decision_id):
    from docxtpl import DocxTemplate
    from io import BytesIO

    decision = Decision.query.get_or_404(decision_id)
    doc = DocxTemplate(os.path.join("docx", "template.docx"))
    doc.render({
        'protocol': decision.protocol,
        'decision': decision,
    })
    filename = "%d.docx" % (decision.id)
    f = BytesIO()
    doc.save(f)
    f.seek(0)
    return send_file(f, as_attachment=True, attachment_filename=filename)
