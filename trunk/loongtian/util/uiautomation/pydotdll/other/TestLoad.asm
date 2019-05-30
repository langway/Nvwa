
;fasm TestLoad.asm

format PE console

include "%include%/win32ax.inc"

xx:
i MessageBoxA, 0, 'Hello guy !', 'i am title .', 0
ret
entry $
i LoadLibraryA, 'PYdotDLL.dll'
i CreateThread, 0, 0, xx, 0, 0, 0
ret