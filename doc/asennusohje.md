# Asennusohje

## Lähdekoodin noutaminen
Navigoi terminaalissa hakemistoon johon haluat tallettaa lähdekoodin paikallisesti ja suorita

```bash
git clone https://github.com/Kailari/tsoha-19.git
```
Sovelluksen lähdekoodi löytyy nyt hakemistosta `tsoha-19`


## Suorittaminen paikallisesti

### Ennakkovaatimukset
Käytettävissä olevan Python-version tulee olla vähintään 3.6.

Sovellus tarvitsee toimiakseen PostgreSQL-tietokantapalvelimen, jonka versio on 11.2 tai korkeampi. Lisätietoa tietokantapalvelimen asennuksesta [täältä](./postgresql_asennus.md).

Sovellus etsii käytettävää tietokantaa ympäristömuuttujasta `DATABASE_URL` ja käytettävää porttia ympäristömuuttujasta `PORT` joten ne tulee olla asetettu joko `.env`-tiedostolla tai jollain muulla tapaa ennen sovelluksen suorittamista.

### Virtuaaliympäristön luominen ja käyttöönotto
Suorita projektin juuressa 

```bash
python3 -m venv venv
```

Tämä luo projektille python-virtuaaliympäristön johon riippuvuudet voidaan turvallisesti asentaa vaikuttamatta mahdollisiin muihin python-sovelluksiin. Virtuaaliympäristö löytyy projektin juuresta hakemistosta `venv` ja voidaan ottaa käyttöön suorittamalla 

```bash
source venv/bin/activate
```

### Asenna riippuvuudet ja suorita
Otettuasi virtuaaliympäristön käyttöön, asenna riippuvuudet komennolla
```bash
pip install -r requirements.txt
```

Mikäli tietokanta ja ympäristömuuttujat on alustettu oikein ja riippuvuuksien asennus onnistui, voit suorittaa ohjelman kutsumalla projektin juuressa

```bash
python3 run.py
```

Sovellus on nyt käynnissä ja kuuntelee `PORT`-ympäristömuuttujassa asetettua porttia. Esimerkiksi jos sovellus on käynnissä portissa `5000`, sovellus avautuu navigoimalla selaimella osoitteeseen `localhost:5000`.


## Suorittaminen Herokussa
Alusta projektista uusi Heroku-sovellus ajamalla projektin juuressa

```bash
heroku create
```

Tämä määrittää projektille automaattisesti uuden *git remoten* nimellä `heroku`, johon muutokset voidaan myöhemmin julkaista.

Mikäli haluat käyttää olemassaolevaa tai aiemmin luotua sovellusta, tee tarvittavat konfiguroinnit paikallisesti esim. `git remote`-komennolla ja herokun dashboardista.

Sovellus tarvitsee tietokantaliitännäisen, jota ei lisätä oletuksena uusiin sovelluksiin. Voit tarkistaa onko sovelluksellasi tietokantaliitännäinen kutsumalla 

```bash
heroku addons
```

Mikäli tulostus on `No addons for app sovelluksen-nimi.` tai tulosteen listasta ei löydy liitännäistä `heroku-postgresql`, asenna liitännäinen kutsumalla esimerkiksi

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

Sovelluksen suorittamista varten on projektin juuressa valmiiksi konfiguroitu `Procfile`, johon ei pitäisi tarvita muutoksia.

Sovelluksen julkaisu pitäisi nyt onnistua kutsumalla

```
git push heroku master
```
