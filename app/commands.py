from app import app, db
import getpass, re
from app.models import  User


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@app.cli.command('createsuperuser')
def createsuperuser():
    """Creates super user"""

    regex = '@.*?\.'
    username = str(input("Enter username: "))
    email = str(input("Enter email: "))
    password = str(getpass.getpass("Password: "))

    if len(password) < 8:
        print(f"{bcolors.WARNING}Warning: Password is too short. Recomended atleast 8 charcters.{bcolors.ENDC}")
        ch = str(input(f"{bcolors.WARNING}Are you sure to go with this password? [y/n] : {bcolors.ENDC}"))
        if ch != 'y':
            return

    if re.search(regex, email):
        try:
            user = User.query.filter_by(email=email).first()

            if user:
                print(f"{bcolors.FAIL}User already exists{bcolors.ENDC}")
                raise Exception()

            else:
                user = User(username=username, email=email, has_admin_previlages=1)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()

            print(f"\n{bcolors.OKGREEN}Superuser created{bcolors.ENDC}")
        except Exception:
            print(f"\n{bcolors.FAIL}Error: Cannot create superuser{bcolors.ENDC}")