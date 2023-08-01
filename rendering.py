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
