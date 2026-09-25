// Write menu driven program to
// Implement circular queue 1) insert 2)
// delete 3) modify 4) display

#include <iostream.h>
#include <stdlib.h>

void circular_insert(int[], int *, int *, int);
int circular_delete(int[], int *, int *);
void circular_display(int[], int, int);

void main()
{
    int q[10], f=-1, r=-1, val, ch, deleteVal;

    do
    {
        cout<<"\n 1.Insert \n 2.Delete \n 3.Display \n 4.Exit";

        cout<<"\n Enter The Ch : ";
        cin>>ch;

        switch (ch)
        {
            case 1:
                cout<<"\n Enter The Value : ";
                cin>>val;
                circular_insert(q,&f,&r,val);
                break;
            case 2:
                deleteVal = circular_delete(q,&f,&r);
                if(deleteVal == -1)
                {
                    cout<<"\n Value Can't Delete";
                    break;
                }
                else
                {
                    cout<<"Deleted Value : "<<deleteVal;
                }
                break;
            case 3:
                circular_display(q,f,r);
                break;

            case 4:
                cout<<"\n Program Ended";
                exit(0);
                break;
            default: cout<<"\n Wrong Choice";
        }
    } while (1);
}

void circular_insert(int q[10],int *f,int *r,int val)
{
    if((*r == *f-1) || (*r==10-1 && *f==0))
    {
        cout<<"\n Circular_queue is full";
        return;
    }

    if(*r == 10-1 && *f!=0)
    {
        *r=0;
    }
    else
    {
        *r = *r+1;
    }

    if(*f == -1)
    {
        *f = *f + 1;
    }

    q[*r] = val; 
}

int circular_delete(int q[10],int *f,int *r)
{
    int val;

    if(*f==-1)
    {
        cout<<"\n Circular Queue Is Empty";
        return -1;
    }

    val = q[*f];

    if(*f == *r)
    {
        *f=*r=-1;
    }
    else if(*f == 10-1)
    {
        *f = 0;
    }
    else
    {
        *f = *f + 1;
    }

    return val;
}

void circular_display(int q[10],int f,int r)
{
    int i;

    i = f;
    
    while(i!=r)
    {
        cout<<"\n"<<q[i];

        if(i==10-1)
        {
            i=0;
        }
        else
        {
            i+=1;
        }
    }

    if(f!=-1)
    {
        cout<<"\n"<<q[i];
    }
    else 
    {
        cout<<"\n Circular Queue Is Empty";
    }
}