```yaml
CTFd:

  config:
    name: Test CTF name
    description: Test CTF description
    user_mode: users
    start: 01/02/2019 21:22
    end: 01/02/2021 21:22
    whitelist: 
      - gmail.com
      - test.com
    logo: logo.png
    style: style.css
    theme_header: header
    theme_footer: footer
    name_changes: 0

  users:
    admin1:
      password: admintest
      email: admin@test.com
      type: admin
    admin2:
      password: test
      email: admin@gmail.com
      type: admin
    testuser:
      password: user
      email: testuser@gmail.com
      type: user
      hidden: 0
      website: https://test.com
      country: DK
      affiliation: Cool Catz

  pages:
    index:
      page: index.html
      file: 
        - frontpage.png
        - page.png
    test: 
      page: test.html
      title: nice
    test/more:
      page: more.html
      title: only users
      auth_required: 1


  challenges:

    Crypto:

      test_challenge_1:
        value: 1337
        description: test_chall_desc.md
        flag:
          flag: test
          case: insensitive
          type: regex
        file: 
          - rex.ty
        tag:
          - hard
        hint1:
          description: ch1_hint1.md
        hint2:
          description: ch1_hint2.md
          cost: 12

      chal_2:
        value: 42
        description: chal_2_desc.md
        flag:
          flag: chal
        tag:
          - easy
          - bruh

    Rev:

      rev_chall:
        value: 92
        description: rev_cha_desc.md
        flag:
          flag: blah
        requirements:
          - math_c
          - chal_2

    CoolMathGames:

      math_c:
        value: 69
        description: math_desc.md
        flag:
          flag: math
        file:
          - mat1.txt
          - mat2.txt
        hint:
          description: mathhint.md
          cost: 1
```
