//
// Created by mgzyqsd on 2022/12/5.
//

#ifndef SIR_SORTNETWORK_SIR_H
#define SIR_SORTNETWORK_SIR_H

#include <vector>
#include <map>
#include "string"
#include "set"
#include <cmath>
#include "random"

enum SIR_TYPE{
    SUSCEPTIBLE=1,INFECTIVE=2,REMOVAL=3
};

class SortNetwork_SIR {
    struct Node{
        int id;
        int SIR_flag;
        int type;
        Node(){
            id=0,SIR_flag=SUSCEPTIBLE,type=0;
        }
        //Node(int flag,int type):SIR_flag(flag),type(type){}
    };
    int totalId=0;
    std::vector<std::vector<int>> Graph;
    std::vector<double> Score;
    std::vector<double> Vote;
    std::vector<int> Node_Degree;
    std::vector<int> Degree;
    std::vector<Node> SIR_Network_Vote,SIR_Network_Degree;
    double averageK;
    double averageK2;
    std::set<int> ImportantNode_Vote,ImportantNode_Degree;
public:
    double judgeP;
    int totalNode;
    int totalNR_Vote,totalIF_Vote,totalSU_Vote;
    int totalNR_Degree,totalIF_Degree,totalSU_Degree;
    SortNetwork_SIR(const std::string& path);
    void Update_Score();
    void Reset_Network();
    void Pre_GetK();
    void BeginSort(const int &NodeNum);
    void PrintImportant(std::ofstream& Output_Vote,std::ofstream & Output_Degree);
    void SIR_Process_Vote(std::ofstream& output,double ratio111);
    void SIR_Process_Degree(std::ofstream& output,double ratio111);
    void Print_SIR(std::ofstream& Output_Vote,std::ofstream & Output_Degree);
    static inline void PrintSIR_Flag(int SIR_TYPE,std::vector<Node>& nowNetWork,std::ofstream& fileOutput);
};

#endif //SIR_SORTNETWORK_SIR_H
