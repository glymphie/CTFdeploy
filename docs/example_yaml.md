```yaml
CTFd:

  config:
    name: Test CTF name
    description: Test CTF description
    usermode: users
    start: 01/02/2019 21:22
    end: 01/02/2021 21:22
    whitelist: ''
    ctf_logo: logo.png
    theme_color: '#0022ff'

  pages:
    index:
      page: index.html
      file: 
        - frontpage.png
    test: 
      page: test.html
    test/more:
      page: more.html

  users:
    admin1:
      password: admintest
      email: admin@test.com
      type: admin
    admin2:
      password: test
      email: admin@gmail.com
      type: admin

  challenges:

    Crypto:

      test_challenge_1:
        value: 1337
        description: "# Test\n
            This is a challenge\n\n
            The port is 2232"
        flag:
          flag: test
          case: insensitive
          type: regex
        file: 
          - rex.ty
        tag:
          - hard
        hint1:
          description: You shouldn't do this xddd
        hint2:
          description: Maybe you should
          cost: 12

      chal_2:
        value: 321
        description: "# test\n
                      Challenge lol"
        flag:
          flag: chal
        tag:
          - easy
          - bruh

    Rev:

      rev_chall:
        value: 92
        description: "# Desc\n
                      slkdjf"
        flag:
          flag: blah
        requirements:
          - chal_2
```
