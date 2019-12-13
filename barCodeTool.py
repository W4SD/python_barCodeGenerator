import barcode
from yattag import Doc
import webbrowser

barCodeType = "code39"
headerText = "Spire SPP30"
itemId = "2010171"
serialId = ""

serialBatch = []
running = False
generatePrint = False


def generateHeader(header_barcode):
    modded_writer_options = {
        'module_width': 0.2,
        'module_height': 15.0,
        'quiet_zone': 1.0,
        'font_size': 10,
        'text_distance': 5.0,
        'background': 'white',
        'foreground': 'black',
        'write_text': False,
        'text': '',
    }
    barcode.generate(barCodeType, str(header_barcode), output="header",
                     writer_options=modded_writer_options)


def getNextSerial():
    print('Read next serialNo: ')
    currentSerialId = input()
    return currentSerialId


def changeDefaults():
    print('Enter header text: ')
    custom_headerText = input()
    print('Enter ID/SERIAL#:')
    custom_itemId = input()
    print('Current config:',
          'barCode type = ' + barCodeType,
          'headerText = ' + custom_headerText,
          'itemId = ' + custom_itemId,
          sep='\n')
    print('Everything Ok? (y/n)')
    allOk = input()
    global headerText
    headerText = custom_headerText
    global itemId
    itemId = custom_itemId
    generateHeader(custom_itemId)
    return allOk


print('default settings:',
      'barCode type = ' + barCodeType,
      'headerText = ' + headerText,
      'itemId = ' + itemId,
      # 'serialId = ' + serialId,
      sep='\n')

print('Change default config? y/n')
changeDefaultValues = input()

# User input for default values

if (changeDefaultValues == 'y' or changeDefaultValues == 'Y'):
    clear = ''
    while (clear != 'y'):
        clear = changeDefaults()
    if (clear == 'y'):
        running = True
    
else:
    generateHeader(itemId)
    running = True

# run item serial collector

while running:
    if (serialId == "" and len(serialBatch) > 0):
        print('...generating print file...')
        generatePrint = True
        running = False
    else:
        serialId = getNextSerial()
        if (serialId != ""):
            serialBatch.append(serialId)
        else:
            serialBatch.sort()
            print('Enter desired filename to save (' + str(len(serialBatch)) + ') serials:')
            batchFileName = input()
            with open(batchFileName + '.txt', 'w') as batchFile:
                for i in serialBatch:
                    # print(i)
                    batchFile.write(i + '\n')
            print('Serials saved as: ' + batchFileName + '.txt')


# Generate html site with barcodes

def populateSheet(thisSerial, count):
    doc, tag, text = Doc().tagtext()

    with tag('div', klass='sheet'):
        # top line barcode
        with tag('p', id='objName'):
            text(headerText + ': ' + itemId)
        
        # doc.stag('img', src='spireId.svg', id='barCodeTop')
        doc.stag('img', src='header.svg', id='barCodeTop')

        # bottom line barcode
        with tag('p', id="serialNo"):
            text('serialNo: ' + str(thisSerial))

        barCodeFileName = 'barCodeSerial' + str(count)
        bCodeAndEnd = barCodeFileName + '.svg'
        barcode.generate(barCodeType, str(thisSerial), output=barCodeFileName)
        doc.stag('img', src=bCodeAndEnd, id='barCodeBottom')
    return doc.getvalue()


if (generatePrint):
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')

    with tag('html'):
        with tag('head'):
            doc.stag('link', rel='stylesheet', type='text/css', href='barCode.css')
            with tag('title'):
                text('barCodeGen v.8')

        with tag('body'):
            loop = 0
            for i in serialBatch:
                doc.asis(populateSheet(i, loop))
                loop += 1
                
    indexString = doc.getvalue()

    with open('index.htm', 'w') as indexFile:
        indexFile.write(indexString)

    webbrowser.open('index.htm', new=0, autoraise=True)

print('END')

