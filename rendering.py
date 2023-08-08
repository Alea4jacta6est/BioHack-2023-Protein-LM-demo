from stmol import showmol
import py3Dmol


def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb, "pdb")
    pdbview.setStyle({"cartoon": {"color": "spectrum"}})
    pdbview.setBackgroundColor("white")  # ('0xeeeeee')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height=500, width=800)


def read_fasta(content):
    """
    Reads a FASTA file and returns a dictionary 
    where keys are the headers (without '>') 
    and values are the sequences.
    """
    sequences = {}
    header = None
    for line in content:
        line = line.decode("utf-8").strip()
        if not line:
            continue
        if line.startswith(">"):
            header = line[1:]
            sequences[header] = []
        else:
            if not header:
                raise ValueError("File does not start with a header!")
            sequences[header].append(line)
    for header, seq_lines in sequences.items():
        sequences[header] = "".join(seq_lines)
    return sequences
