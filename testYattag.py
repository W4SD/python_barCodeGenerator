from yattag import Doc

doc, tag, text = Doc().tagtext()

doc.asis('<!DOCTYPE html>')

with tag('html'):
    with tag('head'):
        doc.stag('link', rel='stylesheet', type='text/css', href='barCode.css')
        with tag('title'):
            text('barCodeGen v.01')
    
    with tag('body'):
        with tag('div', klass='sheet'):
            with tag('p', id='objName'):
                text('SPIRE SPP30: 2010171')
            doc.stag('img', src='spireId.svg', id='barCodeTop')
            with tag('p', id="serialNo"):
                text('SerialNo')
            doc.stag('img', src='barCodeSerial.svg', id='barCodeBottom')

print(doc.getvalue())
indexFile = open('index.htm', 'w')
indexFile.write(doc.getvalue())
indexFile.close