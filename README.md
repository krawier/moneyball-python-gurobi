# OPTIMIZING BASEBALL

## ENG
The project is inspired by the movie Moneyball staring Brad Pitt. The goal is to create the best baseball team roster out of the available players. Their value is determined by sabermetrics and salary. This problem is a modified Multiple Choice Knapsack Problem. To read the whole report go to `moneyball_report.pdf`. 

How to run project: 

1. Ensure you have Python installed along with a valid Gurobi solver license.
2. Install the required dependencies:  `pip install -r requirements.txt`
3.Enter the folder src/ : `cd src`
4. To run the exact optimization (MILP) using Gurobi, execute: `python gurobi-approach.py
5. To run the metaheuristic optimization (BFO), execute: `python bfo-approach.py`  
(It's nice to split your terminal, and run 3. and 4. simultaneously, so that you can see the results side by side)
- If you want to retune the parameters of the BFO: `python bfo-tuner.py` will spit out the result.

## PL
Projekt jest zainspirowany filmem pt. "Moneyball", w którym gra Brad Pitt. Celem programu jest zbudowanie jak najlepszej drużyny baseballowej złożonej z dostępnych nam graczy. Ich wartość jest wyliczana na bazie sabermetri i pensji. Problem to tak naprawdę zmodyfikowana wersja  Problemu Plecakowego z Wielokrotnym Wyborem. Cały raport można przeczytać tutaj `moneyball_report.pdf`

Jak uruchomić projekt: 

1. Upewnij się, że masz zainstalowaengo Pythona na maszynie, wraz z Gurobi.
2. Aby zainstelować wymagane zależności: `pip install -r requirements.txt`
3. Wejdź do folderu src/ : `cd src`
4. Aby uruchomić dokładną optymalizację (MILP) stosując Gurobi: `python gurobi-approach.py`
5. Aby uruchomić metaheurystyczną optymalizację (BFO): `python bfo-approach.py` 
(Dobrze jest podzielić sobie swój terminal na pół, uruchomić 3. i 4. równolegle, żeby móc łatwo porównać wyniki )
- Jeśli chcesz dostroić paramtry BFO ponownie: `python bfo-tuner.py` wyrzuci odpowiedź której szukasz.
