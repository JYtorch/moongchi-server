from django.test import TestCase
from pprint import pprint

# Create your tests here.
from justwatch import JustWatch

just_watch = JustWatch(country='KR')

results = just_watch.search_for_item(query='기생충')

# pprint(results)


def is_netflix(query):
    result = just_watch.search_for_item(query=query).get('items')
    if result:
        target = result[0]
        if target.get('title') == query:
            for item in target.get('offers'):
                if item.get('package_short_name') == 'nfx':
                    return True
    return False


    # result = just_watch.search_for_item(query=query).get('items')[0]
    # for item in just_watch.search_for_item(query=query).get('items')[0].get('offers'):
        # if item.get('package_short_name') == 'nfx':
        #     return True
    # return False

print(is_netflix('이런 바보같ㅇ느나ㅓㅗㅇ마너오ㅑㅁ농나어ㅜㅂ쟈웁자'))

print(is_netflix('기생충'))

print(is_netflix('베놈'))
