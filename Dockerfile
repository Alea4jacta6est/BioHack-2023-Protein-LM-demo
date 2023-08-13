FROM python:3.10

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . /BioHack-2023-Protein-LM-demo
WORKDIR /BioHack-2023-Protein-LM-demo
ENV PYTHONPATH /BioHack-2023-Protein-LM-demo

EXPOSE 8501
CMD streamlit run app.py