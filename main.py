import os

game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2},
    "Super Mario Bros": {"quantity": 5, "cost": 3},
    "Tetris": {"quantity": 2, "cost": 1},
    # Add more games as needed
}

# emp
user_accounts = {}


admin_username = "admin"
admin_password = "adminpass"


def display_available_games():
    os.system('cls')
    print("\nAVAILABLE GAMES: ")
    for idx, (game, details) in enumerate(game_library.items(), start=1):
        print(f"\n\t{idx}. {game}: Quantity: {details['quantity']}, Cost: ${details['cost']}")
        

def user_menu():
    os.system('cls')
    print("\n\t\tUSER MENU: ")
    print("\t1. register")
    print("\t2. log in")
    print("\t3. Return")
    while True:
        try:
            choice = int(input("\n\tWhat would you like to do? "))
            if choice == 1:
                register_user()
            elif choice == 2:
                log_in_user()
            elif choice == 3:
                main()
            else:
                print("\tInvalid choice, try again")
        except ValueError:
            input("Error: Invalid input. . . Try again: ")
            user_menu()
 

def register_user():
    try:
        rented_games = {}
        user_username = input("\n\tInput username: ")
        if len(user_username) < 5:
            raise ValueError("\tUsername must be at least 5 characters long.")
        
        user_password = input("\tEnter password: ")
        if len(user_password) < 8:
            raise ValueError("\tPassword must be at least 8 characters long.")

        if user_username in user_accounts:
            print("\n\tUsername already exists, try again")
        else:
            user_accounts[user_username] = {"username": user_username,
                                            "password": user_password,
                                            "balance": 0, 
                                            "points": 0, 
                                            "rented_games": rented_games}
            print(f"\n\tUser {user_username} created successfully.")
            input("\tYou can now log in, press Enter to Continue. . .")
            user_menu()

    except ValueError as e:
        print(f"\n\tError: {e}")
        choice = input("\t1. Try Again\n\t2. Return\n\tChoose: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            main()
        else:
            input("Invalid choice. Try again")
            register_user()


def log_in_user():
    os.system('cls')
    print("\n\t\tLOG IN MENU")
    user_username = input("\tEnter username: ")
    if user_username in user_accounts:
        user_password = input("\tEnter password: ")
        if user_password == user_accounts[user_username]["password"]:
            print("\tLog in Successfully! ")
            top_up_account(user_username)
        else:
            print("\tInvalid password, try again")
            input("\tPress Enter to try again")
            log_in_user()
    else:
        print("\tUsername doesn't exist. Sign up first.")
        input("\tPress Enter to Sign up")
        user_menu()

def top_up_account(user_username):
    os.system('cls')
    print("\n\t\tTOP UP MENU")
    print(f"\n\t\tUSERNAME: {user_username}")

    while True:
        try:
            top_up_amount = float(input("\n\tInput amount you want to top up: "))
            if top_up_amount < 0:
                print("\tInvalid amount. Try Again")
            else:
                user_accounts[user_username]["balance"] += top_up_amount
                print("\tTop up successful!")
                print(f"\tUsername {user_username} balance: {user_accounts[user_username]['balance']}")
                input("\n\tPress Enter to proceed")
                user_rental_menu(user_username)
                break
        except ValueError:
            input("\tInvalid input. Try again: ")
            top_up_account(user_username)


def user_rental_menu(user_username):
    os.system('cls')
    print("\n\t\tRENTAL GAME MENU")
    print("\t1. Rent a game")
    print("\t2. Return a game")
    print("\t3. Top Up")
    print("\t4. Game Inventory")
    print("\t5. Check Points")
    print("\t6. Redeem Points")
    print("\t7. Log Out")
    while True:
        try:
            choice = int(input("\n\tChoose your action: "))
            if choice == 1:
                rent_game(user_username)
            elif choice == 2:
                return_game(user_username)
            elif choice == 3:
                top_up_account(user_username)
            elif choice == 4:
                display_inventory(user_username)
            elif choice == 5:
                check_and_redeem_points(user_username)
            elif choice == 6:
                redeem_points(user_username)
            elif choice == 7:
                main()
            else:
                print("\tInvalid choice, try again")
        except ValueError:
            input("\tError: Invalid input. . . Try Again: ")
            user_rental_menu(user_username)


def rent_game(user_username):
    os.system('cls')
    while True: 
        try: 
            print("\n\t\tAVAILABLE GAMES: ")
            for idx, (game, details) in enumerate(game_library.items(), start=1):
                print(f"\n\t{idx}. {game}: Quantity: {details['quantity']}, Cost: ${details['cost']}")
            print("\n\t\tRENT A GAME")
            choice = input("\n\tEnter the number of the game you want to rent (leave blank to cancel): ")
            
            if choice.strip() == "":
                print("\tTransaction cancelled.")
                input("\n\tPress Enter to return to the rental menu.")
                user_rental_menu(user_username)
                break
            
            choice = int(choice)
            
            if choice < 1 or choice > len(game_library):
                print("\tInvalid input, try again.")
                continue
            else:
                selected_game = list(game_library.keys())[choice - 1]
                if game_library[selected_game]["quantity"] <= 0:
                    print("\tThe game you selected isn't available. Try again")
                    continue
                
                game_cost = game_library[selected_game]["cost"]
                if user_accounts[user_username]["balance"] < game_cost:
                    print("\tInsufficient balance to rent the game.")
                    continue
                
                user_accounts[user_username]["balance"] -= game_cost
                game_library[selected_game]["quantity"] -= 1
                if selected_game in user_accounts[user_username]["rented_games"]:
                    user_accounts[user_username]["rented_games"][selected_game] += 1
                else:
                    user_accounts[user_username]["rented_games"][selected_game] = 1

                print(f"\n\tSuccessfully rented {selected_game} for ${game_cost}.")
                print(f"\tRemaining balance: ${user_accounts[user_username]['balance']}")
                input("\n\tPress Enter to Return. . .")
                user_rental_menu(user_username)
                break
        except ValueError:
            input("\tInvalid input, try again.")
            return_game()


def return_game(user_username):
    os.system('cls')
    print("\n\t\tRETURN GAME MENU")
    rented_games = user_accounts[user_username]["rented_games"]

    if not rented_games:
        print("\tYou don't have any games to return.")
        return

    print("\n\t\tGames you have rented:")
    for idx, (game, quantity) in enumerate(rented_games.items(), start=1):
        print(f"\t{idx}. {game}: Quantity: {quantity}")

    while True:
        try:
            choice = input("\n\tChoose the game you want to return (leave blank to cancel): ")
            
            if choice.strip() == "":
                print("\tTransaction cancelled.")
                input("\n\tPress Enter to return to the rental menu.")
                user_rental_menu(user_username)
                break
            
            choice = int(choice)
            
            if choice < 1 or choice > len(rented_games):
                print("\tInvalid input, try again.")
                continue
            else:
                selected_game = list(rented_games.keys())[choice - 1]
                quantity_returned = int(input("\tEnter the quantity of the game you want to return: "))
                if quantity_returned <= 0:
                    print("\tInvalid quantity, try again.")
                    continue
                elif quantity_returned > rented_games[selected_game]:
                    print("\tYou cannot return more games than you have rented.")
                    continue
                else:
                    user_accounts[user_username]["balance"] += quantity_returned * game_library[selected_game]["cost"]
                    game_library[selected_game]["quantity"] += quantity_returned
                    rented_games[selected_game] -= quantity_returned
                    if rented_games[selected_game] == 0:
                        del rented_games[selected_game]
                    print(f"\tSuccessfully returned {quantity_returned} copies of {selected_game}.")
                    print(f"\tYour balance is now ${user_accounts[user_username]['balance']}")
                    input("\n\tPress Enter to Return. . .")
                    user_rental_menu(user_username)
                    break
        except ValueError:
            input("\tInvalid input, try again.")
            return_game()


def display_inventory(user_username):
    os.system('cls')
    rented_games = user_accounts[user_username]["rented_games"]
    print(f"\n\t\t{user_username}'s inventory: ")
    if rented_games:
        for game_name, quantity in rented_games.items():
            print(f"\n\t{game_name}; Quantity: {quantity}")
        input("\n\tPress Enter to Return. . .")
        user_rental_menu(user_username)
    else:
        print("\tYou don't own any games")
        input("\tPress Enter to Return. . .")
        user_rental_menu(user_username)


def redeem_points(user_username):
    os.system('cls')
    print("\n\t\tRedeem Points")
    available_points = user_accounts[user_username]["points"]  # Retrieve available points
    if available_points >= 3:
        print("\t\tRedeeming points...")
        user_accounts[user_username]["points"] -= 3  # Deduct points
        print("\t\tPoints redeemed successfully.")
        return True
    else:
        print(f"\n\t\tYou only have {available_points} point(s). You need at least 3 points.")
        return False


def redeem_game(user_username):
    while True:
        try:
            print("\nAVAILABLE GAMES: ")
            for idx, (game, details) in enumerate(game_library.items(), start=1):
                print(f"\n\t{idx}. {game}: Quantity: {details['quantity']}, Cost: ${details['cost']}")
            choice = int(input("\n\tEnter the number of the game you want to rent: "))
            game_names = list(game_library.keys())
            if 1 <= choice <= len(game_names):
                game_name = game_names[choice - 1]
                if game_library[game_name]['quantity'] <= 0:
                    print("\tGame is not available.")
                else:
                    game_library[game_name]['quantity'] -= 1
                    if game_name in user_accounts[user_username]["rented_games"]:
                        user_accounts[user_username]["rented_games"][game_name] += 1
                    else:
                        user_accounts[user_username]["rented_games"][game_name] = 1
                    print("\tGame rented successfully.")
                    input("\n\tPress Enter to return.")
                    user_rental_menu(user_username)
                break
            else:
                print("\tInvalid choice. Please enter a number within the range.")
        except ValueError as e:
            print(f"Value error: {e}")


def check_and_redeem_points(user_username):
    os.system('cls')
    print("\n\t\tChecking Points...")
    total_spent = 0
    for game, quantity in user_accounts[user_username]["rented_games"].items():
        total_spent += quantity * game_library[game]["cost"]

    user_accounts[user_username]["points"] = total_spent // 2  # Update user's points
    points = user_accounts[user_username]["points"]  # Retrieve updated points

    print(f"\n\t\t{user_username}'s points: {points}")

    if points >= 3:
        print("\n\t\tSufficient points, do you want to use it and redeem a free game?")
        choice = input("\t\tyes/no: ").lower()
        if choice == "yes":
            if redeem_points(user_username):
                print("\n\t\tEnjoy your free game!")
                # Update points after redeeming the free game
                total_spent -= 6  # Deduct points equivalent to 3 points for a free game
                redeem_game(user_username)
                user_accounts[user_username]["points"] = total_spent // 2  # Update user's points
                print(f"\n\t\t{user_username}'s points: {user_accounts[user_username]['points']}")
            else:
                print("\n\t\tRedemption failed. Please try again later.")
        elif choice == "no":
            print("\n\t\tBack to menu.")
        else:
            print("\n\t\tInvalid choice.")
    else:
        print("\n\t\tInsufficient points, can't redeem yet. Back to menu.")


import sys

def main():
    os.system('cls')
    while True:
        print("\n\t\tMAIN MENU")
        print("\t1. User")
        print("\t2. Admin")
        print("\t3. Exit")
        choice = input("\n\tEnter your choice: ")

        if choice == "1":
            user_menu()
        elif choice == "2":
            admin_login()
        elif choice == "3":
            print("\tExiting program. Goodbye!")
            sys.exit() 
        else:
            input("\tInvalid choice. Please try again: ")
            main()


def admin_login():
    os.system('cls')
    print("\n\t\tADMIN LOGIN")
    admin = input("\tEnter username: ")
    password = input("\tEnter password: ")
    if admin == admin_username and password == admin_password:
        admin_menu()
    else:
        print("\tInvalid password or username. Try Again")
        input("\n\tPress Enter to try again")
        admin_login()


def display_game_inventory():
    os.system('cls')
    print("\n\t\tGAME INVENTORY")
    for game, details in game_library.items():
        print(f"\tGame: {game}, Quantity: {details['quantity']}, Cost: ${details['cost']}")

    input("\n\tPress Enter to return to the Admin Menu.")
    admin_menu()


def admin_menu():
    os.system('cls')
    print("\n\t\tAdmin Menu")
    print("\t1. Update Game Details")
    print("\t2. Add New Game")
    print("\t3. Display Game Inventory")
    print("\t4. Log Out")
    while True:
        try:
            choice = int(input("\n\tEnter your choice: "))
            if choice == 1:
                admin_update_menu()
                break
            elif choice == 2:
                add_new_game()
                break
            elif choice == 3:
                display_game_inventory()
                break
            elif choice == 4:
                print("\n\tLogging out...Goodbye!")
                main()
                break
            else:
                print("\tPlease input a valid option")
        except ValueError:
            input("\n\tError: Invalid input. Enter to try again")
            admin_menu()


def admin_update_menu():
    os.system('cls')
    print("\n\t\tUpdate Menu")
    print("\t1. Display Available Games")
    print("\t2. Update Game Copies")
    print("\t3. Update Game Cost")
    print("\t4. Return")
    while True:
        try:
            choice = int(input("\n\tWhat would you like to do? "))
            if choice == 1:
                os.system('cls')
                print("\n\tAVAILABLE GAMES: ")
                for idx, (game, details) in enumerate(game_library.items(), start=1):
                    print(f"\n\t{idx}. {game}: Quantity: {details['quantity']}, Cost: ${details['cost']}")
                input("\n\tPress Enter to go back to Update Menu")
                admin_update_menu()
            elif choice == 2:
                update_game_copies()
            elif choice == 3:
                update_game_cost()
            elif choice == 4:
                print("\tGoing back to Admin Menu...")
                admin_menu()
                break
            else:
                print("\tInvalid input, try again.")
        except ValueError:
            input("\n\tError: Invalid input. Enter to try again")
            admin_update_menu()

def add_new_game():
    os.system('cls')
    print("\n\t\tADD NEW GAME")
    try:
        game_name = input("\tEnter the name of the new game: ")
        if game_name in game_library:
            print("\n\tGame already exists.")
            input("\n\tPlease press enter to go back to update menu")
            admin_update_menu()

        quantity = int(input("\tEnter the quantity of copies: "))
        if quantity < 0:
            print("\n\tQuantity cannot be negative.")
            input("\n\tPlease press enter to go back to update menu")
            admin_update_menu()

        cost = float(input("\tEnter the cost of the game: "))
        if cost < 0:
            print("\n\tCost cannot be negative.")
            input("\n\tPlease press enter to go back to update menu")
            admin_update_menu()

        game_library[game_name] = {"quantity": quantity, "cost": cost}
        print(f"\n\tSuccessfully added {game_name} to the game library.")
        input("\n\tPlease press enter to go back to update menu")
        admin_update_menu()
    except ValueError:
        input("\tInvalid input. Click any keys to try again: ")
        add_new_game()


def update_game_copies():
    os.system('cls')
    try:
        print("\n\tAVAILABLE GAMES: ")
        for idx, (game, details) in enumerate(game_library.items(), start=1):
            print(f"\n\t{idx}. {game}: Quantity: {details['quantity']}, Cost: ${details['cost']}")

        print("\n\t\tUpdate Game Quantity")
        game_choice = int(input("\n\tEnter the number of the game you want to update: "))

        if game_choice < 1 or game_choice > len(game_library):
            print("\n\tInvalid choice. Please enter a number corresponding to an available game.")
            input("\n\tPlease press enter to go back to update menu")
            admin_update_menu()

        selected_game = list(game_library.keys())[game_choice - 1]
        new_quantity = int(input(f"\t\nEnter the new quantity for {selected_game}: "))
        
        if new_quantity < 0:
            print("\n]tQuantity cannot be negative.")
            input("\n\tPlease press enter to go back to update menu")
            admin_update_menu()

        game_library[selected_game]["quantity"] = new_quantity
        print(f"\n\tSuccessfully updated quantity of {selected_game} to {new_quantity}.")
        input("\n\tPlease press enter to go back to update menu")
        admin_update_menu()
    except ValueError:
        input("\tInvalid input. Click any keys to try again: ")
        update_game_copies()


def update_game_cost():
    os.system('cls')
    try:
        print("\nAVAILABLE GAMES: ")
        for idx, (game, details) in enumerate(game_library.items(), start=1):
            print(f"\n\t{idx}. {game}: Quantity: {details['quantity']}, Cost: ${details['cost']}")

        print("\n\t\tUpdate Game Cost")
        game_choice = int(input("\n\tEnter the number of the game you want to update: "))

        if game_choice < 1 or game_choice > len(game_library):
            print("\tInvalid choice. Please enter a number corresponding to an available game.")
            input("\n\tPlease press enter to go back to update menu")
            admin_update_menu()

        selected_game = list(game_library.keys())[game_choice - 1]
        new_cost = float(input(f"\n\tEnter the new cost for {selected_game}: "))
        
        if new_cost < 0:
            print("\n\tCost cannot be negative.")
            input("\n\tPlease press enter to go back to update menu")
            admin_update_menu()

        game_library[selected_game]["cost"] = new_cost
        print(f"\n\tSuccessfully updated cost of {selected_game} to ${new_cost}.")
        input("\n\tPlease press enter to go back to update menu")
        admin_update_menu()
    except ValueError:
        input("\tInvalid input. Click any keys to try again: ")
        update_game_cost()


if __name__ == "__main__":
    main()