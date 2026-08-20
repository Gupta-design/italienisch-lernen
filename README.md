# Italienisch lebendig lernen

Eigenständiges, separates Projekt — technisch komplett getrennt von "Bisaya lebendig lernen"
(eigene Datei, kein gemeinsamer Code zur Laufzeit), aber im Aufbau an dessen Struktur und
Funktionsumfang angeglichen.

**Live:** https://gupta-design.github.io/italienisch-lernen/

## Enthalten

- **Alle 30 Lektionen** (Deutsch → Italienisch) im Birkenbihl-Format (Dekodierung, Lautschrift,
  natürliche Übersetzung) — gleiche Themen wie bei Bisaya (Begrüßung bis Beziehungen/Liebe)
- **Wendungen** (24 nützliche Redewendungen, nach Kategorie filterbar, unabhängig von Lektionen)
- **Lieder** (2 traditionelle, gemeinfreie italienische Volkslieder im Birkenbihl-Format)
- **Anwenden** (16 Lückensätze zum Üben, mit aufdeckbarer Lösung)
- **Quiz** (endloses Karten-Deck, deutsch → italienisch, ab Level 3 freigeschaltet, Vokabelpool
  aus abgeschlossenen Lektionen, mit eigenen Achievements für erste Runde und perfekte Runde)
- Wortschatz-Trainer (Karteikarten) mit den Vokabeln aus den Lektionen
- Aussprache-Guide (Italienisch-spezifisch: Doppelkonsonanten, c/g weich/hart, gli/gn)
- **Echte Nutzerkonten** (Firebase Authentication: E-Mail/Passwort, Registrierung mit
  Bestätigungs-E-Mail) — läuft live über ein eigenes Firebase-Projekt ("Italienisch Lebendig")
- **Bestenliste** (Firestore, Standort eur3/Europa) — punktebasiert (1 Punkt/gekonntes Wort,
  5 Punkte/abgeschlossene Lektion), Teilnahme opt-in
- **Belohnungssystem**: XP/Level, Tages-Streak, Tagesziel mit Fortschrittsring, Achievements/Badges
- Italienische UND deutsche Sprachausgabe direkt über die Sprachausgabe des Browsers
  (kein Azure/TTS-Setup nötig)
- Fortschritt (gelernte Wörter, abgeschlossene Lektionen) lokal im Browser gespeichert
  (localStorage), Punktestand zusätzlich mit dem Konto synchronisiert
- Kein VIP-/Bezahlbereich (bewusst nicht enthalten, anders als bei Bisaya)
- Kein Mikrofon-Feature (bewusst nicht enthalten — bei Bisaya wegen unzuverlässiger
  Browser-Unterstützung wieder entfernt)
- Kein Google-Sign-In (bewusst nicht enthalten — bei Bisaya aktuell wegen Problemen auf
  Safari/Android deaktiviert; nur E-Mail/Passwort)

## Was (noch) fehlt

- Geschichten-Bereich
- Eigene E-Mail-Zustellung für Bestätigungsmails (aktuell Firebase-Standard-Versand; für
  zuverlässige Zustellung analog zum Brevo-Setup bei Bisaya inkl. Domain-Authentifizierung
  SPF/DKIM/DMARC empfehlenswert)
- Optional: eigene Domain (aktuell auf gupta-design.github.io gehostet)

## Infrastruktur (Stand: eingerichtet)

- **Firebase-Projekt** "Italienisch Lebendig" (`italienisch-lebendig`), getrennt vom Bisaya-Projekt
  - Authentication: E-Mail/Passwort aktiviert
  - Firestore-Datenbank (Standort eur3/Europa), Sicherheitsregeln: Bestenliste öffentlich lesbar,
    Schreibzugriff nur auf das eigene Nutzerdokument
  - Web-App registriert, `FB_CONFIG` im `<head>`-Bereich der Datei mit den echten Zugangsdaten befüllt
- **GitHub-Repository**: `Gupta-design/italienisch-lernen`
- **GitHub Pages**: aktiviert (Branch `main`, Root) — https://gupta-design.github.io/italienisch-lernen/

## Datei öffnen zum Testen

Einfach `index.html` doppelklicken — funktioniert direkt im Browser, kein Server nötig.
Konto und Bestenliste funktionieren bereits live.
