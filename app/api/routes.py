from flask import jsonify, request
from app.extensions import db 
# Activer la ligne c-dessous lorsque le modele est cree
# from app.modeles import Film
from app.api import api_bp

# Creer les routes pour les operations CRUD

@api_bp.route('/', methods=['GET'])
def accueil():
    return "Page d'accueil"