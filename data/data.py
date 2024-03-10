import requests
from pprint import pformat
import pandas as pd


datas = []

def getstation_data(station_id):

    station_id = "44t"
    param = "PM25,PM10,O3,CO,NO2,SO2,WS,TEMP,RH,WD"
    data_type = "hr"
    start_date = "2023-01-01"
    end_date = "2024-02-27"
    start_time = "00"
    end_time = "23"
    url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
    response = requests.get(url)
    response_json = response.json()
    # print(response_json["stations"])
    for data in response_json["stations"][0]["data"]:
        data["stationID"] = response_json["stations"][0]["stationID"]
        datas.append(data)

    pd_from_dict = pd.DataFrame.from_dict(datas)
    # print(pformat(pd_from_dict))
    # print(pd_from_dict)
    pd_from_dict.to_csv(f"C:\\Users\\ASUS\\Desktop\\241-152\\finalproject\\data\\air4thai{station_id}{start_date}{end_date}.csv", index=False)

def getstationid():
    stationids_url = "http://air4thai.com/forweb/getHistoryStation.php"
    response = requests.get(stationids_url)
    response_json = response.json()
    station_ids = [(i["ID"], i["Area"]) for i in response_json]
    # print(pformat(station_ids))
    return station_ids


if __name__ == "__main__":
    station_ids = getstationid()
    for i in station_ids[:4]:
        getstation_data(i[0])