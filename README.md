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
tej akcji nazwa okna zmienia się na nazwę wybranej bazy danych i 
zostaje wyświetlona list tabeli, które są w niej zawarte. Zerwanie
połączenia z bazą danych następuje po wciśnięciu przycisku "Zamknij".

Po zerwaniu połączenia aplikacja wyświetla ponownie okno logowania
z pustymi polami umożlwiając ponowne zalogowanie.
