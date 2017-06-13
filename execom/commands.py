from app import manager, db
from faker import Factory
import random


from .models import Protocol, Decision
from case.models import Register, Case


@manager.command
def fill():
    "Fill db with sample data"
    print("hello")
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

            print("\tCase#%d of %d: %s" % (case_id, cases, case))
            db.session.add(case)
            db.session.commit()

            protocols = random.randint(1, 50)
            for protocol_id in range(protocols):
                protocol = Protocol()
                protocol.randomize(fake)
                protocol.case = case

                print("\t\tProtocol#%d of %d: %s" % (protocol_id, protocols, protocol))
                db.session.add(protocol)
                db.session.commit()

                decisions = random.randint(1, 20)
                for decision_id in range(decisions):
                    decision = Decision()
                    decision.randomize(fake)
                    decision.protocol = protocol

                    print("\t\t\tDecision#%d of %d: %s" % (decision_id, decisions, decision))
                    db.session.add(decision)
                    db.session.commit()
