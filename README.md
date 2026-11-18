# Meine Bestager-Werkstatt

Diese Werkstatt hat dir der Bestager-Bauplan angelegt. Hier passiert die Technik im Hintergrund, damit du dich um deine Inhalte kümmern kannst.

## Was hier drin ist

- **texte/**: Hier liegen Texte, die mit deiner Stimme vertont werden sollen. Eine Datei pro Text, Endung `.txt`.
- **audio/**: Hier landen die fertigen MP3-Dateien mit deiner Stimme.
- **werkzeug/**: Das kleine Programm, das die Vertonung erledigt. Hier musst du nichts ändern.

## So vertonst du einen Text

1. Öffne den Ordner **texte** und klick auf **Add file > Create new file**.
2. Gib der Datei einen Namen, zum Beispiel `begruessung.txt`, und schreib deinen Text hinein.
3. Klick auf **Commit changes**.
4. Nach ein bis zwei Minuten liegt im Ordner **audio** die Datei `begruessung.mp3`.

Am einfachsten geht es mit Claude: Lass dir den Text schreiben und sag Claude, dass er ihn in deine Werkstatt legen soll. Die passenden Prompts findest du im Bestager-Bauplan.

## Aussprache anpassen

Spricht deine Stimme ein Wort falsch aus, trag es in **werkzeug/aussprache.txt** ein, zum Beispiel `Bestager = Best Ager`. Deine Texte vertonen sich danach von selbst neu.

## Deine Schlüssel

Deine Schlüssel für HeyGen, Brevo und deine Kasse liegen verschlüsselt unter **Settings > Secrets and variables > Actions**. Niemand kann sie dort auslesen, auch du nicht. Wenn du einen Schlüssel änderst, trag ihn einfach in der Startanleitung des Bestager-Bauplans neu ein.
