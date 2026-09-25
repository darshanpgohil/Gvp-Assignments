#include<iostream.h>
#include<stdlib.h>

void priority_insert(int [],int *,int *,int);
int priority_delete(int [],int *,int *);
void priority_display(int [],int *,int *);

void main()
{
    int p1[10],p2[10],p3[10];
    int f1=-1,r1=-1,f2=-1,r2=-1,f3=-1,r3=-1,ch,val,priority,deleteVal;
    
    do
    {
        cout<<"\n 1.Insert \n 2.Delete \n 3.Display \n 4.Exit";

        cout<<"\n Enter Your Choice : ";
        cin>>ch;

        switch(ch)
        {
            case 1:
                   cout<<"\n Enter Value : ";
                   cin>>val;
                   
                   cout<<"\n Enter Priority (1,2,3) : ";
                   cin>>priority;

                   if(priority == 1)
                   {
                        priority_insert(p1,&f1,&r1,val);
                   }
                   else if(priority == 2)
                   {
                        priority_insert(p2,&f2,&r2,val);
                   }
                   else
                   {
                        priority_insert(p3,&f3,&r3,val);
                   }
                   break;

            case 2: 
                   if(f1 != -1)
                   {
                        deleteVal = priority_delete(p1,&f1,&r1);
                        cout<<"\n Deleted Value : "<<deleteVal;
                   }
                   else if(f2 != -1)
                   {
                        deleteVal = priority_delete(p2,&f2,&r2);
                        cout<<"\n Deleted Value : "<<deleteVal;
                   }
                   else if(f3 != -1)
                   {
                        deleteVal = priority_delete(p3,&f3,&r3);
                        cout<<"\n Deleted Value : "<<deleteVal;
                   }
                   else
                   {
                        cout<<"\n Queue is Empty";
                   }
                   break;
            
            case 3:
                    cout<<"\n Priority 1 Queue : ";
                    priority_display(p1,&f1,&r1);
                    cout<<"\n Priority 2 Queue : ";
                    priority_display(p2,&f2,&r2);
                    cout<<"\n Priority 3 Queue : ";
                    priority_display(p3,&f3,&r3);
                    break;

            case 4:
                    exit(0);
                    break;

            default: cout<<"\n Invalid Choice";
                     break;

                    
        }
    }while(1);
}

void priority_insert(int p[],int *f,int *r,int val)
{
    if(*r == 9)
    {
        cout<<"\n Queue is Full";
    }

    *r = *r + 1;

    if(*f == -1)
    {
        *f = 0;
    }

    p[*r] = val;
}

int priority_delete(int p[],int *f,int *r)
{
    int temp;

    if(*f == -1)
    {
        cout<<"\n Queue Is Empty";
        return -1;
    }

    temp = p[*f];

    if(*f == *r)
    {
        *f=*r=-1;
    }
    else
    {
        *f = *f + 1;
    }

    return temp;
}

void priority_display(int p[],int *f,int *r)
{
    int i=0;
    if(*f == -1)
    {
        cout<<"\n Queue Is Empty";
        return;
    }

    i = *f;

    while(i <= *r)
    {
        cout<<"\n"<<p[i];
        i=i+1;
    }
}