import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from Urun_Ekle import *

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

#Veritabani islemleri
import sqlite3
baglanti = sqlite3.connect("urunler.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute("create table if not exists urun (urunKodu int, urunAdi text, birimFiyat int, stokMiktari int, urunAciklamasi text, marka text, kategori text) ")

def kayit_ekle():
    UrunKodu = int(ui.lne_UrunKodu.text())
    UrunAdi = ui.lne_urunadi.text()
    BirimFiyat = int(ui.lne_birimfiyat.text())
    StokMiktari = int(ui.lne_stokmiktari.text())
    UrunAciklama = ui.lne_UrunAciklama.text()
    Marka = ui.cmbMarka.currentText()
    Kategori = ui.cmbKategori.currentText()

    try:
        ekle = "insert into urun (urunKodu,urunAdi,birimFiyat,stokMiktari,urunAciklamasi,marka,kategori) values(?,?,?,?,?,?,?)"
        islem.execute(ekle,(UrunKodu,UrunAdi,BirimFiyat,StokMiktari,UrunAciklama,Marka,Kategori))
        baglanti.commit()
        #mesajin kac saniye duracagini belirttik
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı",10000)
        kayit_listele()

    except Exception as error:
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarısız. Hata: "+str(error))

def kayit_listele():
    ui.tbl_Listele.clear()
    ui.tbl_Listele.setHorizontalHeaderLabels(("Urun Kodu", "Urun Adi", "Birim Fiyati", "Stok Miktari", "Urun Aciklama", "Markasi", "Kategori"))
    ui.tbl_Listele.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    sorgu = "select * from urun"
    islem.execute(sorgu)

    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tbl_Listele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

def kategoriye_gore_listele():
    listelenecek_kategori = ui.cmbKategori_2.currentText()

    sorgu = "select * from urun where kategori = ?"
    islem.execute(sorgu,(listelenecek_kategori,))
    ui.tbl_Listele.clear()
    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tbl_Listele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere,"Silme Onayı", "Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tbl_Listele.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()

        sorgu = "delete from urun where urunKodu = ?"
        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı. Hata: "+str(error))
    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")

def kayit_guncelle():
    guncelle_mesaj = QMessageBox.question(pencere,"Güncelleme Onayı","Bu kaydı Güncellemek istediğinizden Emin Misiniz ?",QMessageBox.Yes | QMessageBox.No)

    if guncelle_mesaj == QMessageBox.Yes:
        try:
            UrunKodu = ui.lne_UrunKodu.text()
            UrunAdi = ui.lne_urunadi.text()
            BirimFiyati = ui.lne_birimfiyat.text()
            StokMiktari = ui.lne_stokmiktari.text()
            UrunAciklama = ui.lne_UrunAciklama.text()
            Marka = ui.cmbMarka.currentText()
            Kategori = ui.cmbKategori.currentText()

            if UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "":
                islem.execute("update urun set kategori = ? where urunKodu = ?",(Kategori,UrunKodu))

            elif UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Kategori == "":
                islem.execute("update urun set marka = ? where urunKodu = ?",(Marka,UrunKodu)) 

            elif UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set urunAciklaması = ? where urunKodu = ?",(UrunAciklama,UrunKodu))
            elif UrunAdi == "" and BirimFiyati == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set stokMiktari = ? where urunKodu = ?",(StokMiktari,UrunKodu))
            elif UrunAdi == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set birimFiyat = ? where urunKodu = ?",(BirimFiyati,UrunKodu))
            elif BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set urunAdi = ? where urunKodu = ?",(UrunAdi,UrunKodu))
            else:
                islem.execute("update urun set urunAdi = ?, birimFiyat = ? , stokMiktari = ?, urunAciklaması = ?, marka = ?, kategori = ? where urunKodu = ?",(UrunAdi,BirimFiyati,StokMiktari,UrunAciklama,Marka, Kategori,UrunKodu))
            baglanti.commit()
            kayit_listele()
            ui.statusbar.showMessage("Kayıt Başarıyla Güncellendi")
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Güncellemede Hata Çıktı === "+str(error))
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi")

#Butonlar
ui.btn_Ekle.clicked.connect(kayit_ekle)
ui.btn_listele.clicked.connect(kayit_listele)
ui.btn_KategoriyeGoreListele.clicked.connect(kategoriye_gore_listele)
ui.btn_Sil.clicked.connect(kayit_sil)
ui.btn_Guncelle.clicked.connect(kayit_guncelle)
# Pencere kapatma butonuna basilmadigi surece acik kalmasi icin yazdik
sys.exit(uygulama.exec_())