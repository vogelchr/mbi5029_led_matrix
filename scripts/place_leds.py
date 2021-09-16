#!/usr/bin/python
import pcbnew
import re
import pathlib

def doit() :
    fn = pathlib.Path('/home/chris/KiCad/mbi5029_lex_matrix/scripts/place_leds.py')
    code = compile(fn.open().read(), fn.name, 'exec')
    exec(code)

def place_leds() :
    pitch = 3.5*1e6 # 2mm

    re_diode = re.compile('^D([0-9]+)')
    print('Place Leds running.')
    board = pcbnew.GetBoard()
    for fp in board.GetFootprints() :
        ref = fp.GetReference()

        m = re_diode.match(ref)
        if not m or fp.GetPadCount() != 2 :
            continue
        ix = int(m.group(1)) - 1
        
        col = ix % 16
        row = ix // 16
        
        p = pcbnew.wxPoint(pitch * col, pitch * row)
        fp.SetPosition(p)

        pad1 = fp.Pads()[0]
        ppos = pad1.GetPosition()
        
        via = pcbnew.Via(b)
        via.v.SetPosition(pcbnew.wxPoint(
            ppos.x + 1000000, ppos.y))
        via.SetDrill(1000000)
        via.SetWidth(1800000)
        
        board.add(via)
        
        print(ref, col, row, p, ppos)


place_leds()
