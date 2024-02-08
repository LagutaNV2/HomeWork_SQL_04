import configparser
import json

import config
import psycopg2
import q
import sqlalchemy

from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale


def add_tables_from_json(name_json):
    with open(name_json, 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))


def get_sales_pablishers(input_name):
    selected = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(
        Shop).join(Sale).filter(Publisher.name.like(input_name))
    for s in selected.all():
        print(f'{s[0]:<50} | {s[1]:<15} | {str(s[2])} | {str(s[3])}')

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('setting.ini')
    DSN = config["PSQL"]["DSN"]
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    add_tables_from_json('tests_data.json')
    session.commit()

    input_name = input('Введите название издателя: ')
    get_sales_pablishers(input_name)

    session.close()