import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = 'aiEwC0TZqi7ZYksP4Ez0qAzTPI5xHSpS8P0ghG3IPyPg'
url = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/8f660912-fdc5-4d14-914a-e37d0141399a'

authenticator = IAMAuthenticator(apikey)
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)
tone_analyzer.set_service_url(url)

tone_analysis = tone_analyzer.tone(
    {'text': "Fuck this shit, im out"}, content_type='application/json').get_result()

print(json.dumps(tone_analysis, indent=4))
