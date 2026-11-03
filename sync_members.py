"""Import an authorized JSON group roster. No scraping or guessed membership."""
import json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path

url=os.environ.get('DGP_MEMBERS_FEED_URL','').strip()
if not url:
    print('DGP_MEMBERS_FEED_URL not configured; leaving members.json unchanged.')
    raise SystemExit(0)
if not url.startswith('https://'):
    raise SystemExit('Feed URL must use HTTPS')
with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AcademicGroupSite/1.0'}),timeout=25) as response:
    data=json.load(response)
if not isinstance(data,dict) or not isinstance(data.get('members'),list):
    raise SystemExit('Feed must be JSON object with members array')
roster=[]
for item in data['members']:
    if not isinstance(item,dict) or not isinstance(item.get('name'),str) or not item['name'].strip():
        raise SystemExit('Every member must have a nonempty name')
    member={'name':item['name'].strip(),'role':str(item.get('role','')),'institution':str(item.get('institution',''))}
    profile=item.get('profile_url','')
    if profile:
        if not isinstance(profile,str) or not profile.startswith('https://'):
            raise SystemExit('Profile URLs must use HTTPS')
        member['profile_url']=profile
    roster.append(member)
result={'updated_at':datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),'members':roster,'source':url}
Path(__file__).with_name('members.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Validated roster:',len(roster),'members')
