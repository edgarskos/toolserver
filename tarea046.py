# -*- coding: utf-8 -*-

# Copyright (C) 2009 emijrp
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import wikipedia
import urllib, re
import htmlentitydefs

#http://groups.google.com/group/comp.lang.python/browse_thread/thread/7f96723282376f8c/
def convertentity(m):
	"""Convert a HTML entity into normal string (ISO-8859-1)"""
	print m.group(2)
	if m.group(1)=='#':
		try:
			return chr(int(m.group(2)))
		except ValueError:
			return '&#%s;' % m.group(2)
	try:
		return htmlentitydefs.entitydefs[m.group(2)]
	except KeyError:
		return '&%s;' % m.group(2)

def unquotehtml(s):
    """Convert a HTML quoted string into normal string (ISO-8859-1).

    Works with &#XX; and with &nbsp; &gt; etc."""
    return re.sub(r'&(#?)(.+?);',convertentity,s) 

site=wikipedia.Site('meta', 'meta')
tables=[
[u"List of Wikipedias/Table", 'http://s23.org/wikistats/wikipedias_wiki.php'],
[u"Wikibooks/Table", 'http://s23.org/wikistats/wikibooks_wiki.php'],
[u"Wiktionary/Table", 'http://s23.org/wikistats/wiktionaries_wiki.php'],
[u"Wikiquote/Table", 'http://s23.org/wikistats/wikiquotes_wiki.php'],
[u"Wikinews/Table", 'http://s23.org/wikistats/wikinews_wiki.php'],
[u"Wikisource/Table", 'http://s23.org/wikistats/wikisources_wiki.php'],
[u"Wikiversity/Table", 'http://s23.org/wikistats/wikiversity_wiki.php'],
]
for table, url in tables:
	wii=wikipedia.Page(site, table)
	output=urllib.urlopen(url).read()
	output="{|"+("{|".join(output.split("{|")[1:]))
	output=re.sub(ur"(?im)(<pre>\n?|\n?</pre>|</?[^>]+?>)", ur"", output)
	output.strip()
	#output=unquotehtml(output)
	if table=="List of Wikipedias/Table":
		output="=== 1 000 000+ articles ===\n"+output
	if wii.get()!=output:
		wii.put(output, u"BOT - Updating page")





