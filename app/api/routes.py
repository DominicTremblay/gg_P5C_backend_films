from flask import jsonify, request
from app.extensions import db

# Activer la ligne c-dessous lorsque le modele est cree
from app.modeles import Film, Utilisateur, Commentaire
from app.api import api_bp

# Creer les routes pour les operations CRUD


@api_bp.route("/", methods=["GET"])
def accueil():
    return "Page d'accueil"


@api_bp.route("/films", methods=["GET"])
def liste_films():
    films = Film.query.all()

    if not films:
        return jsonify({"message": "Aucun film disponible"}), 404

    print(films)
    films_json = [
        {
            "id": film.id,
            "titre": film.titre,
            "description": film.description,
            "genre": film.genre,
            "annee_sortie": film.annee_sortie,
        }
        for film in films
    ]
    return jsonify(films_json)


@api_bp.route("/films/<int:id>", methods=["GET"])
def obtenir_film(id):
    film = Film.query.get(id)

    if not film:
        return jsonify({"message": "Film non disponible"}), 404

    film_json = {
        "id": film.id,
        "titre": film.titre,
        "genre": film.genre,
        "annee_sortie": film.annee_sortie,
    }
    return jsonify(film_json)


@api_bp.route("/films", methods=["POST"])
def creer_film():

    film_data = request.get_json()

    film = Film(
        titre=film_data["titre"],
        description=film_data["description"],
        annee_sortie=film_data["annee_sortie"],
        genre=film_data["genre"],
    )

    db.session.add(film)
    db.session.commit()

    return jsonify({
        "message": "Film cree avec succes",
        "film": {
            "id": film.id,
            "titre": film.titre,
            "genre": film.genre,
            "annee_sortie": film.annee_sortie
        }
    }), 201

# {
# 	"titre": "The Batman",
# 	"description": "Bruce Wayne affronte le Riddler, un tueur mystérieux, dans un Gotham sombre.",
# 	"annee_sortie": 2022,
# 	"genre": "Action epique"
# }