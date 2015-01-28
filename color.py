#!/bin/env python

class Color:
    gray    = '\033[1;30m'
    red     = '\033[1;31m'
    green   = '\033[1;32m'
    yellow  = '\033[1;33m'
    blue    = '\033[1;34m'
    magenta = '\033[1;35m'
    cyan    = '\033[1;36m'
    white   = '\033[1;37m'
    crimson = '\033[1;38m'
 
    hred    = '\033[1;41m'
    hgreen  = '\033[1;42m'
    hbrown  = '\033[1;43m'
    hblue   = '\033[1;44m'
    hmagenta= '\033[1;45m'
    hcyan   = '\033[1;46m'
    hgray   = '\033[1;47m'
    hcrimson= '\033[1;48m'

    blinking='\033[5m'
    end     = '\033[1;m'

def main():
    c = Color()
    print '%sGray like Ghost%s' % (c.gray, c.end)
    print '%sRed like Radish%s'  % (c.red, c.end)
    print '%sGreen like Grass%s' % (c.green, c.end)
    print '%sYellow like Yolk%s' % (c.yellow, c.end)
    print '%sBlue like Blood%s' % (c.blue, c.end)
    print '%sMagenta like Mimosa%s' % (c.magenta, c.end)
    print '%sCyan like Caribbean%s' % (c.cyan, c.end)
    print '%sWhite like Whipped Cream%s' % (c.white, c.end)
    print '%sCrimson like Chianti%s' % (c.crimson, c.end)
    print '%sHighlighted Red like Radish%s' % (c.hred, c.end)
    print '%sHighlighted Green like Grass%s' % (c.hgreen, c.end)
    print '%sHighlighted Brown like Bear%s' % (c.hbrown, c.end)
    print '%sHighlighted Blue like Blood%s' % (c.hblue, c.end)
    print '%sHighlighted Magenta like Mimosa%s' % (c.hmagenta, c.end)
    print '%sHighlighted Cyan like Caribbean%s' % (c.hcyan, c.end)
    print '%sHighlighted Gray like Ghost%s' % (c.hgray, c.end)
    print '%sHighlighted Crimson like Chianti%s' % (c.hcrimson, c.end)

if __name__ == '__main__':
    main()
 
