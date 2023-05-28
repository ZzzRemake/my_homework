//
// Created by mgzyqsd on 2022/12/5.
//

#include "SortNetwork_SIR.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <cmath>
#include <queue>
using namespace std;

SortNetwork_SIR::SortNetwork_SIR(const std::string &path) {
    averageK=averageK2=0.0;
    totalSU_Vote= totalNode= totalIF_Vote= totalNR_Vote= totalId=0;
    totalSU_Degree=totalIF_Degree=totalNR_Degree=0;
    ifstream input(path);
    if(!input.is_open()){
        cout<<"Error: Can't open the data file";
        exit(1);
    }
    string nowLine;
    while(getline(input,nowLine)){
        if(nowLine.empty()||nowLine[0]=='%')continue;
        stringstream sinput(nowLine);
        if(nowLine[0]=='#'){
            char first;
            int n,m;
            sinput>>first>>n>>m;
            totalNode=n;
            Graph=vector<vector<int>>(totalNode + 1);
            Score=vector<double>(totalNode + 1);
            Vote=vector<double>(totalNode + 1);
            SIR_Network_Vote=vector<Node>(totalNode + 1);
            SIR_Network_Degree=vector<Node>(totalNode+1);
            Degree=vector<int>(totalNode+1);
            Node_Degree=vector<int>(totalNode+1);
        }else {
            int u, v;
            sinput >> u >> v;
            Graph[u].push_back(v);
            Graph[v].push_back(u);
        }
    }
    for(int i=0; i < SIR_Network_Vote.size(); ++i){
        SIR_Network_Vote[i].id=SIR_Network_Degree[i].id=i;
        Node_Degree[i]=i;
        Vote[i]=1.0;
    }
    Pre_GetK();
}
void SortNetwork_SIR::Pre_GetK() {
    double cnt=0,cnt2=0;
    auto now=Score.begin();
    auto now_Degree=Degree.begin();
    for(auto &i:Graph){
        *(now_Degree++)=int(i.size());*(now++)=double (i.size());
        cnt+=double (i.size());
        cnt2+=pow(i.size(),2);
    }
    averageK= cnt / (double)totalNode, averageK2= cnt2 / (double)totalNode;
    cout<<averageK<<' '<<averageK2<<endl;
}
void SortNetwork_SIR::BeginSort(const int& NodeNum) {
    while(ImportantNode_Vote.size() < NodeNum){
        cout<<ImportantNode_Vote.size();
        double maxs=-1.0;
        int maxp=0;
        for (int i = 0; i < Score.size(); ++i)
            if (Score[i] > maxs&&!(ImportantNode_Vote.count(i))) {
                maxs = Score[i];
                maxp = i;
            }
        Vote[maxp]=0.0;
        for(auto&i:Graph[maxp]){
            Vote[i]=max(Vote[i]-averageK,0.0);
        }
        //cout<<maxs<<' '<<maxp<<'\n';
        ImportantNode_Vote.insert(maxp);
        //cout<<ImportantNode_Vote.count(maxp);
        Update_Score();

    }
    sort(Node_Degree.begin(),Node_Degree.end(),[&](auto a,auto b){
        return Degree[a]>Degree[b];
    });
    for(int i=0;i<Node_Degree.size()&&i<=NodeNum;++i){
        ImportantNode_Degree.insert(Node_Degree[i]);
    }
}

void SortNetwork_SIR::Update_Score() {
    for(int i=0; i < Score.size(); ++i){
        if(ImportantNode_Vote.count(i)){
            continue;
        }
        Score[i]=0.0;
        for(int j=0;j<Graph[i].size();++j){
            Score[i]+=Vote[j];
        }
    }
}

void SortNetwork_SIR::PrintImportant(ofstream& Output_Vote,ofstream& Output_Degree) {
    Output_Vote<<"Total Important nodes are below:\n";
    Output_Vote<<"The average K is "<<averageK<<", average K^2 is "<<averageK2<<'\n';
    for(auto &i:ImportantNode_Vote){
        Output_Vote << i << "\tPreScore:\t" << double(Score[i]) << '\n';
    }
    Output_Degree<<"Total Important nodes are below:\n";
    Output_Degree<<"The average K is "<<averageK<<", average K^2 is "<<averageK2<<'\n';
    for(auto &i:ImportantNode_Degree){
        Output_Degree << i << "\tDegree:\t" << Degree[i] << '\n';
    }
}
void SortNetwork_SIR::Reset_Network() {
    totalIF_Vote=totalIF_Degree=totalSU_Degree=totalSU_Vote=totalNR_Degree=totalNR_Vote=0;
    totalId=0;
    for(int i=0; i < SIR_Network_Vote.size(); ++i){
        SIR_Network_Vote[i].SIR_flag=SUSCEPTIBLE,SIR_Network_Vote[i].type=0;
        SIR_Network_Degree[i].SIR_flag=SUSCEPTIBLE,SIR_Network_Degree[i].type=0;
    }
}

void SortNetwork_SIR::SIR_Process_Vote(ofstream& output,double ratio111) {
    std::random_device rd; //linux下，读取/dev/random获取硬件产生的随机数
    std::mt19937 e{rd()}; // or std::default_random_engine e{rd()}; 用HRNG作为PRNG的种子
    std::uniform_real_distribution<double> uniformReal(0,1);
    //cout<<"1";
    totalSU_Vote=totalNode;
    judgeP=ratio111*averageK/averageK2;
    deque<int> q,temq;
    vector<bool> vis(totalNode + 1, false);
    for(auto i:ImportantNode_Vote) {
        q.push_back(i);
        vis[i] = true;
        ++totalIF_Vote;
        --totalSU_Vote;
        SIR_Network_Vote[i].SIR_flag = INFECTIVE, SIR_Network_Vote[i].type = ++totalId;
        //SIR_Network_Vote[i]=Node(INFECTIVE,++totalId);
    }
    //judgeP=2*averageK/averageK2;
    //cout<<judgeP<<endl;
    int index=0;
    while(!q.empty()){
        //cout<<q.size()<<endl;
        swap(temq,q);
        q.clear();
        int cnt=0;
        while(!temq.empty()){
            auto nowNode_id=temq.front();
            temq.pop_front();
            for(auto v:Graph[nowNode_id]){
                if(!vis[v]){
                    auto temP=uniformReal(e);
                    if(temP<judgeP){
                        ++cnt;
                        q.push_back(v);
                        vis[v]= true;
                        SIR_Network_Vote[v].type=SIR_Network_Vote[nowNode_id].type;
                        SIR_Network_Vote[v].SIR_flag=INFECTIVE;
                        ++totalIF_Vote;
                        --totalSU_Vote;
                    }
                }
            }
            SIR_Network_Vote[nowNode_id].SIR_flag=REMOVAL;
            ++totalNR_Vote;
            --totalIF_Vote;
        }
        //output<<++index<<" step:\t"<<cnt<<" infected node\n";
    }
}

void SortNetwork_SIR::SIR_Process_Degree(ofstream& output,double ratio111) {
    std::random_device rd;
    std::mt19937 e{rd()}; // or std::default_random_engine e{rd()}; 用HRNG作为PRNG的种子
    std::uniform_real_distribution<double> uniformReal(0,1);
    //cout<<"1";
    judgeP=ratio111*averageK/averageK2;
    totalSU_Degree=totalNode;
    deque<int> q,temq;
    totalId=0;
    vector<bool> vis(totalNode + 1, false);
    for(auto i:ImportantNode_Degree) {
        q.push_back(i);
        vis[i] = true;
        ++totalIF_Degree;
        --totalSU_Degree;
        SIR_Network_Degree[i].SIR_flag = INFECTIVE, SIR_Network_Degree[i].type = ++totalId;
    }
    //cout<<judgeP<<endl;
    int index=0;
    while(!q.empty()){
        //cout<<q.size()<<endl;
        swap(temq,q);
        q.clear();
        int cnt=0;
        while(!temq.empty()){
            auto nowNode_id=temq.front();
            temq.pop_front();
            for(auto v:Graph[nowNode_id]){
                if(!vis[v]){
                    auto temP=uniformReal(e);
                    if(temP<judgeP){
                        ++cnt;
                        q.push_back(v);
                        vis[v]= true;
                        SIR_Network_Degree[v].type=SIR_Network_Degree[nowNode_id].type;
                        SIR_Network_Degree[v].SIR_flag=INFECTIVE;
                        ++totalIF_Degree;
                        --totalSU_Degree;
                    }
                }
            }
            SIR_Network_Degree[nowNode_id].SIR_flag=REMOVAL;
            ++totalNR_Degree;
            --totalIF_Degree;
        }
        //output<<++index<<" step:\t"<<cnt<<" infected node\n";
    }
}

void SortNetwork_SIR::PrintSIR_Flag(int SIR_TYPE,vector<Node>& nowNetWork,std::ofstream& fileOutput) {
    for(auto &i:nowNetWork){
        if(i.SIR_flag==SIR_TYPE){
            fileOutput<<i.id<<'\t'<<i.type<<'\n';
        }
    }
}
void SortNetwork_SIR::Print_SIR(std::ofstream& Output_Vote,std::ofstream & Output_Degree) {
    Output_Vote << "Total Removal Node is:\t" << totalNR_Vote << '\n';
    PrintSIR_Flag(REMOVAL,SIR_Network_Vote,Output_Vote);
    Output_Vote << "Total Infected Node is:\t" << totalIF_Vote << '\n';
    PrintSIR_Flag(INFECTIVE,SIR_Network_Vote,Output_Vote);
    Output_Vote << "Total Susceptible Node is:\t" << totalSU_Vote << '\n';
    PrintSIR_Flag(SUSCEPTIBLE,SIR_Network_Vote,Output_Vote);

    Output_Degree << "Total Removal Node is:\t" << totalNR_Degree << '\n';
    PrintSIR_Flag(REMOVAL,SIR_Network_Degree,Output_Degree);
    Output_Degree << "Total Infected Node is:\t" << totalIF_Degree << '\n';
    PrintSIR_Flag(INFECTIVE,SIR_Network_Degree,Output_Degree);
    Output_Degree << "Total Susceptible Node is:\t" << totalSU_Degree << '\n';
    PrintSIR_Flag(SUSCEPTIBLE,SIR_Network_Degree,Output_Degree);
}