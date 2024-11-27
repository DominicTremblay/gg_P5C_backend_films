from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db

# Activer la ligne c-dessous lorsque le modele est cree
from app.modeles import Film, Utilisateur, Commentaire
from app.api import api_bp

# Creer les routes d'authentifications


# Creer le login (session)
@api_bp.route("/session", methods=["POST"])
def ouvrir_session():
    data = request.get_json()
    print(data)
    utilisateur = Utilisateur.query.filter_by(courriel=data["courriel"]).first()

    # valider le mot de passe
    if not utilisateur or not utilisateur.valide_mot_passe(data["mot_passe"]):
        return jsonify({"erreur": "Donnees d'authentifcation invalides"})

    # l'utilisateur est authentifie, creer le jwt
    jeton_jwt = create_access_token(identity=utilisateur.id)

    return (
        jsonify(
            {
                "jeton": jeton_jwt,
                "id": utilisateur.id,
                "nom": utilisateur.nom,
                "courriel": utilisateur.courriel,
            }
        ),
        201,
    )


# Creer Incription


@api_bp.route("/inscription", methods=["POST"])
def incription():
    data = request.get_json()

    print("DATA ========")
    print(data["mot_passe"])

    # A faire validation si l'utilisateur existe deja

    utilisateur = Utilisateur(nom=data["nom"], courriel=data["courriel"])
    utilisateur.encode_mot_passe(data["mot_passe"])

    db.session.add(utilisateur)
    db.session.commit()

    return jsonify({"message": "L'utilisateur a ete creer avec succes"}), 201


# Creer les routes pour les operations CRUD


@api_bp.route("/", methods=["GET"])
@jwt_required()
def accueil():

    id = get_jwt_identity()
    print(f"Id utilisateur: {id}")

    utilisateur = Utilisateur.query.get(id)

    return {"nom": utilisateur.nom, "courriel": utilisateur.courriel}


@api_bp.route("/films", methods=["GET"])
@jwt_required()
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
@jwt_required()
def obtenir_film(id):
    try:
        film = Film.query.get(id)

        if not film:
            return jsonify({"message": "Film non disponible"}), 404

        film_json = {
            "id": film.id,
            "image_url": film.image_url,
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


@api_bp.route("/films/<int:id>", methods=["DELETE"])
def detruire_film(id):
    try:
        film = Film.query.get_or_404(id)
        db.session.delete(film)
        db.session.commit()
        return (
            jsonify({"message": f"Le film {film.titre} a ete supprime avec succes"}),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": "Une erreur s'est produite"}), 500
