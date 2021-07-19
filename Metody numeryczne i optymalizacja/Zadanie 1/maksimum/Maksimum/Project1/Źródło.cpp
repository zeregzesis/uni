#include <iostream>
#include <chrono>
#include "findMax.h"


//szybsze abs
double inline __declspec (naked) __fastcall newAbs(double n) {
    _asm fld qword ptr[esp + 4]
        _asm fabs
    _asm ret 8
}

/*
Funkcja pomocnicza do przeprowadzania testów wszystkich przypadków dla danej funkcji.

Argumenty:
    begin - pocz¹tek poszukiwañ przedzia³u unimodalnego
    step - krok wykorzystywany w szukaniu przedzia³u unimodalnego
    f - wskaŸnik na funkcjê dla której wykonywane bêd¹ testy
    precision - zadana precyzja z u¿yciem której wykonywane bêd¹ testy
    iterations - zadana iloœæ iteracji z u¿yciem której wykonywane bêd¹ testy

Funckja wypisuje wyniki do terminala, nic nie zwraca.
*/
void runTests(double begin, double step, double (*f)(double), double precision, int iterations) {

    std::pair<double, double> p;

    int rightIterations = iterations;
    int noIterations = -1;

    //dychotomia precyzja
    auto start = std::chrono::steady_clock::now();
    p = dichotomy(begin, step, f, precision, &noIterations);
    auto end = std::chrono::steady_clock::now();

    std::cout << "Dychotomia dla precyzji(" << precision <<
        ") - przedzial: [" << p.first << ";" << p.second <<
        "], iteracji: " << newAbs(noIterations) <<
        ", czas: " <<
        std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() <<
        " ns" << std::endl;

    //dychotomia iteracje
    start = std::chrono::steady_clock::now();
    p = dichotomy(begin, step, f, 0, &rightIterations);
    end = std::chrono::steady_clock::now();

    std::cout << "Dychotomia dla iteracji(" << iterations <<
        ") - przedzial: [" << p.first << ";" << p.second <<
        "], precyzja: " << newAbs(p.second - p.first) <<
        ", czas: " <<
        std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() <<
        " ns" << std::endl;

    rightIterations = iterations;
    noIterations = -1;

    //z³oty podzia³ precyzja
    start = std::chrono::steady_clock::now();
    p = ratio(begin, step, f, precision, &noIterations);
    end = std::chrono::steady_clock::now();

    std::cout << "Zloty podzial dla precyzji(" << precision <<
        ") - przedzial: [" << p.first << ";" << p.second <<
        "], iteracji: " << newAbs(noIterations) <<
        ", czas: " <<
        std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() <<
        " ns" << std::endl;

    //z³oty podzia³ iteracje
    start = std::chrono::steady_clock::now();
    p = ratio(begin, step, f, 0, &rightIterations);
    end = std::chrono::steady_clock::now();

    std::cout << "Zloty podzial dla iteracji(" << iterations <<
        ") - przedzial: [" << p.first << ";" << p.second <<
        "], precyzja: " << newAbs(p.second - p.first) <<
        ", czas: " <<
        std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() <<
        " ns" << std::endl;

}

int main() {

    double(*funcTab[6])(double) = { &poly, &trig, &expp, &opt1, &opt2, &opt3 };

    double precision;
    std::cout << "Podaj precyzje: ";
    std::cin >> precision;

    double iterations;
    std::cout << "Podaj liczbe iteracji: ";
    std::cin >> iterations;

    double start;
    std::cout << "Podaj poczatek poszukiwan przedzialu unimodalnego: ";
    std::cin >> start;

    double step;
    std::cout << "Podaj krok: ";
    std::cin >> step;

    int modeChoice;
    std::cout << "Wszystkie funkcje(1) czy jedna, wybrana z listy funkcja(2)?: ";
    std::cin >> modeChoice;

    if (modeChoice == 1) {
        for (int i = 0; i < 6; i++) {
            runTests(start, step, funcTab[i], precision, iterations);
            std::cout << std::endl;
        }
    }
    else if (modeChoice == 2) {
        int funcChoice;
        std::cout << "Funkcja wielomianowa(1), trygonometryczna(2), wyk³adnicza(3), zlozenie 1(4), zlozenie 2(5), zlozenie 3(6): ";
        std::cin >> funcChoice;
        funcChoice--;
        runTests(start, step, funcTab[funcChoice], precision, iterations);
    }
    else {
        std::cout << "Niepoprawny wybor! Koniec progarmu.";
    }

    return 0;

    /*
    double precision = 0.00001;
    double iterations = 10000; 
    
    runTests(-10, 1, &poly, precision, iterations);
    std::cout << std::endl;

    runTests(-10, 1, &trig, precision, iterations);
    std::cout << std::endl;

    runTests(-9, 2, &expp, precision, iterations);
    std::cout << std::endl;

    runTests(-10, 1, &opt1, precision, iterations);
    std::cout << std::endl;

    runTests(-10, 0.2, &opt2, precision, iterations);
    std::cout << std::endl;

    runTests(-10, 1, &opt3, precision, iterations);
    */

}
