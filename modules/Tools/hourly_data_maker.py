weather_code_map = {
    "1000": "01",
    "1003": "02",
    "1006": "03",
    "1009": "03",
    "1030": "04",
    "1063": "09",
    "1066": "13",
    "1069": "13",
    "1072": "13",
    "1114": "13",
    "1117": "13",
    "1087": "11",
    "1135": "04",
    "1147": "04",
    "1150": "09",
    "1153": "10",
    "1168": "03",
    "1171": "03",
    "1180": "09",
    "1183": "09",
    "1186": "09",
    "1189": "10",
    "1192": "10",
    "1195": "10",
    "1198": "09",
    "1201": "09",
    "1204": "09",
    "1207": "09",
    "1210": "13",
    "1213": "13",
    "1216": "13",
    "1219": "13",
    "1222": "13",
    "1225": "13",
    "1237": "13",
    "1240": "10",
    "1243": "10",
    "1246": "10",
    "1249": "10",
    "1252": "10",
    "1255": "13",
    "1258": "13",
    "1261": "13",
    "1264": "13",
    "1273": "11",
    "1276": "11",
    "1279": "11",
    "1282": "11",
}

def make_hourly_data(data):
    hourly_data = {
        "icon_codes": [],
        "charts_height": [],
        "y_values": []
    }
    if data:
        forecast_day = data["forecast"]["forecastday"][0]
        min_value = round(forecast_day["day"]["mintemp_c"]/5)*5 - 10
        hourly_data["y_values"].append(min_value)
        for i in range(7):
            hourly_data["y_values"].append(min_value+5*(i+1))
        hourly_data["y_values"].reverse()
        for hour in forecast_day["hour"]:
            hourly_data["charts_height"].append((round(hour["temp_c"])-min_value)*3)
            code = hour["condition"]["code"]
            converted_code = weather_code_map[str(code)] + 'd' if hour["is_day"] == 1 else weather_code_map[str(code)]+'n'
            hourly_data["icon_codes"].append(converted_code)
        print(hourly_data)
    return hourly_data