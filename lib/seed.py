#!/usr/bin/env python3

# Script goes here!
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Company, Dev, Freebie

engine = create_engine("sqlite:///freebies.db")

Base.metadata.create_all(engine)

with Session(engine) as session:
    company1 = Company(name="Hajisafi", founding_year=2003)
    company2 = Company(name="Safi", founding_year=2000)
    session.add_all([company1, company2])
    session.commit()

    dev1 = Dev(name="job")
    dev2 = Dev(name="mapesa")
    session.add_all([dev1, dev2])
    session.commit()

    freebie1 = Freebie(item_name="Mariot", value=2, dev=dev1, company=company1)
    freebie2 = Freebie(item_name="watch", value=11, dev=dev1, company=company2)
    freebie3 = Freebie(item_name="soda", value=2, dev=dev2, company=company1)
    session.add_all([freebie1, freebie2, freebie3])
    session.commit()


    print("data created successfully.")