#include<iostream>
#include<stdio.h>
using namespace std;
int main()
{
    int status;
    char fileName[]= "../data/New Bitmap image.bmp";  //change this to filename
    
    status = remove(fileName);
    if(status==0)
        cout<<"\nFile Deleted Successfully!";
    else
        cout<<"\nError Occurred!";
    cout<<endl;
    return 0;
}