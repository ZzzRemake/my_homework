#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <set>
#include <ctime>
#include <algorithm>
using namespace std;

int line_num;//��������

//���ϲ���
//���ɲ���
set<string> add(set<string> &set1, set<string> &set2) {
	set<string> ans(set1.begin(), set1.end());
	for (set<string>::iterator it = set2.begin(); it != set2.end(); it++)
		ans.insert(*it);
	return ans;
}

//����k+1Ƶ�����Ĳ���
bool judgeIsLk_1(const set<string> &a, const set<string> &b) {
	set<string> t = a;
	for (auto &i : b)
		t.erase(i);
	return t.size() == 1;
}

//���ɽ���
set<int> intersec(set<int> &a, set<int> &b) {
	set<int> t;
	set_intersection(a.begin(), a.end(), b.begin(), b.end(), inserter(t, t.begin()));
	return t;
}

class Apriori {//���������ڹ�����,�ṩһϵ��Apriori�㷨�Ĳ���
	private:
		string FileName;// �򿪵��ļ���
		int minSup; // ��С֧�ֶ�
		map< int, set<string> > Database;//���-����
		map< string, set<int> > mp;   //string -- ��������
	public:
		Apriori(string FileName): FileName(FileName), minSup(0) {
		}
		bool buildDataBase();//�������ݼ��͸���ӳ��mp
		map< string, int> getC1();//����C1
		map< set<string>, int > getL1(double min_sup);//����L1
		set< set<string>> keySet(map<set<string>, int> &Lk);//��map���������
		set< set<string> > buildCk_last(int m, set< set<string> > &); //��k����k+1�ĺ�ѡ�,�Ѿ�����֦.
		map< set<string>, int > getLk(int k, set<set<string>> &); //��Lk-1����Lk
		int printFrequntSet(set< set<string> > &setSet); //��ӡ�����Ϣ
};

//��ӡƵ�����Ϣ
int Apriori::printFrequntSet(set<set<string>> &setSet) {
	int cnt = 0;
	for (auto &it : setSet) {
		for (auto &tem : it)
			cout << tem << " ";
		cout << endl;
		++cnt;
	}
	return cnt;
}

//�����ݴ���Map���������ݼ�D:map<TID,�>,������map<int,set<string>>
bool Apriori::buildDataBase() {
	ifstream inFile;
	inFile.open(FileName.c_str());
	if (!inFile.is_open()) {
		cout << "Error:" << FileName << "can't be opened!" << endl;
		return false;
	}
	string textline;
	while (getline(inFile, textline)) {
		istringstream line(textline);
		string word;
		while (line >> word) {
			if (!word.empty()) {
				Database[line_num].insert(word);
				mp[word].insert(line_num);
			}
		}
		line_num++;
	}
	cout << "��������: " << Database.size() << endl;
	return true;
}

//��ȡC1:���ʱ��δ����set����ʾ�(��΢���ٵ㳣��)
map<string, int> Apriori::getC1() {
	map<string, int> C1;
	for (auto &mapIt : Database) {
		for (auto &setIt : mapIt.second) {
			auto ret = C1.insert(make_pair(setIt, 1));  //û��true����false
			if (!ret.second) //ans������setIt��Ӧ��Ԫ��
				ret.first->second++;
		}
	}
	return C1;
}

//��ȡL1
map<set<string>, int> Apriori::getL1(double min_sup) {
	minSup = line_num * min_sup;
	minSup = (int)minSup;
	map<set<string>, int> L1;
	map<string, int> C1 = getC1();
	for (auto &it : C1) {
		if (it.second >= minSup) {
			set<string> Key;
			Key.insert(it.first);
			L1[Key] = it.second;
		}
	}
	return L1;
}

//��ȡ��ѡ�����:ƴ��
set< set<string> > Apriori::keySet(map<set<string>, int> &Lk) {
	set< set<string> > ans;
	for (auto &it : Lk)
		ans.insert(it.first);
	return ans;
}


//L_k-1��ȡCk
set< set<string> > Apriori::buildCk_last(int kless, set<set<string>> &Lk0) {
	set< set<string> > Ck;
	for (auto it = Lk0.begin(); it != Lk0.end(); ) {
		set<string> Li = *it;
		for (auto itr = ++it; itr != Lk0.end(); itr++) {
			set<string> Lj = *itr;
			if (judgeIsLk_1(Li, Lj)) {
				set<string> Ci = add(Li, Lj);
				if (Ci.size() == kless + 1)
					if (!Lk0.count(Ci))
						Ck.insert(Ci);
			}
		}
	}
	return Ck;
}

//����Ƶ��k-1���������ȡƵ��k�
map< set<string>, int > Apriori::getLk(int k, set<set<string> > &Lk0) {
	map< set<string>, int> Lk, Ck;
	set< set<string> > CkSet = buildCk_last(k - 1, Lk0);    //Ck��set-string���ټ��ϳ�set
	for (auto &i : CkSet) { //ÿһ��set<string>
		string head = *i.begin();
		set<int> temp = mp[head];
		for (auto j = ++i.begin(); j != i.end(); ++j) {
			set<int> t = mp[*j];    //j��set<string>���ÿһ��string���ҵ���Ӧ��int
			temp = intersec(temp, t);
		}
		if (temp.size() >= minSup)
			Lk[i] = (int)temp.size();
	}
	return Lk;
}

int main() {
	float min_sup;
	cout << "��������С֧�ֶȣ�";
	cin >> min_sup;
	Apriori apriori("dataset.txt");
	int maxk = 1;
	apriori.buildDataBase();
	map<set<string>, int> L1 = apriori.getL1(min_sup);
	set<set<string>> Set = apriori.keySet(L1); //1-Ƶ��������д�������set
	map<int, set<set<string>>> L;//���е�Ƶ�������,�������С����
	map<set<string>, int> SupportL = L1;
	vector<set<string>> SupportList;//SupprotL��SupprotList����ӳ�����ӳ��
	L.insert(make_pair(1, Set));
	clock_t totalTime = 0;
	for (int k = 2; ; k++) {
		cout << "k=" << k << " ";
		clock_t begin = clock();
		map<set<string>, int> setLk = apriori.getLk(k, Set);  //k-��ȡƵ���������string����Ӧ����
		if (!setLk.empty()) {
			Set = apriori.keySet(setLk);
			L.insert(make_pair(k, Set));
			for (auto &tem : setLk) {
				SupportL[tem.first] = tem.second;
			}
			clock_t end = clock();
			cout << "\ttime used:" << (double)(end - begin) << endl;
			totalTime += (end - begin);
		} else {
			maxk = max(maxk, k);
			clock_t end = clock();
			cout << "\ttime used:" << (double)(end - begin) << endl;
			totalTime += (end - begin);
			break;
		}
	}
	cout << "total time used:" << totalTime << endl;
	for (auto &i : SupportL) {
		SupportList.push_back(i.first);
	}
	sort(SupportList.begin(), SupportList.end(), [&](auto & a, auto & b) { //lambda����������
		return SupportL[a] > SupportL[b];
	});
	ofstream fcout;
	fcout.open("res.txt");
	if (!fcout.is_open()) {
		cout << "����ļ�res.txt����ʧ��" << endl;
		return 0;
	}
	int cnt = 0;
	for (auto &i : L) {
		cout << "Ƶ��" << i.first << "�: " << endl;
		fcout << "Ƶ��" << i.first << "�: " << endl;
		int n = apriori.printFrequntSet(i.second);
		for (auto &j : i.second) {
			for (auto &k : j) {
				fcout << k << " ";
			}
			fcout << endl;
		}
		cout << "n=" << n << endl;
		fcout << "n=" << n << endl;
		cnt += n;
	}
	cout << "����=" << cnt << endl << endl;
	fcout << "����=" << cnt << endl << endl;

	cout << "test1:������е�Ƶ��ģʽ������֧�ֶȽ�������" << endl;
	fcout << "test1:������е�Ƶ��ģʽ������֧�ֶȽ�������" << endl;
	for (auto &i : SupportList) {
		cout << SupportL[i] << ' ';
		fcout << SupportL[i] << ' ';
		for (auto &j : i) {
			cout << j << ' ';
			fcout << j << ' ';
		}
		cout << endl;
		fcout << endl;
	}
	cout << endl;
	fcout << endl;

	cout << "test2:�������Ƶ��ģʽ������֧�ֶ�����" << endl;
	fcout << "test2:�������Ƶ��ģʽ������֧�ֶ�����" << endl;
	vector<set<string>> maxSupportList;
	for (int k = 1; k <= maxk; ++k) {//���ɼ����Ƶ���
		if (k == maxk) {//�����Ƶ�����������
			for (auto &i : L[k]) {
				maxSupportList.push_back(i);
			}
		} else { //Ѱ��k+1��������Լ��Ƿ�Ϊ���,�����Ǳ�Ϊ����Ƶ���
			bool flag = false;
			for (auto &i : L[k]) {
				for (auto &j : L[k + 1]) {
					if (judgeIsLk_1(j, i)) {
						flag = true;
						break;
					}
				}
				if (!flag) {
					maxSupportList.push_back(i);
				}
			}
		}
	}
	sort(maxSupportList.begin(), maxSupportList.end(), [&](auto & a, auto & b) { //����֧�ֶ�����
		return SupportL[a] > SupportL[b];
	});
	for (auto &i : maxSupportList) {
		cout << SupportL[i] << ' ';
		fcout << SupportL[i] << ' ';
		for (auto &j : i) {
			cout << j << ' ';
			fcout << j << ' ';
		}
		cout << endl;
		fcout << endl;
	}
	cout << endl;
	fcout << endl;

	cout << "test3:���֧�ֶ�����ǰk��Ƶ��ģʽ" << endl;
	fcout << "test3:���֧�ֶ�����ǰk��Ƶ��ģʽ" << endl;
	int test4_k;
	cout << "����Ҫ���ļ���Ƶ��ģʽ��������Ƶ��ģʽ�������������Ƶ��ģʽ��";
	cin >> test4_k;
	cout << "֧�ֶ�����ǰ" << test4_k << "��Ƶ��ģʽ:" << endl;
	fcout << "֧�ֶ�����ǰ" << test4_k << "��Ƶ��ģʽ:" << endl;
	for (int i = 0; i < SupportList.size() && i < test4_k; ++i) {
		cout << SupportL[SupportList[i]] << ' ';
		fcout << SupportL[SupportList[i]] << ' ';
		for (auto &j : SupportList[i]) {
			cout << j << ' ';
			fcout << j << ' ';
		}
		cout << endl;
		fcout << endl;
	}
	return 0;
}