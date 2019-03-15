# Suorittaminen paikallisesti
Sovellusta on kehitetty ympäristössä jossa on saatavilla:
 - Python 3.6.7
  - Tarvittavat kirjastot saa noudettua `pip`-apuohjelmalla `requirements.txt` mukaisesti komennolla `pip install -r requirements.txt`
  - Virtuaaliympäristön setuppaaminen komennolla `python3 -m venv venv && source venv/bin/activate` on enemmän kuin suositeltavaa.
 - PostgreSQL 11.2

Johtuen Varsinkin *PostgreSQL 11.2*:n käytöstä paikallisessa ympäristössä setuppaaminen saattaa vaatia lievää tunkkaamista jos/kun pingiinivoimalla pyörivissä koneissa distron repossa on wanha serveri edelleen jaossa. Jotkin sovellukseen toteutetut kyselyt vaativat 11-version mukana tullutta syntaksia, eivätkä välttämättä kymppiversiolla käänny.

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

Projektin pitäisi nyt pyörähtää sorsista käyntiin kutsumalla juurihakemistossa:
 ```sh
 (venv)$ python3 run.py
 ```
