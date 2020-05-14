# CTFdeployment
This deployment script is used for <b>FRESH</b> deployments of a CTF. Used to
cut the time of deployment on new instances of a CTF. Can be customized for
specific admins, challenges, and pages, as to skip the setup step.

Not meant to replace export/import. Rather used for <b>FRESH</b> deployments.

Make sure to read through the [CTFd](https://github.com/CTFd/CTFd) README
and install their dependencies before using this script, as it is dependent on
it.

Only tested on Linux.

# Introduction
This is how good it is.

# Guide

## YAML
This setup is controlled by a YAML file.

The different sections control how the CTF is setup.

---

### config
The `config` section is basic setup and is necessary for the server to function.
Config is defined as a list with the configuration as lists with list members.

##### Must-have
`name`: The name of the CTF.  
`description`: Description of the CTF.  
`usermode`: Can be either `users` or `teams`.  
`start`: Start time of the CTF. Format: `dd/mm/yyyy hh:mm`.  
`end`: End time of the CTF. Format: `dd/mm/yyyy hh:mm`.  
  
##### Optional
`whitelist`: Whitelist of email domains, separated by comma.  
`ctf_logo`: Filename, use a logo instead of the CTF `name`.   
`theme_color`: Hex value of the header.  
`team_size`: Max team size. Useful when `usermode` is `teams`.  
`name_changes`: Allow name change? `1` or `0`. Default is `1`.  
`theme_header`: A global header which is displayed on all pages.  
`theme_footer`: A global footer which is displayed on all pages.  

---

### pages
The `pages` section is used define the pages used to introduce users to the CTF.
Pages are defined as lists named after their path and defined by lists with list
members. 

##### Must-have
`index`: An index is necessary for introduction on the website.  
`page`: The page which is to be displayed according to the path.  

##### Optional
Optionally more pages can be defined.   
`file`: If the page uses a picture, please reference it.

---

### users
The `users` section defines premade users. Usually admins. Users are defined as
lists with their config as lists with list members.

##### Must-have
`password`: Password used to log into the account.  
`email`: This is not necessarily a must but might come in handy if you want to
receive messages about the CTF.  
`type`: Can either be `admin` or `user`.  

##### Optional
`hidden`: Is the user hidden? `0` or `1`. Default is `1`.  
`website`: Website displayed next to username.  
`country`: Country displayed next to username.  
`affiliation`: Affiliation displayed beneath username.  

---

### challenges
The `challenges` section defines premade challenges and their categories.
Categories are defined as lists and their challenges as lists. The
challenges are defined as lists with their config as lists with list members. 
Categories must have a challenge associated with them.

##### Must-have
`description`: Description of the challenge.   
`value`: The amount of points given for solving the challenge.   
`flag`: The flag is defined as a list with list members as its config. Multiple
flags can be defined.

##### Optional
`max_attempts`: Maximum amount of attempts to submit flag. Default is Infinite.  
`requirements`: Can have multiple list members. Names on challenges which are
required to be solved before this challenge is shown.  
`tag`: Can have multiple list members. Tags to be shown when viewing the
challenge.  
`file`: Can have multiple list members. Files which are used in the challenge.  
`hint`: The hint is defined as a list with list member as its config.  

##### flag
The flag is necessary for a challenge to be solvable. It is defined as a list
with its config as lists with list members.  
`flag`: This is the string representing the flag. Must be present.   
`type`: Can be either `static` or `regex`. Default is `static`.  
`case`: Can be either `sensitive` or `insensitive`. Default is `sensitive`. 

##### hint
The hint is to help with the challenge. Multiple hints can be included in one
challenge.   
`description`: Description of the hint which is shown to the user. Must be
present.  
`cost`: Spend points to show the hint. Default is `0`.  

---

## Example:
```
CTFd:
  config:
    name:
      - "Test CTF name"
    description:
      - "Test CTF description"
    usermode:
      - "users"
    start:
      - "01/02/2020 21:22"
    end:
      - "01/02/2021 19:22"
    whitelist:
      - "okay.com, gmail.com"
    ctf_logo:
      - "logo.png"
    theme_color:
      - "#0021ff"

  pages:
    index:
      page:
        - "index.html"
      file:
        - "frontpage.png"
    test: 
      page:
        - "test.html"

  users:
    admin1:
      password:
        - 'admintest'
      email:
        - 'admin@test.com'
      type:
        - 'admin'
    admin2:
      password:
        - 'test'
      email:
        - ''
      type:
        - 'admin'

  challenges:
    Crypto:
      test_challenge_1:
        value:
          - 1337
        description:
          - "# Test
            This is a challenge

            The port is 2232"
        flag:
          type:
            - 'regex'
          flag:
            - 'test'
          case:
            - 'insensitive'
        file:
          - 'rex.ty'
        tag:
          - 'hard'
          - 'lul'
          - 'glhf'
        hint:
          description:
            - "You shouldn't do this xddd"
        hint:
          description:
            - "Maybe you should"
          cost:
            - 12
      chal_2:
        value:
          - 321
        description:
          - "# test2
            Challenge lol"
        flag:
          flag:
            - 'chal'
        tag:
          - 'easy'
    Reverse:
      rev_challenge:
        value:
          - 92
        description:
          - "# Desc
            slkdjf"
        flag:
          flag:
            - 'blah'
        requirements:
          - 'test_challenge_1'
          - 'chal_2'
```

# How does it work?
This is how it works.

# References
### [CTFd](https://github.com/CTFd/CTFd)
The project is based upon the CTFd CTF-framework and is a modification-script of 
this software. The project is not using a modified version of CTFd but is a
separate project.

##### [Project Plan](project_plan.md)
The project plan is for school purposes.

`One-Click Deployment = OCD`
