# Tietokanta

![Tietokantakaavio](./images/tietokantakaavio.png)

Seinät on eriytetty käyttäjistä jotta myöhemmin voitaisiin lisätä toiminnallisuutta jossa seinä ei suoranaisesti olekaan käyttäjän oma, esim. "fanisivujen" luominen yms. Kullakin käyttäjällä tulee kuitenkin olla vähintään oma seinä, joten kantaan on luotu trigger luomaan kullekin käyttäjälle automaattisesti oma seinä kun kantaan lisätään käyttäjiä.

Tietokannan `CREATE TABLE`/`CREATE TRIGGER`-lauseet ovat seuraavat:

```SQL
CREATE TABLE wall (
    id integer PRIMARY KEY
);

CREATE TABLE account (
    id integer PRIMARY KEY,
    date_created timestamp without time zone,
    name VARCHAR(144) NOT NULL,
    username VARCHAR(144) NOT NULL,
    password_hash VARCHAR(144) NOT NULL
);

CREATE TABLE subscription (
    owner_id integer NOT NULL,
    wall_id integer NOT NULL,

    FOREIGN KEY (owner_id) REFERENCES Account(id),
    FOREIGN KEY (wall_id) REFERENCES Wall(id)
);

CREATE TABLE post (
    id integer PRIMARY KEY,
    date_created timestamp without time zone,
    date_modified timestamp without time zone,
    content VARCHAR(255) NOT NULL,
    owner_id integer NOT NULL,
    wall_id integer NOT NULL

    FOREIGN KEY (owner_id) REFERENCES Account(id),
    FOREIGN KEY (wall_id) REFERENCES Wall(id)
);

CREATE TABLE comment (
    id integer PRIMARY KEY,
    date_created timestamp without time zone,
    date_modified timestamp without time zone,
    content VARCHAR(255) NOT NULL,
    owner_id integer NOT NULL,
    post_id integer NOT NULL,

    FOREIGN KEY (owner_id) REFERENCES Account(id),
    FOREIGN KEY (post_id) REFERENCES Post(id)
);

CREATE FUNCTION create_user_wall() RETURNS TRIGGER AS $create_user_wall$
    BEGIN
        IF NEW.id IS NULL THEN
            RAISE EXCEPTION 'id cannot be null';
        END IF;
        INSERT INTO Wall (id) VALUES (NEW.id);
        RETURN NULL;
    END;
$create_user_wall$ LANGUAGE plpgsql;

CREATE TRIGGER create_wall_for_user 
AFTER INSERT ON Account
    FOR EACH ROW EXECUTE FUNCTION create_user_wall();

```
