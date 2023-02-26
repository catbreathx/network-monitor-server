# Admin Script

Creates a user:

```
python admin.py --email <email> --password <password> --first-name <first> --last-name <last> --config-file <config-file>
```

I.e.,

```
python admin.py --email user@user.com --password 12#$password --first-name Bob --last-name Last --config-file ../../dev.env
```

Note:  Password minimum requirements:
- 8 letters
- 2 numerics
- 2 digits
