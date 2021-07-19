#include <iostream>

//szybszy sinus
double inline __declspec (naked) __fastcall newSin(double x) {
    _asm fld qword ptr[esp + 4]
        _asm fsin
    _asm ret 8
}

//szybsze sqrt
double inline __declspec (naked) __fastcall newSqrt(double n) {
    _asm fld qword ptr[esp + 4]
        _asm fsqrt
    _asm ret 8
}

//szybsze abs
double inline __declspec (naked) __fastcall newAbs(double n) {
    _asm fld qword ptr[esp + 4]
        _asm fabs
    _asm ret 8
}

//Funkcja wielomianowa.
double poly(double x) {
    return ((2 * x - 9) * x + 6) * x - 7;
}

//Funkcja trygonometryczna.
double trig(double x) {
    return 5 * newSin(x);
}

//Funkcja wyk�adnicza.
double expp(double x) {
    return x * pow(2, -x);
}

//Funkcja z�o�enia 1.
double opt1(double x) {
    return (x + 5) * x * x * x - pow(3, x);
}

//Funkcja z�o�enia 2.
double opt2(double x) {
    return -3 * (x * x * x) + newSin(10 * x) + 1;
}

//Funkcja z�o�enia 3.
double opt3(double x) {
    return pow(3, newSin(x));
}

/*
Znajdywanie przedzia�u unimodalnego.

Argumenty:
    start - warto�� x od kt�rej nale�y zacz�� poszukiwania
    step - warto�� kroku, im mniejsza tym wi�ksze szanse na to, �e znaleziony przedzia� jest unimodalny
    func - wska�nik na sprawdzan� funkcj� dla x: [-inf,inf]

Zwraca:
    Pocz�tek i koniec znalezionego przedzia�u.
*/
std::pair<double, double> findUnimod(double start, double step, double (*func)(double)) {

    double limit = start + 10000;

    double first = func(start);
    start += step;
    double second = func(start);
    start += step;
    double third = func(start);

    while (!((first < second) && (second > third))) {

        if (start > limit) {
            std::cout << "Nie znaleziono przedzialu unimodalnego.";
            exit(1);
        }

        start += step;
        first = second;
        second = third;
        third = func(start);
    }

    return std::make_pair(start - (2 * step), start);
}

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
std::pair<double, double> newBound(double begin, double end, double left, double right, double (*func)(double)) {
    double fLeft = func(left);
    double fRight = func(right);

    if (fLeft > fRight) {
        return std::make_pair(begin, right);
    }
    return std::make_pair(left, end);


}

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
std::pair<double, double> dichotomy(double start, double step, double (*func)(double), double prec, int* iter) {

    std::pair<double, double> p = findUnimod(start, step, func);
    double begin = p.first;
    double end = p.second;
    double left, right;

    double size = newAbs(end - begin);

    while ((*iter != 0) && (size > prec)) {

        left = ((begin + end) - (size * 0.25)) * 0.5;
        right = ((begin + end) + (size * 0.25)) * 0.5;

        p = newBound(begin, end, left, right, func);
        begin = p.first;
        end = p.second;

        size = newAbs(end - begin);
        (*iter)--;
    }

    return std::make_pair(begin, end);
}

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
std::pair<double, double> ratio(double start, double step, double (*func)(double), double prec, int* iter) {

    std::pair<double, double> p = findUnimod(start, step, func);
    double begin = p.first;
    double end = p.second;

    double k = (newSqrt(5) - 1) * 0.5;
    double left = end - (k * (end - begin));
    double right = begin + (k * (end - begin));
    double size = newAbs(end - begin);

    double fLeft = func(left);
    double fRight = func(right);

    double iterCount = 0;

    while ((*iter != 0) && (size > prec)) {

        if (fRight < fLeft) {
            end = right;
            right = left;
            fRight = fLeft;
            left = end - (k * (end - begin));
            fLeft = func(left);
        }

        else {
            begin = left;
            left = right;
            fLeft = fRight;
            right = begin + (k * (end - begin));
            fRight = func(right);
        }

        (*iter)--;
        size = newAbs(end - begin);
    }

    return std::make_pair(begin, end);
}