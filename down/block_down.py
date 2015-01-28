def PrintMessage(msg):
    print >>sys.stderr,'\r',
    print >>sys.stderr,msg,

def DownloadFile(url,tofile,CallBackFunction=PrintMessage):
    f = urllib2.urlopen(url)
    outf = open(tofile,'wb')        
    c = 0
    CallBackFunction('Download %s to %s'%(url,tofile))
    while True:
        s = f.read(1024*32)
        if len(s) == 0:
                break
        outf.write(s)
        c += len(s)
        CallBackFunction('Download %d'%(c))
    return c