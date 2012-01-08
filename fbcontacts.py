#!/usr/bin/env python
import sys
import base64
import codecs
import sqlite3
import urllib2
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
    return [row for row in c]

def generate_vcard(contact, photos=False):
    card = "BEGIN:VCARD\nVERSION:3.0\n"
    card += "N:%s;%s;;;\n" % (contact['last_name'], contact['first_name'])
    card += "FN:%s\n" % contact['display_name']

    if contact['cell']:
        card += 'TEL;TYPE=CELL:%s\n' % contact['cell']

    if contact['other']:
        card += 'TEL;TYPE=HOME:%s\n' % contact['other']

    if contact['email']:
        card += "EMAIL;TYPE=PREF:%s\n" % contact['email']

    birthday = "-".join([str(f) for f in [contact['birthday_year'],
                                          contact['birthday_month'],
                                          contact['birthday_day']]
                         if f != -1])
    if birthday:
        if birthday.count('-') == 1: birthday = "1900-" + birthday # default year
        card += "BDAY:%s\n" % birthday

    if photos and contact['user_image_url']:
        try:
            photo = urllib2.urlopen(contact['user_image_url']).read()
            card += "PHOTO;ENCODING=B;TYPE=JPEG:%s\n" %\
                    base64.b64encode(photo)
        except:
            pass


    card += "REV:%s\nEND:VCARD\n" % datetime.datetime.now().isoformat()
    return card

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('database', help="path to facebook database", default="fb.db", nargs='?')
    parser.add_argument('vcard', help="file to write contacts to", default="fbcontacts.vcf", nargs='?')
    parser.add_argument('--photos', action="store_true", help="download profile pictures")
    args = parser.parse_args()

    with codecs.open(args.vcard, 'w', 'utf-8') as vcard:
        contacts = parse_database(args.database)
        for i, contact in enumerate(contacts):
            sys.stderr.write("\rexporting contact %s of %s" % (i+1, len(contacts)))
            card = generate_vcard(contact, args.photos)
            print >> vcard, card
            sys.stderr.flush()
        sys.stderr.write("\n")

if __name__ == "__main__": main()
