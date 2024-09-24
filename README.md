# FantasyTeamManager
Fantasy Team manager

Sovelluksen avulla käyttäjä voi koota tiimin fiktiivisiä pelaajia ja toimia niiden managerina, sekä katsoa eri tiimien pelihistoriaa.
Tiimit muodostuvat pelaajista, ja yksitäisillä pelaajilla on omat tilastot heidän historiastaan ja taidoistaan.
Jokainen käyttäjä on joko peruskäyttäjä tai ylläpitäjä.

Sovelluksen inspiraationa toimii siis perinteisen fantasia-urheilun konsepti. 

## Ominaisuudet:
- Käyttäjä voi luoda itselleen tilin ja kirjautua sisään
- Käyttäjä voi valita tiimiinsä pelaajia listalta
- Käyttäjä voi osallistua tiimillään otteluihin muita tiimejä vastaan
- Käyttäjä voi tarkastella otteluiden tuloksia
- Otteluiden tulokset tallennetaan pelaajien historiaan
- Käyttäjä voi tarkastella tilastoja joista näkyy pelaajiensa historia ja suoritukset
- Ylläpitäjä voi luoda uusia pelaajia
- Ylläpitäjä voi poistaa pelaajia käytöstä ja palauttaa niitä käyttöön (vastaten eläkettä pelaajille)
- Ylläpitäjä voi tarkastella tilastoja kaikkien tiimien suorituksista

## Ohjelman testaaminen:
Ohjelman testaaminen on tällä hetkellä työn alla mutta ohjelmaa tulee olla mahdollista testata tuotannossa 
Ohejlman testaaminen tuotannossa on keskeneräinen.

Fly.io linkki: https://fantasy-team-manager.fly.dev/

Ohjelmaa pystyy myös testata lokaalisti 

Ensin luo .env tiedosto, joka sisältää 
```
DATABASE_URL=postgresql:///postgres
SECRET_KEY=secret
```

navigoi src kansioon ja suorita seuraavat komennot:
```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
psql -d postgres -f schema.sql
```

```bash
flask run
```
