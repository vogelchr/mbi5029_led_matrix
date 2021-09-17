#!/usr/bin/python
import pcbnew
import re

# copy to ~/.local/share/kicad/5.99/scripting/plugins/led_matrix_16x16_place_led_grid.py
# so that it appears in pcbnew's Plugin menu

led_pitch_mm = 3.810
offs_x_mm = 127.0
offs_y_mm = 63.0


class LedMatrix16x16PlaceLedGrid(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = 'Build the 16x16 LED Grid'
        self.category = 'Modify PCB'
        self.description = '(description)'

    def Run(self):
        re_ref_led = re.compile('^D([0-9]+)')
        re_netname_cathode = re.compile('.*/LED_K([0-9]+)')
        re_netname_anode = re.compile('.*/LED_A([0-9]+)')
        re_ref_pmosfet = re.compile('Q([0-9]+)')

        board = pcbnew.GetBoard()
        for fp in board.Footprints():
            ref = fp.GetReference()
            re_match = re_ref_led.match(ref)
            if re_match is None or fp.GetPadCount() != 2:
                print(
                    f'Skipping footprint {ref} because of name or pad count.')
                continue

            cath_pad = None
            an_pad = None

            cath_num = None
            an_num = None

            print(f'Diode {ref} ...')
            for pad in fp.Pads():
                netname = pad.GetNetname()
                if (match := re_netname_cathode.match(netname)) is not None:
                    cath_num = int(match.group(1))
                    cath_pad = pad
                if (match := re_netname_anode.match(netname)) is not None:
                    an_num = int(match.group(1))
                    an_pad = pad

            if cath_num is None or an_num is None:
                print('Could not identify anode/cathode pads for {ref}.')
                continue

            print(
                f'{ref}: A{an_num} K{cath_num}')

            led_pos = pcbnew.wxPointMM(led_pitch_mm * (15-cath_num) + offs_x_mm,
                                       led_pitch_mm * (15-an_num) + offs_y_mm)
            fp.SetPosition(led_pos)
            fp.SetOrientationDegrees(45.0)

            via_an_pos = pcbnew.wxPoint(
                an_pad.GetCenter().x + 1000000,
                an_pad.GetCenter().y - 1000000
            )

            nbr_an_pos = pcbnew.wxPoint(
                via_an_pos.x + led_pitch_mm * 1e6,
                via_an_pos.y)

            nbr_cath_pos = pcbnew.wxPoint(
                cath_pad.GetCenter().x,
                cath_pad.GetCenter().y + led_pitch_mm * 1e6)

            if True:
                ###
                # anode pad to anode via
                ###
                v = pcbnew.PCB_VIA(board)
                v.SetPosition(via_an_pos)
                v.SetNet(an_pad.GetNet())
                v.SetViaType(pcbnew.VIATYPE_THROUGH)
                v.SetDrill(500000)
                v.SetWidth(800000)
                board.Add(v)

                trk = pcbnew.PCB_TRACK(board)
                trk.SetStart(an_pad.GetCenter())
                trk.SetEnd(v.GetCenter())
                trk.SetNet(an_pad.GetNet())
                trk.SetWidth(200000)
                board.Add(trk)

                trk = pcbnew.PCB_TRACK(board)
                trk.SetStart(v.GetCenter())
                trk.SetEnd(nbr_an_pos)
                trk.SetNet(an_pad.GetNet())
                trk.SetWidth(200000)
                trk.SetLayer(31)
                board.Add(trk)

            if True:
                trk = pcbnew.PCB_TRACK(board)
                trk.SetStart(cath_pad.GetCenter())
                trk.SetEnd(nbr_cath_pos)
                trk.SetNet(cath_pad.GetNet())
                trk.SetWidth(200000)
                board.Add(trk)

        for fp in board.Footprints():
            ref = fp.GetReference()
            re_match = re_ref_pmosfet.match(ref)
            if re_match is None or fp.GetPadCount() != 3:
                print( f'Skipping footprint {ref} because of name or pad count.')
                continue

            an_pad = None
            an_num = None

            print(f'Diode {ref} ...')
            for pad in fp.Pads():
                netname = pad.GetNetname()
                if (match := re_netname_anode.match(netname)) is not None:
                    an_num = int(match.group(1))
                    an_pad = pad

            if an_pad is None :
                continue

            led_pos = pcbnew.wxPointMM(led_pitch_mm * 17 + offs_x_mm,
                                       led_pitch_mm * (15-an_num) + offs_y_mm)
            fp.SetPosition(led_pos)
            fp.SetOrientationDegrees(-90.0)
   



LedMatrix16x16PlaceLedGrid().register()

print('Initializing of led_matrix_16x16_place_led_grid.py.')
