PS D:\UserData\Desktop\Assistant\VoiceAssistant> python -u "d:\UserData\Desktop\Assistant\VoiceAssistant\test_intent_router.py"
================================================================================
INPUT:
Hi, how are you?

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"greeting","slots":"Hi, how are you?"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'greeting', 'slots': 'Hi, how are you?'}
[ROUTE] conversation -> passing to main LLM: "Hi, how are you?"

DISPATCH RESULT:
None
================================================================================
INPUT:
Come on.

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"greeting","slots":"none"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'greeting', 'slots': 'none'}
[ROUTE] conversation -> passing to main LLM: "Come on."

DISPATCH RESULT:
None
================================================================================
INPUT:
Tell me something interesting.

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"inform","slots":"interesting fact"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'inform', 'slots': 'interesting fact'}
[ROUTE] conversation -> passing to main LLM: "Tell me something interesting."

DISPATCH RESULT:
None
================================================================================
INPUT:
I feel a bit lonely today.

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"greeting","slots":"feels lonely today"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'greeting', 'slots': 'feels lonely today'}
[ROUTE] conversation -> passing to main LLM: "I feel a bit lonely today."

DISPATCH RESULT:
None
================================================================================
INPUT:
What day is it today?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"time","action":"date_enquiry","slots":"today"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'time', 'action': 'date_enquiry', 'slots': 'today'}
[ROUTE] task -> time -> date_enquiry

DISPATCH RESULT:
(filler) date enquiry handled — action=date_enquiry
================================================================================
INPUT:
What's the time right now?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"time","action":"date_enquiry","slots":"time"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'time', 'action': 'date_enquiry', 'slots': 'time'}
[ROUTE] task -> time -> date_enquiry

DISPATCH RESULT:
(filler) date enquiry handled — action=date_enquiry
================================================================================
INPUT:
What month is this?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"time","action":"date_enquiry","slots":"current month"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'time', 'action': 'date_enquiry', 'slots': 'current month'}
[ROUTE] task -> time -> date_enquiry

DISPATCH RESULT:
(filler) date enquiry handled — action=date_enquiry
================================================================================
INPUT:
Remind me to take my tablets at 8 PM.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"take tablets at 8 PM"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'reminder', 'action': 'set_reminder', 'slots': 'take tablets at 8 PM'}
[ROUTE] task -> reminder -> set_reminder -> slots: take tablets at 8 PM

DISPATCH RESULT:
(filler) set a reminder handled — slots=take tablets at 8 PM
================================================================================
INPUT:
Set a reminder to call my daughter tomorrow morning.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"call daughter tomorrow morning"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'reminder', 'action': 'set_reminder', 'slots': 'call daughter tomorrow morning'}
[ROUTE] task -> reminder -> set_reminder -> slots: call daughter tomorrow morning

DISPATCH RESULT:
(filler) set a reminder handled — slots=call daughter tomorrow morning
================================================================================
INPUT:
Don't let me forget my doctor's appointment on Friday.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"event","action":"set_reminder","slots":"doctor\'s appointment on Friday"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'event', 'action': 'set_reminder', 'slots': "doctor's appointment on Friday"}
[ROUTE] task -> event -> set_reminder -> slots: doctor's appointment on Friday

DISPATCH RESULT:
(filler) marked an event — action=set_reminder, slots=doctor's appointment on Friday
================================================================================
INPUT:
Add milk to my shopping list.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"shopping","action":"add_item","slots":"milk"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'shopping', 'action': 'add_item', 'slots': 'milk'}
[ROUTE] task -> shopping -> add_item -> slots: milk

DISPATCH RESULT:
(filler) shopping list handled — action=add_item, slots=milk
================================================================================
INPUT:
Remove rice from the list.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"shopping","action":"remove_item","slots":"rice"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'shopping', 'action': 'remove_item', 'slots': 'rice'}
[ROUTE] task -> shopping -> remove_item -> slots: rice

DISPATCH RESULT:
(filler) shopping list handled — action=remove_item, slots=rice
================================================================================
INPUT:
What's on my shopping list?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"shopping","action":"view_shopping_list","slots":"shopping list"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'shopping', 'action': 'view_shopping_list', 'slots': 'shopping list'}
[ROUTE] task -> shopping -> view_shopping_list -> slots: shopping list

DISPATCH RESULT:
(filler) shopping list handled — action=view_shopping_list, slots=shopping list
================================================================================
INPUT:
What appointments do I have next week?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"event","action":"query_events","slots":"next week"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'event', 'action': 'query_events', 'slots': 'next week'}
[ROUTE] task -> event -> query_events -> slots: next week

DISPATCH RESULT:
(filler) marked an event — action=query_events, slots=next week
================================================================================
INPUT:
Mark that I have a dentist visit on Monday.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"event","action":"add_event","slots":"dentist visit on Monday"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'event', 'action': 'add_event', 'slots': 'dentist visit on Monday'}
[ROUTE] task -> event -> add_event -> slots: dentist visit on Monday

DISPATCH RESULT:
(filler) marked an event — action=add_event, slots=dentist visit on Monday
================================================================================
INPUT:
Do I have anything planned this weekend?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"event","action":"query_events","slots":"this weekend"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'event', 'action': 'query_events', 'slots': 'this weekend'}
[ROUTE] task -> event -> query_events -> slots: this weekend

DISPATCH RESULT:
(filler) marked an event — action=query_events, slots=this weekend
================================================================================
INPUT:
What's in the news today?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"news","action":"query_news","slots":"today"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'news', 'action': 'query_news', 'slots': 'today'}
[ROUTE] task -> news -> query_news

DISPATCH RESULT:
(filler) news headlines handled
================================================================================
INPUT:
Tell me today's headlines.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"news","action":"get_headlines","slots":"today"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'news', 'action': 'get_headlines', 'slots': 'today'}
[ROUTE] task -> news -> get_headlines

DISPATCH RESULT:
(filler) news headlines handled
================================================================================
INPUT:
I fell down and my leg hurts.

========== ROUTER RAW ==========
'{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"fell down, leg pain"}'
=================================


CLASSIFIED:
{'intent': 'emergency', 'task_category': 'none', 'action': 'emergency_alert', 'slots': 'fell down, leg pain'}
[ROUTE] EMERGENCY triggered -> slots: fell down, leg pain

DISPATCH RESULT:
I'm alerting your emergency contact right now. Stay where you are.
================================================================================
INPUT:
I'm having chest pain.

========== ROUTER RAW ==========
'{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"chest pain"}'
=================================


CLASSIFIED:
{'intent': 'emergency', 'task_category': 'none', 'action': 'emergency_alert', 'slots': 'chest pain'}
[ROUTE] EMERGENCY triggered -> slots: chest pain

DISPATCH RESULT:
I'm alerting your emergency contact right now. Stay where you are.
================================================================================
INPUT:
Help me, I can't breathe properly.

========== ROUTER RAW ==========
'{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"can\'t breathe properly"}'
=================================


CLASSIFIED:
{'intent': 'emergency', 'task_category': 'none', 'action': 'emergency_alert', 'slots': "can't breathe properly"}
[ROUTE] EMERGENCY triggered -> slots: can't breathe properly

DISPATCH RESULT:
I'm alerting your emergency contact right now. Stay where you are.
================================================================================
INPUT:
Good morning, did you sleep well?

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"greeting","slots":"good morning, did you sleep well?"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'greeting', 'slots': 'good morning, did you sleep well?'}
[ROUTE] conversation -> passing to main LLM: "Good morning, did you sleep well?"

DISPATCH RESULT:
None
================================================================================
INPUT:
I'm bored, talk to me for a bit.

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"small_talk","slots":"bored"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'small_talk', 'slots': 'bored'}
[ROUTE] conversation -> passing to main LLM: "I'm bored, talk to me for a bit."

DISPATCH RESULT:
None
================================================================================
INPUT:
Do you think it will rain later?

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"weather_check","slots":"weather"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'weather_check', 'slots': 'weather'}
[ROUTE] conversation -> passing to main LLM: "Do you think it will rain later?"

DISPATCH RESULT:
None
================================================================================
INPUT:
What's your favourite season?

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"greeting","slots":"favourite season"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'greeting', 'slots': 'favourite season'}
[ROUTE] conversation -> passing to main LLM: "What's your favourite season?"

DISPATCH RESULT:
None
================================================================================
INPUT:
I miss my late husband sometimes.

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"greeting","slots":"missed late husband"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'greeting', 'slots': 'missed late husband'}
[ROUTE] conversation -> passing to main LLM: "I miss my late husband sometimes."

DISPATCH RESULT:
None
================================================================================
INPUT:
You're a good listener.

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"greeting","slots":"none"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'greeting', 'slots': 'none'}
[ROUTE] conversation -> passing to main LLM: "You're a good listener."

DISPATCH RESULT:
None
================================================================================
INPUT:
Sing me a little tune.

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"none","action":"song_request","slots":"sing a little tune"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'none', 'action': 'song_request', 'slots': 'sing a little tune'}
[ROUTE] conversation -> passing to main LLM: "Sing me a little tune."

DISPATCH RESULT:
None
================================================================================
INPUT:
How many days left until Sunday?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"time","action":"date_enquiry","slots":"days until Sunday"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'time', 'action': 'date_enquiry', 'slots': 'days until Sunday'}
[ROUTE] task -> time -> date_enquiry

DISPATCH RESULT:
(filler) date enquiry handled — action=date_enquiry
================================================================================
INPUT:
Is it still morning or afternoon now?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"time","action":"date_enquiry","slots":"current time"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'time', 'action': 'date_enquiry', 'slots': 'current time'}
[ROUTE] task -> time -> date_enquiry

DISPATCH RESULT:
(filler) date enquiry handled — action=date_enquiry
================================================================================
INPUT:
What year are we in?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"time","action":"date_enquiry","slots":"current year"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'time', 'action': 'date_enquiry', 'slots': 'current year'}
[ROUTE] task -> time -> date_enquiry

DISPATCH RESULT:
(filler) date enquiry handled — action=date_enquiry
================================================================================
INPUT:
How long ago was yesterday?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"time","action":"date_enquiry","slots":"yesterday"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'time', 'action': 'date_enquiry', 'slots': 'yesterday'}
[ROUTE] task -> time -> date_enquiry

DISPATCH RESULT:
(filler) date enquiry handled — action=date_enquiry
================================================================================
INPUT:
Ping me when it's time for my insulin shot.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"insulin shot time"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'reminder', 'action': 'set_reminder', 'slots': 'insulin shot time'}
[ROUTE] task -> reminder -> set_reminder -> slots: insulin shot time

DISPATCH RESULT:
(filler) set a reminder handled — slots=insulin shot time
================================================================================
INPUT:
I need to remember to water the plants every evening.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"water plants every evening"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'reminder', 'action': 'set_reminder', 'slots': 'water plants every evening'}
[ROUTE] task -> reminder -> set_reminder -> slots: water plants every evening

DISPATCH RESULT:
(filler) set a reminder handled — slots=water plants every evening
================================================================================
INPUT:
Nudge me before my grandson's birthday next month.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"nudge before grandson\'s birthday next month"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'reminder', 'action': 'set_reminder', 'slots': "nudge before grandson's birthday next month"}
[ROUTE] task -> reminder -> set_reminder -> slots: nudge before grandson's birthday next month

DISPATCH RESULT:
(filler) set a reminder handled — slots=nudge before grandson's birthday next month
================================================================================
INPUT:
Make sure I don't miss my physiotherapy session.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"physiotherapy session"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'reminder', 'action': 'set_reminder', 'slots': 'physiotherapy session'}
[ROUTE] task -> reminder -> set_reminder -> slots: physiotherapy session

DISPATCH RESULT:
(filler) set a reminder handled — slots=physiotherapy session
================================================================================
INPUT:
I'm running low on sugar, note that down.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"shopping","action":"add_item","slots":"sugar"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'shopping', 'action': 'add_item', 'slots': 'sugar'}
[ROUTE] task -> shopping -> add_item -> slots: sugar

DISPATCH RESULT:
(filler) shopping list handled — action=add_item, slots=sugar
================================================================================
INPUT:
Take rice off whatever I need to buy.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"shopping","action":"add_item","slots":"rice"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'shopping', 'action': 'add_item', 'slots': 'rice'}
[ROUTE] task -> shopping -> add_item -> slots: rice

DISPATCH RESULT:
(filler) shopping list handled — action=add_item, slots=rice
================================================================================
INPUT:
We need more coconut oil at home.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"shopping","action":"add_item","slots":"coconut oil"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'shopping', 'action': 'add_item', 'slots': 'coconut oil'}
[ROUTE] task -> shopping -> add_item -> slots: coconut oil

DISPATCH RESULT:
(filler) shopping list handled — action=add_item, slots=coconut oil
================================================================================
INPUT:
What all do I still need to pick up from the store?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"shopping","action":"list_items","slots":"items to pick up"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'shopping', 'action': 'list_items', 'slots': 'items to pick up'}
[ROUTE] task -> shopping -> list_items -> slots: items to pick up

DISPATCH RESULT:
(filler) shopping list handled — action=list_items, slots=items to pick up
================================================================================
INPUT:
Put it in my calendar that Ravi is visiting on Tuesday.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"event","action":"add_event","slots":"Ravi visiting on Tuesday"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'event', 'action': 'add_event', 'slots': 'Ravi visiting on Tuesday'}
[ROUTE] task -> event -> add_event -> slots: Ravi visiting on Tuesday

DISPATCH RESULT:
(filler) marked an event — action=add_event, slots=Ravi visiting on Tuesday
================================================================================
INPUT:
Anything scheduled for tomorrow?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"event","action":"query_events","slots":"tomorrow"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'event', 'action': 'query_events', 'slots': 'tomorrow'}
[ROUTE] task -> event -> query_events -> slots: tomorrow

DISPATCH RESULT:
(filler) marked an event — action=query_events, slots=tomorrow
================================================================================
INPUT:
I have a checkup coming up, note the date as the 14th.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"checkup on 14th"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'reminder', 'action': 'set_reminder', 'slots': 'checkup on 14th'}
[ROUTE] task -> reminder -> set_reminder -> slots: checkup on 14th

DISPATCH RESULT:
(filler) set a reminder handled — slots=checkup on 14th
================================================================================
INPUT:
Am I free this Saturday?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"time","action":"date_enquiry","slots":"Saturday"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'time', 'action': 'date_enquiry', 'slots': 'Saturday'}
[ROUTE] task -> time -> date_enquiry

DISPATCH RESULT:
(filler) date enquiry handled — action=date_enquiry
================================================================================
INPUT:
What's happening in the world today?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"news","action":"news_headlines","slots":"today"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'news', 'action': 'news_headlines', 'slots': 'today'}
[ROUTE] task -> news -> news_headlines

DISPATCH RESULT:
(filler) news headlines handled
================================================================================
INPUT:
Anything important going on that I should know about?

========== ROUTER RAW ==========
'{"intent":"task","task_category":"event","action":"query_events","slots":"nothing"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'event', 'action': 'query_events', 'slots': 'nothing'}
[ROUTE] task -> event -> query_events -> slots: nothing

DISPATCH RESULT:
(filler) marked an event — action=query_events, slots=nothing
================================================================================
INPUT:
Catch me up on current events.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"news","action":"current_events","slots":"none"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'news', 'action': 'current_events', 'slots': 'none'}
[ROUTE] task -> news -> current_events

DISPATCH RESULT:
(filler) news headlines handled
================================================================================
INPUT:
Everything is spinning and I feel like I might pass out.

========== ROUTER RAW ==========
'{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"feeling dizzy, might pass out"}'
=================================


CLASSIFIED:
{'intent': 'emergency', 'task_category': 'none', 'action': 'emergency_alert', 'slots': 'feeling dizzy, might pass out'}
[ROUTE] EMERGENCY triggered -> slots: feeling dizzy, might pass out

DISPATCH RESULT:
I'm alerting your emergency contact right now. Stay where you are.
================================================================================
INPUT:
There's blood coming from my arm, quite a lot.

========== ROUTER RAW ==========
'{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"blood from arm, quite a lot"}'
=================================


CLASSIFIED:
{'intent': 'emergency', 'task_category': 'none', 'action': 'emergency_alert', 'slots': 'blood from arm, quite a lot'}
[ROUTE] EMERGENCY triggered -> slots: blood from arm, quite a lot

DISPATCH RESULT:
I'm alerting your emergency contact right now. Stay where you are.
================================================================================
INPUT:
I think something is seriously wrong, I can't move my left side.

========== ROUTER RAW ==========
'{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"left side unable to move"}'
=================================


CLASSIFIED:
{'intent': 'emergency', 'task_category': 'none', 'action': 'emergency_alert', 'slots': 'left side unable to move'}
[ROUTE] EMERGENCY triggered -> slots: left side unable to move

DISPATCH RESULT:
I'm alerting your emergency contact right now. Stay where you are.
================================================================================
INPUT:
The pain is unbearable, I don't know what to do.

========== ROUTER RAW ==========
'{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"unbearable pain, fall"}'
=================================


CLASSIFIED:
{'intent': 'emergency', 'task_category': 'none', 'action': 'emergency_alert', 'slots': 'unbearable pain, fall'}
[ROUTE] EMERGENCY triggered -> slots: unbearable pain, fall

DISPATCH RESULT:
I'm alerting your emergency contact right now. Stay where you are.
================================================================================
INPUT:
Remind me what day my son's flight lands.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"reminder","action":"set_reminder","slots":"son\'s flight landing day"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'reminder', 'action': 'set_reminder', 'slots': "son's flight landing day"}
[ROUTE] task -> reminder -> set_reminder -> slots: son's flight landing day

DISPATCH RESULT:
(filler) set a reminder handled — slots=son's flight landing day
================================================================================
INPUT:
I bought vegetables today, add tomatoes to next week's list.

========== ROUTER RAW ==========
'{"intent":"task","task_category":"shopping","action":"add_item","slots":"tomatoes"}'
=================================


CLASSIFIED:
{'intent': 'task', 'task_category': 'shopping', 'action': 'add_item', 'slots': 'tomatoes'}
[ROUTE] task -> shopping -> add_item -> slots: tomatoes

DISPATCH RESULT:
(filler) shopping list handled — action=add_item, slots=tomatoes
================================================================================
INPUT:
It's been ages since I checked the news, what's new?

========== ROUTER RAW ==========
'{"intent":"conversation","task_category":"news","action":"news_headlines","slots":"none"}'
=================================


CLASSIFIED:
{'intent': 'conversation', 'task_category': 'news', 'action': 'news_headlines', 'slots': 'none'}
[ROUTE] conversation -> passing to main LLM: "It's been ages since I checked the news, what's new?"

DISPATCH RESULT:
None
================================================================================
INPUT:
My chest has felt tight since this morning, should I worry?

========== ROUTER RAW ==========
'{"intent":"emergency","task_category":"none","action":"emergency_alert","slots":"chest tightness"}'
=================================


CLASSIFIED:
{'intent': 'emergency', 'task_category': 'none', 'action': 'emergency_alert', 'slots': 'chest tightness'}
[ROUTE] EMERGENCY triggered -> slots: chest tightness

DISPATCH RESULT:
I'm alerting your emergency contact right now. Stay where you are.
(venv) PS D:\UserData\Desktop\Assistant\VoiceAssistant> 
