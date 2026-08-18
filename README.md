# AllPhones

Marketplace d'annonces de téléphones et ordinateurs de seconde main, avec médiation obligatoire par AllPhones.

## Règle métier centrale
- Le déposant remet son bien et ses informations à AllPhones.
- L'agence crée/publie l'annonce et fixe manuellement sa marge.
- Le prix public est calculé automatiquement : prix d'acquisition + marge AllPhones.
- Un acheteur intéressé envoie sa demande uniquement à AllPhones.
- Les coordonnées du déposant ne sont jamais affichées à l'acheteur.
- Les coordonnées de l'acheteur ne sont jamais affichées au déposant.
- AllPhones traite la demande et organise la rencontre dans ses bureaux.
- Le suivi de la demande et du rendez-vous reste dans l'espace d'administration.

## Démarrage local

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Administration : `/admin/`
