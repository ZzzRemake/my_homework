#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <set>
#include <ctime>
#include <algorithm>
using namespace std;

int line_num;//事务数量

//集合操作
//生成并集
set<string> add(set<string> &set1, set<string> &set2) {
	set<string> ans(set1.begin(), set1.end());
	for (set<string>::iterator it = set2.begin(); it != set2.end(); it++)
		ans.insert(*it);
	return ans;
}

//生成k+1频繁集的操作
bool judgeIsLk_1(const set<string> &a, const set<string> &b) {
	set<string> t = a;
	for (auto &i : b)
		t.erase(i);
	return t.size() == 1;
}

//生成交集
set<int> intersec(set<int> &a, set<int> &b) {
	set<int> t;
	set_intersection(a.begin(), a.end(), b.begin(), b.end(), inserter(t, t.begin()));
	return t;
}

class Apriori {//该类类似于工具类,提供一系列Apriori算法的操作
	private:
		string FileName;// 打开的文件名
		int minSup; // 最小支持度
		map< int, set<string> > Database;//编号-事务
		map< string, set<int> > mp;   //string -- 所有行数
	public:
		Apriori(string FileName): FileName(FileName), minSup(0) {
		}
		bool buildDataBase();//生成数据集和辅助映射mp
		map< string, int> getC1();//生成C1
		map< set<string>, int > getL1(double min_sup);//生成L1
		set< set<string>> keySet(map<set<string>, int> &Lk);//由map生成项集集合
		set< set<string> > buildCk_last(int m, set< set<string> > &); //由k生成k+1的候选项集,已经过剪枝.
		map< set<string>, int > getLk(int k, set<set<string>> &); //由Lk-1生成Lk
		int printFrequntSet(set< set<string> > &setSet); //打印相关信息
};

//打印频繁项集信息
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

//将数据存入Map，产生数据集D:map<TID,项集>,这里是map<int,set<string>>
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
	cout << "事物总数: " << Database.size() << endl;
	return true;
}

//获取C1:这个时候还未生成set来表示项集(稍微减少点常数)
map<string, int> Apriori::getC1() {
	map<string, int> C1;
	for (auto &mapIt : Database) {
		for (auto &setIt : mapIt.second) {
			auto ret = C1.insert(make_pair(setIt, 1));  //没有true，有false
			if (!ret.second) //ans中已有setIt对应的元素
				ret.first->second++;
		}
	}
	return C1;
}

//获取L1
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

//获取候选项集集合:拼接
set< set<string> > Apriori::keySet(map<set<string>, int> &Lk) {
	set< set<string> > ans;
	for (auto &it : Lk)
		ans.insert(it.first);
	return ans;
}


//L_k-1获取Ck
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

//根据频繁k-1项集键集，获取频繁k项集
map< set<string>, int > Apriori::getLk(int k, set<set<string> > &Lk0) {
	map< set<string>, int> Lk, Ck;
	set< set<string> > CkSet = buildCk_last(k - 1, Lk0);    //Ck的set-string，再集合成set
	for (auto &i : CkSet) { //每一个set<string>
		string head = *i.begin();
		set<int> temp = mp[head];
		for (auto j = ++i.begin(); j != i.end(); ++j) {
			set<int> t = mp[*j];    //j是set<string>里的每一个string，找到对应的int
			temp = intersec(temp, t);
		}
		if (temp.size() >= minSup)
			Lk[i] = (int)temp.size();
	}
	return Lk;
}

int main() {
	float min_sup;
	cout << "请输入最小支持度：";
	cin >> min_sup;
	Apriori apriori("dataset.txt");
	int maxk = 1;
	apriori.buildDataBase();
	map<set<string>, int> L1 = apriori.getL1(min_sup);
	set<set<string>> Set = apriori.keySet(L1); //1-频繁项集的所有串，做成set
	map<int, set<set<string>>> L;//所有的频繁项集集合,按照项集大小索引
	map<set<string>, int> SupportL = L1;
	vector<set<string>> SupportList;//SupprotL和SupprotList建立映射和逆映射
	L.insert(make_pair(1, Set));
	clock_t totalTime = 0;
	for (int k = 2; ; k++) {
		cout << "k=" << k << " ";
		clock_t begin = clock();
		map<set<string>, int> setLk = apriori.getLk(k, Set);  //k-获取频繁项集的所有string和相应个数
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
	sort(SupportList.begin(), SupportList.end(), [&](auto & a, auto & b) { //lambda来进行排序
		return SupportL[a] > SupportL[b];
	});
	ofstream fcout;
	fcout.open("res.txt");
	if (!fcout.is_open()) {
		cout << "输出文件res.txt创建失败" << endl;
		return 0;
	}
	int cnt = 0;
	for (auto &i : L) {
		cout << "频繁" << i.first << "项集: " << endl;
		fcout << "频繁" << i.first << "项集: " << endl;
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
	cout << "总数=" << cnt << endl << endl;
	fcout << "总数=" << cnt << endl << endl;

	cout << "test1:输出所有的频繁模式，并按支持度降序排列" << endl;
	fcout << "test1:输出所有的频繁模式，并按支持度降序排列" << endl;
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

	cout << "test2:输出极大频繁模式，并按支持度排序" << endl;
	fcout << "test2:输出极大频繁模式，并按支持度排序" << endl;
	vector<set<string>> maxSupportList;
	for (int k = 1; k <= maxk; ++k) {//生成极大的频繁项集
		if (k == maxk) {//对最大频繁项集进行特判
			for (auto &i : L[k]) {
				maxSupportList.push_back(i);
			}
		} else { //寻找k+1项集集合中自己是否为子项集,若不是便为极大频繁项集
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
	sort(maxSupportList.begin(), maxSupportList.end(), [&](auto & a, auto & b) { //按照支持度排序
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

	cout << "test3:输出支持度最大的前k个频繁模式" << endl;
	fcout << "test3:输出支持度最大的前k个频繁模式" << endl;
	int test4_k;
	cout << "你需要最大的几个频繁模式？若超出频繁模式总数则输出所有频繁模式：";
	cin >> test4_k;
	cout << "支持度最大的前" << test4_k << "个频繁模式:" << endl;
	fcout << "支持度最大的前" << test4_k << "个频繁模式:" << endl;
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