from flask import Flask
import requests
from flask_cors import CORS, cross_origin
import json
import os
import time
import subprocess
app = Flask(__name__)
CORS(app)

@app.route("/pdf",methods=["POST"])
@cross_origin()
def pdf():
    
    ############# First_curl_commend ##########

    url = 'https://pdf-services.adobe.io/assets'

    header_one = {
        'X-API-Key': '8dcedc78c4e3472bafb0ae554a207fc1',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE2Nzk2NDM5NjE0MTVfNDY0MGVjZmItNTU5ZC00OTY1LTgzYzItNzA2NGIxN2EzY2RjX3VlMSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiI4ZGNlZGM3OGM0ZTM0NzJiYWZiMGFlNTU0YTIwN2ZjMSIsInVzZXJfaWQiOiJBMEUxM0RGODY0MUQ1NEZCMEE0OTVFRTRAdGVjaGFjY3QuYWRvYmUuY29tIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJBMEUxM0RGODY0MUQ1NEZCMEE0OTVFRTRAdGVjaGFjY3QuYWRvYmUuY29tIiwiY3RwIjozLCJmZyI6IlhKVExFWUFPRlBONU5ONEtFTVFWWkhRQTRRPT09PT09IiwibW9pIjoiMjM2MTIzY2MiLCJleHBpcmVzX2luIjoiODY0MDAwMDAiLCJjcmVhdGVkX2F0IjoiMTY3OTY0Mzk2MTQxNSIsInNjb3BlIjoib3BlbmlkLERDQVBJLEFkb2JlSUQsYWRkaXRpb25hbF9pbmZvLm9wdGlvbmFsQWdyZWVtZW50cyJ9.PmOQwll17RK6YivqyJtmye9Xc-ocEHx1VniHYISrNNA3pSuLcpOZNDoaTtu-7g1yka7dAyibFH_b3PkMQh_ik9hyOTr5N7DOFWLCo5PLZk84R7vz1xpyk7xpLBrXGD6Z4IDHjmzU9dQ6Cxl8F2Bg53kepZapPjfMT651Ah2jNMaNU1MMeUZM2WLkwEDo6cc69raslAzALAvVbzsbMW_kdQB_izx9kzCJCJlFrZfaF30EfSAAM2xtp2XHxkEOIg-zH2jvPjnWpsePzZkuhIJLCB1nYJxfrihPj_ZuEAn2nRn7j-ndbju09r4fIrUK_ezl1LjTS2hs8ECaSDGmsvUDRg',
        'Content-Type': 'application/json'
    }

    payload = {
        "mediaType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }

    first_curl_response = requests.post(url=url, headers=header_one, json=payload)
    location_path = json.loads(first_curl_response.text)
    
    ################## location_path_returns ##################
    
    uploadUri = location_path["uploadUri"]
    assetID = location_path["assetID"]
    
    header_two = {'Content-Type':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
    
    ############# Secound_curl_commend ##########
    
    data = open('document.docx', 'rb').read()
    secound_response = requests.put(url=uploadUri, headers=header_two, data=data)

    ######## Change_assetID #####
    with open("data.json","r") as file:
        jsonData = json.load(file)
        jsonData["assetID"]=assetID
    
    
    os.remove("data.json")
    with open("data.json", 'w') as f:
        json.dump(jsonData, f)
        
    ################## Third_curl_commend ##################

    upload_url = "https://pdf-services-ue1.adobe.io/operation/documentgeneration"
    
    
    with open("data.json","r") as file:
        updated_file = json.load(file)
    
    third_response = requests.post(url=upload_url, headers=header_one, json=updated_file)

    ############### forth_curl_commend ######
    
    location_url = third_response.headers["location"]

    header_two = {
        'X-API-Key': '8dcedc78c4e3472bafb0ae554a207fc1',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE2Nzk2NDM5NjE0MTVfNDY0MGVjZmItNTU5ZC00OTY1LTgzYzItNzA2NGIxN2EzY2RjX3VlMSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiI4ZGNlZGM3OGM0ZTM0NzJiYWZiMGFlNTU0YTIwN2ZjMSIsInVzZXJfaWQiOiJBMEUxM0RGODY0MUQ1NEZCMEE0OTVFRTRAdGVjaGFjY3QuYWRvYmUuY29tIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJBMEUxM0RGODY0MUQ1NEZCMEE0OTVFRTRAdGVjaGFjY3QuYWRvYmUuY29tIiwiY3RwIjozLCJmZyI6IlhKVExFWUFPRlBONU5ONEtFTVFWWkhRQTRRPT09PT09IiwibW9pIjoiMjM2MTIzY2MiLCJleHBpcmVzX2luIjoiODY0MDAwMDAiLCJjcmVhdGVkX2F0IjoiMTY3OTY0Mzk2MTQxNSIsInNjb3BlIjoib3BlbmlkLERDQVBJLEFkb2JlSUQsYWRkaXRpb25hbF9pbmZvLm9wdGlvbmFsQWdyZWVtZW50cyJ9.PmOQwll17RK6YivqyJtmye9Xc-ocEHx1VniHYISrNNA3pSuLcpOZNDoaTtu-7g1yka7dAyibFH_b3PkMQh_ik9hyOTr5N7DOFWLCo5PLZk84R7vz1xpyk7xpLBrXGD6Z4IDHjmzU9dQ6Cxl8F2Bg53kepZapPjfMT651Ah2jNMaNU1MMeUZM2WLkwEDo6cc69raslAzALAvVbzsbMW_kdQB_izx9kzCJCJlFrZfaF30EfSAAM2xtp2XHxkEOIg-zH2jvPjnWpsePzZkuhIJLCB1nYJxfrihPj_ZuEAn2nRn7j-ndbju09r4fIrUK_ezl1LjTS2hs8ECaSDGmsvUDRg'
    }
    
    with requests.Session() as s:
        final_response= s.get(url=location_url, headers=header_two)
    final_response.raise_for_status()
    print(final_response.json()["status"])
    print(final_response.__dict__) 
    print(final_response.request.__dict__)    
 
  
    return(location_path ) 
    
    
    



if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 5000
    app.run(HOST, PORT, debug=True)

