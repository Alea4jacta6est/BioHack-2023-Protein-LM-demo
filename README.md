# BioHack-2023-Protein-LM-demo

A demo application that uses Protein Languages models to visualize secondary and tertiary structure prediction results

## Run the application locally:

- Install dependencies using `pip install requirements.txt`
- Download fine-tuned models (ask the authors of this repository) and update paths
- Run the application inside the downloaded repository `streamlit run app.py`

## Run the application through docker:

`docker build . -t "app:v1"`

`docker run -p 8501:8501 "app:v1"`


![2023-08-13 13 05 47](https://github.com/Alea4jacta6est/BioHack-2023-Protein-LM-demo/assets/26580860/92dcaf52-f472-4c94-9219-92fabbe6ecdc)
