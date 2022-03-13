#!/usr/bin/env bash

# to test if not missing any dependencies 

echo "Cloning repository ..."
git clone git@github.com:cacoch/crime-dashboard.git . 

echo "Creating venv ..."
python -m venv . 
source bin/activate

echo "Installing packages ..."
pip install -r requirements.txt 


streamlit run app.py


