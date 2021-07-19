#pragma once

//Funkcja wielomianowa.
double poly(double x);

//Funkcja trygonometryczna.
double trig(double x);

//Funkcja wyk�adnicza.
double expp(double x);

//Funkcja z�o�enia 1.
double opt1(double x);

//Funkcja z�o�enia 2.
double opt2(double x);

//Funkcja z�o�enia 3.
double opt3(double x);

/*
Znajdywanie przedzia�u unimodalnego.

Argumenty:
    start - warto�� x od kt�rej nale�y zacz�� poszukiwania
    step - warto�� kroku, im mniejsza tym wi�ksze szanse na to, �e znaleziony przedzia� jest unimodalny
    func - wska�nik na sprawdzan� funkcj� dla x: [-inf,inf]

Zwraca:
    Pocz�tek i koniec znalezionego przedzia�u.
*/
std::pair<double, double> findUnimod(double start, double step, double (*func)(double));

/*
Wyznaczanie nowego przedzia�u.

Argumenty:
    begin - pocz�tek obecnego przedzia�u
    end - koniec obecnego przedzia�u
    left - pierwszy z wyznaczonych punkt�w
    right - drugi z wyznaczonych punkt�w
    func - wska�nik na sprawdzan� funkcj�

Zwraca:
    Pocz�tek i koniec nowego przedzia�u.
*/
std::pair<double, double> newBound(double begin, double end, double left, double right, double (*func)(double));

/*
Wyznaczanie maksimum metod� dychotomii.

Argument:
    start - pocz�tek wyszukiwania dla funkcji findUnimod
    step - krok wyszukiwania dla funkcji findUnimod
    func - wska�nik na sprawdzan� funkcj�
    prec - precyzja wyszukiwania, nale�y ustawi� na 0 aby jedynie ilo�� iteracji mia�a znaczenie
    iter - wska�nik na ilo�� iteracji do wykonania, nale�y ustawi� warto�� na -1 aby jedynie precyzja mia�a znaczenie

Zwraca:
    Pocz�tek i koniec przedzia�u, w kt�rym jest maksimum.
*/
std::pair<double, double> dichotomy(double start, double step, double (*func)(double), double prec, int* iter);

/*
Wyznaczanie maksimum metod� z�otego podzia�u.

Argument:
    start - pocz�tek wyszukiwania dla funkcji findUnimod
    step - krok wyszukiwania dla funkcji findUnimod
    func - wska�nik na sprawdzan� funkcj�
    prec - precyzja wyszukiwania, nale�y ustawi� na 0 aby jedynie ilo�� iteracji mia�a znaczenie
    iter - wska�nik na ilo�� iteracji do wykonania, nale�y ustawi� warto�� na -1 aby jedynie precyzja mia�a znaczenie

Zwraca:
    Pocz�tek i koniec przedzia�u, w kt�rym jest maksimum.
*/
std::pair<double, double> ratio(double start, double step, double (*func)(double), double prec, int* iter);