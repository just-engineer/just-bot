modify enviroment .yml files:
- condaenv.yml automaticaly generates by Conda;
- update.yml file for manually adding packages, installed with pip

for create new project enviroment type in terminal:
conda env create -f condaenv.yml
conda activate just-bot
conda env update --file update.yml

for update existed enviroment type in terminal:
conda env update --file condaenv.yml
and\or
conda env update --file update.yml