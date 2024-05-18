import re

isClipboardInstalled = False
try:
    import clipboard
    isClipboardInstalled = True
except ImportError:
    print('\033[92mclipboard is not installed, Using clipboard, you can easily parse the data\n[ shell ] pip install clipboard\033[0m')
    isClipboardInstalled = False

data = '''data:0000000140003000 byte_140003000  db 0, 4Dh, 51h, 50h, 0EFh, 0FBh, 0C3h, 0CFh, 92h, 45h
.data:0000000140003000                                         ; DATA XREF: sub_140001000+40↑o
.data:000000014000300A                 db 4Dh, 0CFh, 0F5h, 4, 40h, 50h, 43h, 63h, 0Eh dup(10)'''

def sanitize(text):
    text = text.strip()
    if text[0:3] == 'db ': text = text[3:]
    if text[-1] == 'h': text = text[:-1]
    if text == '0': return '00'
    else:
        if text[0] == '0': text = text[1:]
        text = text.rjust(2, '0')
        return text

data = sanitize(data)

class Format():
    def __init__(self, data) -> None:
        self._data = []
        self.data = []
        
        data = ','.join(re.findall('db.*', data))
        for item in data.split(','):
            item = item.strip()
            if 'dup' in item:
                val, count = item.split()
                count = int(count[4:-1])
                val = sanitize(val)
                for _ in range(count):
                    self._data.append(val)
                    self.data.append('0x'+val)
            else:
                item = sanitize(item)
                self._data.append(item)
                self.data.append('0x'+item)

    def _join(self, arr:list, sep=', '):
        return sep.join(arr)
    def python(self, name:str='arr', short=False):
        if short:
            result = f'{name} = \'{self._join(self._data, sep=' ')}\''
        else:
            result = f'{name} = [{self._join(self.data)}]'
        if(isClipboardInstalled):
            print('copied in clipboard')
            clipboard.copy(result)
        print(result)
        return result
    def c(self, name:str='arr'):
        result = f'int {name}[{len(self.data)+1}] = {{{self._join(self.data)}}};'
        if(isClipboardInstalled):
            print('copied in clipboard')
            clipboard.copy(result)
        print(result)
        return result

format = Format(data)
format.python()
format.python(short=True)
format.c()
