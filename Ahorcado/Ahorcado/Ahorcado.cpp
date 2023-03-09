// Ahorcado.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>
#include <fstream>
#include <string>
#include <random>
#include <vector>
#include<ctime>
using namespace std;
string getWord();
string procces(string word, string guess, char letter, int* health);
int main()
{

    srand(time(0));
    string word = getWord();
    string guess(word.size(), '_');
    int health = 3;
    cout << "welcome to hangman"<<endl;
    cout << "You have three lives"<<endl;
    cout << "You must find the word by introducing letters"<<endl;
    cout << "yout word have been chosen good luck "<<endl<<endl;
    char letter;
    while (true)
    {
        cout << "your word is " << guess << endl;
        cout << "guess the next letter:";
        cin >> letter;
        guess = procces(word, guess, letter, &health);

        if (health <= 0) {
            cout << "you are death"<<endl;
            return 0;
        }
        if (word == guess) {
            cout << "you win" << endl;
            return 0;
        }
        cout << endl;
    }

    


}

string getWord() {
    
    ifstream lemario("Words.txt");
    vector<string> words;
    for (std::string line; getline(lemario, line); )
    {
        words.push_back(line);
    }
    int index = rand() % words.size();
    return words[index];
}
string procces(string word,string guess,char letter,int *health) {

    int cont = 0;
    for (int i = 0; i < word.size(); i++)
    {
        if (letter == word[i]) {
            guess[i] = letter;
            cont++;
        }
    }
    if (cont == 0) {
        
        health[0]--;
        cout << "good luck next time your health is now " << health[0] <<endl;
    }
    else {
        cout << "nice" << endl;
    }
    return guess;
}