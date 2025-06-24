#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>

#define endl "\n"
#define all(v) (v).begin(), (v).end()

using namespace std;
int NUM_OF_V;
int TOTAL_DEG, TOTAL_EDGE;
int SEQ_NUM;

// 1-indexed fenwick tree
template <class T> struct Fenwick
{
    int n;
    vector<T> fw;
    Fenwick() = default;
    Fenwick(int n) : n{n}, fw(n+1, T{}) {}
    void update(int ind, T delta) {
        while(ind <= n){
            fw[ind] += delta;
            ind += (ind&-ind);
        }
    }
    T get(int ind) {
        T ret{};
        while(ind > 0){
            ret += fw[ind];
            ind -= (ind&-ind);
        }
        return ret;
    }
};

// check deg_{i}+deg{n+1-i} == NUM_OF_V-1 for all i = 1, 2, ... NUM_OF_V
bool deg_symmetry(vector<int>& deg)
{
    for(int i = 1; i <= NUM_OF_V; ++i){
        if(deg[i]+deg[NUM_OF_V+1-i] != NUM_OF_V-1) return false;
    }
    return true;
}

// return True if deg is graphic
bool Erdos_Gallai(vector<int>& deg, Fenwick<int>& acc, int odd)
{
    if(odd&1) return false;

    for(int k = 1; k <= NUM_OF_V; ++k){
        int left = acc.get(k);
        int right = k*(k-1);
        auto p = upper_bound(deg.begin(), deg.end(), k,
                               [](int a, int b) { return a > b; }) - deg.begin(); // leftmost index p s.t. deg[p] < k
        if(p < k+1){
            right += acc.get(NUM_OF_V)-acc.get(k);
        }
        else if(p <= NUM_OF_V){
            right += (p-k-1)*k;
            right += acc.get(NUM_OF_V)-acc.get(p-1);
        }
        else{
            right += (NUM_OF_V-k)*k;
        }
        if(left > right) return false;
    }   
    
    return true;
}

void partition(vector<int>& deg, Fenwick<int>& acc, int ind, int rm_deg, int sum, int odd)
{
    if(ind > NUM_OF_V){
        if(!deg_symmetry(deg)) return;
        if(!Erdos_Gallai(deg, acc, odd)) return;
        for(int i = 1; i <= NUM_OF_V; ++i) cout << deg[i] << " ";
        cout << endl;
        SEQ_NUM += 1;
 
        return;
    }

    for(int d = min(rm_deg, deg.back()); d >= 0; --d){
        deg.push_back(d); odd += (d&1); acc.update(ind, d);
        if(sum+(NUM_OF_V-ind+1)*d >= TOTAL_DEG) {
            partition(deg, acc, ind+1, rm_deg-deg.back(), sum+deg.back(), odd);
            deg.pop_back(); odd -= (d&1); acc.update(ind, -d);
        }
        else{
            deg.pop_back(); odd -= (d&1); acc.update(ind, -d);
            return;
        }
    }
}

int main()
{
    cin >> NUM_OF_V;
    assert(NUM_OF_V%4 == 0 || NUM_OF_V%4 == 1);
    assert(NUM_OF_V < 1e4); // prevent interger v overflow

    TOTAL_DEG = NUM_OF_V*(NUM_OF_V-1)/2; 
    TOTAL_EDGE = NUM_OF_V*(NUM_OF_V-1)/4; 
    vector<int> deg; deg.push_back(NUM_OF_V-1); // use base-1 index
    Fenwick<int> acc(NUM_OF_V);                 // use base-1 index
    partition(deg, acc, 1, TOTAL_DEG, 0, 0);
    cout << "\nTotal: " << SEQ_NUM << endl;

    return 0;
}

