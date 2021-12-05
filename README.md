# purpleair-telegram-push
Push PurpleAir sensor updates to a telegram channel

___
### Expected environment variables:
| Key   |      Description      | 
|----------|:-------------:|
| SENSOR_ID |  PurpleAir sensor ID |
| TELEGRAM_BOT_API_KEY |    Telegram BOT API Key    |
| TELEGRAM_CHANNEL_NAME | Channel name (in @channel_name format) |

### AWS credentials:
Execute using an AWS profile/role with SSM read/write permissions,
or modify the following line and add your api access key/secret/token:
```python
# replace
ssm_client = boto3.client('ssm')

# with 
ssm_client = boto3.client('ssm',
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key
                          (or aws_session_token=token))
```