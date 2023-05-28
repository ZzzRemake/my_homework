#pragma once
#include "DecisionTree.h"
#include <vector>
using namespace std;
#ifndef ID3_DECISIEFOREST_H
#define ID3_DECISIEFOREST_H
class DecideForest {
private:
	std::vector<DecisionTree*> Forest;

    std::vector<std::string> Total_type;
    std::vector<std::vector<std::string>> Data_table_row;
    std::map<std::string, std::set<std::string>> Type_list_set;
    std::set<std::string> Tag_set;
    std::vector<std::vector<std::string>> Questions;
    void GenerateOther(vector<vector<string>>& nowData,set<string>&nowTagSet,map<string,set<string>>& nowTypeList) {
        for (auto& i : nowData) {
            nowTagSet.insert(i.back());
            for (int j = 0; j < i.size(); ++j) {
                nowTypeList[Total_type[j]].insert(i[j]);
            }
        }
    }
public:
    void ReadDataBase(const std::string& path) {
        std::fstream finput(path);
        if (!finput.is_open()) {
            std::cout << "Error:Open file failure!" << endl;
            exit(1);
        }
        int row = 0, rank = 0;
        string temline; string temword;
        bool haveType = false;
        while (std::getline(finput, temline)) {
            if (temline.empty() || temline[0] == '#') {
                continue;
            }

            std::stringstream sinput(temline);
            if (temline[0] == '$') {
                sinput >> temword;
                sinput >> row >> rank;
                continue;
            }
            if (!haveType) {
                while (sinput >> temword)
                    Total_type.emplace_back(temword);
                haveType = true;
                //  cout << "Total:" << Total_type.size()<<endl;
            }
            else {
                vector<string> OneList;
                int tem = 0;
                while (sinput >> temword) {
                    OneList.emplace_back(temword);
                    //Type_list_set[Total_type[tem++]].insert(temword);
                }
                Data_table_row.emplace_back(OneList);
                //Tag_set.insert(OneList.back());
                //cout << OneList.size();
            }
        }
        GenerateOther(Data_table_row, Tag_set, Type_list_set);
        finput.close();
    }
   DecideForest(int num,const std::string& path) {
        ReadDataBase(path);
        int judgeDataNum = (double(Data_table_row.size()) + 0.5) / 2;
        if (judgeDataNum >= Data_table_row.size()) {
            judgeDataNum = Data_table_row.size() - 1;
        }
        vector<vector<string>> temDataTable;
        set<string> temTagSet;
        map<string, set<string>> temTypeList;
        for (int i = 0; i < num; ++i) {
            cout << i << endl;
            for (int j = 0; j < judgeDataNum; ++j) {
                temDataTable.push_back(Data_table_row[rand() % Data_table_row.size()]);
            }
            GenerateOther(temDataTable, temTagSet, temTypeList);
            DecisionTree* tem=new DecisionTree(Total_type, temDataTable, temTypeList, temTagSet);
            //tem->PrintTree(tem->root, 0);
            Forest.push_back(tem);
            temDataTable.clear();
            temTagSet.clear();
            temTypeList.clear();
        }
	}
    ~DecideForest() {
        for (auto& i : Forest) {
            delete i;
        }
    }
    void DoDecision(const string& path) {
        std::fstream finput(path);
        if (!finput.is_open()) {
            std::cout << "Error:Open file failure!" << endl;
            exit(1);
        }
        Questions.clear();
        string nowLine,nowWord;
        while (getline(finput, nowLine)) {
            //cout << nowLine << endl;
            std::stringstream sinput(nowLine);
            vector<string> temQuestion;
            while (sinput >> nowWord) {
                temQuestion.emplace_back(nowWord);
            }
            Questions.emplace_back(temQuestion);
        }
        int cnt = 0;
        int currect = 0;
        for (auto& i : Questions) {
            cout << "Questions " << ++cnt << endl;
            for (auto& j : i) {
                cout << j << '\t';
            }
            cout << endl;
            map<string, int> count;
            int kkk = 0;
            for (auto& j : Forest) {
                auto result = j->DoDecision(j->root,i);
                count[result]++;
            }
            int maxs = 0;
            string maxp;
            for (auto& j : count) {
                if (maxs < j.second) {
                    maxp = j.first, maxs = j.second;
                }
                cout << j.first << ":\t" << j.second << "/" << Forest.size() << endl;
            }
            if (maxp == i.back()) {
                currect++;
                cout << "Yes!" << endl;
            }
            else {
                cout << "No!" << endl;
            }
        }
        cout << "Currect:" << currect << "/" << Questions.size();
    }
};
#endif