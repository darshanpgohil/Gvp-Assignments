// Write Menu driven program to 
// implement operations of stack 1) Push 2) 
// pop 3) peep  
// 4) modify  5) display

#include<iostream.h>
#include<stdlib.h>
void push(int s[10],int *top,int val)
{
    if(*top == 9)
    {
        cout<<"\n Stack Overflow";
        return;
    }

    *top = *top + 1;
    s[*top] = val;
}

void pop(int s[10],int *top)
{
    if(*top == -1)
    {
        cout<<"\n Stack is empty";
        return;
    }

    cout<<"\n Poped Value : "<<s[*top];
    *top = *top - 1;
}

void peep(int s[10],int top)
{
    if(top == -1)
    {
        cout<<"Stack Is Empty ";
        return;
    }

    cout<<"Peep Value : "<<s[top];
}

void modify(int s[10],int *top,int pos,int val)
{
    if(*top == -1)
    {
        cout<<"\n Stack Empty";
        return;
    }

    if(pos<0 || pos>*top)
    {
        cout<<"Invalid Position";
        return;
    }

    s[pos] = val;

    cout<<"Value Modify Succesfully";
}

void display(int s[10],int top)
{
    int i;

    if(top == -1)
    {
        cout<<"\n Stack is empty";
        return;
    }

    for(i=top;i>=0;i--)
    {
        cout<<"\n Stack : "<<s[i];
    }
}

void main()
{
    int stack[10];
    int top = -1,val,ch,pos;

    do{
        cout<<"\n 1.push \n 2.pop \n 3.peep \n 4.modify \n 5.display \n 6.exit";

        cout<<"\n Enter Your Choice : ";
        cin>>ch;

        switch(ch)
        {
            case 1: cout<<"\n Enter The Value : ";
                    cin>>val;
                    push(stack,&top,val);
                    break;

            case 2: pop(stack,&top);
                    break;

            case 3: peep(stack,top);
                    break;
            
            case 4: cout<<"\n Enter The Position : ";
                    cin>>pos;
                    cout<<"\n Enter The Value : ";
                    cin>>val;
                    modify(stack,&top,pos,val);
                    break;
            
            case 5: display(stack,top);
                    break;

            case 6: exit(0);
                    break;

            default: cout<<"\n Wrong Choice";
        }
    }while(1);
}