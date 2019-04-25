# Käyttäjätarinat

## Käyttäjä voi lisätä seinälleen tilapäivityksen
Käyttäjän tilapäivitystä varten luodaan uusi rivi tauluun `Post` (`INSERT INTO Post(...) VALUES (...)`), ja kenttien `owner_id` ja `wall_id` avulla kontrolloidaan kenen seinälle tilapäivitys lisätään ja kuka on päivityksen tehnyt.

## Käyttäjä voi tilata muiden päivityksiä
Käyttäjän tilatessa toisen käyttäjän tilapäivitykset, luodaan liitostauluun `Subscription` uusi rivi, jonka kentät `owner_id` ja `wall_id` kontrolloivat kenen feedille tilapäivityksiä ollaan tilaamassa ja minkä seinän päivitykset halutaan tilata.

## Käyttäjä voi kommentoida tilaamiensa käyttäjien päivityksiin
Käyttäjän kommenttia varten luodaan tauluun `Comment` uusi rivi, jonka kentillä `owner_id` ja `post_id` kontrolloidaan kuka kommentoi ja mihin tilapäivitykseen.

## Käyttäjä voi lukea tilaamiensa käyttäjien päivityksiä hänelle kootulta feediltä
Käyttäjän navigoidessa feedille, haetaan kannasta tämän tilauksia vastaavat tiläpäivitykset kaksiosaisella kyselyllä. Ensisijaisesti haetaan kunkin tilapäivityksen tiedot (päivityksen sisältö, päivämäärät, kuka postasi, mihin seinälle, yms.) ja alikyselyllä liitetään mukaan vielä kunkin tilapäivityksen kommenttien määrä.

Koska tilapäivityksiä on potentiaalisesti paljon, rajoitetaan kerralla näkyvien päivitysten lukumäärää `LIMIT`:llä ja hakemalla ainoastaan tiettyä päivämäärää vanhempia rivejä. Sivutus on toteutettu säätelemällä aloitusajankohtaa.

## Käyttäjä voi lukea omia ja muiden käyttäjien päivityksiä hänen omalta seinältään
Seinä on kyselyiden suhteen ikään kuin yksinkertaistettu versio feedistä, ja toiminta on hyvin vastaavaa kuin feedin suhteen, mutta ilman tarvetta välittää tilauksista.


---

## Käyttäjä voi muokata halutessaan tekemiään päivityksiä
Muokkaukset tallennetaan kantaan `UPDATE ... SET ... WHERE ...`-lausetta käyttäen, rajaten päivityksen pääavaimella muokkaukset yksittäiseen riviin. Muokkausajankohta päivitetään jokaisen muokkauksen yhteydessä vastaamaan nykyhetkeä.

## Käyttäjä voi muokata tekemiään kommentteja
Toiminto on vastaava kuin tilapäivityksien kommentointi.

## Käyttäjä näkee tilapäivityksistä onko niitä muokattu ja muokkauksen tapahtumahetken
Tilapäivityksiä haettaessa feediä/seinää varten, mukaan liitetään tieto viimeisimmästä muokkausajankohdasta. Mikäli päivityksen luontihetki on eri kuin viimeisimmän muokkauksen ajankohta, näytetään käyttöliittymässä että tekstiä on muokattu.

---

# Käyttäjä näkee tilaamiensa käyttäjien lukumäärän
Käyttäjän seinän yhteydessä näytetään tilattujen käyttäjien lukumäärä. Lukumäärä saadaan `COUNT`-yhteenvetokyselyllä tauluun `Subscription`, valiten vain rivit joiden kohdeseinä on halutun käyttäjän seinä.

# Käyttäjä näkee tekemiensä tilapäivitysten ja kommenttien lukumäärän
Toiminto on vastaava kuin tilauksien määrä.

---

# Toteuttamattomat toiminnot

 - Käyttäjä voi hakea feediltään tilapäivityksiä avainsanoilla.
