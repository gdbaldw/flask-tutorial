from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import g

Base = declarative_base()

from . import models


def init_app(app):
    engine = create_engine(
        'sqlite:///{}'.format(app.config['DATABASE'])
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    @app.before_request
    def create_session():
        g.session = Session()

    @app.teardown_appcontext
    def shutdown_session(error=None):
        session = g.pop('session', None)
        if session:
            if error:
                session.rollback()
            else:
                session.commit()
            session.close()
