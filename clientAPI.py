import requests
URL_BASE = 'http://127.0.0.1:5000'



filename = 'C:/Users/vkalokyri/Desktop/testData.xlsx'
files = {'data_file': open(filename,'rb')}
credentials = {'username':'valia', 'password':'valia'}


# url = URL_BASE + '/getPatients/'
# r = requests.get(url, data=credentials)
# print(r.status_code)
# print(r.text)

# url = URL_BASE + '/getSeries/'
# r = requests.get(url, data=credentials)
# print(r.status_code)
# print(r.text)


# url = URL_BASE + '/getPatientByID/'
# r = requests.get(url, data=credentials, params={"id":"8732322741"})
# print(r.status_code)
# print(r.text)


# url = URL_BASE + '/getSeriesByID/'
# r = requests.get(url, data=credentials, params={"id":"t2_spc_rsl obl_Prostate"})
# print(r.status_code)
# print(r.text)


# url = URL_BASE + '/updatePatientByID/'
# r = requests.put(url, data=credentials, params={"id":"8732322741",  "attribute":"PatientAge","newValue":"63"})
# print(r.status_code)
# print(r.text)

# url = URL_BASE + '/updateSeriesByID/'
# r = requests.put(url, data=credentials, params={"id":"t2_spc_rst_axial obl_Pate",  "attribute":"ManufacturerModelName","newValue":"Skyra"})
# print(r.status_code)
# print(r.text)


# url = URL_BASE + '/deletePatientList/'
# r = requests.delete(url, data=credentials, params={"list":["8732322741"]})
# print(r.status_code)
# print(r.text)

url = URL_BASE + '/deleteAllSeries/'
r = requests.delete(url, data=credentials)
print(r.status_code)
print(r.text)

url = URL_BASE + '/deleteAllPatients/'
r = requests.delete(url, data=credentials)
print(r.status_code)
print(r.text)


url = URL_BASE + '/importData/'
r = requests.post(url, files=files, data=credentials)
print(r.status_code)
print(r.text)

# url = URL_BASE + '/deleteSeriesList/'
# r = requests.delete(url, data=credentials, params={"list":["LIghgghk"]})
# print(r.status_code)
# print(r.text)