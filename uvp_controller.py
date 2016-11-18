import urllib2
import urllib

class uvp_controller (object) :
    
    #Initialization of global varibles in class 
    def __init__(self):
        #Configuration Constants
        self.DEVICE_IP = "10.100.200.9:9443"
        self.PBX_IP = "10.100.200.10"
        self.PASSWORD = "percipia123"
        self.GUEST_VOICE_MAIL = "*97"
        self.opener = None
    
    def connect(self, ip):
        if ":" in ip :
            self.DEVICE_IP = ip
        else :
            self.DEVICE_IP = ip+":9443"
        self.opener = _get_the_cookie_and_ssl()
        
    def login(self,username,password):
        print "Trying to Login to Controller..."
        login_url = 'https://'+self.DEVICE_IP+'/api/login'
        urldata = '{\"username\":\"'+username+'\",\"password\":\"'+password+'\"}'
        r = self.opener.open(login_url, urldata)
        print r.read()
        print "Logged in successfully"
        
    
    #-------------------------------------------------------------------
    def _get_the_cookie_and_ssl (self):
        import cookielib
        import ssl
        cj = cookielib.CookieJar()
        ctx = ssl._create_unverified_context()
        opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx),urllib2.HTTPCookieProcessor(cj))
        r= opener.open('https://'+self.DEVICE_IP+'/')
        return opener   
    
    def add_extension (self,opener,account_id,mac,ext,roomno,name,pbx):
        url = 'https://'+self.DEVICE_IP+'/api/s/default/add/extension'
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
    
    def delete_all_ext (self,opener):
        url = 'https://'+self.DEVICE_IP+'/api/s/default/list/extension'
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
    
    def extension_id (self,opener,ext):
        url = 'https://'+self.DEVICE_IP+'/api/s/default/list/extension'
        respond_html = opener.open (url)
        data = respond_html.read()
        import json
        data_j = json.loads(data)
        if ext in data_j["data"][i]["extension"]:
            return data_j["data"][i]["_id"]
    
    def delete_ext (self,opener,ext,ext_id):
        url = 'https://'+self.DEVICE_IP+'/api/s/default/del/extension/'+ext_id
        try :
            respond_html = opener.open (url,{'':''}).read()
        except :
            pass
        print "Extension "+ext+" deleted!"
    
#-------------------------------------------------------------------


