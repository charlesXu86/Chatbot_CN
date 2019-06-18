## simple path with greet
* greet
  - utter_greet
* weather_address_date-time{"address": "上海", "date-time": "明天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## simple path
* weather_address_date-time{"address": "上海", "date-time": "明天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## address + date-time path with greet
* greet
  - utter_greet
* weather_address{"address": "上海"}
  - utter_ask_date-time
* weather_date-time{"date-time": "明天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## address + date-time path
* weather_address{"address": "上海"}
  - utter_ask_date-time
* weather_date-time{"date-time": "明天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## date-time + address path with greet
* greet
  - utter_greet
* weather_date-time{"date-time": "明天"}
  - utter_ask_address
* weather_address{"address": "上海"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## date-time + address path
* weather_date-time{"date-time": "明天"}
  - utter_ask_address
* weather_address{"address": "上海"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## None + date-time + address path
* weather
  - utter_ask_date-time
* weather_date-time{"date-time": "明天"}
  - utter_ask_address
* weather_address{"address": "上海"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## None + address + date-time path
* weather
  - utter_ask_date-time
* weather_address{"address": "上海"}
  - utter_ask_date-time
* weather_date-time{"date-time": "明天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## None + date-time + address path with greet
* greet
  - utter_greet
* weather
  - utter_ask_date-time
* weather_date-time{"date-time": "明天"}
  - utter_ask_address
* weather_address{"address": "上海"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## None + address + date-time path with greet
* greet
  - utter_greet
* weather
  - utter_ask_date-time
* weather_address{"address": "上海"}
  - utter_ask_date-time
* weather_date-time{"date-time": "明天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## simple path with change address
* greet
  - utter_greet
* weather_address_date-time{"address": "上海", "date-time": "明天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather
* weather_address{"address": "北京"} OR weather_date-time{"date-time": "明天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather
* weather_address{"address": "杭州"} OR weather_date-time{"date-time": "后天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather
* weather_address{"address": "南京"} OR weather_date-time{"date-time": "大后天"}
  - utter_working_on_it
  - action_report_weather
  - utter_report_weather

## say goodbye
* goodbye
  - utter_goodbye