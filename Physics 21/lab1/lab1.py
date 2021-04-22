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


"""
---- FEEDBACK ---- 
(no action needed) 

You don't need to declare figure_no as a "global" to access it within plot() - it's global 
(with respect to that function at least) because youy declared it outside the function.

Also, you don't need to explicitly call plt.figure() with a figure number each time - you 
can just call plt.figure() without an argument, or just call plt.scatter() without creating a 
figure (pyplot automatically creates one in this case)

Also, nice job making a doctsring!
"""

"""
---- FEEDBACK ----
(action needed)

Having parts of your script floating between methods like this works, but it's not pretty.
I would suggest consolidating the commands you want to execute into a "__main__" segment 
at the end of the script, and keep all your functions before and outside of this "__main__" segment.
It's much cleaner code, and good practice!
"""




def getValues(source):
    '''
    For Part 1:
        Gets values using html format
    '''
    # find the start and end points of the data in the end file (indexes selected by hand)
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
    # lengths assigned by first values that are selected by hand
    
    while(pos >= leng):
        # loop over the entire value set, and get all the mag and mjd
        mag.append(float(vals[pos: pos + mag_len]))
        mjd.append(float(vals[pos + diff: pos + diff + mjd_len]))
        vals = vals[pos + diff + mjd_len:]
        pos = vals.find('1135075045477<td>') + leng
        
    return (mag, mjd)
    
    
"""
---- FEEDBACK ----
(action needed)

You should add a comment or two to this method (getValues()), to (briefly) explain what your code is
doing 
"""

"""
---- FEEDBACK ----
(action needed)

Same comment as before about consolidating the floating parts into a "__main__" segment
"""




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
    

"""
---- FEEDBACK ----
(action needed)

Same comment as before about consolidating the floating parts into a "__main__" segment
"""

if __name__ == "__main__":
    url = "http://nesssi.cacr.caltech.edu/cgi-bin/getcssconedbid_release2.cgi"

    value = {"Name" : "Her X-1", "DB" : "photcal", "OUT" : "html", "SHORT" : "short"}
    data = urllib.parse.urlencode(value).encode('ascii')

    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
       page = response.read()

    source = str(page.decode('ascii'))

    mag, mjd = getValues(source)
    
    plot(mjd, mag, "html.png")

    url = "http://nesssi.cacr.caltech.edu/DataRelease/upload/result_web_fileyUkAfF.vot"

    source = urllib.request.urlretrieve(url, filename="data.xml")

    mag, mjd = getVOTvalues("data.xml")

    plot(mjd, mag, "vot.png")


