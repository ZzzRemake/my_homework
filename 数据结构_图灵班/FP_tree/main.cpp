#include <iostream>
#include <fstream>
#include <sstream>
#include "FPtree.h"
using namespace std;

const string path("dataset.txt");

std::vector<std::vector<std::string>> ReadData(const std::string &path) {
    vector<vector<string>> originData;
    ifstream fInput(path);
    if(!fInput.is_open()){
        cout<<"Error:can't open the file!";
        exit(0);
    }
    string nowLine;
    while(getline(fInput,nowLine)){
        stringstream sInput(nowLine);
        string nowWord;
        vector<string> nowEvent;
        while(sInput>>nowWord){
            nowEvent.push_back(nowWord);
        }
        originData.push_back(nowEvent);
    }
    return originData;
}

void Print_Patterns(const set<pair<set<string>,unsigned long long>>& frequencyPatterns){
    ofstream fOutput("frequencePatterns.txt");
    for(auto&i:frequencyPatterns){
        fOutput<<"[";
        for(auto&j:i.first){
            fOutput<<j<<"   ";
        }
        fOutput<<i.second<<"]\n";
    }
    cout<<"Generate "<<frequencyPatterns.size()<<"patterns.\n";
    fOutput<<"Generate "<<frequencyPatterns.size()<<"patterns.";
}

void Print_Rules(const map<pair<set<string>,set<string>>,double>& rules){
    ofstream fOutput("confidenceRules.txt");
    vector<int> totalCnt;
    int cnt=0;
    for(int i=1;;++i){
        cnt=0;
        for(auto& rule:rules){
            if(rule.first.first.size()==i){
                ++cnt;
                fOutput<<"[";
                for(auto &item:rule.first.first){
                    fOutput<<item<<"  ";
                }
                fOutput<<"]-->[";
                for(auto &item:rule.first.second){
                    fOutput<<item<<"  ";
                }
                fOutput<<"]: "<<rule.second<<"\n";
            }
        }
        if(!cnt&&i>=2){
            break;
        } else {
            totalCnt.push_back(cnt);
        }
    }

    cnt=0;
    for(auto i:totalCnt){
        fOutput<<"The number of"<<++cnt<<" rule(s) is "<<i<<'\n';
    }
    cout<<"Generate "<<rules.size()<<" rules.\n";
    fOutput<<"Generate "<<rules.size()<<" rules";
}

int main(){
    unsigned long long minSup;
    double minCon;
    cin>>minSup>>minCon;
    FPTree testTree(ReadData(
            path)
                    ,minSup,minCon);
    cout<<"The construction of the FP-tree complete!\n";
    testTree.GenerateFrequentRules();
    Print_Patterns(testTree.frequentSet);
    testTree.GenerateRules();
    Print_Rules(testTree.rulesWithConfidence);
    cout<<"ALL OVER! THANKS FOR THE CLASS!";
}
