from stmol import showmol
import py3Dmol
from visuliaze_secondary import HelixPlotter, SheetPlotter
import biotite.sequence as seq
import biotite.sequence.graphics as graphics
import matplotlib.pyplot as plt

TYPE_NAMES = ['helix', 'sheet']


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


def ret_secondary_figure(classif_res):
    annotation_lst = []
    prev_el = classif_res[0]
    prev_pos = 1
    cur_pos = 1
    for cur_el in classif_res[1:]:
        cur_pos+=1
        if cur_el!=prev_el and prev_el != 2:
            annotation_lst.append(seq.Feature("SecStr", [seq.Location(prev_pos, cur_pos)], 
                                              {"sec_str_type" : TYPE_NAMES[prev_el]})
                                 )
            prev_pos = cur_pos
        elif cur_el!=prev_el and prev_el == 2:
            prev_pos = cur_pos
        prev_el = cur_el
        
    if prev_pos!=cur_pos and cur_el!=2:
        annotation_lst.append(seq.Feature("SecStr", [seq.Location(prev_pos, cur_pos)], 
                                              {"sec_str_type" : TYPE_NAMES[prev_el]})
                                 )
    
    annotation = seq.Annotation(annotation_lst)
    fig = plt.figure(figsize=(8.0, 3.0))
    ax = fig.add_subplot(111)
    graphics.plot_feature_map(
            ax, annotation, symbols_per_line=100,
            show_numbers=True, show_line_position=True,
            # 'loc_range' takes exclusive stop -> length+1 is required
            loc_range=(1,len(classif_res)+1),
            feature_plotters=[HelixPlotter(), SheetPlotter()]
        )
    fig.tight_layout()

    return fig