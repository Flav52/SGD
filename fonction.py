from pymongo import MongoClient
from bson.objectid import ObjectId
uri="mongodb://fr108211:fr108211@mongo/?authSource=fr108211&authMechanism=SCRAM-SHA-1"

#On recupère la connexion à mongoDB
c=MongoClient(uri)
db=c.fr108211
db

#Affiche tous les jeux disponibles sur le catalogue pour chaque categorie :
def jeuxCategorie():
    c = db.jeux.aggregate([{"$unwind":"$categorie"},{"$sort":{"nom":1}},{"$group":{"_id":"$categorie","jeux":{"$push":{"nom":"$nom"}}}},{"$sort":{"_id":1}}])
    for doc in c :
        #Pour chaque categorie on recupère les jeux et on les affiche
        print("Categorie "+ doc["_id"]+" :")
        for j in doc["jeux"]:
            print("\t" + j["nom"])
        print()

#Affichage des avis publiés par un utilisateur
def informationUser(pseudo):
    c = db.jeux.aggregate([{"$unwind" : "$avis"},{"$match" : {"avis.user.pseudo" : pseudo}},
                            {"$group" : {"_id" : "$avis"}}])
    commentaire = False
    for doc in c:
        #Pour chacun des avis, on affiche les informations.
        print("\t" + "Note : " + str(doc["_id"]["note"]))
        print("\t\t" + str(doc["_id"]["commentaire"]))
        print("")
        commentaire = True
    if not commentaire :
        #Si aucun commentaire
        print("L'utilisateur " + pseudo + " n'a jamais laisse de commentaire.")

#Fait varier tous les prix en fonction d'un pourcentage donné pour simuler des soldes
def VariationPrixGlobal(pourcentage):
    c = db.jeux.find({"prix" : { "$exists" : True}});
    for doc in c:
        variation = ((pourcentage)*doc["prix"])/100
        db.jeux.update({"nom":doc["nom"]},{"$set":{"prix":variation}})
        doc["prix"] = variation
        print("Le prix du jeu " + doc["nom"] + " a varie de " + str(pourcentage) + " pourcent. Le prix est maintenant de : " + str(doc["prix"]) + "euro.")

#Suppression des descriptions :
def SuppressionDescription():
    #On recupère tous les jeux, et on supprime l'attribut dans le document
    db.jeux.update_many({"description" : {"$exists" : True}},{"$unset" : {"description" : ""}})
    print("Descriptions effacees")

#Affichage de la note moyenne, maximum et minimum de chaque catégorie.
def MoyMinMax():
    c = db.jeux.aggregate([{$group:[_id: "$categorie", moyenne : {$avg: "$avis.note"}, minimal : {$min : "$avis.note"}, maximal : {$max : "$avis.note"}]}])
    for doc in c:
        print("La note moyenne de la categorie" + doc["categorie"] + " est de " + str(doc["_id"][moyenne]))
        print("La note minimal de la categorie" + doc["categorie"] + " est de " + str(doc["_id"][minimal]))
        print("La note maximal de la categorie" + doc["categorie"] + " est de " + str(doc["_id"][maximal]))


#Affiche la moyenne des notes des user qui ont commenté dans au moins 2 catégories différentes
def moyUser2Comment():
    c = db.jeux.aggregate({$unwind: {"categorie"}, $group: [_id:"$pseudo", sum:{$sum: {"$avis.commentaire" : 2}}]})
    for doc in c:
        count = 0
        note = 0
        for i in doc["pseudo"]
            count=count+1
            note = note + doc["note"]
            for j in doc["pseudo"]
                avg = note/count
                print("user : " + str(doc["_id"]) + " note moyenne :" + avg)

#La fonction est pas top mais en voiture j'ai du mal à réflechir, sorry



#jeuxCategorie()
informationUser("LMAV")
#VariationPrixGlobal(90)
#SuppressionDescription()