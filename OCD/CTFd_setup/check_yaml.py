import os, sys, time, calendar, re
import yaml, pycountry


# Global error output
class Error:
    def __init__(self):
        self.error = 0
        self.section = ''

    def print_section(self):
        return 'Under ' + self.section + ': '


# Colorcode output
class Colors:
    FAIL = '\033[1;31m'
    SUCCES = '\033[1;32m'
    NORMAL = '\033[1;31m'


# Read the setup.yml file
def read_setup_yaml(YAMLfile):
    with open(YAMLfile,'r') as setup:
        if setup.read()[:-1] == 'Configure me':
            print("You need to alter 'setup.yml' before trying to setup CTFd with CTFdeploy")
            quit(1)

    with open(YAMLfile,'r') as setup:
        try:
            return yaml.safe_load(setup)
        except yaml.parser.ParserError:
            raise Exception('Please format setup.yml correctly')


# Check if keys are present 
def check_keys(YAMLfile):
    # Quit if error is 1
    def check_error(func):
        def error_quit(*args,**kwargs):
            func(*args,**kwargs)
            if error.error == 1:
                print(Colors().NORMAL,end='')
                quit(1)
        return error_quit

    
    # Make sure yaml doesn't contain None values
    def check_yaml_none(*args,**kwargs):
        for key in kwargs:
            if type(kwargs[key]) == dict:
                check_yaml_none(*args,key,**kwargs[key])
            elif type(kwargs[key]) == list:
                for item in kwargs[key]:
                    if item == None:
                        for arg in args:
                            print(arg,end=', ')
                        print(key + ': Has an empty value')
                        error.error = 1
            elif kwargs[key] == None:
                for arg in args:
                    print(arg,end=', ')
                print(key + ': Has an emtpy value')
                error.error = 1

    # Check if key is in YAMLfile
    def check_config_musts(YAMLfile,key):
        if key not in YAMLfile:
            print(error.print_section() + 'missing ' + key )
            error.error = 1


    # Check if key is int
    def check_if_int(key,value):
        try:
            int(value)
            if int(value) < 0:
                raise
        except:
            print(error.print_section() + key + ', must be a positive number') 
            error.error = 1


    # Check between keyvalue and two values and print error
    def check_if_vorv(key,keyvalue,value1,value2):
        if keyvalue == value1 or keyvalue == value2: 
            return
        print(error.print_section() + key + ', must be either ' + str(value1) + ' or ' + str(value2))
        error.error = 1

    
    # Check if timeformat is correct
    def check_time(key,timevalue):
        try:
            if not calendar.timegm(time.strptime(timevalue,'%d/%m/%Y %H:%M')) >= 0:
                print(error.print_section() + key + ', must be set to a time later than 01/01/1970 00:00')
                error.error = 1
        except ValueError:
            print(error.print_section() + key + ', is formatted incorrectly')
            error.error = 1

    
    # Check if email domains are formatted correctly
    def check_whitelist(key,domains):
        for domain in domains:
            try:
                if not re.match(re.compile('^(([a-zA-Z]*\d+\.?)*(\d*[a-zA-Z]+\.?)*)+[^\.]\.[a-zA-Z]+$'),domain):
                    print(error.print_section() + key + ', is formatted incorrectly, ' + domain)
                    error.error = 1
            except TypeError:
                print(error.print_section() + key + ', please check your whitelist members')
                error.error = 1


    # Check if email is formatted correctly - stolen from http://emailregex.com/
    def check_email(key,email):
        if not re.match(re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""),email):
            print(error.print_section() + key + ', is formatted incorrectly, ' + email)
            error.error = 1
        

    # Check if file exists
    def check_file(key,folder,keyfile):
        if not os.path.isfile(folder + keyfile):
            print(error.print_section() + key + ', file does not exist, ' + keyfile)
            error.error = 1

    
    # Check if website is valid format - stolen from https://www.regextester.com/93652
    def check_website(key,website):
        if not re.match(re.compile('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'),website):
            print(error.print_section() + key + ', is formatted incorrectly, ' + website)
            error.error = 1


    # Check if countrycode is valid
    def check_countrycode(key,countrycode):
        if pycountry.countries.get(alpha_2=countrycode) is None:
            print(error.print_section() + key + ', is formatted incorrectly, ' + countrycode)
            error.error = 1


    # Check if challenge exists
    def check_challenge(key,requirement,challengesList):
        if requirement not in challengesList:
            print(error.print_section() + key + ', this challenge is not defined in the setup, ' + requirement)
            error.error = 1
    # Checks for syntax

    # Key configs - config, users, pages, and challenges
    @check_error
    def root_config_check():
        configKeys = YAMLfile['CTFd']

        # Check if key values exist
        check_config_musts(configKeys,'config')
        check_config_musts(configKeys,'users')
        check_config_musts(configKeys,'pages')
        check_config_musts(configKeys,'challenges')


    # Keys in config
    def config_check():
        # Check if key values exist
        @check_error
        def config_key_check():
            check_config_musts(configKeys,'name')
            check_config_musts(configKeys,'description')
            check_config_musts(configKeys,'user_mode')
            check_config_musts(configKeys,'start')
            check_config_musts(configKeys,'end')

        # Check if syntax is correct
        @check_error
        def syntax_check():
            check_time('start',configKeys['start'])
            check_time('end',configKeys['end'])

            check_if_vorv('user_mode',configKeys['user_mode'],'users','teams') 

            
            if 'team_size' in configKeys:
                check_if_int('team_size',configKeys['team_size'])

            if 'name_changes' in configKeys:
                check_if_vorv('name_changes',configKeys['name_changes'],1,0)

            if 'whitelist' in configKeys:
                check_whitelist('whitelist',configKeys['whitelist'])
            
            if 'logo' in configKeys:
                check_file('logo','OCD/config_files/',configKeys['logo'])

            if 'style' in configKeys:
                check_file('style','OCD/config_files/',configKeys['style'])

            if 'theme_header' in configKeys:
                check_file('theme_header','OCD/config_files/',configKeys['theme_header'])

            if 'theme_footer' in configKeys:
                check_file('theme_footer','OCD/config_files/',configKeys['theme_footer'])


        configKeys = YAMLfile['CTFd']['config']
        config_key_check()
        syntax_check()


    # Keys in users
    def users_check():
        # Check if key values exist
        @check_error
        def users_key_check(user):
            check_config_musts(usersKeys[user],'password')
            check_config_musts(usersKeys[user],'email')
            check_config_musts(usersKeys[user],'type')

        
        # Check if syntax is correct
        @check_error
        def syntax_check(user):
            check_email('email',usersKeys[user]['email'])
            check_if_vorv('type',usersKeys[user]['type'],'admin','user')

            if 'hidden' in usersKeys[user]:
                check_if_vorv('hidden',usersKeys[user]['hidden'],1,0)

            if 'website' in usersKeys[user]:
                check_website('website',usersKeys[user]['website'])
                 
            if 'country' in usersKeys[user]:
                check_countrycode('country',usersKeys[user]['country'])


        # Loop through all users
        usersKeys = YAMLfile['CTFd']['users']
        for user in usersKeys:
            error.section = 'users, ' + user
            users_key_check(user)
            syntax_check(user)


    # Keys in pages
    def pages_check():
        # Check if key values exist
        @check_error
        def pages_key_check(page):
            check_config_musts(pagesKeys[page],'page')

        # Check if syntax is correct
        @check_error
        def syntax_check(page):
            if 'file' in pagesKeys[page]:
                for pagefile in pagesKeys[page]['file']:
                    check_file('file','OCD/pages_files/',pagefile)
            if 'auth_required' in pagesKeys[page]:
                check_if_vorv('auth_required',pagesKeys[page]['auth_required'],1,0)

    
        # Loop through all pages
        pagesKeys = YAMLfile['CTFd']['pages']
        check_config_musts(pagesKeys,'index')
        for page in pagesKeys:
                error.section = 'pages, ' + page
                pages_key_check(page)
                syntax_check(page)


    # Keys in challenges
    def challenges_check():
        # Check if key values exist
        @check_error
        def challenges_key_check(challenge):
            check_config_musts(challengesKeys[category][challenge],'value')
            check_config_musts(challengesKeys[category][challenge],'description')
            check_config_musts(challengesKeys[category][challenge],'flag')

        # Check if syntax is correct
        @check_error
        def syntax_check(challenge):
            # Check if flag syntax is valid
            @check_error
            def flag_check(flag):
                error.section = 'challenges, ' + category + ', ' + challenge + ', flag' 
                check_config_musts(flag,'flag')

                if 'type' in flag:
                    check_if_vorv('type',flag['type'],'static','regex')
                if 'case' in flag:
                    check_if_vorv('type',flag['case'],'insensitive','sensitive')

            # Check if hint syntax is valid
            @check_error
            def hint_check(hint):
                error.section = 'challenges, ' + category + ', ' + challenge + ', ' + hint
                check_config_musts(challengesKeys[category][challenge][hint],'description')

                if 'description' in challengesKeys[category][challenge][hint]:
                    check_file('description','OCD/challenge_files/',challengesKeys[category][challenge][hint]['description'])
                if 'cost' in challengesKeys[category][challenge][hint]:
                    check_if_int('cost',challengesKeys[category][challenge][hint]['cost'])


            if 'max_attempts' in challengesKeys[category][challenge]:
                check_if_int('max_attempts',challengesKeys[category][challenge]['max_attempts'])

            if 'file' in challengesKeys[category][challenge]:
                for challengeFile in challengesKeys[category][challenge]['file']:
                    check_file('file','OCD/challenge_files/',challengeFile)

            if 'requirements' in challengesKeys[category][challenge]:
                for requirement in challengesKeys[category][challenge]['requirements']:
                    check_challenge('requirements',requirement,challengesList)

            
            hintmatches = [hint for hint in challengesKeys[category][challenge] if re.match(re.compile('^hint*'),hint)]
            for hint in hintmatches:
                hint_check(hint)

            flag_check(challengesKeys[category][challenge]['flag'])


        challengesKeys = YAMLfile['CTFd']['challenges']

        # Get a list of all challenges
        challengesList = []
        for challenges in [challengesKeys[challenge] for challenge in [category for category in challengesKeys]]:
            for name in challenges.keys():
                challengesList.append(name)

        # Loop through all the challenges
        for category in challengesKeys:
            for challenge in challengesKeys[category]:
                error.section = 'challenges, ' + category + ', ' + challenge
                challenges_key_check(challenge)
                syntax_check(challenge)


    # Fake Main
    error = Error() 

    check_yaml_none(**YAMLfile)

    error.section = 'CTFd'
    root_config_check()

    error.section = 'config'
    config_check()

    error.section = 'users'
    users_check()

    error.section = 'pages'
    pages_check()

    error.section = 'challenges'
    challenges_check()


def main():
    print(Colors().FAIL,end='')
    YAMLfile = read_setup_yaml(sys.argv[1])

    check_keys(YAMLfile)

    print(Colors().SUCCES,end='')
    print('setup.yml seems good')
    print(Colors().NORMAL,end='')


if __name__ == '__main__':
    main()
