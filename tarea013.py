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

from __future__ import generators
import sys, re
import wikipedia, pagegenerators,catlib, config
import urllib, time, random

l3=[]
salida=u"<noinclude>{{Advertencia|Esta plantilla es actualizada automáticamente. No hagas cambios aquí.}}</noinclude>\n==[[:Categoría:Wikipedia:Mantenimiento|Mantenimiento]]=="
for i in [u'Wikipedia:Artículos sin contextualizar', u'Wikipedia:Fusionar', u'Wikipedia:Copyedit', u'Wikipedia:No neutral', u'Wikipedia:Veracidad discutida', u'Wikipedia:Artículos que necesitan referencias']:
    cat=catlib.Category(wikipedia.Site("es", "wikipedia"), u"Category:%s" % i)
    l=[]
    l2=[]
    
    try:
        l=cat.articles()
    except:
        continue
    
    for j in l:
        if j.namespace() in [0, 104]:
            l2.append(j.title())
    
    length=len(l2)
    l3.append([l2[random.randint(0, length-1)], l2[random.randint(0, length-1)], l2[random.randint(0, length-1)]])
    

#salida+=u"\n* '''[[Wikipedia:Encontrar y arreglar un esbozo|Ampliar]]''': [[%s]], [[%s]], [[%s]], '''''[[:Categoría:Wikipedia:Esbozo|más...]]'''''" % (l3[0][0], l3[0][1], l3[0][2])
#salida+=u"\n* '''[[Wikiproyecto:Categorías|Categorizar]]''': [[%s]], [[%s]], [[%s]], '''''[[Especial:Uncategorizedpages|más...]]'''''"  % (l3[1][0], l3[1][1], l3[1][2])
salida+=u"\n* '''[[Wikipedia:Contextualizar|Contextualizar]]''': [[%s]], [[%s]], [[%s]], '''''[[:Categoría:Wikipedia:Artículos sin contextualizar|más...]]'''''" % (l3[0][0], l3[0][1], l3[0][2])
salida+=u"\n* '''[[Wikipedia:Páginas para fusionar|Duplicados]]''': [[%s]], [[%s]], [[%s]],  '''''[[:Categoría:Wikipedia:Fusionar|más...]]'''''" % (l3[1][0], l3[1][1], l3[1][2])
salida+=u"\n* '''[[Wikiproyecto:Corrección ortográfica|Mejorar]]''': [[%s]], [[%s]], [[%s]],  '''''[[:Categoría:Wikipedia:Copyedit|más...]]'''''" % (l3[2][0], l3[2][1], l3[2][2])
salida+=u"\n* '''[[Wikipedia:Páginas sospechosas de no neutralidad|No neutral]]''': [[%s]], [[%s]], [[%s]],  '''''[[:Categoría:Wikipedia:No neutral|más...]]'''''" % (l3[3][0], l3[3][1], l3[3][2])
salida+=u"\n* '''[[Wikipedia:Veracidad discutida|Veracidad discutida]]''': [[%s]], [[%s]], [[%s]], '''''[[:Categoría:Wikipedia:Veracidad discutida|más...]]'''''" % (l3[4][0], l3[4][1], l3[4][2])
salida+=u"\n* '''[[Wikipedia:Verificabilidad|Verificar]]''': [[%s]], [[%s]], [[%s]], '''''[[:Categoría:Wikipedia:Artículos que necesitan referencias|más...]]'''''" % (l3[5][0], l3[5][1], l3[5][2])
#salida+=u"\n* '''[[Wikiproyecto:Wikificar|Wikificar]]''': [[%s]], [[%s]], [[%s]], '''''[[:Categoría:Wikipedia:Wikificar|más...]]'''''" % (l3[7][0], l3[7][1], l3[7][2])

salida+=u"<noinclude>{{documentación}}</noinclude>"
wiii = wikipedia.Page(wikipedia.Site("es", "wikipedia"), u"Portal:Comunidad/Mantenimiento")
wiii.put(u"%s" % salida, u"BOT - Actualizando plantilla")

