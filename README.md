# Leihladen Web-App

Entstanden im Rahmen meiner Masterarbeit mit dem Thema "Digitalisierungsprozesse in der Sharing Economy am Beispiel einer Leihladen Web-App".

Die Progressive Web-App wurde entwickelt, um das in der Arbeit erarbeitete Konzept zur Digitalisierung des Ausleihprozesses eines Leihladens zu veranschaulichen. Die Web-App ermöglicht Benutzern einen einfachen Zugang zu Ressourcen, während das Personal von einer effizienten Verwaltungsoberfläche profitiert.

Live-Demo: ~~https://leihladen.schuster-julian.de/~~

## Technologie-Stack
- Vue.js
* Django
+ SQLite

## Setup für Vue.js

1. Navigiere in das Verzeichnis "leihladen_vue":
```
cd leihladen_vue
```

2. Installiere die erforderlichen Pakete:
```
npm install
```

3. Starte den Vue Development Server:
```
npm run serve
```

## Setup für Django

1. Erstelle eine virtuelle Umgebung:
```
virtualenv environment_3_10_5 
```

Wenn virtualenv nicht installiert ist:
```
pip install virtualenv
```

2. Aktiviere die virtuelle Umgebung (Linux):
```
source environment_3_10_5/bin/activate
```

Aktiviere die virtuelle Umgebung (Windows):
```
source environment_3_10_5/Scripts/activate
```

3. Installiere die Django-Abhängigkeiten:
```
pip install -r req.txt
```

4. Erstelle die SQLite-Datenbank und führe die Migration durch:
```
cd leihladen_django
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```

5. Erstelle einen Admin-Account:
```
python manage.py createsuperuser
```

6. (Optional) Fülle die Datenbank mit Beispieldaten:
```
python loadIntoDB.py
```

7. Starte den Django Development Server:
```
python manage.py runserver
```

## Kontakt
Julian Schuster (Schuster.Julian@web.de)
