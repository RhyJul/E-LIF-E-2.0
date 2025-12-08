def decision():
    """Show a simple menu, validate input, and return the choice."""

    menu = (
        "Hello luv — please give us a hint what we should do today?\n\n"
        "Would you like to:\n"
        "1. Spill the tea for today\n"
        "2. Give a report for this month\n"
        "3. I'd rather not talk about it\n\n"
        "Enter 1, 2 or 3: "
    )

    while True:
        choice_str = input(menu)
        try:
            choice = int(choice_str)
        except ValueError:
            print("Please enter a number (1, 2 or 3).\n")
            continue

        if choice == 1:
            print("Of course girl! I'll make some snacks and coffee ready!!")
            return choice
        elif choice == 2:
            print("Don't lose your way! I'll show you guidance <3")
            return choice
        elif choice == 3:
            print("No problem. If you need to spill the tea, I'm here for you :)")
            return choice
        else:
            print("Please choose 1, 2 or 3.\n")


if __name__ == "__main__":
    decision()
