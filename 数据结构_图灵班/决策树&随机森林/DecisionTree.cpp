//
// Created by mgzyqsd on 2022/11/18.
//

#include "DecisionTree.h"
#include "cmath"
#include "algorithm"
#include <set>
using namespace std;
DecisionTree::DecisionTree(const std::vector<std::string>& totaltype, const std::vector<std::vector<std::string>>& Datatablerow,
    const std::map<std::string, std::set<std::string>>& Typelistset, const std::set<std::string>& Tagset):Total_type(totaltype),Data_table_row(Datatablerow),
    Type_list_set(Typelistset),Tag_set(Tagset){
    root = nullptr;
    BuildTree(root, Data_table_row, Total_type);
}

//析构过程
void DecisionTree::DesTroyTree(DecisionTree::TreeNode* nowNode) {

    if (nowNode == nullptr) {
        return;
    }
    for (auto& i : nowNode->child) {
        DesTroyTree(i);
    }
    delete nowNode;
    //nowNode = nullptr;
    return;
}
DecisionTree::~DecisionTree() {
  //  PrintTree(root, 0);
    DesTroyTree(root);
}

//获取总熵
double DecisionTree::ComputeEntropy(const vector<vector<string>>& nowData) {
    map<string, int> count;
    int cnt = 0;
    for (auto& i : nowData) {
        count[i.back()]++;
    }
    double output = 0;
    if (count.size() < Tag_set.size()) {
        return 0.0;
    }
    
    for (auto& i : count) {
        double p = (double)i.second / (double)nowData.size();
        //cout <<i.second<<' ' << p << endl;
        output -= p * log(p) / log(2.0);
        //cout << '?' << output << endl;
    }
    //cout << output << endl;
    return output;
}
double DecisionTree::ComputeEntropyPartly(const std::vector<std::vector<std::string> >& nowData,
    const std::string& type, const std::string& typeValue) {
    int cnt = 0;
    map<string, int> count;
    auto typeindex = find(Total_type.begin(), Total_type.end(), type) - Total_type.begin();
    if (typeindex == Total_type.size()) {
        cout << "Error Value in Compute Entropy Partly" << endl;
        return 0.0;
    }
    for (auto& i : nowData) {
        if (i[typeindex] == typeValue) {
            ++cnt;
            count[i.back()]++;
        }
    }
    double output = 0;
    if (count.size() < Tag_set.size()) {
        return 0.0;
    }
    for (auto& i : count) {
        double p = (double)i.second / (double)cnt;
        output -= p * log(p) / log(2.0);

    }
    return output;
}
double DecisionTree::ComputeSumOfEntropy(const std::vector <std::vector<std::string>>& now_data,
    const string& type) {
    map<string, int> count;
    auto typeindex = find(Total_type.begin(), Total_type.end(), type) - Total_type.begin();
    if (typeindex == Total_type.size()) {
        cout << "Error Value in Compute Sum of Entropy" << endl;
        return 0.0;
    }
    for (auto& i : now_data) {
        count[i[typeindex]]++;
    }
    double output = 0.0;
    for (auto& i : count) {
        double ratio = (double)i.second / (double)now_data.size();
        output += ratio * ComputeEntropyPartly(now_data, type, i.first);
    }
    return output;
}

DecisionTree::TreeNode* DecisionTree::BuildTree(TreeNode* nowNode, const std::vector<std::vector<std::string>>& nowData,
    const std::vector<std::string>& nowType) {
    //cout << test++ << endl;
    if (nowNode == nullptr) nowNode = new TreeNode;
    if (root == nullptr) root = nowNode;
    //随机森林：所建的树若无法继续分裂，取有最大数量的tag值作为节点数量。
    if (nowType.empty()) {
        nowNode->type = Total_type.back();
        nowNode->value.push_back( BuildLastNode(nowData));
        return nowNode;
    }
    //
    for (auto& i : Tag_set) {
        if (checkPure(nowData, i)) {
            nowNode->type = Total_type.back();
            nowNode->value.push_back(i);
            return nowNode;
        }
    }

    //计算标签信息熵以及信息最大增益的type
    double totalEntropy = ComputeEntropy(nowData);
  //  cout << "该结点标签信息熵：" << totalEntropy << endl;
    double maxRaiseEntropy = 0.0;
    auto maxRaiseType = nowType.begin();
    for (auto i = nowType.begin(); i < nowType.end()-1; ++i) {

        double temEntropy = ComputeSumOfEntropy(nowData, *i);
        double RaiseEntropy = totalEntropy - temEntropy;//增益捏
    //    cout << "type:\t" << *i << " Conditional Entropy:\t" << temEntropy << " RaiseEntropy:\t" << RaiseEntropy << endl;
        if (maxRaiseEntropy < RaiseEntropy) {
            maxRaiseEntropy = RaiseEntropy;
            maxRaiseType = i;
        }
    }

    nowNode->type = *maxRaiseType;
    vector<string> newType;
    for (auto& i : nowType) {
        if (i != *maxRaiseType) {
            newType.emplace_back(i);
        }
    }

    int maxRaiseIndex = 0;
    for (auto& i : Total_type) {
        if (i == *maxRaiseType)break;
        ++maxRaiseIndex;
    }

    vector<vector<string>> newData;
    for (auto& i : Type_list_set[*maxRaiseType]) {
        for (auto& j : nowData) {
            if (j[maxRaiseIndex] == i) {
                newData.emplace_back(j);
            }
        }
        auto* newNode = new TreeNode();
        nowNode->value.push_back(i);
        if (newData.empty()) {
            newNode->type = Total_type.back();
            newNode->value.push_back( BuildLastNode(nowData));
        }
        else {
          // newNode->value = i;
            BuildTree(newNode, newData, newType);
        }
        nowNode->child.emplace_back(newNode);
        newData.clear();
    }
    return nowNode;
}
bool DecisionTree::checkPure(const std::vector <std::vector<std::string>>& nowData, const std::string& nowTag) {
    int cnt = 0;
    for (auto& i : nowData) {
        if (i.back() == nowTag) {
            ++cnt;
        }
    }
    return cnt == nowData.size();
}
string DecisionTree::BuildLastNode(const std::vector <std::vector<std::string>>& nowData) {
    map<string, int> count;
    for(int i=0;i<nowData.size();++i){
        count[nowData[i].back()]++;
    }
    auto tem = count.begin();
    int maxs = tem->second;
    for (auto i = count.begin(); i != count.end(); ++i) {
        if (maxs < i->second) {
            maxs = i->second;
            tem = i;
        }
    }
    return tem->first;
}
void DecisionTree::PrintTree(const DecisionTree::TreeNode* nowRoot,int depth) {
    for (int i = 0; i < depth; ++i) {
        cout << "\t";
    }
    if (nowRoot->type == Total_type.back()) {
        cout << "Result:" << nowRoot->value.back() << endl;
    }
    else {
        cout <<"Type:"<< nowRoot->type << endl;
        for (int i = 0; i < nowRoot->value.size(); ++i) {
            for (int i = 0; i < depth; ++i) {
                cout << "\t";
            }
            cout <<i+1<<" " << nowRoot->value[i] << endl;
            PrintTree(nowRoot->child[i], depth + 1);
        }

    }
}

string DecisionTree::DoDecision(const TreeNode* nowNode, std::vector<std::string>& question) {
    //cout << nowNode->type << endl;
    if (nowNode->type == Total_type.back()) {
        return nowNode->value.back();
    }
    if (nowNode == nullptr) {
        cout << "Error!";
        exit(0);
    }
    int index = find(Total_type.begin(), Total_type.end(), nowNode->type) - Total_type.begin();
    for (int i = 0; i < nowNode->child.size(); ++i) {
        if (question[index] == nowNode->value[i]) {
            return this->DoDecision(nowNode->child[i], question);
        }
    }
    return "no found!";
}