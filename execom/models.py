from app import db
from wtforms import TextAreaField
import random


class Protocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    protocol_id = db.Column(
        db.Integer,
        nullable=False,
        default=1,
        info={'label': "Протокол №"}
    )
    description = db.Column(db.UnicodeText, info={'label': "Описание"})
    protocol_date = db.Column(db.Date, info={'label': "Дата"})

    case = db.relationship("Case", backref="protocols")
    decisions = db.relationship("Decision", backref="protocol")

    def title(self, format="Протокол №%d от %s"):
        return format % (self.protocol_id, self.date)

    def __repr__(self):
        return self.title()

    @property
    def date(self):
        if self.protocol_date:
            return self.protocol_date.strftime("%x")
        return None

    @property
    def decisions_count(self):
        return len(self.decisions)

    def randomize(self, fake):
        self.protocol_id = fake.pyint()
        self.protocol_date = fake.past_date(start_date="-20y")
        chance = random.randint(0, 100)
        if chance < 25:
            self.description = "\n".join(fake.paragraphs())


class Decision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocol_id = db.Column(db.Integer, db.ForeignKey('protocol.id'))
    decision_id = db.Column(
        db.String(16),
        nullable=False,
        default="1",
        info={'label': "Решение №"}
    )
    decision_num = db.Column(db.Integer, nullable=False, default=0)
    topic = db.Column(
        db.String(256),
        info={
            'label': "Тема",
            'form_field_class': TextAreaField,
        }
    )
    decision_date = db.Column(db.Date, info={'label': "Дата"})
    description = db.Column(db.UnicodeText, info={'label': "Описание"})

    # protocol = db.relationship("Protocol")

    def title(self, format="%s Решение №%s \"%s\""):
        return format % (self.protocol, self.decision_id, self.topic)

    def __repr__(self):
        return self.title()

    @property
    def date(self):
        if self.decision_date is not None:
            return self.decision_date
        else:
            return self.protocol.protocol_date

    def randomize(self, fake):
        self.decision_num = fake.pyint()
        self.topic = fake.sentence()
        chance = random.randint(0, 100)
        if chance < 10:
            self.decision_date = fake.past_date(start_date="-20y")
        chance = random.randint(0, 100)
        if chance < 25:
            self.description = "\n".join(fake.paragraphs())


class DecisionMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    decision_id = db.Column(db.Integer, db.ForeignKey('decision.id'))
    filename = db.Column(db.String(32), nullable=False, info={'label': "Файл"})
    title = db.Column(db.String(128), info={'label': "Заголовок"})
    description = db.Column(db.UnicodeText, info={'label': "Описание"})

    decision = db.relationship("Decision")

    def __repr__(self):
        if self.title:
            return self.title
        else:
            return self.filename


class Resolution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    decision_id = db.Column(db.Integer, db.ForeignKey('decision.id'))
    resolution_id = db.Column(
        db.String(16),
        nullable=False,
        default="1",
        info={'label': "Постановление №"}
    )
    resolution_num = db.Column(db.Integer, nullable=False, default=0)
    resolution_date = db.Column(db.Date, info={'label': "Дата"})
    description = db.Column(db.UnicodeText, info={'label': "Текст"})

    decision = db.relationship("Decision")

    def title(self, format="Постановление №%s"):
        return format % (self.resolution_id)

    def __repr__(self):
        return self.title()

    def randomize(self, fake):
        self.resolution_num = fake.pyint()
        self.resolution_date = fake.past_date(start_date="-20y")
        self.description = "\n".join(fake.paragraphs())
