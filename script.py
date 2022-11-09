import os
import sys
from pathlib import Path
import requests
from urllib.parse import urlparse

arg_len = len(sys.argv)
if arg_len < 2 :
    raise Exception("URL not provided to script")

url = sys.argv[1]

domain = urlparse(url).netloc

file_name = Path("report_of_" + domain + ".txt")
file_name.touch(exist_ok=True)
report_file = open(file_name, "w+", encoding="utf-8")
report_file.write(f"\n")
report_file.write("Analysis of " + url + f"\n")

class Call:
  method = "undefined"  #attribute 1
  response = ""  #attribute 2

  def __init__(self,method,response): 
          self.method = method
          self.response = response

successful_calls = []

def check_success(response, method, successful_calls):
    if response.status_code != 404:
        successful_calls.append(Call(method, response))

def get_content_type(response):
    if response.headers["Content-Type"] is None:
        return "No Content-Type set"
    else:
        return response.headers["Content-Type"]

#Check if GET request possible
get_response = requests.get(url)
check_success(get_response, "GET", successful_calls)

#Check if POST request possible
post_response = requests.post(url)
check_success(post_response, "POST", successful_calls)

#Check if PUT request possible
put_response = requests.put(url)
check_success(put_response, "PUT", successful_calls)

#Check if DELETE request possible
delete_response = requests.delete(url)
check_success(delete_response, "DELETE", successful_calls)

#Check if OPTIONS request possible
options_response = requests.options(url)
check_success(options_response, "OPTIONS", successful_calls)

#Check if PATCH request possible
patch_response = requests.patch(url)
check_success(patch_response, "PATCH", successful_calls)

if len(successful_calls) < 1:
    report_file.write("No successful calls to provided URL")
else:
    report_file.write("Sucessful calls:" + f"\n")
    for success_call in successful_calls:

        call_folder = "./" + domain + "_" + success_call.method
        if  not os.path.exists(call_folder):
            os.mkdir(call_folder)

        file_name_string = call_folder + "/" + domain + "_" + success_call.method + "_response.txt"
        Path(file_name).touch(exist_ok=True)
        report_file.write(success_call.method + f"\n")
        report_file.write("Response received in: " + str(success_call.response.elapsed.total_seconds()) + " seconds" + f"\n")
        report_file.write("Content-Type is: " + get_content_type(success_call.response) + f"\n")
        report_file.write("Check response and headers at: "+ call_folder + f"\n")

        response_file = open(file_name_string,"w+", encoding="utf-8")
        response_file.write(success_call.response.text)
        response_file.close()
       
        response_header_file_name = call_folder + "/" + domain + "_" + success_call.method + "_headers.txt"
        Path(response_header_file_name).touch(exist_ok=True)
        response_header_file = open(response_header_file_name, "w+", encoding="utf-8")
        response_header_file.write(str(success_call.response.headers))
        response_header_file.close()

report_file.close()