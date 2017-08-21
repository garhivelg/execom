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
def export(output=None):
    "Export data from db"
    export_data = {'version': '1.0.0', }
    export_data['registers'] = [{
        'id': r.id,
        'fund': r.fund,
        'register': r.register,
    } for r in Register.query.all()]

    cases = Case.query.all()
    export_data['cases'] = []
    for case in cases:
        case.normalize()
        export_data['cases'].append({
            'id': str(case.id),
            'register': str(case.register.id),
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
    print(yaml.dump(export_data, allow_unicode=True))
    if output is not None:
        print("Save to \"%s\"" % (output))
        with open(output, "w") as outfile:
            yaml.dump(export_data, outfile, default_flow_style=False, allow_unicode=True)
        print("Saved to %s" % (output, ))


@manager.command
def import_yml(input=None):
    "Import data from db"
    if input is None:
        print("No data to import")
        return
    else:
        with open(input, 'r') as infile:
            try:
                print("Load from \"%s\"" % (input))
                data = yaml.load(infile)
                version = data.get('version')
                if version == "1.0.0":
                    print(version)

                    registers = data.get('registers', [])
                    register_lookup = dict()
                    for r in registers:
                        fund = r.get('fund')
                        register = Register.query.filter_by(fund=fund, register=r.get('register')).first()
                        if register is None:
                            register = Register(fund=fund)
                        register.import_yml(r)
                        print("%s:\t%s" % (r.get('fund'), r))
                        register_lookup[r.get('id')] = register
                        db.session.add(register)
                    db.session.commit()

                    cases = data.get('cases', [])
                    case_lookup = dict()
                    for c in cases:
                        register = register_lookup.get(int(c.get('register')))
                        case = Case(register=register)
                        case.import_yml(c)
                        print("%s:\t%s" % (register, c))
                        case_lookup[int(c.get('id'))] = case
                        db.session.add(case)
                    db.session.commit()

                    protocols = data.get('protocols', [])
                    protocol_lookup = dict()
                    for p in protocols:
                        case = case_lookup.get(p.get('case'))
                        protocol = Protocol(case=case)
                        protocol.import_yml(p)
                        print("%s:\t%s" % (case, p))
                        protocol_lookup[int(p.get('id'))] = protocol
                        db.session.add(protocol)
                    db.session.commit()

                    decisions = data.get('decisions', [])
                    decision_lookup = dict()
                    for d in decisions:
                        protocol = protocol_lookup.get(d.get('protocol'))
                        decision = Decision(protocol=protocol)
                        decision.import_yml(d)
                        print("%s:\t%s" % (protocol, d))
                        decision_lookup[int(d.get('id'))] = decision
                        db.session.add(decision)
                    db.session.commit()

                    resolutions = data.get('resolutions', [])
                    for r in resolutions:
                        case = case_lookup.get(r.get('case'))
                        decision = decision_lookup.get(r.get('decision'))
                        resolution = Resolution(case=case, decision=decision)
                        resolution.import_yml(r)
                        print("%s, %s:\t%s" % (case, decision, r))
                        db.session.add(resolution)
                    db.session.commit()

                    print(register_lookup)
                    print(case_lookup)
                    print(protocol_lookup)
                print("Loaded from \"%s\"" % (input))
            except yaml.YAMLError as exc:
                print(exc)
