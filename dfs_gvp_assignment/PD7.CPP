#include<iostream.h>
#include<stdlib.h>
#include<conio.h>

void process_insert(int [],int *,int *,int);
int process_delete(int [],int *,int *);

void main()
{
    int q[10],f=-1,r=-1;
    int process[5] = {5,7,4,8,3};
    int i=0,val=0,count = 5;

    for(i=0;i<5;i++)
    {
	process_insert(q,&f,&r,process[i]);
    }

    i=0;

    while(count != 0)
    {
	val = process_delete(q,&f,&r);

	if(val != -1)
	{
	    cout<<"\n Process "<<i+1<<" : ";

	    if(val > 2)
	    {
		val = val -2;
		cout<<"\n 2 Unit Executed";
	    }
	    else
	    {
		cout<<"\n"<<val<<" Unit Executed";
		val = 0;
		count--;
	    }

	    if(val != 0)
	    {
		process_insert(q,&f,&r,val);
	    }
	}

	i++;

	if(i==5)
	{
	    i=0;
	}
    }

    cout<<"\n All Process Executed";

    getch();
}

void process_insert(int q[],int *f,int *r,int val)
{
    if(*r == *f-1 || (*f==0 && *r==9))
    {
	cout<<"\n Queue is Full";
	return;
    }

    if(*r == 9 && *f != 0)
    {
	*r = 0;
    }
    else
    {
	*r = *r + 1;
    }

    if(*f == -1)
    {
	*f = 0;
    }

    q[*r] = val;
}

int process_delete(int q[],int *f,int *r)
{
    int temp;

    if(*f == -1)
    {
	cout<<"\n Queue Is Empty";
	return -1;
    }

    temp = q[*f];

    if(*f == *r)
    {
	*f = *r = -1;
    }
    else if(*f == 9)
    {
	*f = 0;
    }
    else
    {
	*f = *f + 1;
    }

    return temp;
}

void process_display(int q[],int *f,int *r)
{
    int i=0;

    i = *f;

    while(i != *r)
    {
	cout<<"\n"<<q[i];

	if(i == 9)
	{
	    i=0;
	}
	else
	{
	    i = i + 1;
	}
    }

    cout<<"\n"<<q[i];
}