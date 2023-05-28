#include "SortNetwork_SIR.h"
#include <fstream>
#include <iostream>
#include <chrono>
using namespace std;

string path=R"(D:\Desktop_total\Class\First_semester_of_sophomore_year\Data_Structure_and_Algorithm\homework\SIR\)";
string fileName="health.txt";
int NodeNum=10000;
//double voteRemoval=0,voteInfect=0,voteSus=0;
//double degreeRemoval=0,degreeInfect=0,degreeSus=0;
int totalNode=0;
int totalCnt=100;

vector<double> ratioTotal;
double total_voteRemoval,total_voteInfect,total_voteSus,total_degreeRemoval,total_degreeInfect,total_degreeSus;
double vari_voteRemoval,vari_voteInfect,vari_voteSus,vari_degreeRemoval,vari_degreeInfect,vari_degreeSus;
vector<double> voteRemoval,voteInfect,voteSus,degreeRemoval,degreeInfect,degreeSus;
ofstream DegreeOut(fileName+"_DegreeRes.txt"),VoteOut(fileName+"_VoteRes.txt");

double calVariance(vector<double>& total,double average,double num){
    double sum=0;
    for(auto &i:total){
        sum+=pow(i-average,2);
    }
    return sum/(num-1);
}

void calculateTotal(SortNetwork_SIR& sortNetworkSir){
    totalNode=sortNetworkSir.totalNode;
    //sortNetworkSir.PrintImportant(VoteOut,DegreeOut);
    cout<<"step 1:vote\n";
    for(int j=0;j<ratioTotal.size();++j){
        VoteOut<<"The "<<j+1<<" alpha case:\n";
        auto start=std::chrono::steady_clock::now();
        for(int i=0; i < totalCnt; ++i){
            sortNetworkSir.SIR_Process_Vote(VoteOut,ratioTotal[j]);
            voteRemoval.push_back(sortNetworkSir.totalNR_Vote);
            voteInfect.push_back(sortNetworkSir.totalIF_Vote);
            voteSus.push_back(sortNetworkSir.totalSU_Vote);
            sortNetworkSir.Reset_Network();
        }
        VoteOut<<"alpha:\t"<<sortNetworkSir.judgeP<<'\n';
        auto end=std::chrono::steady_clock::now();
        std::chrono::duration<double> elapsed_seconds=end-start;
        VoteOut<<"elapsed time: "<<elapsed_seconds.count()<<"s\n";
        VoteOut<<"alpha:"<<sortNetworkSir.judgeP<<'\n';

        total_voteInfect= accumulate(voteInfect.begin(),voteInfect.end(),0);
        total_voteRemoval= accumulate(voteRemoval.begin(), voteRemoval.end(),0);
        total_voteSus= accumulate(voteSus.begin(), voteSus.end(),0);
        vari_voteInfect= calVariance(voteInfect,total_voteInfect/totalCnt,totalCnt);
        vari_voteRemoval= calVariance(voteRemoval,total_voteRemoval/totalCnt,totalCnt);
        vari_voteSus= calVariance(voteSus, total_voteSus / totalCnt, totalCnt);
        VoteOut << totalCnt << " round:\nthe average removal node is " <<total_voteRemoval/(double)totalCnt << "/" << totalNode <<
                ", variance is "<<vari_voteRemoval<< '\n';
        VoteOut << "the average infected node is " << total_voteInfect / (double)totalCnt << "/" << totalNode <<
                ", variance is "<<vari_voteInfect<< '\n';
        VoteOut << "the average susceptible node is " << total_voteSus / (double)totalCnt << "/" << totalNode <<
                ", variance is "<<vari_voteSus<<'\n';
        voteSus.clear();voteInfect.clear();voteRemoval.clear();
    }

    cout<<"step 2: degree:";
    for(int j=0;j<ratioTotal.size();++j){
        DegreeOut<<"The "<<j+1<<" alpha case:\n";
        auto start=std::chrono::steady_clock::now();
        for(int i=0;i<totalCnt;++i){
            sortNetworkSir.SIR_Process_Degree(DegreeOut,ratioTotal[j]);
            degreeRemoval.push_back(sortNetworkSir.totalNR_Degree);
            degreeInfect.push_back(sortNetworkSir.totalIF_Degree);
            degreeSus.push_back(sortNetworkSir.totalSU_Degree);
            sortNetworkSir.Reset_Network();
        }
        DegreeOut<<"alpha:\t"<<sortNetworkSir.judgeP<<'\n';
        auto end=std::chrono::steady_clock::now();
        std::chrono::duration<double> elapsed_seconds=end-start;
        DegreeOut<<"elapsed time: "<<elapsed_seconds.count()<<"s\n";
        DegreeOut<<"alpha:"<<sortNetworkSir.judgeP<<'\n';

        total_degreeInfect= accumulate(degreeInfect.begin(),degreeInfect.end(),0);
        total_degreeRemoval= accumulate(degreeRemoval.begin(),degreeRemoval.end(),0);
        total_degreeSus= accumulate(degreeSus.begin(),degreeSus.end(),0);
        vari_degreeInfect= calVariance(degreeInfect,total_degreeInfect/totalCnt,totalCnt);
        vari_degreeRemoval= calVariance(degreeRemoval,total_degreeRemoval/totalCnt,totalCnt);
        vari_degreeSus=calVariance(degreeSus,total_degreeSus/totalCnt,totalCnt);
        DegreeOut << totalCnt << " round:\nthe average removal node is " << total_degreeRemoval / (double)totalCnt << "/" << totalNode <<
                  ", variance is "<<vari_degreeRemoval<<'\n';
        DegreeOut << "the average infected node is " << total_degreeInfect / (double)totalCnt << "/" << totalNode <<
                  ", variance is "<<vari_degreeInfect<<'\n';
        DegreeOut << "the average susceptible node is " << total_degreeSus / (double)totalCnt << "/" << totalNode <<
                  ", variance is "<<vari_degreeSus<<'\n';
        degreeSus.clear();degreeRemoval.clear();degreeInfect.clear();
    }




}
int main() {
    int n;
    cin>>NodeNum>>n;
    for(int i=0;i<n;i++){
        double tem;
        cin>>tem;
        ratioTotal.push_back(tem);
        cout<<tem<<"\n";
    }
    SortNetwork_SIR sortNetworkSir(path+fileName);
    //cin>>fileName;

    //NodeNum=sortNetworkSir.totalNode/100;
    //cout<<NodeNum<<'\n';
    sortNetworkSir.BeginSort(NodeNum);
    //sortNetworkSir.PrintImportant(VoteOut,DegreeOut);
    calculateTotal(sortNetworkSir);
    //sortNetworkSir.Print_SIR(VoteOut,DegreeOut);
    cout<<"over";
    return 0;
}
