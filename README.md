# DatabaseConnector

==Projekt w trakcie rozbudowy==

Aplikacja z graficznym interfejsem umożliwiająca nawiązanie 
połączenia z serwerem baz danych MySQL.

Program tworzy okno, w którym użytkownik wprowadza dane do
połączenia z serwerem bazą danych. Po wciśnięciu przycisku 
"Połącz" program nawiązuje połączenie z serwerem. Następnie
otwiera nowe okno, w którym są wyświetlone nazwy wszystkich 
baz danych należących do użytkownika. Wciśnięcie przycisku
"Rozłącz" powoduje przerwanie połączenia z serwerem i 
zamknięcie okna z bazami danych.

Użytkownik ma możliwość wybrania bazy danych z listy i nawiązania
z nią połączenia przez wciśnięcie przycisku "Otwórz". Po wykonaniu
tej akcji zostaje utworzone nowe okno z nazwą wybranej bazy danych i 
zostaje wyświetlona w nim lista tabeli, które są w niej zawarte. 
Zakończenie połączenia z bazą danych następuje po wciśnięciu przycisku
"Zamknij". Przycisk "Utwórz" otwiera nowe okno w którym należy podać
nazwę dla nowo tworzonej bazy danych. Przycisk "Utwórz" zatwierdza operację,
a przycisk "Zamknij" anuluje.

Użytkownik może wybrać tabelę z listy i wyświetlić jej zawartość przy
pomocy przycisku "Otwórz".

Zawartość tabeli zostaje wyświetlona w nowym oknie. Widok jest 
podzielony na kolumny zwieńczone nazwami, a poniżej jest ich 
zawartość. Suwak z prawej strony umożlwia przewijanie w przypadku
większej ilości rekordów.

Po zamknięciu połączenia aplikacja wyświetla ponownie okno logowania
z pustymi polami umożlwiając ponowne zalogowanie.
