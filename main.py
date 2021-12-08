import json
import os
from enum import Enum

import boto3 as boto3
import requests


class AirLevel(Enum):
    NA = "No Data"
    Good = "Good"
    Fair = "Fair"
    Moderate = "Moderate"
    Poor = "Poor"
    VeryPoor = "Very Poor"
    ExtremelyPoor = "Extremely Poor"


def is_dangerous(level: AirLevel):
    return level not in [AirLevel.NA, AirLevel.Good, AirLevel.Fair]


def get_avg_data(avg: int):
    if avg == -1:
        return "No current data; sensor is disconnected", AirLevel.NA
    elif avg <= 10:
        return "<b>0-10: Good.</b>%0a%0aThe air quality is good. Enjoy your usual outdoor activities.", AirLevel.Good
    elif avg <= 20:
        return "<b>10-20: Fair.</b>%0a%0aEnjoy your usual outdoor activities.", AirLevel.Fair
    elif avg <= 25:
        return "<b>20-25: Moderate.</b>%0a%0aEnjoy your usual outdoor activities.%0a" \
               "Sensitive groups should consider reducing intense outdoor activities, if you experience symptoms.", \
               AirLevel.Moderate
    elif avg <= 50:
        return "<b>25-50: Poor.</b>%0a%0aConsider reducing intense activities outdoors, " \
               "if you experience symptoms such as sore eyes, a cough or sore throat.%0a" \
               "Sensitive groups should consider reducing physical activities, particularly outdoors, " \
               "especially if you experience symptoms.", AirLevel.Poor
    elif avg <= 75:
        return "<b>50-75: Very Poor.</b>%0a%0aConsider reducing intense activities outdoors, " \
               "if you experience symptoms such as sore eyes, a cough or sore throat.%0a" \
               "Sensitive groups should reduce physical activities, particularly outdoors, " \
               "especially if you experience symptoms.", AirLevel.VeryPoor
    elif avg > 75:
        return "<b>over 75! Extremely Poor.</b>%0a%0aReduce physical activities outdoors.%0a" \
               "Sensitive groups should avoid physical activities outdoors.", AirLevel.ExtremelyPoor
    else:
        raise RuntimeError(f"Error - unknown value: {avg}")


def execute(events):
    sid = events.get("SENSOR_ID") or os.environ["SENSOR_ID"]
    assert sid, "Missing SENSOR_ID env"

    bot_api_key = events.get("TELEGRAM_BOT_API_KEY") or os.environ["TELEGRAM_BOT_API_KEY"]
    assert bot_api_key, "Missing TELEGRAM_BOT_API_KEY env"

    channel_name = events.get("TELEGRAM_CHANNEL_NAME") or os.environ["TELEGRAM_CHANNEL_NAME"]
    assert channel_name, "Missing TELEGRAM_CHANNEL_NAME env"

    # get sensor data
    sensor_data = requests.get(f"https://www.purpleair.com/json?show={sid}")
    sensor_data.raise_for_status()

    # find PM2.5 avg over all returned channels
    results = sensor_data.json()["results"]
    total = -1
    for result in results:
        total += float(result["PM2_5Value"])
    avg = int(round(total / len(results))) if total >= 0 else -1

    # retrieve msg & level for current avg
    (msg, level) = get_avg_data(avg)

    # retrieve last exec level
    ssm_client = boto3.client('ssm')
    param_name = "purpleair_push_last_avg"
    try:
        stored_param = ssm_client.get_parameter(Name=param_name)
        (_, last_level) = get_avg_data(int(stored_param["Parameter"]["Value"]))
    except Exception as e:
        if e.__class__.__name__ == "ParameterNotFound":
            last_level = None
        else:
            raise e

    if last_level and last_level == level:
        return f"Nothing Changed, avg: {avg}, level: {level}"

    # notify when moving between is_dangerous states (e.g. no reason to notify between "poor" and "extremely poor"),
    # unless it's N/A which shouldn't trigger at all
    should_notify = level != AirLevel.NA and (
        (last_level != AirLevel.NA and is_dangerous(last_level) != is_dangerous(level)) if last_level
        else is_dangerous(level)
    )

    # push msg to telegram channel
    push_url = f"https://api.telegram.org/bot{bot_api_key}/sendMessage" \
               f"?chat_id={channel_name}" \
               f"&text={msg}" \
               f"&disable_notification={not should_notify}" \
               f"&parse_mode=HTML"
    push_result = requests.get(push_url)
    push_result.raise_for_status()

    # store new avg
    ssm_client.put_parameter(Name=param_name, Value=str(avg), Type='String', Overwrite=True)

    return f"Success! new avg: {avg}, new level: {level}"


def lambda_handler(event, context):
    lambda_call_result = execute(event)
    print(lambda_call_result)
    return {
        'statusCode': 200,
        'body': json.dumps(lambda_call_result)
    }


if __name__ == '__main__':
    main_call_result = execute({})
    print(main_call_result)
