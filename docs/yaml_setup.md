# YAML
The overall structure of the database is controlled by a `setup.yml` file. This
file is used by `start.sh`. More specifically, it's used by `OCD.py` to
create queries for the database to populate it.

The file starts with `CTFd:` as the root dictionary.

By default, lists can only have one list member unless specified otherwise.

Look at [this example](example_yaml.md) for inspiration.

---

### config
The `config` section is basic setup and is necessary for the server to function.
Config is defined as a dictionary with the configuration as lists with list members.

##### Must-have
`name`: The name of the CTF.  
`description`: Description of the CTF.  
`usermode`: Can be either `users` or `teams`.  
`start`: Start time of the CTF. Format: `dd/mm/yyyy hh:mm`.  
`end`: End time of the CTF. Format: `dd/mm/yyyy hh:mm`.  
  
##### Optional
`whitelist`: Whitelist of email domains, separated by comma.  
`ctf_logo`: Filename, use a logo instead of the CTF `name`.   
`theme_color`: Hex value of the header. Must be made a string with quotes 
due to YAML syntax.
`team_size`: Max team size. Useful when `usermode` is `teams`.  
`name_changes`: Allow name change? `1` or `0`. Default is `1`.  
`theme_header`: A global header which is displayed on all pages.  
`theme_footer`: A global footer which is displayed on all pages.  

---

### pages
The `pages` section is used to define the pages used to introduce users to the CTF.
Pages are defined as dictionaries named after their path and configured by lists 
with list members. 

##### Must-have
`index`: An index is necessary for introduction on the website.  
`page`: The page which is to be displayed according to the path.  

##### Optional
Optionally more pages can be defined.   
`file`: If the page uses a picture, please reference it.

---

### users
The `users` section defines premade users. Usually admins. Users are defined as
dictionaries with their config as lists with list members.

##### Must-have
`password`: Password used to log into the account.  
`email`: The email which should be used by CTFd to send information to the user.
`type`: Can either be `admin` or `user`.  

##### Optional
`hidden`: Is the user hidden? `0` or `1`. Default is `1`.  
`website`: Website displayed next to username.  
`country`: Country displayed next to username.  
`affiliation`: Affiliation displayed beneath username.  

---

### challenges
The `challenges` section defines premade challenges and their categories.
Categories are defined as dictionaries and their challenges as dictionaries. The
challenges are defined as dictionaries with their config as lists with list members. 
Categories must have a challenge associated with them.

##### Must-have
`description`: Description of the challenge.   
`value`: The amount of points given for solving the challenge.   
`flag`: The flag is defined as a dictionary with list members as its config.

##### Optional
`max_attempts`: Maximum amount of attempts to submit flag. Default is infinite.  
`requirements`: Can have multiple list members. Names of challenges which are
required to be solved before this challenge is shown.  
`tag`: Can have multiple list members. Tags to be shown when viewing the
challenge.  
`file`: Can have multiple list members. Files which are used in the challenge.  
`hint`: Hints are defined as a lists with list member as its config. Multiple
hints have to be named differently.

##### flag
The flag is necessary for a challenge to be solvable. It is defined as a
dictionary with its config as lists with list members.  
`flag`: This is the string representing the flag. Must be present.   
`type`: Can be either `static` or `regex`. Default is `static`.  
`case`: Can be either `sensitive` or `insensitive`. Default is `sensitive`. 

##### hint
The hint is to help with the challenge. Multiple hints can be included in one
challenge if named differently eg. hint1, hint_exp, etc.   
`description`: Description of the hint which is shown to the user. Must be
present.  
`cost`: Spend points to show the hint. Default is `0`.  
