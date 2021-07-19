#pragma once

//Funkcja wielomianowa.
double poly(double x);

//Funkcja trygonometryczna.
double trig(double x);

//Funkcja wyk³adnicza.
double expp(double x);

//Funkcja z³o¿enia 1.
double opt1(double x);

//Funkcja z³o¿enia 2.
double opt2(double x);

//Funkcja z³o¿enia 3.
double opt3(double x);

/*
Znajdywanie przedzia³u unimodalnego.

Argumenty:
    start - wartoœæ x od której nale¿y zacz¹æ poszukiwania
    step - wartoœæ kroku, im mniejsza tym wiêksze szanse na to, ¿e znaleziony przedzia³ jest unimodalny
    func - wskaŸnik na sprawdzan¹ funkcjê dla x: [-inf,inf]

Zwraca:
    Pocz¹tek i koniec znalezionego przedzia³u.
*/
std::pair<double, double> findUnimod(double start, double step, double (*func)(double));

/*
Wyznaczanie nowego przedzia³u.

Argumenty:
    begin - pocz¹tek obecnego przedzia³u
    end - koniec obecnego przedzia³u
    left - pierwszy z wyznaczonych punktów
    right - drugi z wyznaczonych punktów
    func - wskaŸnik na sprawdzan¹ funkcjê

Zwraca:
    Pocz¹tek i koniec nowego przedzia³u.
*/
std::pair<double, double> newBound(double begin, double end, double left, double right, double (*func)(double));

/*
Wyznaczanie maksimum metod¹ dychotomii.

Argument:
    start - pocz¹tek wyszukiwania dla funkcji findUnimod
    step - krok wyszukiwania dla funkcji findUnimod
    func - wskaŸnik na sprawdzan¹ funkcjê
    prec - precyzja wyszukiwania, nale¿y ustawiæ na 0 aby jedynie iloœæ iteracji mia³a znaczenie
    iter - wskaŸnik na iloœæ iteracji do wykonania, nale¿y ustawiæ wartoœæ na -1 aby jedynie precyzja mia³a znaczenie

Zwraca:
    Pocz¹tek i koniec przedzia³u, w którym jest maksimum.
*/
std::pair<double, double> dichotomy(double start, double step, double (*func)(double), double prec, int* iter);

/*
Wyznaczanie maksimum metod¹ z³otego podzia³u.

Argument:
    start - pocz¹tek wyszukiwania dla funkcji findUnimod
    step - krok wyszukiwania dla funkcji findUnimod
    func - wskaŸnik na sprawdzan¹ funkcjê
    prec - precyzja wyszukiwania, nale¿y ustawiæ na 0 aby jedynie iloœæ iteracji mia³a znaczenie
    iter - wskaŸnik na iloœæ iteracji do wykonania, nale¿y ustawiæ wartoœæ na -1 aby jedynie precyzja mia³a znaczenie

Zwraca:
    Pocz¹tek i koniec przedzia³u, w którym jest maksimum.
*/
std::pair<double, double> ratio(double start, double step, double (*func)(double), double prec, int* iter);