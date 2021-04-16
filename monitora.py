import os
import time
from datetime import datetime
import json
import speedtest   
  
  
def try_speed_test(now):
    date_test = do_speed_test()
    with open('output_test.txt', 'a') as file:
        file.write(json.dumps({
            "date": now.strftime("%d/%m/%Y %H:%M:%S"),
            "data": date_test    
        }, indent=4, sort_keys=True))
        file.close()
  
def do_speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    data = {}
    data["download"] = ((st.download()/1024)/1024)
    data["upload"] = ((st.upload()/1024)/1024)
    servernames =[]   
    st.get_servers(servernames)   
    data["ping"] = st.results.ping
    return data

def check_ping():
    hostname = "8.8.8.8"
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "1"
    else:
        pingstatus = "0"
    resp = ""
    if response == 256:
        resp = "Internet fora"
    elif response == 512:
        resp = "Desconectado wifi"
    else:
        resp = str(response)


    return pingstatus, resp

if __name__ == "__main__":
    start = datetime.now()
    # try_speed_test(start)
    while True:
        data = []
        with open('output_downtime.txt') as json_file:
            data = json.load(json_file)
        
        
        start_key = "start"
        end_key = "end"
        if len(data) > 0:
            sorted(data, key=lambda k: k[start_key]) 
        
        now = datetime.now()
        minutes_diff = (now - start).total_seconds() / 60.0
        if minutes_diff >= 60:
            try:
                try_speed_test(now)
            except Exception as e:
                pass
            start = now
            
        
        today = now.strftime("%d/%m/%Y %H:%M:%S")
        check = check_ping()
        resp = check[1]
        check = check[0]
        day = now.strftime("%d/%m/%Y")
        has_end = True
        if len(data) > 0:
            has_end = data[-1][end_key] != ""
        if has_end and check == "0":
            data.append({
                start_key: today,
                "check": check,
                end_key: "",
                "desc": resp
            })
        elif check == "1" and not has_end:
            data[-1][end_key] = today
            data[-1]["speedtest"] = do_speed_test()
            
        with open('output_downtime.txt', 'w') as file:
            file.write(json.dumps(data, indent=4, sort_keys=True))
            file.close()
        time.sleep(10)