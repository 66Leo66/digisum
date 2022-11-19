#include <bits/stdc++.h>
#define MAXN 10000005
#define int long long

using namespace std;

int n;
int he;
int aswh;
int ans;

int uu[MAXN];

inline void init(int n) {
    for (int i = 1; i <= n; i++) {
        uu[i] = i;
    }
}

inline int swh(int x) {
    int tot = 0;
    while (x) {
        tot += x % 10;
        x /= 10;
    }

    return tot;
}

inline int anssum(int n, int k) {
    printf("%lld\n", k);
    if (n < 10) return k;
    int e = n;
    int tot = 0;
    int _p = 1;
    while (e / 10) {
        e /= 10;
        tot++;
    }
    for (int i = 1; i <= tot; i++) e *= 10, _p *= 10;
    e -= 1;
    if (n - e == _p) e = n;
    //	printf("%lld",e);
    int aaaswh = swh(e);
    int ooo;
    while (aaaswh > 0) {
        ooo = swh(aaaswh);
        while (ooo >= 10) ooo = swh(ooo);
        if (ooo == k) return aaaswh;
        aaaswh--;
    }

    //	if(n == 2018 && k == 3)
    //	{
    //		return 21;
    //	}
    return 1;
}

inline void out(int l, int r) {
    int e;
    for (int i = l + 1; i <= r; i++) {
        e = swh(uu[i - 1] + uu[i]);
        printf("%lld + %lld -> %lld\n", uu[i - 1], uu[i], e);
        uu[i] = e;
    }
}

inline void solve(int n, int sss) {
    int e = n;
    int k = 0;
    int o;
    while (e) k++, e /= 10;
    k--;
    int mid = 0;
    if (k != 0) {
        o = sss % k ? sss / k + 1 : sss / k;
        o = o >= 9 ? 8 : o;
        int _p = 1;
        for (int i = 1; i < k; i++) {
            mid += o;
            mid *= 10;
            _p *= 10;
        }
        if (sss - (k - 1) * o >= 9)
            mid += 8;
        else
            mid += sss - (k - 1) * o;
    } else
        mid = sss;
    printf("%lld\n", mid);
    out(1, mid - 1);
    out(mid + 1, n);
    int aans;
    if (mid > 1 && mid < n) {
        printf("%lld + %lld -> %lld\n", uu[mid - 1], uu[n], e = swh(uu[mid - 1] + uu[n]));
        printf("%lld + %lld -> %lld\n", e, mid, aans = swh(e + mid));
    } else {
        if (mid == 1)
            e = uu[n];
        else if (mid == n)
            e = uu[n - 1];
        printf("%lld + %lld -> %lld\n", e, mid, aans = swh(e + mid));
    }
    if (aans != sss) {
        printf("NO,ans should be : %lld\n\n", sss);
    } else
        printf("YES,ans : %lld\n\n", sss);
}

inline void out2(int l, int r) {
    int e;
    for (int i = r - 1; i >= l; i--) {
        e = swh(uu[i + 1] + uu[i]);
        printf("%lld + %lld -> %lld\n", uu[i + 1], uu[i], e);
        uu[i] = e;
    }
}

inline void solve2() {
    init(n);
    out2(2, n);
    int aans;
    printf("%lld + %lld -> %lld\n", uu[2], uu[1], aans = swh(uu[2] + uu[1]));

    if (aans != aswh) {
        printf("NO,ans should be : %lld\n\n", aswh);
    } else
        printf("YES,ans : %lld\n\n", aswh);
}

#undef int
int main() {
#define int long long
    scanf("%lld", &n);
    if (n == 1) {
        printf("1");
        return 0;
    }
    //	for(int i = 1;i <= n;i++)
    //	{
    //		uu[i] = i;
    //	}

    init(n);
    he = (n + 1) * n / 2;
    aswh = swh(he);
    //	printf("%lld\n",aswh);
    while (aswh >= 10) aswh = swh(aswh);
    //	printf("%lld\n",aswh);
    ans = anssum(n, aswh);

    //	printf("%lld\n",ans);
    solve(n, ans);

    solve2();

    return 0;
}

/*12351*/