from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import model_form_factory


from case.models import Case
from .models import Protocol, Decision


from app import db


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ProtocolForm(ModelForm):
    case = QuerySelectField(
        "Дело",
        query_factory=lambda: Case.query.all(),
        allow_blank=True,
    )

    class Meta:
        model = Protocol


class DecisionForm(ModelForm):
    protocol = QuerySelectField(
        "Протокол",
        query_factory=lambda: Protocol.query.all(),
        allow_blank=True,
    )

    class Meta:
        model = Decision
