# CeneoWebScraper

&nbsp;  
## Struktura opinii w serwisie [Ceneo.pl](https://www.ceneo.pl/)


|Składowa opinii|Selektor|Nazwa zmiennej|Typ danych|
|---------------|--------|--------------|----------|
|opinia|div.js_product-review|opinion|bs4.element.Tag|
|identyfikator opinii|div.js_product-review\["data-entry-id"\]|opinion_id||
|autor opinii|span.user-post__author-name|author||
|rekomendacja autora|span.user-post__author-recomendation > em|recommendation||
|liczba gwiazdek|span.user-post__score-count|stars||
|treść opinii|div.user-post__text|content||
|lista zalet|div\[class$=positives\] ~ div.review-feature__item|pros||
|lista wad|div\[class$=negatives\] ~ div.review-feature__item|cons||
|dla ilu osób przydatna|button.vote-yes > span|useful||
|dla ilu osób nieprzydatna|button.vote-no > span|useless||
|data wystawienia opinii|span.user-post__published > time:nth-child(1)\["datetime"\]|published||
|data zakupu produktu|span.user-post__published > time:nth-child(2)\["datetime"\]|purchased||

&nbsp;  
## Etapy pracy nad projektem obiektowym
1. Pobranie elementów pojedynczej opinii do niezależnych zmiennych
2. Zapisanie wszystkich elemntów pojedynczej opinii do jednej zmiennej \(słownik\)
3. Pobranie wszystkich opinii z pojedynczej strony do słowników i dodnie ich do listy
4. Pobranie wszystkich opinii o produkcie z wszystkich stron i zapisanie ich do pliku .json
5. Dodanie możliowści podania id produktu przez użytkownika za pomocą klawiatury
6. Refaktoryzacja \(optymalizacja\) kodu:
    1. utworzenie funkcji do pobierania składowych strony HTML
    2. utworzenie słownika opisującego strukturę opinii wraz z selektorami poszczególnych elementów
    3. zamiana instrukcji pobierających składowe opinii do pojedynczych zmiennych i tworzących z nich słownik na wyrażenie słownikowe \(dictionary comprehension\) tworzące słownik reprezentujący pojedynczą opinię na podstawie słownika selektorów
7. Analiza opinii o wybranym produkcie
    1. wczytanie wszystkich opinii o wskazanym produkcie do obiektu DataFrame
    2. wyliczenie podstawowych statystyk na podstawie opinii
        1. liczba wszystkich opinii o produkcie
        2. liczba opinii w których autor podał listę zalet produktu
        3. liczba opinii w których autor podał listę wad produktu
        4. średnia ocena produktu
    3. przygotowanie wykresów na podstawie zawartości opinii
        1. udział poszczególnych rekomendacji w ogólnej liczbie opinii
        2. histogram częstości występowania poszczególnych ocen (liczby gwiazdek)

&nbsp;  
## Lista wykorzystanych bibliotek

    - BeautifulSoup - parsowanie kodu HTML
    - Flask - sieciowy framework, który udostępnia przydatne narzędzia i funkcje ułatwiające tworzenie aplikacji sieciowych
    - Pandas - narzędzie do analizy i manipulacji pobieranymi danymi
    - os - udostępnia funkcje umożliwiające interakcję z systemem operacyjnym np. otwieranie plików, tworzenie folderów
    - Markdown -  umożliwia konwersję tekstu Markdown na HTML
    - Requests - wykonywanie requestów, czyli żądań dostępu do strony internetowej Ceneo.pl
    - NumPY - biblioteka ułatiająca pracę z listami, np. arange - lista równomiernie rozmieszczonych wartości
    - Pyplot - tworzenie wykresów dla produtków i opinii
    - json - obsługa plików json zawierających opinie i produkty