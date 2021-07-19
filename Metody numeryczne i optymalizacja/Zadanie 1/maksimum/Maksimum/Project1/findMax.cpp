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

//Funkcja wyk³adnicza.
double expp(double x) {
    return x * pow(2, -x);
}

//Funkcja z³o¿enia 1.
double opt1(double x) {
    return (x + 5) * x * x * x - pow(3, x);
}

//Funkcja z³o¿enia 2.
double opt2(double x) {
    return -3 * (x * x * x) + newSin(10 * x) + 1;
}

//Funkcja z³o¿enia 3.
double opt3(double x) {
    return pow(3, newSin(x));
}

/*
Znajdywanie przedzia³u unimodalnego.

Argumenty:
    start - wartoœæ x od której nale¿y zacz¹æ poszukiwania
    step - wartoœæ kroku, im mniejsza tym wiêksze szanse na to, ¿e znaleziony przedzia³ jest unimodalny
    func - wskaŸnik na sprawdzan¹ funkcjê dla x: [-inf,inf]

Zwraca:
    Pocz¹tek i koniec znalezionego przedzia³u.
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
std::pair<double, double> newBound(double begin, double end, double left, double right, double (*func)(double)) {
    double fLeft = func(left);
    double fRight = func(right);

    if (fLeft > fRight) {
        return std::make_pair(begin, right);
    }
    return std::make_pair(left, end);


}

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