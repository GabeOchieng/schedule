#!/usr/bin/env python
import os
import meetup.api
import pandas
import pypandoc

key = os.environ['MEETUP_API_KEY']
client = meetup.api.Client(key)
group = client.GetGroup({'urlname': 'MadPython'})
events = client.GetEvents({'group_id': group.id, 'status': 'past'})
data = pandas.DataFrame.from_records(events.results)
data.rename(columns={'name': 'event_name'}, inplace=True)
event_names = data.apply(lambda r: f'* [{r.event_name}]({r.event_url})', axis=1)
with open('README.md', 'w') as f:
    f.write('\n'.join(event_names.tolist()))
