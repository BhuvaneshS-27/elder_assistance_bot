from task_dispatcher import handle_time

tests = [
    "What day is it today?",
    "What's the time right now?",
    "What month is this?",
    "How many days left until Wednesday?",
    "Is it still morning or afternoon now?",
    "What year are we in?",
    "How long ago was yesterday?",
    "How much time is left until 5?",
    "How much time is left until 5 pm?",
    "How long until 9:30?",
    "How many months left until December?",
    "How many years left until 2029?",
    "How late is it?",
    "What time is it in New York?",
    "Is it almost bedtime yet?",
    "Can you check the clock now ?",
    "Is today a weekend or a weekday?",
    "Has July started?",
    "Are we still in August?",
    "Has the new year begun?",
    "Are we still in 2026?",
    "What comes after this year?",
    "How many months are left this year?",
    "Give me the current date and clock reading.", 
    "Is Christmas close?",
    "Are we in the first half or second half of the year?",
    "How much of the day has passed?",

]

for sentence in tests:
    # result normally comes from classify_intent() — a plain dict is enough
    # here since handle_time reads user_text directly, not the LLM's slots.
    fake_result = {"intent": "task", "task_category": "time", "action": "date_enquiry", "slots": ""}
    print("=" * 60)
    print("INPUT :", sentence)
    print("REPLY :", handle_time(sentence, fake_result))