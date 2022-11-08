###通过excel课表生成ios日历订阅文件

import pandas as pd
from datetime import date, datetime, timedelta, timezone

######################################################

XLSX_PATH = 'week11.xlsx'
ICAL_PATH = 'export.ics'

day_one = date(2022, 11, 7)



cols = { 2:1, 4:3, 5:3, 6:3, 7:3 }

######################################################

tz_shanghai=timezone(timedelta(hours=8), 'Asia/Shanghai')

df = pd.read_excel(XLSX_PATH)
denan = df.fillna('空')
class_all = denan.to_dict('list')
del class_all['FAP-W11']
del class_all['Unnamed: 1']
del class_all['Unnamed: 3']
#for k,v in class_all.items
for n in class_all:
    class_alls = []
    news_ids = []
    for id in class_all[n]:
        if id not in news_ids:
            news_ids.append(id)
    class_alls += news_ids
    class_alls_list = list(set(class_alls))

classes = class_alls_list
ical = open(ICAL_PATH, 'w')

ical.write('BEGIN:VCALENDAR\n')
for day_offset, col in enumerate(cols):

    times = df.loc[:, df.columns[cols[col]]].dropna()

    day = day_one + timedelta(days=day_offset)

    for index in df.loc[:, df.columns[col]].dropna().index:

        if any([cls for cls in classes if cls in df.loc[index, df.columns[col]]]):

            ical.write('BEGIN:VEVENT\n')

            term = df.loc[index, df.columns[col]].split('-')
            time = ''

            if (term.__len__() == 2):

                ical.write('SUMMARY:{}\n'.format(term[1]))

            if (term.__len__() == 3):

                ical.write('SUMMARY:{}\n'.format(term[0]))
                ical.write('LOCATION:{} {}\n'.format(term[2], term[1]))

            if (term.__len__() == 4):

                if 'class' in term[1].lower():
                    ical.write('SUMMARY:{}\n'.format(term[0]))
                    ical.write('LOCATION:{} {}\n'.format(term[3], term[2]))
                else:
                    ical.write('SUMMARY:{}\n'.format(term[1]))
                    ical.write('LOCATION:{} {}\n'.format(term[3], term[2]))

            for time_index in range(times.index.size):
                
                if times.index[time_index] > index:

                    time = times.loc[times.index[time_index - 1]].split('-')
                    break

            dtstart_list = time[0].split(':')
            dtend_list = time[1].split(':')

            dtstart = datetime(day.year, day.month, day.day, int(dtstart_list[0]), int(dtstart_list[1]), tzinfo=tz_shanghai)
            dtend = datetime(day.year, day.month, day.day, int(dtend_list[0]), int(dtend_list[1]), tzinfo=tz_shanghai)

            ical.write(f'DTSTART:{dtstart.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")}\n')
            ical.write(f'DTEND:{dtend.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")}\n')

            ical.write('END:VEVENT\n')

ical.write('END:VCALENDAR\n')
ical.close()