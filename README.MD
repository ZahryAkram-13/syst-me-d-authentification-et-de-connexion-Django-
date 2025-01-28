# Création d'un Système d'Authentification et Connexion avec Django

Ce document explique comment créer un système d'authentification et de connexion à l'aide de Django, en mettant en évidence les mesures de sécurité fournies par le framework ainsi que les validations supplémentaires que j'ai ajoutées pour renforcer la protection contre certaines vulnérabilités courantes.

---

## Fonctionnalités incluses

- Gestion des utilisateurs avec modèle personnalisé.
- Validation des formulaires pour éviter les attaques (comme les injections SQL ou XSS).
- Utilisation des décorateurs de Django pour protéger les vues sensibles.
- Messages de validation pour informer les utilisateurs des succès ou des erreurs (par exemple, "Compte créé avec succès").

---

## Sécurité fournie par Django

### 1. Protection contre les Injections SQL
Django utilise un ORM (Object-Relational Mapping) pour interagir avec la base de données, ce qui signifie que toutes les requêtes SQL sont automatiquement paramétrisées, évitant ainsi les injections SQL. Par exemple :

```python
# Django ORM empêche l'injection SQL
user = User.objects.filter(username="admin' --")
```
Cette requête est sécurisée par défaut, même si un utilisateur malveillant essaie d'injecter du code SQL.

### 2. Protection contre le Cross-Site Scripting (XSS)
Les gabarits (templates) de Django échappent automatiquement le contenu HTML dangereux, ce qui empêche l'exécution de scripts malveillants. Par exemple :

```html
<p>{{ user_input }}</p>
```
Si `user_input` contient `<script>alert('XSS')</script>`, cela sera rendu comme du texte brut.

### 3. Protection contre les Attaques CSRF (Cross-Site Request Forgery)
Django inclut un système de protection CSRF par défaut. Un jeton CSRF est généré et validé pour chaque requête POST, empêchant ainsi les attaques qui exploitent les sessions actives des utilisateurs.

---

## Mesures Supplémentaires de Sécurité

### Validation des Entrées Utilisateur
J'ai ajouté des fonctions pour vérifier et assainir les données entrées par les utilisateurs, comme la validation des noms de connexion pour éviter les caractères non autorisés et les scripts malveillants. Voici un exemple de fonction :

```python
import re
from html import escape

def is_valid_login_name(login_name):
    login_name = login_name.strip()
    if re.search(r'<[^>]*script[^>]*>|<[^>]*>', login_name, re.IGNORECASE):
        return False
    login_name = escape(login_name)
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9 _-]*$', login_name):
        return True
    return False
```

Cette fonction empêche les caractères non valides et les tentatives d'injection de scripts JavaScript dans les noms de connexion.

### Utilisation des Décorateurs
Les vues sensibles, comme la page de compte, sont protégées par le décorateur `@login_required`, ce qui garantit que seuls les utilisateurs authentifiés peuvent y accéder.

```python
from django.contrib.auth.decorators import login_required

@login_required
def account_page(request):
    return render(request, 'account.html')
```

### Utilisation des Messages
Les messages sont utilisés pour fournir des retours utiles à l'utilisateur après certaines actions (par exemple, connexion, inscription). Voici un exemple :

```python
from django.contrib import messages

def register(request):
    if form.is_valid():
        form.save()
        messages.success(request, "Votre compte a été créé avec succès !")
        return redirect('login')
    else:
        messages.error(request, "Erreur lors de la création du compte.")
```

---

## Exemples de Vulnérabilités et Protection

### 1. Injection SQL
Un utilisateur tente d'entrer le texte suivant comme identifiant :

```
admin' OR 1=1 --
```
Django bloque cette tentative grâce à son ORM, qui paramètre automatiquement les requêtes.

### 2. Cross-Site Scripting (XSS)
Un utilisateur malveillant essaie d'injecter du code JavaScript :

```
<script>alert('XSS')</script>
```
Les gabarits de Django échappent automatiquement ces scripts, empêchant leur exécution.

### 3. Cross-Site Request Forgery (CSRF)
Une attaque consiste à forcer un utilisateur à exécuter une action sans son consentement (par exemple, changer un mot de passe). Django génère un jeton CSRF unique pour chaque formulaire POST, ce qui empêche de telles attaques.

---

## Conclusion
En combinant les protections de Django et les validations personnalisées des entrées, ce système offre un haut niveau de sécurité contre les attaques courantes. Vous pouvez être assuré que les données des utilisateurs et les actions critiques sont protégées.

