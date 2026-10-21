"""Add scoped, idempotent story annotations to the currently authored state map."""
from pathlib import Path
import copy
import json

SITE = Path(__file__).resolve().parents[1]
p = SITE / 'specs/05-symbol-map.json'
s = json.loads(p.read_text(encoding='utf-8'))
s['layer'] = [layer for layer in s['layer'] if not layer.get('name', '').startswith('story_')]
# Derive labels from the unchanged state data and retain the original encodings.
base = {
    'data': {'url': 'data/states.json'},
    'transform': [
        {'filter': "stateFocus == 'All states' ? (datum.code == 'NSW' || (width >= 400 && (datum.code == 'QLD' || datum.code == 'VIC'))) : datum.code == stateFocus"},
        {'calculate': "datum.code == 'QLD' ? 153 : datum.code == 'NSW' ? 156 : datum.code == 'VIC' ? 137 : datum.code == 'ACT' ? 156 : datum.code == 'TAS' ? 137 : datum.longitude", 'as': 'story_lon'},
        {'calculate': "datum.code == 'QLD' ? -15 : datum.code == 'NSW' ? -27 : datum.code == 'VIC' ? -43 : datum.code == 'ACT' ? -33 : datum.code == 'TAS' ? -40 : datum.latitude - 5", 'as': 'story_lat'},
        {'calculate': "datum.code == 'NSW' ? 'New South\\nWales' : datum.code == 'ACT' ? 'Australian Capital\\nTerritory' : datum.state", 'as': 'story_name'},
        {'calculate': "datum.story_name + '\\n' + (datum.visitors >= 1e6 ? format(datum.visitors / 1e6, '.1f') + 'm' : format(datum.visitors, ',')) + ' visits'", 'as': 'story_label'},
    ],
}
line = copy.deepcopy(base)
line.update(name='story_state_leaders', mark={'type':'rule','color':'#4E6078','strokeWidth':1}, encoding={
    'longitude':{'field':'longitude','type':'quantitative'}, 'latitude':{'field':'latitude','type':'quantitative'},
    'longitude2':{'field':'story_lon'},'latitude2':{'field':'story_lat'},
})
label = copy.deepcopy(base)
label.update(name='story_state_labels',mark={'type':'text','fontSize':14,'fontWeight':600,'lineHeight':17,'lineBreak':'\n','align':'center','baseline':'top','dy':{'expr': "datum.code == 'NSW' || datum.code == 'ACT' ? -59 : datum.code == 'QLD' || datum.code == 'TAS' ? -42 : 6"},'color':'#162B4D'},encoding={
    'longitude':{'field':'story_lon','type':'quantitative'},'latitude':{'field':'story_lat','type':'quantitative'},'text':{'field':'story_label'},
})
s['layer'].extend([line,label])
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(p)
