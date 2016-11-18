from controller_class import *
import sys

if len(sys.argv) > 1 :

    unifi_controller = uvp_controller()
    unifi_controller.connect ("10.100.200.9")
    unifi_controller.login("unifi","percipia123")

    for i in range(1,len(sys.argv),2):
        if "--clear-all" in sys.argv[i]:
            unifi_controller.clear_extension_list()
        elif "--file" in sys.argv[i]:
            filename = sys.argv[i+1]
            import csv
            f = open(filename)
            csv_f = csv.reader(f)
            for row in csv_f:
                _account_no = row[0]
                _mac = row[1]
                _ext = row[2]
                _roomno = row[3]
                _name = row[4]
                _pbx = row[5]
                frequency = pbx(_pbx,"*97")
                new_account = account(_account_no,_name,_ext,"percipia123",frequency)
                new_phone = phone("UVP-Executive",_mac,new_account)
                unifi_controller.add_phone(new_phone)
                del frequency,new_account,new_phone
        elif "--alias" in sys.argv[i]:
            filename = sys.argv[i+1]
            import csv
            f = open(filename)
            csv_f = csv.reader(f)
            for row in csv_f:
                _account_no = row[0]
                _mac = row[1]
                _ext = row[2]
                _roomno = row[3]
                _name = row[4]
                _pbx = row[5]
                frequency = pbx(_pbx,"*97")
                new_account = account(_account_no,_name,_ext,"percipia123",frequency)
                new_phone = phone("UVP-Executive",_mac,new_account)
                unifi_controller.set_alias_by_mac(new_phone.mac,new_account.name)
                del frequency,new_account,new_phone
        else :
            print "Bad Argument !"
else :
    print 
    print "    EXAMPLE : python uvp_controller.py [--argument value]"
    print 
    print "    --clear-all    ->   Clear all of extensions from controller "
    print "    --file [file]  ->   To add extension using the CSV file "
    print "    --alias [file] ->   To configure devie aliases using CSV file "