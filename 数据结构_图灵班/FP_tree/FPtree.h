//
// Created by mgzyqsd on 2023/1/9.
//

#ifndef UNTITLED_FPTREE_H
#define UNTITLED_FPTREE_H

#include "map"
#include "string"
#include "vector"
#include "iostream"
#include "set"
#include "utility"
#include "memory"

struct FPNode {
    const std::string item;
    unsigned long long cnt;
    std::shared_ptr<FPNode> link;
    std::weak_ptr<FPNode> parent;
    std::vector<std::shared_ptr<FPNode>> children;

    FPNode(std::string  item, const std::shared_ptr<FPNode>& parent);
};

class FPTree {
private:
    void ReadData(const std::string& path);
    std::map<std::string,unsigned long long> itemCnt;
    std::vector<std::vector<std::string>> originData;
    unsigned long long minSup;
    double minCon;

    std::shared_ptr<FPNode> root;
    std::map<std::string,std::shared_ptr<FPNode>> headTable;

    bool isSinglePath(const std::shared_ptr<FPNode>& nowNode);
    bool isSinglePath(const FPTree& nowTree);

    std::set<std::pair<std::set<std::string>, unsigned long long int>> FP_Growth(const FPTree& nowTree);
    void getRules(const std::pair<std::set<std::string>,unsigned long long>& freItem,
                  const std::pair<std::set<std::string>,unsigned long long>& nowFreItem);
public:
    std::set<std::pair<std::set<std::string>,unsigned long long>> frequentSet;
    std::map<std::pair<std::set<std::string>,std::set<std::string>>,double>
        rulesWithConfidence;

    FPTree(const std::vector<std::vector<std::string>>& nowTransactions,
           const unsigned long long minSup,double minCon);

    bool empty() const;
    void GenerateFrequentRules();
    void GenerateRules();
};

#endif //UNTITLED_FPTREE_H
