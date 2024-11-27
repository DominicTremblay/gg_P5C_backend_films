from app.extensions import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Table d'association pour la relation many-to-many entre Film et Utilisateur
favoris = db.Table(
    'favoris',
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True),
    db.Column('utilisateur_id', db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
)

class Film(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(50))
    annee_sortie = db.Column(db.Integer)

    # Relation one-to-many avec Commentaire
    commentaires = db.relationship('Commentaire', back_populates='film', cascade='all, delete-orphan')

    # Relation many-to-many avec Utilisateur
    utilisateurs = db.relationship(
        'Utilisateur', secondary='favoris', back_populates='films'
    )

class Utilisateur(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    courriel = db.Column(db.String(100), nullable=False, index=True, unique=True)
    mot_passe_hache = db.Column(db.String(256), nullable=False)
    avatar_url = db.Column(db.String(200), nullable=True)

    # Relation one-to-many avec Commentaire
    commentaires = db.relationship('Commentaire', back_populates='utilisateur', cascade='all, delete-orphan')

    # Relation many-to-many avec Film
    films = db.relationship(
        'Film', secondary='favoris', back_populates='utilisateurs'
    )

    def encode_mot_passe(self, mot_passe):
        self.mot_passe_hache = generate_password_hash(mot_passe)

    def valide_mot_passe(self, mot_passe):
        return check_password_hash(self.mot_passe_hache, mot_passe)

    @login.user_loader
    def load_user(id):
        return db.session.get(Utilisateur, int(id))

class Commentaire(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False)

    # Clé étrangère vers Film
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)

    # Clé étrangère vers Utilisateur
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)

    # Relation avec Film et Utilisateur
    film = db.relationship('Film', back_populates='commentaires')
    utilisateur = db.relationship('Utilisateur', back_populates='commentaires')
