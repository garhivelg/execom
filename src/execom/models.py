from app import db
from wtforms import TextAreaField
import random


class Protocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    protocol_id = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        info={'label': "Протокол №"}
    )
    protocol_txt = db.Column(
        db.String(16),
        nullable=True,
        default="",
        info={'label': "Протокол №"}
    )
    description = db.Column(db.UnicodeText, info={'label': "Описание"})
    protocol_date = db.Column(db.Date, info={'label': "Дата"})

    case = db.relationship("Case", backref="protocols")
    decisions = db.relationship("Decision", backref="protocol")

    def title(self, format="Протокол №%s%s", from_format=" от %s"):
        if self.date:
            date = from_format % (self.date.strftime("%x"))
        else:
            date = ""
        return format % (self.protocol_id_txt, date)

    def __repr__(self):
        return self.title()

    @property
    def date(self):
        if self.protocol_date:
            return self.protocol_date
        return None

    @property
    def decisions_count(self):
        return len(self.decisions)

    @property
    def protocol_id_txt(self):
        if not self.protocol_txt:
            if self.protocol_id:
                return self.protocol_id
            else:
                return "б/н"
        return self.protocol_txt

    def randomize(self, fake):
        self.protocol_id = fake.pyint()
        self.protocol_date = fake.past_date(start_date="-20y")
        chance = random.randint(0, 100)
        if chance < 25:
            self.description = "\n".join(fake.paragraphs())

    def normalize(self):
        if not self.protocol_txt:
            self.protocol_txt = self.protocol_id
            return

        try:
            res = int(''.join(c for c in self.protocol_txt if c.isdigit()))
        except ValueError:
            res = 0
        self.protocol_id = res

    def import_yml(self, data=dict()):
        self.protocol_txt = str(data.get('protocol_id'))
        self.protocol_date = data.get('date')
        self.description = data.get('description')
        self.normalize()


class Decision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocol_id = db.Column(db.Integer, db.ForeignKey('protocol.id'))
    decision_id = db.Column(
        db.String(16),
        nullable=True,
        default="",
        info={'label': "Решение №"}
    )
    decision_num = db.Column(db.Integer, nullable=False, default=0)
    topic = db.Column(
        db.String(512),
        info={
            'label': "Тема",
            'form_field_class': TextAreaField,
        }
    )
    decision_date = db.Column(db.Date, info={'label': "Дата"})
    description = db.Column(db.UnicodeText, info={'label': "Описание"})

    # protocol = db.relationship("Protocol")

    def title(
        self,
        format="%sРешение %s %s",
        protocol_format="%s ",
        id_format=" №%s",
        no_id="б/н"
    ):
        if self.protocol:
            protocol = protocol_format % (self.protocol)
        else:
            protocol = ""
        if self.decision_id:
            decision = id_format % (self.decision_id)
        else:
            decision = no_id
        if self.topic:
            topic = "\"%s\"" % (self.topic)
        else:
            topic = ""
        return format % (protocol, decision, topic)

    def __repr__(self):
        return self.title()

    @property
    def date(self):
        if self.decision_date is not None:
            return self.decision_date
        else:
            if self.protocol:
                return self.protocol.protocol_date
            else:
                return None

    @property
    def decision_id_txt(self):
        if not self.decision_id:
            if self.decision_num:
                return self.decision_num
            else:
                return "б/н"
        return self.decision_id

    def randomize(self, fake):
        self.decision_num = fake.pyint()
        self.topic = fake.sentence()
        chance = random.randint(0, 100)
        if chance < 10:
            self.decision_date = fake.past_date(start_date="-20y")
        chance = random.randint(0, 100)
        if chance < 25:
            self.description = "\n".join(fake.paragraphs())

    def normalize(self):
        if not self.decision_id:
            self.decision_id = self.decision_num
            return

        res = int(''.join(c for c in self.decision_id if c.isdigit()))
        self.decision_num = res

    def import_yml(self, data=dict()):
        self.decision_id = str(data.get('decision_id'))
        self.decision_date = data.get('date')
        self.topic = data.get('topic')
        self.description = data.get('description')
        self.normalize()


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
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    decision_id = db.Column(db.Integer, db.ForeignKey('decision.id'))
    resolution_id = db.Column(
        db.String(16),
        nullable=True,
        default="",
        info={'label': "Постановление №"}
    )
    resolution_num = db.Column(db.Integer, nullable=False, default=0)
    resolution_date = db.Column(db.Date, info={'label': "Дата"})
    description = db.Column(db.UnicodeText, info={'label': "Текст"})

    case = db.relationship("Case", backref="resolutions")
    decision = db.relationship("Decision")

    def title(self, format="Постановление %s", id_format="№%s", no_id=" б/н"):
        if self.resolution_id:
            resolution = id_format % (self.resolution_id)
        else:
            resolution = no_id
        return format % (resolution)

    def __repr__(self):
        return self.title()

    def randomize(self, fake):
        self.resolution_num = fake.pyint()
        self.resolution_date = fake.past_date(start_date="-20y")
        self.description = "\n".join(fake.paragraphs())

    def normalize(self):
        if not self.resolution_id:
            self.resolution_id = self.resolution_num
            return

        try:
            res = int(''.join(c for c in self.resolution_id if c.isdigit()))
        except ValueError:
            res = self.resolution_num
        self.resolution_num = res

    def import_yml(self, data=dict()):
        self.resolution_id = str(data.get('resolution_id'))
        self.resolution_date = data.get('date')
        self.description = data.get('description')
        self.normalize()
