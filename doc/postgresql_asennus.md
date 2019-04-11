# Tietokannan luominen paikallista suorittamista varten
Sovellusta on kehitetty ympäristössä jossa on saatavilla:
 - Python 3.6.7
  - Tarvittavat kirjastot saa noudettua `pip`-apuohjelmalla `requirements.txt` mukaisesti komennolla `pip install -r requirements.txt`
  - Virtuaaliympäristön setuppaaminen komennolla `python3 -m venv venv && source venv/bin/activate` on enemmän kuin suositeltavaa.
 - PostgreSQL 11.2

Esimerkiksi Ubuntussa tai Linux Mintissä PostgreSQL:n asennus onnistuu asentamalla pakkaus `postgresql-11` eli ajamalla `apt install postgresql-11`. Mikäli pakkausta ei löydy tai jos asennettu versio (*version voi tarkistaa asennuksen jälkeen ajamalla `psql --version`*) on alle 11.2, löytyy kattavammat ohjeet ajantasaisen version asentamiseen [PostgreSQL:n virallisista asennusohjeista](https://www.postgresql.org/download/linux/ubuntu/).

Ohjelma lataa käynnistyessään juurihakemistosta löytyvän tiedoston `.env`, jota voidaan käyttää ympäristömuuttujien asettamiseen. Ympäristömuuttujille on määritetty jokseenkin "fiksut" vakioarvot, joten ainoa muuttuja josta oikeastaan tarvitsee murehtia on `DATABASE_URL`, jonka tulee osoittaa käytettävissä olevaan tietokantapalvelimeen. Tietokannan oletetaan olevan yhteensopiva PostgreSQL 11.2 kanssa.

Kehitystä varten uuden kannan luominen osoitteessa `localhost:5432` raksuttavaan PostgreSQL-serveriin onnistuisi esimerkiksi seuraavasti:

 1. Kirjaudutaan sisään pääkäyttäjänä:
    ```sh
    $ sudo -i -u postgres psql
    ```
 2. Luodaan sovellukselle uusi käyttäjä/rooli ja alustetaan tietokanta:
    ```sql
    postgres> CREATE USER <käyttäjänimi> WITH ENCRYPTED PASSWORD '<salasana>';
    postgres> CREATE DATABASE <tietokannan_nimi>;
    postgres> \q
    ```
 3. Tämän jälkeen luodaan projektin juureen tiedosto `.env` ja annetaan sille sisällöksi: 
  ```sh
  export DATABASE_URL='postgresql://<käyttäjänimi>:<salasana>@localhost:5432/<tietokannan_nimi>'
  export FLASK_ENV=development
  ```
