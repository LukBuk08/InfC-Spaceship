# InfC-Spaceship

Commands:

git status                  # Viser hvilke filer der er ændret, og hvilken branch du er på
git pull                    # Henter de nyeste ændringer fra GitHub
git checkout -b "Branch navn"       # Opretter en ny branch og skifter til den
git branch                  # Viser alle branches (* markerer den aktive)
git add .                   # Tilføjer alle ændrede filer klar til commit
git commit -m "Min ændring" # Gemmer ændringerne lokalt med en besked
git push origin "Branch navn"       # Sender din branch op til GitHub
git checkout main           # Skifter tilbage til main-branchen


Normal workflow
git checkout -b "Branch navn"

git add .                   # Tilføjer alle ændrede filer klar til commit
git commit -m "Min ændring" # Gemmer ændringerne lokalt med en besked
git push origin "Branch navn"       # Sender din branch op til GitHub
