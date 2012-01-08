# Export Facebook Contacts from Android #

## Introduction ##

This script exports all of your Facebook contacts from an internal database used by 
the Facebook app (on Android). Unlike other methods, you get phone numbers and 
profile pictures in addition to email addresses and names.

## Requirements ##

* rooted android phone
* facebook application installed on phone
* fb.db (located on your phone at /data/data/com.facebook.katana/databases/fb.db)

## Usage ##

	usage: fbcontacts.py [-h] [--photos] [database] [vcard]
	
	positional arguments:
	  database    path to facebook database
	  vcard       file to write contacts to
	
	optional arguments:
	  -h, --help  show this help message and exit
	  --photos    download profile pictures
