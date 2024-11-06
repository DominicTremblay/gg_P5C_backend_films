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
    try:
        films = Film.query.all()

        if not films:
            return jsonify({"message": "Aucun film disponible"}), 404

        print(films)
        films_json = [
            {
                "id": film.id,
                "image_url": film.image_url,
                "titre": film.titre,
                "description": film.description,
                "genre": film.genre,
                "annee_sortie": film.annee_sortie,
            }
            for film in films
        ]
        return jsonify(films_json)

    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": "Une erreur s'est produite"}), 500


@api_bp.route("/films/<int:id>", methods=["GET"])
def obtenir_film(id):
    try:
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

    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": "Une erreur s'est produite"}), 500


@api_bp.route("/films", methods=["POST"])
def creer_film():

    try:
        film_data = request.get_json()

        film = Film(
            titre=film_data["titre"],
            description=film_data["description"],
            annee_sortie=film_data["annee_sortie"],
            genre=film_data["genre"],
        )

        db.session.add(film)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Film cree avec succes",
                    "film": {
                        "id": film.id,
                        "titre": film.titre,
                        "genre": film.genre,
                        "annee_sortie": film.annee_sortie,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": "Une erreur s'est produite"}), 500


# {
# 	"titre": "The Batman",
# 	"description": "Bruce Wayne affronte le Riddler, un tueur mystérieux, dans un Gotham sombre.",
# 	"annee_sortie": 2022,
# 	"genre": "Action epique"
# }

@api_bp.route("/films/<int:id>", methods=["PUT"])
def mise_a_jour_film(id):
    try:
        film = Film.query.get_or_404(id)
        film_data = request.get_json()

        if "titre" in film_data:
            film.titre = film_data["titre"]

        if "description" in film_data:
            film.description = film_data["description"]

        if "annee_sortie" in film_data:
            film.annee_sortie = film["annee_sortie"]

        if "genre" in film_data:
            film.genre = film_data["genre"]

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Film mis à jour avec succès",
                    "film": {
                        "id": film.id,
                        "titre": film.titre,
                        "genre": film.genre,
                        "annee_sortie": film.annee_sortie,
                        "description": film.description,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": "Une erreur s'est produite"}), 500


@api_bp.route('/films/<int:id>', methods=["DELETE"])
def detruire_film(id):
    try:
        film = Film.query.get_or_404(id)
        db.session.delete(film)
        db.session.commit() 
        return jsonify({"message": f"Le film {film.titre} a ete supprime avec succes"}), 200    

    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": "Une erreur s'est produite"}), 500