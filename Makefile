# Colors for echos 
ccend=$(shell tput sgr0)
ccso=$(shell tput smso)
create_pyenv_env : 
	@pyenv virtualenv 3.8.6 house_prediction
	@echo "$(ccso)--> Saisir dans la console : pyenv activate house_prediction && make install_requirements $(ccend)"
#	source "~/home/pierre/.pyenv/versions/3.8.6/envs/house_predictionbin/activate"

install_requirements: requirements.txt
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@pip freeze > requirements.txt
clean:
	rm -rf __pycache__