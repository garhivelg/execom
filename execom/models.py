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

    case = db.relationship("Case")

    def title(self, format="Протокол №%d от %s"):
        return format % (self.protocol_id, self.protocol_date)

    def __repr__(self):
        return self.title()


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
    description = db.Column(db.UnicodeText, info={'label': "Описание"})

    protocol = db.relationship("Protocol")

    def title(self, format="%s Решение №%s"):
        return format % (self.protocol, self.decision_id)

    def __repr__(self):
        return self.title()
