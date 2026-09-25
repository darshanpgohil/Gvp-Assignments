// Write menu driven program to
// Implement Double stack 1) Push 2) pop 3)
// peep
// 4) modify  5) display

#include <iostream.h>
#include<stdlib.h>

void push(int s[10], int *top1, int *top2, int val)
{
    if (*top1 + 1 == *top2)
    {
        cout << "\nStack Overflow";
        return;
    }

    int stackChoice;

    cout << "\n 1.pre-stack 2.de-stack";

    cout << "\nEnter The StackChoice : ";
    cin >> stackChoice;

    if (stackChoice == 1)
    {
        *top1 = *top1 + 1;
        s[*top1] = val;
    }
    else if (stackChoice == 2)
    {
        *top2 = *top2 - 1;
        s[*top2] = val;
    }
    else
    {
        cout << "\nWrong Choice Please Choice Only 1 or 2 stackChoice";
    }
}

void pop(int s[10], int *top1, int *top2)
{
    int popChoice = 0;

    cout << "\n1. Pop From Pre-stack \n 2. Pop From De-stack";

    cout << "\nEnter The PopChoice : ";
    cin >> popChoice;

    if (popChoice == 1)
    {
        if (*top1 == -1)
        {
            cout << "Stack is Empty";
            return;
        }
        cout << "\nPre-stack value pop : " << s[*top1];
        *top1 = *top1 - 1;
    }
    else if (popChoice == 2)
    {
        if (*top2 == 10)
        {
            cout << "\nStack is Empty";
            return;
        }
        cout << "\nDe-stack value pop : " << s[*top2];
        *top2 = *top2 + 1;
    }
}

void peep(int s[10], int *top1, int *top2)
{
    int peepChoice;

    cout << "\n Enter The Peep Choice : ";
    cin >> peepChoice;

    if (peepChoice == 1)
    {
        if (*top1 == -1)
        {
            cout << "\n Pre-stack Is An Empty";
            return;
        }

        cout << "\n Peep Value In Pre-stack : " << s[*top1];
    }
    else if (peepChoice == 2)
    {
        if (*top2 == 10)
        {
            cout << "\n De-stack Is An Empty";
            return;
        }

        cout << "\n Peep Value In De-stack : " << s[*top2];
    }
    else
    {
        cout << "\n Wrong peepChoice Pleace Choice Only 1 OR 2 Value Only";
    }
}

void modify(int s[10], int *top1, int *top2)
{
    int modifyChoice, pos, val;

    cout << "\n Enter The ModifyChoice : ";
    cin >> modifyChoice;

    cout << "\n Enter The Position : ";
    cin >> pos;

    cout << "\n Enter The Value : ";
    cin >> val;

    if (modifyChoice == 1)
    {
        if (*top1 == -1)
        {
            cout << "\n Pre-stack Is Empty";
            return;
        }

        if (pos < 0 || pos > *top1)
        {
            cout << "\n Invalid Position";
            return;
        }

        s[pos] = val;

        cout << "\n Pre Stack Value Modify Successfully";
    }
    else if (modifyChoice == 2)
    {
        if (*top2 == 10)
        {
            cout << "\n De-stack Is Empty";
            return;
        }

        if (pos > 10 || pos < *top2)
        {
            cout << "\n Invalid Position";
            return;
        }

        s[pos] = val;

        cout << "\n De Stack Value Modify Successfully";
    }
    else
    {
        cout << "\n Wrong Modify Choice Please Choice Modify Only 1 OR 2";
    }
}

void display(int s[10], int top1, int top2)
{
    int i = 0, j = 0, displayChoice;

    cout << "\n Enter The DisplayChoice : ";
    cin >> displayChoice;

    if (displayChoice == 1)
    {
        if (top1 == -1)
        {
            cout << "\nPre-Stck is Empty";
        }
        else
        {
            for (i = top1; i >= 0; i--)
            {
                cout << "\n Pre-stack : " << s[i];
            }
        }
    }
    else if (displayChoice == 2)
    {
        if (top2 == 10)
        {
            cout << "\nDe-stack is Empty";
        }
        else
        {
            for (j = top2; j < 10; j++)
            {
                cout << "\nDe-stack : " << s[j];
            }
        }
    }
    else
    {
        cout << "\n Wrong Display Choice, Only Allow Display Choice (1 OR 2)";
    }
}

void main()
{
    int stack[10];
    int top1 = -1, top2 = 10, ch, val;

    do
    {
        cout << "\n 1.Push \n 2.Pop \n 3.Peep \n 4.Modify \n 5.Display  \n 6.Exit";

        cout << "\nEnter Your Choice : ";
        cin >> ch;

        switch (ch)
        {
        case 1:
            cout << "\nEnter The Value : ";
            cin >> val;
            push(stack, &top1, &top2, val);
            break;

        case 2:
            pop(stack, &top1, &top2);
            break;

        case 3:
            peep(stack, &top1, &top2);
            break;

        case 4:
            modify(stack, &top1, &top2);
            break;

        case 5:
            display(stack, top1, top2);
            break;

        case 6:
            exit(0);
            break;

        default:
            cout << "\n Wrong Choice";
        }
    } while (1);
}