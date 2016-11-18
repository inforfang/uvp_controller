import urllib2
import urllib

class pbx (object):
    def __init__(self,ip,voicemail):
        self.ip = ip
        self.voicemail = voicemail

class account (object):
    def __init__(self,account_no,name,extension,password,pbx_object):
        self.account_no = account_no
        self.extension = extension        
        self.pbx = pbx_object
        self.password = password
        self.name = name
        self._database_id = None
    
    
class phone (object):
    def __init__(self,model,mac_,account):
        self.model = model
        self.account = account
        if ":" not in mac_ :
            # 44D9E70570C1 ----Convert it to-----> 44:d9:e7:05:70:00
            self.mac_plain = mac_
            self.mac = (mac_[0:2]+':'+mac_[2:4]+':'+mac_[4:6]+':'+mac_[6:8]+':'+mac_[8:10]+':'+mac_[10:12]).lower()

class uvp_controller (object) :   
    #Initialization of global varibles in class 
    def __init__(self):
        #Configuration Constants
        self.ip = None
        self.opener = None
        self.data_j = None
    
    def connect(self, ip):
        if ":" in ip :
            self.ip = ip
        else :
            self.ip = ip+":9443"
        self.opener = self._get_the_cookie_and_ssl()
        
    def login(self,username,password):
        print "Trying to Login to Controller..."
        login_url = 'https://'+self.ip+'/api/login'
        urldata = '{\"username\":\"'+username+'\",\"password\":\"'+password+'\"}'
        r = self.opener.open(login_url, urldata)
        if "ok" in r.read():
            print "Logged in successfully"        
    
    #Internal Functions 
    #-------------------------------------------------------------------
    def _get_the_cookie_and_ssl (self):
        import cookielib
        import ssl
        cj = cookielib.CookieJar()
        ctx = ssl._create_unverified_context()
        opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx),urllib2.HTTPCookieProcessor(cj))
        r= opener.open('https://'+self.ip+'/')
        return opener
    
    def _post_to_delete (self,_database_id):
        url = 'https://'+self.ip+'/api/s/default/del/extension/'+_database_id
        try :
            respond_html = self.opener.open (url,{'':''}).read()
        except :
            pass
      
    def _find_database_id_for_extension(self,ext):
        url = 'https://'+self.ip+'/api/s/default/list/extension'
        respond_html = self.opener.open (url)
        data = respond_html.read()
        import json
        data_j = json.loads(data)
        for i in range(0,len(data_j["data"])) :
            if ext in data_j["data"][i]["extension"]:
                return data_j["data"][i]["_id"]
    
    def _find_device_mac_by_ext (self,ext):
        url = 'https://'+self.ip+'/api/s/default/list/extension'
        respond_html = self.opener.open (url)
        data = respond_html.read()
        import json
        data_j = json.loads(data)
        for i in range(0,len(data_j["data"])) :
            if ext in data_j["data"][i]["extension"]:
                return data_j["data"][i]["device_mac"]
            
    def _update_ext_info(self,_device_id,urldata):
        url = 'https://'+self.ip+'/api/s/default/upd/device/'+_device_id
        #print url
        import json
        jj = json.dumps (urldata)
        opener = self.opener
        opener.addheaders = [("Content-Type", "application/json; charset=utf-8")]
        opener.addheaders = [("Content-Length", len(jj))]
        #try : 
        respond_html = opener.open (url,jj)
        #except :
        #    pass  
    
    def _find_device_id_from_mac_address(self,mac):
        url = 'https://'+self.ip+'/api/s/default/stat/device'
        respond_html = self.opener.open (url)
        data = respond_html.read()
        import json
        data_j = json.loads(data)
        for i in range(0,len(data_j["data"])) :            
            if mac in data_j["data"][i]["mac"]:
                return data_j["data"][i]["_id"]
            
    def _update_device_data (self):
        url = 'https://'+self.ip+'/api/s/default/stat/device'
        respond_html = self.opener.open (url)
        data = respond_html.read()
        import json
        data_j = json.loads(data)
        self.device_data = data_j
    
    def _update_extension_data(self):
        url = 'https://'+self.ip+'/api/s/default/list/extension'
        respond_html = self.opener.open (url)
        data = respond_html.read()
        import json
        data_j = json.loads(data)
        self.extension_data = data_j
        
    #-------------------------------------------------------------------
     
    # Functions  
    #-------------------------------------------------------------------  
    def add_phone(self, phone):
        url = 'https://'+self.ip+'/api/s/default/add/extension'
        urldata = {"sip_id":phone.account.account_no,
                   "extension":phone.account.extension,
                   "name":phone.account.name,
                   "device_mac":phone.mac,
                   "x_sip_username":phone.account.extension,
                   "x_sip_password":phone.account.password,
                   "sip_proxy":"",
                   "sip_authname":"",
                   "sip_voicemail":phone.account.pbx.voicemail,
                   "x_sip_server":phone.account.pbx.ip,
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
        opener = self.opener
        opener.addheaders = [("Content-Type", "application/json; charset=utf-8")]
        opener.addheaders = [("Content-Length", len(jj))]
        try : 
            respond_html = opener.open (url,jj)
            print "Extension "+phone.account.extension+ " added successfully to Controller"    
        except :
            print "Warning => Extension "+phone.account.extension+ " is existing on Controller"

    def delete_extension (self,extension):
        temp_database_id = self._find_database_id_for_extension(extension)
        self._post_to_delete (temp_database_id)
        print "Extension "+extension+" deleted!"
        
    def delete_account (self,account):
        if account._database_id == None :
            account._database_id = self._find_database_id_for_extension (account.extension)
        self._post_to_delete (account._database_id)
        print "Account "+account.name+" deleted!"
        
    def clear_extension_list (self):        
        url = 'https://'+self.ip+'/api/s/default/list/extension'
        respond_html = self.opener.open (url)
        data = respond_html.read()
        import json
        data_j = json.loads(data)
        for i in range(0,len(data_j["data"])) :
            ext =  data_j["data"][i]["extension"]
            self.delete_extension (ext)
    
    def set_alias_by_extension(self,ext,alias):
        mac = self._find_device_mac_by_ext (ext)
        self.set_alias_by_mac(mac,alias)
    
    def set_alias_by_mac(self,mac,alias):
        mac = mac.lower()
        if mac != None and mac != "":
            temp_database_id = self._find_device_id_from_mac_address(mac)
            if temp_database_id != None : 
                urldata = {"name":alias}
                self._update_ext_info(temp_database_id,urldata)
                print "Alias set to "+alias+" for Mac "+mac
            else :
                print "No Device ("+mac+") found on controller!"
        else :
            print "No extension ("+ext+") found / No Devices associated to this extension"