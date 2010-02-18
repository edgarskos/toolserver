#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys
import os
import MySQLdb

path="/home/emijrp/public_html/wikimediacounter"
f=open('%s/wpcounter.log' % path, 'r')
raw=f.read().splitlines()[0]
[timestamp_old, total_old]=raw.split(';')
timestamp_old=int(timestamp_old)
total_old=int(total_old)
print "timestamp_old =", timestamp_old, "total_old =", total_old
f.close()

timestamp=int(datetime.datetime.now().strftime('%s'))*1000
total=0.0

conn = MySQLdb.connect(host='sql-s1', db='toolserver', read_default_file='~/.my.cnf', use_unicode=True)
cursor = conn.cursor()
cursor.execute("SELECT lang, family, CONCAT('sql-s', server) AS dbserver, dbname FROM toolserver.wiki WHERE 1;")
result=cursor.fetchall()
checked=0
families=["wikibooks", "wikipedia", "wiktionary", "wikimedia", "wikiquote", "wikisource", "wikinews", "wikiversity", "commons", "wikispecies"]
for row in result:
	lang=row[0]
	family=row[1]
	if family not in families:
		continue
	dbserver=row[2]+""
	dbname=row[3]
	
	try:
		conn2 = MySQLdb.connect(host=dbserver, db=dbname, read_default_file='~/.my.cnf', use_unicode=True)
		cursor2 = conn2.cursor()
		#print "OK:", dbserver, dbname
		cursor2.execute("select ss_total_edits from site_stats where 1")
		result2=cursor2.fetchall()
		for row2 in result2:
			edits=int(row2[0])
			total+=edits
			checked+=1
			if edits>1:
				print "%s;%s;%s" % (edits, dbname, dbserver)

		cursor2.close()
		conn2.close()
	except:
		print "Error in", dbserver, dbname

print "timestamp =", timestamp, "total =", total
editrate=(total-total_old)/(timestamp-timestamp_old) # per milisecond
print "editrate =", editrate
print families
print "databases =",checked

if editrate<=0:
	sys.exit() #wait to the next update

#output=getPHPHeader(tool_id, tool_title)
output=u"""<html>
<head>
<title>Wikimedia projects edits counter</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<style type="text/css">
<!--
body {
	margin:0;border:0;padding:0;
	font-family:monospace;
	background: #fff;
	color: #000;
	text-align: center;
}
div#wrapper{
	display:table;
	width:100%%;
}
div#content{
	display:table-cell;vertical-align:middle;
	background-image: url('wplogo.png');
	background-repeat: no-repeat;
	background-attachment: fixed;
	background-position: center center;
	height:100%%;
	}
span#header {
	font-size:250%%;
	font-weight:bold;
	}
span#counter {
	font-size:1000%%;
	font-weight:bold;
	}
p#followus, p#translateit {
	position:absolute;
	margin:0;border:0;padding:0;
	top:10;
}
p#followus {
	left:10;
}
p#translateit{
	right:10;
}
p#donate, p#author, p#f11 {
	position:absolute;
	margin:0;border:0;padding:0;
	bottom:10;
	}
p#donate {
	left:10;
	}
p#author {
	right:10;
	}
p#f11 {
	left:50%%;
	width:40em;
	margin-left:-20em;
	text-align:center;
	bottom:30;
	}
-->
</style>

</head>

<body>

<div id='wrapper'>
<div id='content'>

<p id="followus"><a href="http://www.facebook.com/group.php?gid=287466429242">Facebook group</a></p>

<p id="translateit"><a href="http://en.wikipedia.org/wiki/User:Emijrp/Wikimedia_counter">Translate it!</a></p>

<span id="header">Total edits in <a href="http://www.wikimedia.org">Wikimedia projects</a>:</span>

<span id='counter'>&nbsp;</span>

<p id="donate"><a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Donate to Wikimedia Foundation</a></p>
<p id="f11">Press F11 for fullscreen</p>
<p id="author">Developed by <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspired by <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)</p>

</div>
</div>


<script type="text/javascript">

//language
var lang="";
var spliter=",";
var header="";
var donate="";
var f11="";
var author="";
if (navigator.systemLanguage){
	lang=navigator.systemLanguage
}else if (navigator.userLanguage){
	lang=navigator.userLanguage;
}else if(navigator.language){
	lang=navigator.language;
}else{
	lang="en";
}

if (lang.length>2) { lang=lang.substring(0,2); }

switch(lang){
	case "example":
		header='<a href="http://www.wikimedia.org"></a>:';
		spliter='&nbsp;';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia"></a>';
		f11='';
		author='<a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (<a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "ar":
		header='مجموع التعديلات في <a href="http://www.wikimedia.org">مشاريع ويكيميديا</a>:';
		spliter=',';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">تبرع لمؤسسة ويكيميديا</a>';
		f11='للشاشة الكاملة اضغط F11';
		author='من تطوير <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (ملهمة من <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "ca":
		header='Edicions entre tots els <a href="http://www.wikimedia.org">projectes de Wikimedia</a>:';
		spliter='.';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Dona a la Fundació Wikimedia</a>';
		f11='Pantalla completa pulsant F11';
		author='Desarrollat per <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspirat en <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "cs":
		header='Celkový počet editací v <a href="http://www.wikimedia.org">projektech nadace Wikimedia</a>:';
		spliter='&nbsp;';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Podpořte Wikimedia Foundation</a>';
		f11='Stisknutím klávesy F11 zobrazíte stránku na celou obrazovku';
		author='Vyvinul <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (inspirováno stránkami <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "da":
		header='Totalt antal redigeringer i <a href="http://www.wikimedia.org">Wikimedias projekter</a>:';
		spliter='.';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Giv et bidrag til Wikimedia Foundation</a>';
		f11='Tryk F11 for fuldskærmsvisning';
		author='Udviklet af <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspireret af <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "de":
		header='Gesamtzahl der Bearbeitungen an <a href="http://www.wikimedia.org">den Wikimedia Projekten</a>:';
		//spliter='';
		//donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia"></a>';
		//f11='';
		//author='<a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (<a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "eo":
		header='Totala nombro de redaktoj en <a href="http://www.wikimedia.org">Vikimediaj projektoj</a>:';
		spliter='.';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Donaci al Fondaĵo Vikimedio</a>';
		f11='Premu F11 por plenekrana modo';
		author='Kreita de <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspirita de <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "es":
		header='Ediciones entre todos los <a href="http://www.wikimedia.org">proyectos Wikimedia</a>:';
		spliter='.';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Dona a la Fundación Wikimedia</a>';
		f11='Pantalla completa pulsando F11';
		author='Desarrollado por <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspirado en <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "eu":
		header='<a href="http://www.wikimedia.org">Wikimedia proiektuetan</a> egindako eguneraketak guztira:';
		spliter='.';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Wikimedia Foundazioari dohaintza egin</a>';
		f11='F11 sakatu pantaila osoan erakusteko';
		author='<a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a>-ek garatua (<a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>-ek inspiratuta)';
		break;
	case "fr":
		header="Nombre total d'éditions dans les <a href='http://www.wikimedia.org'>projets Wikimedia</a>:"; // be careful with d'éditions
		spliter='&nbsp;';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Donner à la Wikimedia Foundation</a>';
		f11='Appuyez sur F11 pour passer en plein écran';
		author='Développé par <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspiré par <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "hu":
		header='<a href="http://www.wikimedia.org">A Wikimédia projektek</a> együttes szerkesztésszáma:';
		spliter='&nbsp;';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Támogasd a Wikimédia Alapítványt</a>';
		f11='Teljes képernyős mód: F11';
		author='Készítette: <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (<a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a> ötlete alapján)';
		break;
	case "it":
		header='Modifiche totali nei <a href="http://www.wikimedia.org">progetti Wikimedia</a>:';
		spliter='.';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Fai una donazione alla Wikimedia Foundation</a>';
		f11='Premi F11 per visualizzare a schermo intero';
		author='Sviluppato da <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Ispirato da <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "kl":
		header='Tamakkiisumik amerlassutsit aaqqissuussinerni <a href="http://www.wikimedia.org">Wikimedia suliniutaani</a>:';
		spliter='.';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Wikimedia suliniutaani tunissuteqarit</a>';
		f11='F11 tooruk tamaat saqqummissagukku';
		author='Siuarsaasuuvoq <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Peqatigalugu <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "nl":
		header='Totaal aantal bewerkingen in <a href="http://www.wikimedia.org">Wikimediaprojecten</a>:';
		//spliter='&nbsp;';
		//donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia"></a>';
		//f11='';
		//author='<a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (<a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "pl":
		header='Ogólna liczba edycji w <a href="http://www.wikimedia.org">projektach Wikimedia</a>:';
		spliter='&nbsp;';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Wesprzyj Wikimedia Foundation</a>';
		f11='Naciśnij F11, aby włączyć tryb pełnoekranowy';
		author='Stworzony przez <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (zainspirowany przez <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "pt":
		header='Total de edições nos <a href="http://www.wikimedia.org">projetos Wikimedia</a>:';
		spliter='.';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Doe para a Fundação Wikimedia</a>';
		f11='Pressione F11 para tela cheia';
		author='Desenvolvido por <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspirado em <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "ru":
		header='Всего правок в <a href="http://www.wikimedia.org">проектах Wikimedia</a>:';
		spliter='&nbsp;';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Пожертвовать Фонду Wikimedia</a>';
		f11='Нажмите F11 для полноэкранного просмотра';
		author='Разработано <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (при поддержке<a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "sv":
		header='Antal redigeringar i <a href="http://www.wikimedia.org">Wikimediaprojekten</a>:';
		spliter='&nbsp;';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Donera till Wikimedia Foundation</a>';
		f11='Tryck F11 för helskärm';
		author='Utvecklad av <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspirerad av <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
		break;
	case "te":
		header='<a href="http://www.wikimedia.org">వికీమీడియా ప్రాజెక్టుల</a>లో మొత్తం దిద్దుబాట్లు:';
		spliter=',';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">వికీమీడియా ఫౌండేషనుకి విరాళమివ్వండి</a>';
		f11='నిండుతెర కొరకు F11 నొక్కండి';
		author='రూపొందించినది <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (<a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a> ప్రేరణతో)';
		break;
	default:
		header='Total edits in <a href="http://www.wikimedia.org">Wikimedia projects</a>:';
		spliter=',';
		donate='<a href="http://wikimediafoundation.org/wiki/Support_Wikipedia">Donate to Wikimedia Foundation</a>';
		f11='Press F11 for fullscreen';
		author='Developed by <a href="http://es.wikipedia.org/wiki/User:Emijrp">emijrp</a> (Inspired by <a href="http://www.7is7.com/software/firefox/partycounter.html">7is7</a>)';
}

document.getElementById('header').innerHTML=header;
document.getElementById('donate').innerHTML=donate;
document.getElementById('f11').innerHTML=f11;
document.getElementById('author').innerHTML=author;

var editinit=%.0f;
var timeinit=%d;
var timenow=new Date().getTime();
var period=1000/10; // period update in miliseconds
var editrate=%.3f; //per milisecond
editrate=editrate*period;
var editnow=editinit+((timenow-timeinit)/period)*editrate;
id=window.setTimeout("update();",period);
function update() {
   editnow+=editrate;
   editnowtext=""+Math.round(editnow)
   for(var i=3; i<editnowtext.length; i+=3) {
      editnowtext=editnowtext.replace(/(^|\s)(\d+)(\d{3})/,'$2'+spliter+'$3');
   }
   document.getElementById('counter').innerHTML=editnowtext;
   id=window.setTimeout("update();",period);
}

function adjustSizes(){
	var width=800;
	var height=600;
	if (self.innerWidth) { 
		width=self.innerWidth;
		height=self.innerHeight;
	} else if (document.documentElement && document.documentElement.clientWidth) { 
		width=document.documentElement.clientWidth;
		height=document.documentElement.clientHeight;
	} else if (document.body) {
		width=document.body.clientWidth;
		height=document.body.clientHeight;
	}
	document.getElementById('wrapper').style.height=(height-10)+'px';
	document.getElementById('header').style.fontSize=width/60+'pt';
	document.getElementById('counter').style.fontSize=width/12+'pt';
}

window.onload=adjustSizes;
window.onresize=adjustSizes;

</script>



</body>

</html>

""" % (total, timestamp, editrate)

if total>total_old:
	f=open("%s/index.php" % path, 'w')
	f.write(output.encode("utf-8"))
	f.close()

	f=open('%s/wpcounter.log' % path, 'w')
	f.write("%d;%.0f" % (timestamp, total))
	f.close()

cursor.close()
conn.close()


