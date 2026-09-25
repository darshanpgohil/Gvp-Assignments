// Write program to convert infix expression 
// to suffix expression using stack

#include<iostream.h>
#include<conio.h>
#include<string.h>

char nextChar(char infix[])
{
    static int i=-1;
    i+=1;
    return (infix[i]);
}

void push(char s[50],int *top, char val)
{
    if(*top == 49)
    {
        cout<<"\n Stack Overflow";
        return;
    }

    *top = *top + 1;
    s[*top] = val;
}

char pop(char s[50], int *top)
{
    *top = *top - 1;
    return (s[*top + 1]);
}

int getRank(char ch)
{
    switch(ch)
    {
        case '#': return 0;
                  break;

        case '+':
        case '-':
        case '*':
        case '/': return -1;
                  break;

        case ')':
        case '(': return 0;
                  break;

        default: return 1;
                 break;
    }
}

int f(char ch)
{
    switch(ch)
    {
        case '#':
        case '(': return 0;
                  break;

        case ')': return -1;
                  break;

        case '+':
        case '-': return 1;
                  break;

        case '*':
        case '/': return 2;
                  break;

        default: return 3;
                 break;
    }
}

void main()
{
    char infix[50],postfix[50]="",stack[50],ch[2],next,temp;
    int top = -1,r = 0;

    cout<<"\n Enter The Infix Expression : ";
    cin>>infix;

    strcat(infix,"#");

    top = top + 1;

    stack[top] = '#';

    next = nextChar(infix);

    while(next != '#')
    {
        if(next == '(')
        {
            push(stack,&top,next);
        }
        else if(next == ')')
        {
            while(stack[top] != '(')
            {
                temp = pop(stack,&top);
                ch[0] = temp;
                ch[1] = '\0';
                strcat(postfix,ch);

                r += getRank(temp);
            }

            pop(stack, &top);
        }
        else if(f(next) == 3){
            ch[0] = next;
            ch[1] = '\0';
            strcat(postfix,ch);

            r += getRank(next);
        }
        else{
            while(f(next) <= f(stack[top]))
            {
                temp = pop(stack,&top);
                ch[0] = temp;
                ch[1] = '\0';
                strcat(postfix,ch);

                r += getRank(temp);
            }

            push(stack,&top,next);
        }

        next = nextChar(infix);
    }

    while(stack[top] != '#')
    {
        if(stack[top] == '(')
        {
            cout<<"\n Invalid Expression";
            return;
        }
        temp = pop(stack, &top);
        ch[0] = temp;
        ch[1] = '\0';

        strcat(postfix, ch);

        r += getRank(temp);
    }


    if(r == 1)
    {
        cout<<"\n Postfix Expression : "<<postfix;
    }
    else{
        cout<<"\n Invalid Infix Expression";
    }

    getch();
}