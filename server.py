from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import datetime,timedelta
import time
import os

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
with SimpleXMLRPCServer(
    ("192.168.1.12",8008),
    requestHandler=RequestHandler,
    allow_none=True) as server:
    server.register_introspection_functions()

    #Melihat Antrian Dari Setiap Klinik Yang Ada
    def Lihat_Antrian_Pasien(Nomor_Rekam_Medis_Pasien, Poliklinik):
        global list_pasien
        k = 0

        for j in range(len(list_pasien)):
            if list_pasien[j][3] == Poliklinik and list_pasien[j][0] == Nomor_Rekam_Medis_Pasien:
                return k,list_pasien[j][5]
            else:
                if list_pasien[j][3] == Poliklinik:
                    k += 1
        return False,False
    
    #Memperbaharui Urutan Dari Antrian Ketika Terdapat Antrian Yang Baru
    def Refresh_Urutan_Pasien():
        global list_pasien, counter
        if len(list_pasien) > 0:
            return True
    
    #Melihat list Dari Pasien Yang Telah Di Input
    def Lihat_List_Pasien():
        return list_pasien
    

    list_pasien = []   
    counter = 0
    
    #Fungsi Registrasi Yang Akan Memasukkan Nomor Rekam Medis Pasien, Nama Pasien, Tanggal lahir, dan Poliklinik
    def Registrasi_Data_Pasien(
        Nomor_Rekam_Medis_Pasien,
        Nama_Pasien,
        Tanggal_Lahir_Pasien,
        Poliklinik):

        global counter

        if not list_pasien:
            counter = 0

        list_pasien.append([])
        list_pasien[counter].append(Nomor_Rekam_Medis_Pasien)
        list_pasien[counter].append(Nama_Pasien)
        list_pasien[counter].append(Tanggal_Lahir_Pasien)
        list_pasien[counter].append(Poliklinik)

        Nomor_Antrian_Pasien = 0
        for i in range(len(list_pasien)):
            for j in range(len(list_pasien[i])):
                if list_pasien[i][j] == Poliklinik:
                    Nomor_Antrian_Pasien += 1

        if Nomor_Antrian_Pasien == 0:
            Nomor_Antrian_Pasien = Nomor_Antrian_Pasien + 1
            
        if(Nomor_Antrian_Pasien-1 == 0):   
            list_pasien[counter].append((datetime.now() + timedelta(minutes = 1)).strftime("%H:%M:%S"))
        else:
            Waktu_Kelar = datetime.strptime(datetime.now().date().strftime("%d%m%y")+" "+list_pasien[len(list_pasien)-2][4], "%d%m%y %H:%M:%S")        
            if(Waktu_Kelar < datetime.now()):
                list_pasien[counter].append((datetime.now() + timedelta(minutes = 1)).strftime("%H:%M:%S"))
            else:
                list_pasien[counter].append((Waktu_Kelar + timedelta(minutes = 1)).strftime("%H:%M:%S"))

        list_pasien[counter].append(Nomor_Antrian_Pasien)
        counter += 1

        return Nomor_Antrian_Pasien

    server.register_function(Lihat_Antrian_Pasien, 'lihatAntrian')
    server.register_function(Refresh_Urutan_Pasien, 'refreshUrutan')
    server.register_function(Lihat_List_Pasien, 'lihatlist')
    server.register_function(Registrasi_Data_Pasien, 'registrasi')
    
   
    
    os.system("CLS")
    print("Menjalankan Server .....")

    server.serve_forever()