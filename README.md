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
├── templates       
└├──── index.html  
├── .gitignore    
├── README.md      
├── requirements.txt     
