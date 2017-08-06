from app import manager, db
from faker import Factory
import random
import yaml


from .models import Protocol, Decision, Resolution
from case.models import Register, Case


@manager.command
def fill():
    "Fill db with sample data"
    fake = Factory.create('ru_RU')

    registers = random.randint(10, 50)
    for register_id in range(registers):
        register = Register()
        register.randomize(fake)

        print("Record#%d of %d: %s" % (register_id, registers, register))
        db.session.add(register)
        db.session.commit()

        cases = random.randint(1, 100)
        for case_id in range(cases):
            case = Case()
            case.randomize(fake)
            case.register = register

            print("\tRecord#%d of %d: %s" % (register_id, registers, register))
            print("\tCase#%d of %d: %s" % (case_id, cases, case))
            db.session.add(case)
            db.session.commit()

            protocols = random.randint(1, 50)
            for protocol_id in range(protocols):
                protocol = Protocol()
                protocol.randomize(fake)
                protocol.case = case

                print("\t\tRecord#%d of %d: %s" % (register_id, registers, register))
                print("\t\tCase#%d of %d: %s" % (case_id, cases, case))
                print("\t\tProtocol#%d of %d: %s" % (protocol_id, protocols, protocol))
                db.session.add(protocol)
                db.session.commit()

                decisions = random.randint(1, 20)
                for decision_id in range(decisions):
                    decision = Decision()
                    decision.randomize(fake)
                    decision.protocol = protocol

                    print("\t\t\tRecord#%d of %d: %s" % (register_id, registers, register))
                    print("\t\t\tCase#%d of %d: %s" % (case_id, cases, case))
                    print("\t\t\tProtocol#%d of %d: %s" % (protocol_id, protocols, protocol))
                    print("\t\t\tDecision#%d of %d: %s" % (decision_id, decisions, decision))
                    db.session.add(decision)
                    db.session.commit()


@manager.command
def export():
    "Export data from db"
    export_data = {'version': '1.0.0', }
    export_data['registers'] = [str(r) for r in Register.query.all()]

    cases = Case.query.all()
    export_data['cases'] = []
    for case in cases:
        case.normalize()
        export_data['cases'].append({
            'id': str(case.id),
            'register': str(case.register),
            'book': str(case.book_id),
            'description': case.description,
        })

    protocols = Protocol.query.all()
    export_data['protocols'] = []
    for protocol in protocols:
        protocol.normalize()
        export_data['protocols'].append({
            'id': protocol.id,
            'protocol_id': protocol.protocol_txt,
            'case': protocol.case_id,
            'date': protocol.protocol_date,
            'description': protocol.description,
        })

    decisions = Decision.query.all()
    export_data['decisions'] = []
    for decision in decisions:
        decision.normalize()
        export_data['decisions'].append({
            'id': decision.id,
            'protocol': decision.protocol_id,
            'decision_id': decision.decision_id,
            'date': decision.decision_date,
            'topic': decision.topic,
            'description': decision.description,
        })

    resolutions = Resolution.query.all()
    export_data['resolutions'] = []
    for resolution in resolutions:
        resolution.normalize()
        export_data['resolutions'].append({
            'id': resolution.id,
            'case': resolution.case_id,
            'decision': resolution.decision_id,
            'resolution_id': resolution.resolution_id,
            'date': resolution.resolution_date,
            'description': resolution.description,
        })
    print(export_data)
    new_export_data = {
        'version': export_data['version'],
        'cases': export_data['cases'],
        'protocols': export_data['protocols'],
        'decisions': export_data['decisions'],
        'resolutions': export_data['resolutions'],
    }
    print(yaml.dump(export_data))
