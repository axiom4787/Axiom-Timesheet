# Axiom Timesheet
> Managing and checking time for logins and logouts with unique ids

Axiom Timesheet is essentially a "clocking" program to track hours. 
You link up a spreadsheet and can input your school or work id number and it will sign you in. 
Put it in again and it will sign you out. 

## Installing / Getting started

A quick introduction of the minimal setup you need to get a hello world up &
running.

```shell
git clone https://github.com/axiom4787/Axiom-Timesheet
pip install -r reqs.txt # WIP
python timesheet.py
```

This will clone the repo, install the requirements for the repo, and then run the app. 
Obviously, the uncompiled version of this requires python. 

### Initial Configuration

You need to set some stuff up before you can use this. 

1. Set up a sheet with the following layout (google sheet): `Timesheet Log #1 | Timesheet Log #2 | Master Log | IDs`
> Timesheet Log #1 - You log for 1 timesheet instance. 
> Timesheet Log #2 - Make this even if you don't have another timesheet instance unless you want to change the code.
> Master Log - Timesheet #1 and #2 are merged into this, good if you want to make a dashboard or extract data. 
> IDs - Where IDs will be looked up from. Collums should be `Timestamp | Email | Name | ID` for code consistancy.

2. Add your credentials.
> Log into google cloud manager and get your google sheets api key as a json. Call it `credentials.json` and place it in the main directory

3. Edit `connection.py`'s `sheets_id` to be the last part of the url of your google sheet. Ie. `https://docs.google.com/spreadsheets/d/1xlz2lMJph320OcxRxOpEJ_A7M0uXdAhCkl0V_9p2Kwc` would be `"1xlz2lMJph320OcxRxOpEJ_A7M0uXdAhCkl0V_9p2Kwc"`

## Developing

Here's a brief intro about what a developer must do in order to start developing
the project further:

```shell
git clone https://github.com/axiom4787/Axiom-Timesheet
pip install -r reqs.txt # WIP
```

Clone the repository and install required imports.

### Deploying / Publishing

Here is how to run the program. Only do this after following all prior instructions. 

```shell
python window.py
```
> Run the app


```shell
python window.py cs
```
> Run the app and log into the first timesheet log


```shell
python window.py mech
```
> Run the app and log into the second

## Features

What's all the bells and whistles this project can perform?
* Log time into 2 different logs on 2 different machines
* add more...

## Configuration

Here you should write what are all of the configurations a user can enter when
using the project.

#### Argument 1
Type: `String`  
Default: `'default value'`

State what an argument does and how you can use it. If needed, you can provide
an example below.

Example:
```bash
awesome-project "Some other value"  # Prints "You're nailing this readme!"
```

#### Argument 2
Type: `Number|Boolean`  
Default: 100

Copy-paste as many of these as you need.

## Contributing

When you publish something open source, one of the greatest motivations is that
anyone can just jump in and start contributing to your project.

These paragraphs are meant to welcome those kind souls to feel that they are
needed. You should state something like:

"If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome."

If there's anything else the developer needs to know (e.g. the code style
guide), you should link it here. If there's a lot of things to take into
consideration, it is common to separate this section to its own file called
`CONTRIBUTING.md` (or similar). If so, you should say that it exists here.

## Links

Even though this information can be found inside the project on machine-readable
format like in a .json file, it's good to include a summary of most useful
links to humans using your project. You can include links like:

- Project homepage: https://your.github.com/awesome-project/
- Repository: https://github.com/your/awesome-project/
- Issue tracker: https://github.com/your/awesome-project/issues
  - In case of sensitive bugs like security vulnerabilities, please contact
    my@email.com directly instead of using issue tracker. We value your effort
    to improve the security and privacy of this project!
- Related projects:
  - Your other project: https://github.com/your/other-project/
  - Someone else's project: https://github.com/someones/awesome-project/


## Licensing

One really important part: Give your project a proper license. Here you should
state what the license is and how to find the text version of the license.
Something like:

"The code in this project is licensed under MIT license."
