# Tsohabook
Sosiaalisen median palvelu Facebookin/Twitterin hengessä. Kullakin käyttäjällä on oma seinä, johon he voivat julkaista tilapäivityksiä. Käyttäjät voivat kommentoida toistensa tilapäivityksiin ja "tilata" muiden käyttäjien seiniä, jolloin näiden päivitykset ilmestyvät heille yksilöityyn "feediin".


## Dokumentaatio
 - [Käyttötapaukset ja SQL-kyselyt](./doc/user_stories.md)

 - [Tietokanta](./doc/tietokantakaavio.md)

 - [Asennusohje](./doc/asennusohje.md)

 - [Käyttöohje](./doc/kayttoohje.md)


## Toimintoja
 - Rekisteröityminen/Kirjautuminen
 - Tilapäivityksen lisääminen/muokkaus/poisto
 - Tilapäivityksien kommentointi
 - Päivityksen tekijä voi poistaa kommentteja
 - Kommentoija voi itse poistaa kommentin
 - Käyttäjä voi tilata muiden käyttäjien päivityksiä (ja perua tilauksen)
 - Käyttäjälle kootaan yhdelle sivulle kaikki tilattujen käyttäjien päivityksen kronologisessa järjestyksessä

### Jatkokehitysideoita/ominaisuudet joita ei ole toteutettu
 - Päivityksiä voi hakea avainsanoilla ja/tai ajankohdan mukaan


## Sovellus
Sovelluksen backend pyörii Python + Flask combolla ja renderöi frontin flaskin templaateilla (*Jinja2*). "Tuotantoversio" raksuttaa Herokussa.

[Linkki sovellukseen](http://tsohabook.herokuapp.com)

Sovellukseen on luotu kokeilua varten testikäyttäjät "Jaska Jokunen" ja "Joku Jaskanen" joiden kirjautumistiedot ovat seuraavat:

 |Käyttäjätunnus |Salasana|
 |---------------|--------|
 |jaskajoku      |abc123  |
 |jokutoinen     |abc123  |
