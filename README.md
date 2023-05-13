# Sharing Economy Web-App

Entstanden im Rahmen meiner Masterthesis "Digitalisierungsprozesse in der Sharing Economy am Beispiel einer Leihladen Web-App".

Live-Demo: https://leihladen.schuster-julian.de/

username: admin

passwort: leihladen123

# Installation Vue

In leihladen_vue navigieren:
```
cd leihladen_vue
```

Packages installieren:
```
npm install
```

Vue development Server starten:
```
npm run serve
```

# Installation Django

Virtuelle Umgebung erstellen:
```
virtualenv environment_3_10_5 
```

Wenn virtualenv nicht installiert ist:
```
pip install virtualenv
```

Virtuelle Umgebung aktivieren (Linux):
```
source environment_3_10_5/bin/activate
```

Virtuelle Umgebung aktivieren (Windows):
```
source environment_3_10_5/Scripts/activate
```

Django requirements installieren:
```
pip install -r req.txt
```

SQLite Datenbank erstellen und migration ausführen:
```
cd leihladen_django
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```

Django development Server starten:
```
python manage.py runserver
```
