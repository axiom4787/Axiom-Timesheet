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

## Contributing

If you are looking to contribute, first, Thank You!

If you want to jump in, create a branch, add some features, and make a pull request back to main. 

Right now we are looking for topics listed in the branches so contributions there are warmly welcome. 
If proposing a new feature, just make a pull to main and we'll see how applicable and useful it is.

## Licensing
**Liscenced under MIT.**

Copyright 2025 Respective Copyright Holders and Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
