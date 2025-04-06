from colored import *

class buffer:
    def __init__(self):
        self.txt = []
        self.x = 120
        self.y = 29

    def write(self, txt, newline=False):
        if newline:
            self.txt.append(txt)
        else:
            self.txt[len(self.txt)-1] += txt
    
    def flush(self):
        print(*self.txt, sep="\n")
        self.txt = []

def healthBar(buffer, name, hp, plr=False):
    width = buffer.x
    space_width = (width - width//3 - len(name) - 6) // 2
    color = Fore.green if plr else Fore.red
    buffer.write(Style.bold + '\\'*(width//6) + ' '*space_width + f'>> {name} <<' + ' '*space_width + '/'*(width//6) + Style.reset, True)
    buffer.write('-'*(60-hp) + color + '='*hp*2 + Style.reset + '-'*(60-hp), True)
    buffer.write(Style.bold + '/'*(width//6) + ' '*space_width + '~'*(len(name)+6) + ' '*space_width + '\\'*(width//6) + Style.reset, True)

def splitText(txt, maxlen=59) -> list:
    stxt = txt.split()
    out = ['', '', '']
    lineid = 0
    for word in stxt:
        if len(out[lineid] + word) < maxlen:
            out[lineid] += word + ' '
        else:
            lineid += 1
            out[lineid] += word + ' '
    return out

def controls(buffer, acts: list, full=False):
    ...

if __name__ == '__main__':
    # splitText test
    print(*splitText('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore'), sep="\n")
    print('|'*60)