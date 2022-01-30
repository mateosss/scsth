Example assuming 7ms predictions, 10ms image transfers, 16ms basalt computation

t (ms): event
----------------------------------------------
00: Camera shoots frame t=0 (half of exposure time)
00: OpenXR app requests prediction for t=7
07:
10: Host receives frame t=0 and redirects it to Basalt
16: OpenXR app requests prediction for t=23
23:
26: Basalt produces estimate pose for t=0
33: Camera shoots frame t=0 (half of exposure time)
33: OpenXR app requests prediction for t=40

(notice that the cycle will repeat from 33ms and on)
