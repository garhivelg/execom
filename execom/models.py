from app import db


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
        return format % (self.protocol_id, self.protocol_date.strftime("%x"))

    def __repr__(self):
        return self.title()

    @property
    def decisions_count(self):
        return len(self.decisions)


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
    topic = db.Column(db.String(256), info={'label': "Тема"})
    description = db.Column(db.UnicodeText, info={'label': "Описание"})

    # protocol = db.relationship("Protocol")

    def title(self, format="%s Решение №%s \"%s\""):
        return format % (self.protocol, self.decision_id, self.topic)

    def __repr__(self):
        return self.title()


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
