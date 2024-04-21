# Discord Bot Personality Mobius
Temperamental Python (3.12) Discord Bot

## How to run locally
1. Install [Python](https://www.python.org/downloads/) (obviously)
2. Clone
3. CD to cloned repository and open with VSCode 
```sh
code .
```
4. Create a Python virtual environment ((VSCode VE Setup)[https://code.visualstudio.com/docs/python/python-tutorial#_create-a-virtual-environment])
5. Install project dependencies
```sh 
python3 -m pip install -r requirements.txt
```
6. Create `.env` file at the project level with bot token
```sh
TOKEN=discord_bot_token_without_quotes
```
7. Run Server
```sh
python3 main.py runserver
```