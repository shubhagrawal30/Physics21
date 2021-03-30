"""
Physics 21, Assignment 1, Version 1.0
Shubh Agrawal
Class of 2022

This .py file is my submission for Caltech's Physics 21.
It accessses the online astrophysics data set for the Catalina survey,
scraps data in html or VOTable format, and plots the data.
"""

import urllib.request
import matplotlib.pyplot as plt
from astropy.io.votable import parse_single_table


# To allow for multiple figure to be printed in the same run
figure_no = 0
def plot(x, y, filename):
    '''
    Plots the data from the two lists x & y and stores it under filename.
    '''
    global figure_no
    plt.figure(figure_no)
    plt.scatter(x, y)
    plt.xlabel("time in MJD")
    plt.ylabel("magnitude")
    plt.savefig(filename)
    figure_no = figure_no + 1

url = "http://nesssi.cacr.caltech.edu/cgi-bin/getcssconedbid_release2.cgi"

value = {"Name" : "Her X-1", "DB" : "photcal", "OUT" : "html", "SHORT" : "short"}
data = urllib.parse.urlencode(value).encode('ascii')

req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
   page = response.read()

source = str(page.decode('ascii'))

def getValues(source):
    '''
    For Part 1:
        Gets values using html format
    '''
    start = source.find('<td>1135075045477<td>13.34<td>0.05<td>254.4576')
    end = source.find('\n</table><br><p>\n<p><br><p></HTML>')
    vals = source[start: end]
    
    mag = []
    mjd = []
    leng = len('1135075045477<td>')
    diff = len('13.34<td>0.05<td>254.4576<td>35.3424<td>')
    mag_len = len("13.34")
    mjd_len = len("53557.32593")
    pos = vals.find('1135075045477<td>') + leng
    
    while(pos >= leng):
        mag.append(float(vals[pos: pos + mag_len]))
        mjd.append(float(vals[pos + diff: pos + diff + mjd_len]))
        vals = vals[pos + diff + mjd_len:]
        pos = vals.find('1135075045477<td>') + leng
        
    return (mag, mjd)

mag, mjd = getValues(source)
    
plot(mjd, mag, "html.png")

url = "http://nesssi.cacr.caltech.edu/DataRelease/upload/result_web_fileyUkAfF.vot"

source = urllib.request.urlretrieve(url, filename="data.xml")

def getVOTvalues(filename):
    '''
    For Part 1:
        Gets values using VOTable format
    '''
    mag = []
    mjd = []
    votable = parse_single_table(filename, pedantic=False)
    votable = votable.array
    for item in votable['Mag']:
        mag.append(item[0])
    for item in votable['ObsTime']:
        mjd.append(item[0])
    return (mag, mjd)
    
mag, mjd = getVOTvalues("data.xml")

plot(mjd, mag, "vot.png")