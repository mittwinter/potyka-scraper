#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import re

urlTemplate = 'http://www.potyka.com/shop/shop_menu.php3?nPos={pos}&g={groupID}&VID={sessionID}'
sessionID = 'SmLZf2oeXDAUHMiD'

print( '"groupID","artNo","name","allocation","deposit","price","normalizedPrice"' )
for g in [ 1, 2, 28, 29, 37, 5, 3, 46, 31, 30, 4, 6, 27, 32, 33, 49, 7, 25, 26, 35, 34, 39, 40, 42, 50 ]: # iterate groups
	for p in range( 0, 200, 20): # iterate pages
		#print( '-> group: {0}, page: {1}'.format( g, int( p / 20 ) ) )
		url = urllib.request.urlopen( urlTemplate.format( groupID = g, pos = p, sessionID = sessionID ) )
		content = url.read()
		soup = BeautifulSoup( content )
		t = soup.find( 'table', 'artlisttable' )
		rows = t.find_all( 'tr' )
		if len( rows ) > 1:
			for row in rows:
				cells = row.find_all( 'td' )
				if cells:
					matchArtNo = re.match( '^[0-9]+$', cells[ 0 ].get_text().strip() )
					if matchArtNo is not None:
						artNo = matchArtNo.group( 0 )
						name = cells[ 1 ].b.get_text()
						matchAllocdeposit = re.search( r'(.+)\+([0-9]+,[0-9]{2}) EUR Pfand', cells[ 2 ].get_text() )
						if matchAllocdeposit is not None:
							allocation = matchAllocdeposit.group( 1 )
							deposit = matchAllocdeposit.group( 2 )
						else:
							allocation = cells[ 2 ].get_text()
							deposit = '0,00'
						price = cells[ 4 ].b.get_text()
						normPrice = re.search( r'Liter: ([0-9]+,[0-9]{2})', cells[ 4 ].get_text() ).group( 1 )
						#print( 'g: {0:>2}, artNo: {1:>5s}, name: {2:60s}, allocation: {3:30s}, deposit: {4:>6s}, price: {5:>6s}, normPrice: {6:>6s}'.format( g, artNo, name, allocation, deposit, price, normPrice ) )
						print( '"{0}","{1}","{2}","{3}","{4}","{5}","{6}"'.format( g, artNo, name, allocation, deposit, price, normPrice ) )
		else:
			break
