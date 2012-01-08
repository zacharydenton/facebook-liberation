#!/usr/bin/env python
import sys
import sqlite3
import argparse
import datetime

def parse_database(database):
    conn = sqlite3.connect(database)
    conn.row_factory=sqlite3.Row
    c = conn.cursor()
    fields = 'display_name, user_image_url, first_name, ' +\
             'last_name, cell, other, email, birthday_month, ' +\
             'birthday_day, birthday_year'
    c.execute('select %s from friends' % fields)
    for row in c:
        yield row

def generate_vcard(contact):
    card = "BEGIN:VCARD\nVERSION:4.0\n"
    card += "N:%s;%s;;;\n" % (contact['last_name'], contact['first_name'])
    card += "FN:%s\n" % contact['display_name']

    if contact['user_image_url']:
        card += "PHOTO:%s\n" % contact['user_image_url']

    if contact['cell']:
        card += 'TEL;TYPE="cell,voice";VALUE=uri:tel:%s\n' % contact['cell']

    if contact['other']:
        card += 'TEL;TYPE="home,voice";VALUE=uri:tel:%s\n' % contact['other']

    if contact['email']:
        card += "EMAIL:%s\n" % contact['email']

    birthday = "-".join([str(f) for f in [contact['birthday_year'],
                                          contact['birthday_month'],
                                          contact['birthday_day']]
                         if f != -1])
    if birthday:
        card += "BDAY:%s\n" % birthday

    card += "REV:%s\nEND:VCARD\n" % datetime.datetime.now().isoformat()
    return card

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('database', help="path to facebook database", default="fb.db", nargs='?')
    parser.add_argument('vcard', help="file to write contacts to", default="fbcontacts.vcf", nargs='?')
    args = parser.parse_args()

    with open(args.vcard, 'w') as vcard:
        for contact in parse_database(args.database):
            card = generate_vcard(contact)
            print >> vcard, card.encode('utf-8')

if __name__ == "__main__": main()
