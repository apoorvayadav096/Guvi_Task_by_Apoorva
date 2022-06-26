##Validation of username
def valid_user_name(user_name):
    count = 0
    if ('@' in user_name) and ('.' in user_name):
        count += 1
    if '.' in user_name[user_name.index('@')+1:]:   #email/username should have "@" and followed by "." and
                                                    # there should not be any "." immediate next to "@"
        count += 1
    if (user_name.index('.') - user_name.index('@')) >= 4:
        count += 1
    special_characters = list('@_!#$%^&*()<>?/\|}{~:0123456789')
    if user_name[0] not in special_characters:
        count += 1
    if count == 4:
        return True
    else:
        return False

###Validation of password
def valid_password(password):
    count = 0
    special_characters = list('@_!#$%^&*()<>?/\|}{~:')
    for i in password:
        if i in special_characters:
            count += 1
            break
    for i in password:
        if i.isupper():
            count += 1
            break
    for i in password:
        if i.islower():
            count += 1
            break
    for i in password:
        if i.isdigit():
            count += 1
            break
    if 5<len(password)<16:
        count += 1

    if count == 5:
        return True
    else:
        return False

class check_credentials():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_username(self):
        with open("login_credentials.txt", 'a+') as f:
            f.seek(0)
            global username_count
            username_count = 0
            for line in f.readlines():
                both_cred = line.split('*')
                for i in both_cred:                     #both_cred = both credentials
                    if i != '':                          #a line in .txt file after spliting is ['','username,password','\n']
                        if i != '\n':
                            lc_username = i.split(',')[0]            ##lc_username = login credentials username
                            if lc_username == self.username:
                                print("Your email exists")
                                username_count += 1
                                return True
            if username_count == 0:
                print("username doesn't exist")
                return False

    def check_password(self):
        global username_count
        if username_count != 0:
            with open("login_credentials.txt", 'a+') as f:
                f.seek(0)
                count = 0
                for line in f.readlines():
                    both_cred = line.split('*')  # lc_username = login credentials username
                    for i in both_cred:
                        if i != '':
                            if i != '\n':
                                lc_username = i.split(',')[0]
                                lc_password = i.split(',')[1]
                                if (lc_username == self.username) and (lc_password == self.password):
                                    count += 1
                                    return True
                if count == 0:
                    print("You have entered a wrong password")
                    return False

####Registration
def registration():
    while True:
        username = input("Enter a username(Email-id) :")
        check = valid_user_name(username)
        if check == True:
            break
        else:
            print("Kindly enter a valid username")

    while True:
        password = input("Enter you password: ")
        check = valid_password(password)
        if check == True:
            break
        else:
            print(
                "Your password must contain one upper letter, one lower letter, one special character, one digit and minimum of 5 letters")
            print("Enter a valid Password")
    with open('login_credentials.txt','a+') as f:
        f.write(f"*{username},{password}*\n")
    return True

###Retrive the old password and ask for new password(If they choose forget password)
def forgot_password_fun(username):
    print("Do you want to change or retrive the old password: ")
    while True:
        try:
            choice = int(input("To retrive the password choose '1' || To change the password choose '2' : "))
            if choice not in [1,2]:
                raise ValueError("Enter a valid input")
        except:
            print("Enter a valid input")
        else:
            break

    with open("login_credentials.txt", 'a+') as f:
        f.seek(0)
        s = f.read()
    lc_list = s.split('*')                             #lc_list-----> login credentials list
    count = -1
    for i in lc_list:
        count += 1                             #Here count gives the index
        if username in i:
            old_password = lc_list[count].split(',')[1]
            if choice == 1:
                print(f'Your password is:{old_password}')
                break
            elif choice == 2:
                new_password = input("Enter a new password: ")
                val_password = valid_password(new_password)
                while not(val_password):
                    print("Your password must contain one upper letter, one lower letter, one special character, one digit and minimum of 5 letters")
                    new_password = input("Enter a valid password: ")
                    val_password = valid_password(new_password)
                lc_list[count] = lc_list[count].replace(old_password, new_password)
                print('Your password is updated')
                string = '*'.join(lc_list)
                with open("login_credentials.txt", 'w+') as f:
                    f.write(string)
                break

def login():
    print("Enter your credentials to login")
    username = input("Enter the username: ")
    password = input("Enter your password: ")
##check if the username already exists
    check = check_credentials(username, password)
    check_username = check.check_username()
    check_password = check.check_password()

    if check_username == True:
        if check_password == True:
            print("Login is successful")
        elif check_password == False:
            print("Go for forgot password or to retrive your old password")
            while True:
                try1 = int(input("For trying again choose '1'. To choose forgot password choose '2'"))
                try:
                    try1 in [1,2]
                except:
                    print('You have given a wrong input')
                else:
                    if try1 == 1:
                        login()
                        break
                    elif try1 == 2:
                        forgot_password_fun(username)
                        while True:
                            try:
                                ask_again = input("Do you want to login.Choose 'yes' or 'no': ")
                                if ask_again.lower()[0] not in ['y', 'n']:
                                    raise ValueError
                            except:
                                print("Enter a valid input")
                            else:
                                if ask_again.lower()[0] == 'y':
                                    login()
                                else:
                                    break
                        break


    elif check_username == False:
        print("Kindly go for registration")
        choice = input("Do you want to register('y'/'n'): ")
        if choice.lower()[0] == 'y':
            result = registration()
            if result == True:
                print("Your registration is successful")
                while True:
                    try:
                        ask_again = input("Do you want to login.Choose 'yes' or 'no': ")
                        if ask_again.lower()[0] not in ['y','n']:
                            raise ValueError
                    except:
                        print("Enter a valid input")
                    else:
                        if ask_again == 'y':
                            login()
                        else:
                            break

login()



###check whether the userexists or not



