from database.DAO import DAO
from model.model import Model

mymodel = Model()

mymodel.creaGrafo(valore1, valore2)

attori = DAO.getAllActors(valore1, valore2)

print(len(attori))

#NODI
n = mymodel.getNodi()
print(f"il Grafo ha {len(n) } nodi")

#archi

#tutto dettagli
n, m = mymodel.getGrafoDetails()
print(f"Grafo creato: {n} nodi, {m} archi")
