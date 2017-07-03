
import re
from .psparser import PSLiteral
from .glyphlist import glyphname2unicode
from .latin_enc import ENCODING

import six # Python 2+3 compatibility

STRIP_NAME = re.compile(r'[0-9]+')


##  name2unicode
##
def name2unicode(name):
    """Converts Adobe glyph names to Unicode numbers."""
    if name in glyphname2unicode:
        return glyphname2unicode[name]
    m = STRIP_NAME.search(name)
    if not m:
        raise KeyError(name)
    return six.unichr(int(m.group(0)))


##  EncodingDB
##
class EncodingDB(object):

    std2unicode = {}
    mac2unicode = {}
    win2unicode = {}
    pdf2unicode = {}
    std_glyphs = {}
    mac_glyphs = {}
    win_glyphs = {}
    pdf_glyphs = {}
    for (name, std, mac, win, pdf) in ENCODING:
        c = name2unicode(name)
        if std:
            std2unicode[std] = c
            std_glyphs[std] = name
        if mac:
            mac2unicode[mac] = c
            mac_glyphs[mac] = name
        if win:
            win2unicode[win] = c
            win_glyphs[win] = name
        if pdf:
            pdf2unicode[pdf] = c
            pdf_glyphs[pdf] = name

    encodings = {
        'StandardEncoding': std2unicode,
        'MacRomanEncoding': mac2unicode,
        'WinAnsiEncoding': win2unicode,
        'PDFDocEncoding': pdf2unicode,
    }

    glyphnames = {
        'StandardEncoding': std_glyphs,
        'MacRomanEncoding': mac_glyphs,
        'WinAnsiEncoding': win_glyphs,
        'PDFdocEncoding': pdf_glyphs,
    }

    @classmethod
    def get_encoding(klass, name, diff=None):
        cid2unicode = klass.encodings.get(name, klass.std2unicode)
        if diff:
            cid2unicode = cid2unicode.copy()
            cid = 0
            for x in diff:
                if isinstance(x, int):
                    cid = x
                elif isinstance(x, PSLiteral):
                    try:
                        cid2unicode[cid] = name2unicode(x.name)
                    except KeyError:
                        pass
                    cid += 1
        return cid2unicode

    @classmethod
    def get_glyphnames(klass, name, diff=None):
        cid2glyphname = klass.glyphnames.get(name, klass.std_glyphs)
        if diff:
            cid2glyphname = cid2glyphname.copy()
            cid = 0
            for x in diff:
                if isinstance(x, int):
                    cid = x
                elif isinstance(x, PSLiteral):
                    cid2glyphname[cid] = x.name
                cid += 1
        return cid2glyphname

