class uvp_controller (object) :
    #-------------------------------------------------------------------
    def get_the_cookie ():
        import cookielib
        cj = cookielib.CookieJar()
        ctx = ssl._create_unverified_context()
        opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx),urllib2.HTTPCookieProcessor(cj))
        r= opener.open('https://'+DEVICE_IP+'/')
        return opener
    
    def login_to_webgui(opener):
        print "Trying to Login to Controller..."
        login_url = 'https://'+DEVICE_IP+'/api/login'
        urldata = '{\"username\":\"unifi\",\"password\":\"percipia123\"}'
        r = opener.open(login_url, urldata)
        print "Logged in successfully"
    
    def add_extension (opener,account_id,mac,ext,roomno,name,pbx):
        url = 'https://'+DEVICE_IP+'/api/s/default/add/extension'
        urldata = {"sip_id":account_id,
                   "extension":ext,
                   "name":name,
                   "device_mac":mac,
                   "x_sip_username":ext,
                   "x_sip_password":PASSWORD,
                   "sip_proxy":"",
                   "sip_authname":"",
                   "sip_voicemail":GUEST_VOICE_MAIL,
                   "x_sip_server":pbx,
                   "x_sip_auth":"user",
                   "sip_enabled":"true",
                   "sip_locked":"true",
                   "sip_on_call_act":"0",
                   "sip_reg_exp":"60",
                   "sip_rtp_dscp":"46",
                   "sip_over_tcp":"false",
                   "sip_rtp_start_port":"4000",
                   "sip_rtp_port_range":"0",
                   "sip_msg_ind":"true",
                   "sip_timer_hdr":"true",
                   "sip_via_rw":"true",
                   "sip_contact_rw":"true",
                   "sip_sdp_rw":"false",
                   "sip_fwd_uri":"",
                   "sip_stun_enabled":"false",
                   "sip_ice_enabled":"false",
                   "sip_turn_enabled":"false",
                   "sip_turn_type":"UDP",
                   "sip_turn_server":"",
                   "sip_turn_username":"",
                   "sip_turn_password":"",
                   "sip_is_template":"false",
                   "sip_template":"",
                   "sip_dtmf_type":"1"}
        import json
        jj = json.dumps (urldata)
        opener.addheaders = [("Content-Type", "application/json; charset=utf-8")]
        opener.addheaders = [("Content-Length", len(jj))]
        respond_html = opener.open (url,jj)
        print "Extension "+ext+ " added successfully to Controller"
    
    def delete_all_ext (opener):
        url = 'https://'+DEVICE_IP+'/api/s/default/list/extension'
        respond_html = opener.open (url)
        data = respond_html.read()
        #print type (data)
        import json
        data_j = json.loads(data)
        #print data_j
        for i in range(0,len(data_j["data"])) :
            ext_id = data_j["data"][i]["_id"]            
            ext =  data_j["data"][i]["extension"]
            delete_ext (opener,ext,ext_id)
    
    def extension_id (opener,ext):
        url = 'https://'+DEVICE_IP+'/api/s/default/list/extension'
        respond_html = opener.open (url)
        data = respond_html.read()
        import json
        data_j = json.loads(data)
        if ext in data_j["data"][i]["extension"]:
            return data_j["data"][i]["_id"]
    
    def delete_ext (opener,ext,ext_id):
        url = 'https://'+DEVICE_IP+'/api/s/default/del/extension/'+ext_id
        try :
            respond_html = opener.open (url,{'':''}).read()
        except :
            pass
        print "Extension "+ext+" deleted!"
    
#-------------------------------------------------------------------



# ====================
# Main Function 
# ====================
import urllib2
import urllib
import ssl
import csv

DEVICE_IP = "10.100.200.9:9443"
#PBX_IP = "10.100.200.10"
PASSWORD = "percipia123"
GUEST_VOICE_MAIL = "*97"

opener = get_the_cookie()
login_to_webgui(opener)
delete_all_ext(opener)

"""
f = open('test.csv')
csv_f = csv.reader(f)
for row in csv_f:
    account_id = row[0]
    mac_ = row[1] 
    # 44D9E70570C1 ----Convert it to-----> 44:d9:e7:05:70:00
    mac = (mac_[0:2]+':'+mac_[2:4]+':'+mac_[4:6]+':'+mac_[6:8]+':'+mac_[8:10]+':'+mac_[10:12]).lower()
    ext = row[2]
    roomno = row[3]
    name = row[4]
    pbx = row[5]
    add_extension (opener,account_id,mac,ext,roomno,name,pbx)
"""