from fact_extractor import extract_facts

tests = [

    # ---------- Family ----------
    "My wife's name is Lakshmi.",
    "My husband is Rajesh.",
    "I have two sons named Arun and Karthik.",
    "My granddaughter is Ananya.",
    "My nephew is Vivek.",
    "My sister lives in Coimbatore.",

    # ---------- Medical ----------
    "I have Parkinson's disease.",
    "I have high blood pressure.",
    "I suffer from asthma.",
    "I have poor eyesight.",
    "I wear dentures.",
    "I use a wheelchair.",
    "I use a pacemaker.",
    "I had a knee replacement surgery.",
    "I wear glasses.",

    # ---------- Medicines ----------
    "I take Metformin every night.",
    "I take blood pressure tablets after breakfast.",
    "I need insulin before dinner.",

    # ---------- Preferences ----------
    "I love filter coffee.",
    "I enjoy Carnatic music.",
    "Blue is my favourite colour.",
    "My favourite actor is Rajinikanth.",
    "My favourite cricket team is CSK.",
    "I enjoy reading history books.",
    "I prefer vegetarian food.",

    # ---------- Languages ----------
    "I can speak Hindi, Tamil and English.",
    "I understand Telugu but cannot speak it.",

    # ---------- Daily routine ----------
    "I usually sleep at 9 PM.",
    "I go for a walk every morning.",
    "I drink coffee at 6 AM.",
    "I pray every evening.",
    "I watch the news every night.",

    # ---------- Home ----------
    "I live alone.",
    "I live with my daughter.",
    "I stay on the second floor.",
    "My bedroom is upstairs.",

    # ---------- Emergency ----------
    "My emergency contact is Ravi.",
    "Call my son Arun if something happens.",
    "My neighbour Meena has a spare key.",

    # ---------- Devices ----------
    "I use a hearing aid in my left ear.",
    "I keep my spectacles near the television.",
    "My walking stick is beside the sofa.",
    "My medicines are in the kitchen cupboard.",

    # ---------- Pets ----------
    "I have a cat named Whiskers.",
    "I own a parrot named Kittu.",
    "My dog's favourite toy is a red ball.",

    # ---------- Religious / Cultural ----------
    "I visit the temple every Friday.",
    "I celebrate Deepavali with my family.",

    # ---------- Occupation ----------
    "I am a retired school teacher.",
    "I worked at Indian Railways.",
    "I served in the Indian Army.",

    # ---------- Vehicle ----------
    "My scooter number is TN09AB1234.",
    "I drive a white Alto.",

    # ---------- Hobbies ----------
    "I enjoy painting.",
    "I collect old coins.",
    "I love solving crossword puzzles.",
    "I play chess every Sunday.",

    # ---------- Things that SHOULD NOT be stored ----------
    "The weather is very hot today.",
    "Today I ate dosa.",
    "I'm watching television now.",
    "The stock market went up today.",
    "Tomorrow I am going to Chennai.",
    "My friend is coming home this evening.",
    "I just finished lunch.",
    "The power went off today.",
    "It is raining outside.",
    "I bought vegetables this morning."

]

for sentence in tests:

    print("=" * 80)
    print("INPUT:")
    print(sentence)

    facts = extract_facts(sentence)

    print("\nEXTRACTED:")
    print(facts)