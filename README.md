# how to setup?
- create a virtual env
- install the requirements
- run the app 
- we use alembic for database migration so connect to db in .env add the path of your database [mySQL]
  - alembic revision --autogenerate -m "initials"
  - alembic upgrade head
- to connect to discord bot, generate bot or ask me token to use same as this bot 
- use that .env.example and copy to .env and fill the necessary stuffs accordingly

# requirements for contributors?
- not much just use pyright as a lsp
- ruff_format and ruff_organize_imports for formatting
- try best to add documentation in # [comments] of what you did and whats its for, so that other contributors can know 


