def call_llm(prompt):
    while True:
        user_input = input(prompt)
        try:
            result = eval(user_input)
            print(result)
        except Exception as e:
            print("Error:", e)