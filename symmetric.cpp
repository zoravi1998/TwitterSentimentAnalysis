#include<bits/stdc++.h>

using namespace std;

int makeSymmetric(int N, string s)
{
    int count = 0;
    for (int i = 0; i < N / 2; i++)
    {
        // Left pointer
        int left = i;

        // Right pointer
        int right = N - left - 1;

        // A loop which run from right
        // pointer towards left pointer
        while (left < right)
        {
            // if both char same then
            // break the loop.
            // If not, then we have to
            // move right pointer to one
            // position left
            if (s[left] == s[right])
            {
                //cout<<left<<","<<right<<endl;
                break;
            }
            else
            {
                right--;
            }
        }
        if (left == right)
        {
            return -1;
        }
        /*for (int j = right; j < N-left - 1; j++)
        {
            swap(s[j], s[j + 1]);
            count++;
        }*/
        swap(s[right],s[N-left-1]);
        count+=abs(right-(N-left-1));
    }
    return count;
}
int main()
{

    int n;
    string s;
    cin >> n;
    cin >> s;

    cout << makeSymmetric(n, s) << endl;
}