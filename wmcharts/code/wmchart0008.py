# -*- coding: utf-8 -*-

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

from wmchart0000 import *

filename = 'wmchart0008.html'
title = 'Reverts'
description = "This chart shows how many edits were reverted in the last days."

projectdbs = getProjectDatabases(lang='en', family='wikipedia')

undo = '([Rr]evert|[Uu]ndid)'
queries = [
    ["All", "SELECT CONCAT(YEAR(rc_timestamp),'-',LPAD(MONTH(rc_timestamp),2,'0'),'-',LPAD(DAY(rc_timestamp),2,'0'),'T00:00:00Z') AS date, COUNT(*) AS count FROM recentchanges WHERE rc_timestamp>=DATE_ADD(NOW(), INTERVAL -%d DAY) AND rc_type=0 AND rc_namespace=0 AND rc_comment rlike '%s' GROUP BY date ORDER BY date ASC" % (lastdays, undo)],
    ["ClueBot NG", "SELECT CONCAT(YEAR(rc_timestamp),'-',LPAD(MONTH(rc_timestamp),2,'0'),'-',LPAD(DAY(rc_timestamp),2,'0'),'T00:00:00Z') AS date, COUNT(*) AS count FROM recentchanges WHERE rc_timestamp>=DATE_ADD(NOW(), INTERVAL -%d DAY) AND rc_type=0 AND rc_namespace=0 AND rc_comment rlike '%s' AND rc_user_text='ClueBot NG' GROUP BY date ORDER BY date ASC" % (lastdays, undo)],
    ["XLinkBot", "SELECT CONCAT(YEAR(rc_timestamp),'-',LPAD(MONTH(rc_timestamp),2,'0'),'-',LPAD(DAY(rc_timestamp),2,'0'),'T00:00:00Z') AS date, COUNT(*) AS count FROM recentchanges WHERE rc_timestamp>=DATE_ADD(NOW(), INTERVAL -%d DAY) AND rc_type=0 AND rc_namespace=0 AND rc_comment rlike '%s' AND rc_user_text='XLinkBot' GROUP BY date ORDER BY date ASC" % (lastdays, undo)],
    ["Huggle", "SELECT CONCAT(YEAR(rc_timestamp),'-',LPAD(MONTH(rc_timestamp),2,'0'),'-',LPAD(DAY(rc_timestamp),2,'0'),'T00:00:00Z') AS date, COUNT(*) AS count FROM recentchanges WHERE rc_timestamp>=DATE_ADD(NOW(), INTERVAL -%d DAY) AND rc_type=0 AND rc_namespace=0 AND rc_comment rlike '%s' AND rc_comment rlike 'WP:HG' GROUP BY date ORDER BY date ASC" % (lastdays, undo)],
    ["Twinkle", "SELECT CONCAT(YEAR(rc_timestamp),'-',LPAD(MONTH(rc_timestamp),2,'0'),'-',LPAD(DAY(rc_timestamp),2,'0'),'T00:00:00Z') AS date, COUNT(*) AS count FROM recentchanges WHERE rc_timestamp>=DATE_ADD(NOW(), INTERVAL -%d DAY) AND rc_type=0 AND rc_namespace=0 AND rc_comment rlike '%s' AND rc_comment rlike 'WP:TW' GROUP BY date ORDER BY date ASC" % (lastdays, undo)],
]
projects = runQueries(projectdbs=projectdbs, queries=queries)
select = generateHTMLSelect(projects)

var1 = []
var2 = []
var3 = []
var4 = []
var5 = []
varother = []
for project, values in projects:
    var1.append(values["All"])
    var2.append(values["ClueBot NG"])
    var3.append(values["XLinkBot"])
    var4.append(values["Huggle"])
    var5.append(values["Twinkle"])
    varother.append(values["All"]-(values["ClueBot NG"]+values["XLinkBot"]+values["Huggle"]+values["Twinkle"]))

js = """function p() {
    var d1 = %s;
    var d2 = %s;
    var d3 = %s;
    var d4 = %s;
    var d5 = %s;
    var dother = %s;
    var placeholder = $("#placeholder");
    var selected = document.getElementById('projects').selectedIndex;
    var data = [{ data: d1[selected], label: "All"}, { data: d2[selected], label: "ClueBot NG"}, { data: d3[selected], label: "XLinkBot"}, { data: d4[selected], label: "Huggle"}, { data: d5[selected], label: "Twinkle"}, { data: dother[selected], label: "Other"}];
    var options = { xaxis: { mode: "time" }, lines: {show: true}, points: {show: true}, legend: {noColumns: 6}, grid: { hoverable: true }, };
    $.plot(placeholder, data, options);
}
p();""" % (str(var1), str(var2), str(var3), str(var4), str(var5), str(varother))

output = generateHTML(title=title, description=description, select=select, js=js)
writeHTML(filename=filename, output=output)