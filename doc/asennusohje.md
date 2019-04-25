# Asennusohje
Tässä ohjeessa vaiheittain sovelluksen asentaminen ja suorittaminen paikallisesti lähdekoodista. Projektin juuressa on `Procfile` Herokussa suorittamista varten.

## Ennakkovaatimukset
- PostgreSQL palvelin johon viitataan ympäristömuuttujalla `DATABASE_URL` (ks. [ohje postgresql asennukseen](./postgresql_asennus.md))
- Python 3.6

## Virtuaaliympäristön luominen ja käyttöönotto
Kloonattuasi repon, suorita juuressa `python3 -m venv venv`, jolla saat luotua projektille virtuaaliympäristön johon riippuvuudet voidaan turvallisesti asentaa. Virtuaaliympäristö löytyy projektin juuresta hakemistosta `venv` ja voidaan ottaa käyttöön ajamalla `source venv/bin/activate`

## Asenna riippuvuudet ja suorita
Otettuasi virtuaaliympäristön käyttöön, asenna riippuvuudet komennolla `pip install -r requirements.txt`. Mikäli tietokanta on alustettu oikein ja riippuvuuksien asennus onnistui, voit nyt suorittaa ohjelman kutsumalla projektin juuressa `python3 run.py`
