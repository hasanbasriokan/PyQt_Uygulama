from PyQt5 import uic
from sympy import O

with open("Urun_Ekle.py","w", encoding="utf-8") as fout:
    uic.compileUi("gui.ui", fout)