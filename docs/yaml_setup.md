# YAML
The overall structure of the database is controlled by a `setup.yml` file. This
file is used by `start.sh`. More specifically, it's used by `OCD.py` to
create queries for the database to populate it.

The file starts with `CTFd:` as the root dictionary.

By default, values are assigned as strings unless specified otherwise. Example: `key: value`.  
This will not work:   
```
key: 
  -value
```

Look at [this example](example_yaml.md) for inspiration.

Descriptions for challenges and hints does support Markdown.

## config
The `config` section is basic setup and is necessary for the server to function.
Config is defined as a dictionary with the configuration as lists with list members or strings.

##### Must-have
`name`: The name of the CTF.  
`description`: Description of the CTF.  
`user_mode`: Can be either `users` or `teams`.  
`start`: Start time of the CTF. Format: `dd/mm/yyyy hh:mm`.  
`end`: End time of the CTF. Format: `dd/mm/yyyy hh:mm`.  
  
##### Optional
`whitelist`: Can have multiple list members. Whitelist of email domains.    
`team_size`: Max team size. Useful when `usermode` is `teams`. Default is infinite.
`name_changes`: Allow name change? `1` or `0`. Default is `1`.   
`logo`: Filename, use a logo instead of the CTF `name`. Stored in `OCD/config_files`.   
`theme_header`: Filename, a global HTML header which is displayed on all pages. Stored in `OCD/config_files`.   
`theme_footer`: Filename, a global HTML footer which is displayed on all pages. Stored in `OCD/config_files`.   
`style`: Filename, if you've configured a style sheet for another CTFd. Stored in `OCD/config_files`.   


## users
The `users` section defines premade users. Usually admins. Users are defined as
dictionaries with their config as lists with list members or strings.

##### Must-have
`password`: Password used to log into the account.    
`email`: The email which should be used by CTFd to send information to the user.   
`type`: Can either be `admin` or `user`.    

##### Optional
`hidden`: Is the user hidden? `0` or `1`. Default is `1`.  
`website`: Website displayed next to username.  
`country`: Countrycode, country displayed next to username. Will show as NULL if countrycode is invalid.  
`affiliation`: Affiliation displayed beneath username.  


## pages
The `pages` section is used to define the pages used to introduce users to the CTF.
Pages are defined as dictionaries named after their path and configured by lists 
with list members or strings. 

##### Must-have
`index`: An index is necessary for introduction on the website.   
`page`: Filename, the page which is to be displayed according to the path. Stored in `OCD/pages_files`. 

##### Optional
Optionally more pages can be defined.   
`file`: Filename, can have multiple list members. If the page uses a local picture, please reference it by its name. Stored in `OCD/pages_files`.  
`auth_required`: Does it required an account to watch the page? 0 or 1. Default is 0.  
`title`: Giving the page a title create a link in the top bar on the front page. Doesn't work with index as it already has a link.  


## challenges
The `challenges` section defines premade challenges and their categories.
Categories are defined as dictionaries and their challenges as dictionaries. The
challenges are defined as dictionaries with their config as lists with list members or strings. 
Categories must have a challenge associated with them.

##### Must-have
`description`: Filename, description of the challenge. Store in `OCD/challenge_files`.  
`value`: The amount of points given for solving the challenge.    
`flag`: The flag is defined as a dictionary with list members as its config.  

##### Optional
`max_attempts`: Maximum amount of attempts to submit flag. Default is infinite.    
`requirements`: Can have multiple list members. Names of challenges which are
required to be solved before this challenge is shown.  
`tag`: Can have multiple list members. Tags to be shown when viewing the
challenge.  
`file`:Filename, can have multiple list members. Files which are used in the challenge. Stored in `OCD/challenge_files`.  
`hint`:Hints are defined as a lists with list member as its config. Multiple
hints have to be named differently.  

##### flag
The `flag` is necessary for a challenge to be solvable. It is defined as a
dictionary with its config as lists with list members or strings.   
`flag`: This is the string representing the flag. Must be present.   
`type`: Can be either `static` or `regex`. Default is `static`.  
`case`: Can be either `sensitive` or `insensitive`. Default is `sensitive`. 

##### hint
The `hint` is to help with the challenge. Multiple hints can be included in one
challenge if named differently eg. `hint1`, `hint_exp`, etc. Defnied as a list with 
list members or strings.  
`description`: Filename, description of the hint which is shown to the user. Must be
present. Stored in `OCD/challenge_files`.   
`cost`: Spend points to show the hint. Default is `0`.  
