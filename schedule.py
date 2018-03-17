#!/usr/bin/env python
import os
from datetime import datetime
import meetup.api
import pandas

key = os.environ['MEETUP_API_KEY']
client = meetup.api.Client(key)
group = client.GetGroup({'urlname': 'MadPython'})
events = client.GetEvents({'group_id': group.id, 'status': 'upcoming'})
data = pandas.DataFrame.from_records(events.results)
data.rename(columns={'name': 'event_name'}, inplace=True)
data['date'] = data.time.apply(
        lambda ms: datetime.fromtimestamp(ms/1000))
data['datef'] = data.date.apply(
        lambda dt: datetime.strftime(dt, '%a %b %d, %Y'))

event_names = data.apply(lambda r: f'* {r.datef}: [{r.event_name}]({r.event_url})', axis=1)
with open('README.md', 'w') as f:
    f.write('\n'.join(event_names.tolist()))
