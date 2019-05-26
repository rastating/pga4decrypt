<p align="center">
  <img src="https://static.rastating.com/images/pga4decrypt.png">
</p>

What is pga4decrypt?
====================
It is a Python**3** script to recover the plain-text credentials of servers stored within a pgadmin4 database.

Quick Start
===========
```
# Clone the source code and install the dependencies
git clone git@github.com:rastating/pga4decrypt.git
cd pga4decrypt
pip install -r requirements.txt

# Launch pga4decrypt against the sample database
./pga4decrypt test/pgadmin4.db
```

Usage
=====
```
usage: pga4decrypt [-h] [-f {text,json}] [-o PATH] path

A tool for recovering server credentials from a pgadmin4 database

positional arguments:
  path            Path to the database (typically named pgadmin4.db)

optional arguments:
  -h, --help      show this help message and exit
  -f {text,json}  The output format for the -o option (default: text)
  -o PATH         Path to a file to save the credentials in
```

Examples
========
Run without an output file
--------------------------
```shell_session
$ ./pga4decrypt test/pgadmin4.db                          

Decrypted 3 sets of credentials

Name: Server 2
Host: 10.8.0.101
Port: 5432
Username: billy
Password: DespiteAllMyRageIAmStillJustARatInACage
-----------------------------------
Name: Server 3
Host: 10.8.0.102
Port: 5432
Username: billy
Password: iamone
-----------------------------------
Name: Server 1
Host: 10.8.0.100
Port: 5432
Username: alice
Password: GetOutOfMySwamp
-----------------------------------
```

Save to a JSON file
-------------------
```shell_session
$ ./pga4decrypt test/pgadmin4.db -o ~/example.json -f json

Decrypted 3 sets of credentials

Name: Server 2
Host: 10.8.0.101
Port: 5432
Username: billy
Password: DespiteAllMyRageIAmStillJustARatInACage
-----------------------------------
Name: Server 3
Host: 10.8.0.102
Port: 5432
Username: billy
Password: iamone
-----------------------------------
Name: Server 1
Host: 10.8.0.100
Port: 5432
Username: alice
Password: GetOutOfMySwamp
-----------------------------------

$ cat ~/example.json| json_pp
[
   {
      "password" : "DespiteAllMyRageIAmStillJustARatInACage",
      "username" : "billy",
      "port" : 5432,
      "name" : "Server 2",
      "host" : "10.8.0.101"
   },
   {
      "password" : "iamone",
      "port" : 5432,
      "username" : "billy",
      "name" : "Server 3",
      "host" : "10.8.0.102"
   },
   {
      "host" : "10.8.0.100",
      "password" : "GetOutOfMySwamp",
      "username" : "alice",
      "name" : "Server 1",
      "port" : 5432
   }
]
```
