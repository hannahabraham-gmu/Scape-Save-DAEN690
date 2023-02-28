import requests
import xml.dom.minidom

soc_code = "17-2051.00"
api_url = f"https://services.onetcenter.org/ws/mnm/careers/{soc_code}/technology"
api_key = "aWRlbnRpZnlpbmdfYWN0dWFsX3M6NDkyMmt5cQ=="

headers = {
    "Authorization": f"Basic {api_key}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(api_url, headers=headers)
dom=xml.dom.minidom.parseString(response.content)
pretty_xml = dom.toprettyxml(indent="  ", newl="\n")
print(pretty_xml)
