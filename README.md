# Discord Bot Personality Mobius
Temperamental Python (3.12) Discord Bot

Inspired by [kkrypt0nn](https://github.com/kkrypt0nn/Python-Discord-Bot-Template)

## How to run locally
1. Install [Python](https://www.python.org/downloads/) (obviously)
2. Clone
3. CD to cloned repository and open with VSCode:
```sh
code .
```
4. Create a Python virtual environment ([VSCode VE Setup](https://code.visualstudio.com/docs/python/python-tutorial#_create-a-virtual-environment))
5. Install project dependencies:
```sh 
python3 -m pip install -r requirements.txt
```
6. Create a `config.json` file at the project level and add a `prefix` and `invite_link`:
```json
{
    "prefix": "!",
    "invite_link": "https://discord.com/oauth2/authorize?client_id=1231284567344812033&permissions=633318429163329&scope=bot"
}
```
7. Create an `.env` file at the project level with a bot `TOKEN` from Discord's [developer portal](https://discord.com/developers/applications):
```sh
TOKEN=discord_bot_token_without_quotes
```
8. Start the server:
```sh
python3 main.py runserver
```