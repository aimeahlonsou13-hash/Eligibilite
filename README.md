# Application de prédiction d'éligibilité au crédit

## Contenu du dossier
- `app.py` : l'application Streamlit
- `model.pkl` : ton modèle de régression logistique (renommé depuis `modèle.pkl` pour éviter les problèmes d'accents dans les chemins)
- `requirements.txt` : les bibliothèques nécessaires

## Installation (à faire une seule fois)

1. Ouvre une invite de commande (PowerShell ou CMD) dans le dossier où tu as placé ces 3 fichiers.
   Exemple : si le dossier est `D:\vid logiciel\Data science\Exercice\Akp`, tape :
   ```
   cd "D:\vid logiciel\Data science\Exercice\Akp"
   ```

2. Installe les bibliothèques nécessaires :
   ```
   pip install -r requirements.txt --break-system-packages
   ```
   (si `--break-system-packages` provoque une erreur sur ta machine, retire simplement cette option)

## Lancer l'application

Toujours dans le même dossier, tape :
```
streamlit run app.py
```

Cela ouvre automatiquement une page dans ton navigateur (en général à l'adresse `http://localhost:8501`). Si elle ne s'ouvre pas automatiquement, copie l'adresse affichée dans le terminal et colle-la dans ton navigateur.

## Utilisation
Remplis le formulaire (genre, statut marital, revenu, montant du prêt, historique de crédit, etc.) puis clique sur **"Évaluer l'éligibilité"**. Le résultat (éligible / non éligible) s'affiche avec la probabilité associée.

## ⚠️ Point important à vérifier
L'encodage des variables catégorielles (Gender, Married, Education, Self_Employed, Property_Area, Dependents) utilisé dans `app.py` suit la convention la plus courante pour ce dataset :

| Variable | Encodage |
|---|---|
| Gender | Male=1, Female=0 |
| Married | Yes=1, No=0 |
| Education | Graduate=1, Not Graduate=0 |
| Self_Employed | Yes=1, No=0 |
| Property_Area | Urban=2, Semiurban=1, Rural=0 |
| Dependents | "3+" → 3 |

**Si tu as le code/notebook utilisé pour entraîner `modèle.pkl`, vérifie l'encodage exact qui a été appliqué avant l'entraînement.** Si l'encodage est différent, les prédictions de l'application seront incorrectes même si le code fonctionne sans erreur. Dans ce cas, ajuste les dictionnaires dans la fonction `encode_inputs()` du fichier `app.py`.

## Déploiement en ligne (optionnel)
Une fois que l'application fonctionne en local, tu peux la déployer gratuitement sur **Streamlit Community Cloud** :
1. Crée un dépôt GitHub contenant `app.py`, `model.pkl`, `requirements.txt`
2. Va sur https://streamlit.io/cloud, connecte-toi avec GitHub
3. Sélectionne ton dépôt et clique sur "Deploy"
