import streamlit as st
import requests
import biotite.structure.io as bsio
import os

from rendering import render_mol, read_fasta
from predictors import SSPredictor, ProtTransSSPredictor
from rendering import ret_secondary_figure


DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAA\
            LRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSST\
            NFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQA\
            LIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
st.set_page_config(layout="wide")
st.sidebar.title("Protein Structure Prediction")
st.subheader("Visualization of predicted protein structure")
option = st.sidebar.selectbox(
    "How would you like upload protein data?", ("Paste a sequence", "Upload FASTA file")
)
if option == "Paste a sequence":
    sequences = {
        "test protein": st.sidebar.text_area(
            "Paste your sequence", DEFAULT_SEQ, height=275
        )
    }
else:
    uploaded_file = st.sidebar.file_uploader("Upload a file")
    if uploaded_file:
        ff = uploaded_file.readlines()
        sequences = read_fasta(ff)
model_option = st.sidebar.selectbox(
    "Choose the model", ("ESM", "AlphaFold", "ProtTrans", "Ankh")
)
dimension_option = st.sidebar.selectbox(
    "Which structure do you prefer to visualize?", ("Secondary", "Tertiary")
)


def update(sequence, model, header, dimension):
    if dimension == 'Secondary':
        if model == "ESM":
                pipe = SSPredictor(model_name='esm2_35m_tuned')
                res = pipe.predict(sequence)
                classif_res = pipe.convert_esm2_output(res)
                fig = ret_secondary_figure(classif_res)
                st.text(f"Protein description: {header}")
                st.pyplot(fig)
        # elif model == 'ProtTrans':
        #     pipe = ProtTransSSPredictor()
        #     # Compute embeddings and/or secondary structure predictions
        #     results = get_embeddings( pipe.model, pipe.tokenizer, sequence)
        #     classif_res = pipe.convert_prottrans_output(results)
        #     fig = ret_secondary_figure(classif_res)
        #     st.pyplot(fig)
        elif model == 'ProtGPT2':
            pipe = SSPredictor(model_name='nferruz/ProtGPT2')
        else:
            st.error("Not implemented")
    else:
        if model == "ESM":
            # 3D-Case
            #TODO: MAKE A REAL MODEL INFERENCE CALL
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
            response = requests.post(
                "https://api.esmatlas.com/foldSequence/v1/pdb/",
                headers=headers,
                data=sequence,
            )
            pdb_string = response.content.decode("utf-8")
            st.text(f"Protein description: {header}")
            render_mol(pdb_string)
            os.makedirs("data/pdb_files/", exist_ok=True)
            with open("data/pdb_files/predicted.pdb", "w") as f:
                f.write(pdb_string)
        else:
            st.error("Not implemented")
         

predict = st.sidebar.button("Predict")
if predict:
    for header, seq in sequences.items():
        update(seq, model_option, header, dimension_option)
