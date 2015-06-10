from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server, prompt_bool
import yaml
import sqlalchemy

from radar.app import create_app
from radar.models import Structure, db, EveType, SolarSystem
from radar.utils import get_standing

with open('./config.yml') as f:
    config_file = f.read()

app = create_app(config_object=yaml.load(config_file))

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def update_structures():
    with app.app_context():
        keys = [key.split(',') for key in app.config.get('API_KEYS', [])]
        Structure.update_structures(keys)


@manager.command
def load_eve_data(data_dump):
    """
    Load EveTypes, SolarSystems and Moons in DB for quick lookup and links.
    This should only be ran once.
    """
    if not prompt_bool("This will load eve data into the database, if you already have done it, you should stop right here, are you sure you want to continue?"):
        return
    with app.app_context():
        app.config['SQLALCHEMY_ECHO'] = False
        eve_db = sqlalchemy.create_engine('sqlite:///' + data_dump)
        eve_metadata = sqlalchemy.MetaData(eve_db)

        eve_type = sqlalchemy.Table('invTypes', eve_metadata, autoload=True)
        solar_system = sqlalchemy.Table('mapSolarSystems', eve_metadata, autoload=True)
        regions = sqlalchemy.Table('mapRegions', eve_metadata, autoload=True)
        constellations = sqlalchemy.Table('mapConstellations', eve_metadata, autoload=True)

        types_count = sqlalchemy.select([sqlalchemy.func.count()]).select_from(eve_type).execute().fetchone()[0]
        types_processed = 0
        for row in eve_type.select().execute():
            types_processed += 1
            db.session.add(EveType(id=row['typeID'], name=row['typeName']))
            db.session.flush()
            if types_processed % 100 == 0:
                print('Adding types: {0:.2f}%'.format((types_processed / types_count) * 100))
        db.session.commit()

        systems_count = sqlalchemy.select([sqlalchemy.func.count()]).select_from(solar_system).execute().fetchone()[0]
        systems_processed = 0
        for row in solar_system.join(regions, solar_system.c.regionID == regions.c.regionID).join(constellations, solar_system.c.constellationID == constellations.c.constellationID).select(use_labels=True).execute():
            systems_processed += 1
            db.session.add(SolarSystem(
                id=row['mapSolarSystems_solarSystemID'],
                name=row['mapSolarSystems_solarSystemName'],
                region=row['mapRegions_regionName'],
                region_id=row['mapRegions_regionID'],
                constellation=row['mapConstellations_constellationName'],
                constellation_id=row['mapConstellations_constellationID'])
            )
            db.session.flush()
            if systems_processed % 100 == 0:
                print('Adding systems: {0:.2f}%'.format((systems_processed / systems_count) * 100))
        db.session.commit()


@manager.command
def get_stand():
    with app.app_context():
        print(get_standing(1301367357))

if __name__ == '__main__':
    manager.run()
