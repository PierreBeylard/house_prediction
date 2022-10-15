# House prices Prediction
## Objective of the project :
The purpose of the project is to predict house prices in France at national level (exclusion of Alsace Moselle et TOM)

## Introduction to the external ressources used to conduct the project
*Data found on https://www.data.gouv.fr/fr/pages/donnees-machine-learning/*
This dataset regroups all real estates transactions that occured in 2021 in France (exclusion of Alsace Moselle et TOM)
The project also use the governemental API Adresse : https://guides.etalab.gouv.fr/apis-geo/1-api-adresse.html#gros-consommateurs-de-l-api-api-adresse-data-gouv-fr
and finaly some open sources API in order to retreive IRIS code based on coordinates : https://public.opendatasoft.com
Data enrichment thanks to INSEE open data :
 * https://www.insee.fr/fr/information/2383389 : Documentation sur les bases de données infracommunales à l'IRIS
 * https://www.insee.fr/fr/statistiques/5650714#consulter : Couples - Familles - Ménages en 2018
 * https://www.insee.fr/fr/statistiques/5650708#dictionnaire Activité des résidents en 2018
 * https://www.insee.fr/fr/statistiques/5650749#dictionnaire : Logement en 2018


## Project layout :
2 main parts :
  * Model creation phase that includes :
      * Notebooks for iteration
      * POO code used to create the model
  * API creation phase :
      * Front : html/Css files
      * Back: python files

Project skeleton :
├── API :
└├──── main.py
└├──── data.py
└├──── enrichissement.py
└├──── retraitement.py
└├──── model.sav
├── House prediction package
└├──── data.py
└├──── ml.py
└├──── pipeline.py
└├──── preprocessing.py
├── notebooks
└├──── Data Discovery.ipynb
└├──── Model.ipynb
├── static :
└├──── form-validation.js
└├──── logo.png
└├──── proprieté.png
└├──── cover.css
├── templates
└├──── index.html
└├──── cover.html
├── .gitignore
├── README.md
├── requirements.txt


## heroku production
Best is tu use heroku CLI to have access to logs :
`heroku logs --tail `
1. create an app on heroku website
2. link the app to github repository
3. activate automatic deploys
4. create the file named Procfile (without extension) at project root and add :
`web: uvicorn api.main:app --host=0.0.0.0 --port=${PORT:-5000}`
4. add postgres addons
`heroku addons:create heroku-postgresql:hobby-dev`
5. create a dump of local postgres db
  ` PGPASSWORD="password" pg_dump -h localhost -U "user" "db name" --no-owner --no-acl -f database.dump`
6. upload dump db into prod db : DB_URI can be found into the settings of heroku postgres
` heroku pg:psql "DB_URI" --app propertyestimatorsimplon < database.dump`
7. Attention points :
 * Be carrefull connection to your db must be done through environment variables thanks to that, you can modify this variable directly in Heroku in settings config vars
 * Nowodays (october 2022 know issue with sql alchemy https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy) forces us to change DB_uri name postgres to postgresql
 * Import and path must be setup from Procfile point of view. If so, local test app must be launch from root path:
 `uvicorn api.main:app --reload`
* Don't forget to start postgresql database when running local test :)
 `sudo service postgresql start`
* Large file heroku & git. It is possible to upload large file on Github using git LFS (with some limitation):
    1. dowload setup git lfs - https://git-lfs.github.com./
    2. install : `git lfs install`
    3. track large files with extension : `git lfs track "*.pickle"`
    4.  `git add .gitattributes`
    5. classique steps : `git add file.pickle`, `git commit -m "Add design file"`, `git push origin master`
Unfortunetely, heroku does not support git lfs natively
Some extra steps have to be executed before using the file in Heroku :
    1. Create a personnal access token for github accouut
    2. Add heroku buildpack for Git-LFS `heroku buildpacks:add (buildpack_git_lfs_location) -a (your_heroku_app_name)
    3. Add configuration variable to heroku app : HEROKU_BUILDPACK_GIT_LFS_REPO with value github repo

 |git reset --soft HEAD~2
