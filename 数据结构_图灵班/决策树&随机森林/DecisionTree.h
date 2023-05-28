//
// Created by mgzyqsd on 2022/11/18.
//

#ifndef ID3_DECISIONTREE_H
#define ID3_DECISIONTREE_H

#include <map>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include "set"
#include "iostream"

class DecisionTree {
private:
    std::vector<std::string> Total_type;
    std::vector<std::vector<std::string>> Data_table_row;
    std::map<std::string, std::set<std::string>> Type_list_set;
    std::set<std::string> Tag_set;
    struct TreeNode {
        std::vector<TreeNode*> child;
        std::string type;
        std::vector<std::string> value;
    };
    void DesTroyTree(TreeNode* nowNode);
    bool checkPure(const std::vector<std::vector<std::string>>& nowData, const std::string& nowTag);
    std::string BuildLastNode(const std::vector<std::vector<std::string>>& nowData);
    double ComputeEntropy(const std::vector<std::vector<std::string>>& nowData);
    double ComputeEntropyPartly(const std::vector<std::vector<std::string> >& nowData,
        const std::string& type, const std::string& typeValue);
    double ComputeSumOfEntropy(const std::vector<std::vector<std::string>>& nowData,
        const std::string& type);
public:
    TreeNode* root;
    DecisionTree(const std::vector<std::string>& totaltype, const std::vector<std::vector<std::string>>& Datatablerow,
        const std::map<std::string, std::set<std::string>>& Typelistset,const std::set<std::string>& Tagset);
    ~DecisionTree();
    TreeNode* BuildTree(TreeNode* nowNode, const std::vector<std::vector<std::string>>& nowData,
        const std::vector<std::string>& nowType);
    void PrintTree(const TreeNode* nowRoot,int depth);
    std::string DoDecision(const TreeNode*nowNode,std::vector<std::string>& question);
};


#endif //ID3_DECISIONTREE_H