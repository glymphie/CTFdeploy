```yaml
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
        - 'test@gmail.com'
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
