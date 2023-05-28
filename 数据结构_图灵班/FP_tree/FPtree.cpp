//
// Created by mgzyqsd on 2023/1/9.
//

#include "FPtree.h"
#include <utility>
#include "sstream"
#include "algorithm"

using namespace std;

FPNode::FPNode::FPNode(std::string item, const std::shared_ptr<FPNode> &parent):
    item(std::move(item)),cnt(1),link(nullptr),parent(parent),children(){
}

bool FPTree::empty() const {
    if(root== nullptr){
        cout<<"Error:root is null!";
        exit(0);
    }
    return root->children.empty();
}



FPTree::FPTree(const std::vector<std::vector<std::string>>& nowTransactions,const unsigned long long min_Sup,
    double min_Con):
    root(std::make_shared<FPNode>(std::string(), nullptr)),headTable(),minSup(min_Sup),minCon(min_Con),
    originData(nowTransactions){

    for(auto &i :originData){
        for(auto &j:i){
            ++itemCnt[j];
        }
    }
    for(auto i=itemCnt.begin(); i!=itemCnt.end();){
        const unsigned long long temCnt=i->second;
        if(temCnt<minSup){
            itemCnt.erase(i++);
        } else {
            ++i;
        }
    }
    struct self_compare{
        bool operator()(const pair<string,unsigned long long>&l,const pair<string,unsigned long long>& r) const {
            return tie(l.second,l.first)>tie(r.second,r.first);
        }
    };
    set<pair<string,unsigned long long>,self_compare> sortedItem(itemCnt.cbegin(),itemCnt.cend());

    for(auto &event:originData){
        auto nowRoot=root;
        for(auto & nowPair:sortedItem){
            auto & nowItem=nowPair.first;
            if(find(event.begin(),event.end(),nowItem)!=event.end()){
                auto nxtChild_it=find_if(
                        nowRoot->children.begin(),nowRoot->children.end(),[nowItem](const shared_ptr<FPNode>& nowChild) {
                            return nowItem == nowChild->item;
                        });

                //若未能在现节点下的root的child找到，新建节点。
                if(nxtChild_it == nowRoot->children.end()){

                    //维护新的信息。
                    auto newChild= make_shared<FPNode>(nowItem,nowRoot);
                    nowRoot->children.push_back(newChild);

                    //更新项头表信息
                    if(headTable.count(newChild->item)){
                        auto preNode=headTable[newChild->item];
                        while(preNode->link){
                            preNode=preNode->link;
                        }
                        preNode->link=newChild;
                    } else {
                        headTable[newChild->item]=newChild;
                    }

                    nowRoot=newChild;
                } else {
                    auto nxtNode=*nxtChild_it;
                    ++nxtNode->cnt;
                    nowRoot=nxtNode;
                }
            }
        }
    }
}

bool FPTree::isSinglePath(const FPTree &nowTree) {
    return nowTree.empty()|| isSinglePath(nowTree.root);
}

bool FPTree::isSinglePath(const std::shared_ptr<FPNode> &nowNode) {
    if(nowNode->children.empty()){
        return true;
    }
    if(nowNode->children.size()>1){
        return false;
    }
    return isSinglePath(nowNode->children[0]);
}

std::set<std::pair<std::set<std::string>, unsigned long long int>> FPTree::FP_Growth(const FPTree &nowTree) {
    if(nowTree.empty()){
        return {};
    }
    if(isSinglePath(nowTree)){

        set<pair<set<string>,unsigned long long>> singlePatterns;

        auto nowNode=nowTree.root->children.front();
        while(nowNode){
            auto &nowItem=nowNode->item;
            auto nowCnt=nowNode->cnt;
            pair<set<string>,unsigned long long> newPattern{{nowItem},nowCnt};

            singlePatterns.insert(newPattern);

            for(auto & nowPattern:singlePatterns){
                auto newPattern_2{nowPattern};
                newPattern_2.first.insert(nowItem);
                newPattern_2.second=nowCnt;
                singlePatterns.insert(newPattern_2);
            }

            if (nowNode->children.size() == 1)
                nowNode = nowNode->children[0];
            else
                nowNode = nullptr;
        }

        return singlePatterns;
    } else {
        set<pair<set<string>,unsigned long long>> multiPatterns;
        for(auto & p:nowTree.headTable){
            auto & nowItem=p.first;
            vector<pair<vector<string>,unsigned long long>> conditionalPattern_Prefix;
            auto baseNode=p.second;
            while(baseNode){
                auto nowCnt=baseNode->cnt;
                auto nowNode=baseNode->parent.lock();
                if(nowNode->parent.lock()){
                    pair<vector<string>,unsigned long long> nowPrefix{{},nowCnt};
                    while(nowNode->parent.lock()){
                        nowPrefix.first.push_back(nowNode->item);
                        nowNode=nowNode->parent.lock();
                    }
                    conditionalPattern_Prefix.push_back(nowPrefix);
                }

                baseNode=baseNode->link;
            }

            vector<vector<string>> conditionalTransactions;
            for(auto& nowPath:conditionalPattern_Prefix){
                auto& nowPathItems=nowPath.first;
                auto nowPathCnt=nowPath.second;

                for(unsigned long long i=0;i<nowPathCnt;++i){
                   conditionalTransactions.push_back(nowPathItems);
                }
            }

            const FPTree conditionalFPTree(conditionalTransactions,nowTree.minSup,minCon);
            auto conditionalPatterns= FP_Growth(conditionalFPTree);

            set<pair<set<string>,unsigned long long>> nowPatterns;
            unsigned long long nowCnt=0;
            auto nowNode=p.second;
            while(nowNode){
                nowCnt+=nowNode->cnt;
                nowNode=nowNode->link;
            }
            pair<set<string>,unsigned long long> temPattern{{nowItem},nowCnt};
            nowPatterns.insert(temPattern);

            for(auto& conditionalPattern:conditionalPatterns){
                auto newConditionalPattern{conditionalPattern};
                newConditionalPattern.first.insert(nowItem);
                newConditionalPattern.second=conditionalPattern.second;
                nowPatterns.insert({newConditionalPattern});
            }

            multiPatterns.insert(nowPatterns.cbegin(),nowPatterns.cend());
        }
        return multiPatterns;
    }
}

void FPTree::GenerateFrequentRules() {
    frequentSet=FP_Growth(*this);
}

std::set<std::string> subtractSet(const set<string>& a,const set<string>& b){
    auto ans=a;
    for(const auto& i:b){
        if(ans.count(i)){
            ans.erase(i);
        }
    }
    return ans;
}

void FPTree::getRules(
        const std::pair<std::set<std::string>,unsigned long long>& freItem,
        const std::pair<std::set<std::string>, unsigned long long> &nowFreItem) {
    for(auto& item:nowFreItem.first){
        auto subSet=nowFreItem.first;
        subSet.erase(item);

        unsigned long long value= 0;
        for(auto &j:frequentSet){
            if(j.first==subSet){
                value=j.second;
                break;
            }
        }

        double confidence=0;
        if(value){
            confidence= (double)freItem.second / (double )value;
        }
        if(confidence>=minCon){
            bool flag=false;
            auto temSet= subtractSet(freItem.first,subSet);
            for(auto& rule:rulesWithConfidence){
                if(rule.first.first==subSet&&rule.first.second== temSet){
                    flag=true;
                    break;
                }
            }
            if(!flag){
                rulesWithConfidence[{subSet,temSet}]=confidence;
            }
            if(subSet.size()>1){
                getRules(freItem,{subSet,value});
            }
        }
    }
}

void FPTree::GenerateRules() {
    int cnt=0;
    for(auto& i:frequentSet){
        cout<<++cnt<<' '<<rulesWithConfidence.size()<<'\n';
        if(i.first.size()>1){
            getRules(i,i);
        }
    }
}