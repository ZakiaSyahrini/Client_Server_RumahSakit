#Library Yang Digunakan
import xmlrpc.client
import datetime
import time
import os

#Pendefinisian Server
Server = xmlrpc.client.ServerProxy("http://192.168.1.12:8008", allow_none=True)

#Mengurutkan Pasien Berdasarkan Fungsi Lihat List Yang Terdapat Pada Server, Urutan Berdasarkan Waktu
def List_Urutan_Pasien() :
    List_Pasien = Server.lihatlist()
    for item in List_Pasien :
        print(item)
    input()
    os.system("CLS")

#Mencari Nomor Antrian Pasien Dan Waktu Tunggu Pasien
def Cari_Antrian_Pasien():
    Inputan = input("Masukan Pilihan Poliklinik : ")
    Rekam_Medis_Pasien = input("Masukan Nomor Rekam Medis Pasien : ")
 
    Antrian_Pasien, Hasil_Pasien = Server.lihatAntrian(Rekam_Medis_Pasien,Inputan)

    if Antrian_Pasien and Hasil_Pasien == False :
        print("Data Not Found")
    else :
        print("Nomor Antrian Anda adalah",Hasil_Pasien)
        if Hasil_Pasien == 1 :
            print("Anda harus Menunggu Sekitar ",(Hasil_Pasien)*5," menit lagi")
        elif Hasil_Pasien > 1 :
            print("Anda harus Menunggu Sekitar ",(Hasil_Pasien-1)*5," menit lagi")
        elif Hasil_Pasien == 0 :
            print("Anda harus Menunggu Sekitar ",(Hasil_Pasien+1)*5," menit lagi")

    input()
    os.system("CLS")

#Mendaftarkan Pasien Beserta Dengan Data-Data Yang Diperlukan Seperti Nomor Rekam Medis Pasien, Nama, Tanggal Lahir, dan Poliklinik
def Pendaftaran_Pasien():
    os.system("CLS")
    global Nomor_Rekam_Medis_Pasien, Nama_Pasien, Tanggal_Lahir, Pilihan_Poliklinik

    print("Masukkan Data Pasien : ")

    Nomor_Rekam_Medis_Pasien = input("Nomor Rekam Medis Pasien : ")
    Nama_Pasien = input("Nama Pasien : ")
    Tanggal_Lahir = input("Tanggal Lahir Pasien : ")

    os.system("CLS")
    print("Processing Data")
    time.sleep(1)
    print("Silahkan Memilih Poliklinik")
    print("1. Poliklinik Gigi")
    print("2. Poliklinik Umum")
    print("3. Poliklinik Anak")
    print("4. Poliklinik Jantung")
    print("5. Poliklinik Gizi")
    print("6. Poliklinik Saraf")
    print("Masukkan Nama Poliklinik :")
    Pilihan_Poliklinik = input()

    Hasil_Pasien = Server.registrasi(Nomor_Rekam_Medis_Pasien,Nama_Pasien,Tanggal_Lahir,Pilihan_Poliklinik)

    print("Nomor Antrian",Hasil_Pasien)
    input()
    os.system("CLS")

#Main Function Dari Program, Program Atau Tampilan Pertama Yang Akan Ditampilkan Ketika Program Dijalankan
def Halaman_Utama() :
    while True :
        waktu = datetime.datetime.now()
        Server.refreshUrutan()

        print("Welcome to Telkom Medikaversity")
        print("=======================================")
        print("Waktu Saat Ini : ", waktu.strftime("%m/%d/%Y, %H:%M:%S"))
        print("=======================================")
        print()
        print("1. Registrasi Data Pasien")
        print("2. Cek Nomor Antrian Pasien ")
        print("3. Cek Urutan Data Pasien")
        print("4. Keluar")
        print("")
        pilihan = input('Masukkan Pilihan Anda : ')

        if pilihan == "1" :
            Pendaftaran_Pasien()

        elif pilihan == "2" :
            Cari_Antrian_Pasien()

        elif pilihan == "3" :
            List_Urutan_Pasien()
        else :
            exit()

Halaman_Utama()