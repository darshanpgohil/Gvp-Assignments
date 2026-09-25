#include <iostream.h>
#include<stdlib.h>

struct node
{
    int info;
    struct node *next;
};

void insert_sl(struct node *, struct node **, int);
void delete_sl(struct node **,int);
void modify_sl(struct node **,int,int);
void display_sl(struct node **);

void main()
{
    struct node *nd, *head = NULL;
    int val, newVal, ch;

    do
    {
        cout<<"\n 1. Insert \n 2. Delete \n 3. Modify \n 4. Display \n 5. Exit \n";

        cout<<"\n Enter The Ch : ";
        cin>>ch;

        switch (ch)
        {
        case 1:
            cout<<"\n Enter The Val : ";
            cin>>val;
            insert_sl(nd, &head, val);
            break;

        case 2:
            cout<<"\n Enter The Val For Delete : ";
            cin>>val;
            delete_sl(&head,val);
            break;

        case 3:
            cout<<"\n Enter The Val For Modify : ";
            cin>>val;
            cout<<"\n Enter The New Val : ";
            cin>>newVal;
            modify_sl(&head,val,newVal);
            break;

        case 4:
            display_sl(&head);
            break;

        case 5:
            exit(0);
            break;

        default:
            cout << "\n Wrong Choice";
            break;
        }
    } while (1);
}

void insert_sl(struct node *nd, struct node **head, int val)
{
    struct node *t1 = NULL, *t2 = NULL;

    nd = (struct node *)malloc(sizeof(struct node));
    nd->info = val;
    nd->next = NULL;

    if (*head == NULL)
    {
        *head = nd;
    }
    else if ((*head)->info > val)
    {
        nd->next = *head;
        *head = nd;
    }
    else
    {
        t1 = *head;

        while (t1 != NULL && t1->info < val)
        {
            t2 = t1;
            t1 = t1->next;
        }

        t2->next = nd;
        nd->next = t1;
    }
}

void delete_sl(struct node **head,int val)
{
    struct node *temp,*t1,*t2;

    if(*head == NULL)
    {
        cout<<"\n Linked List Is Empty";
        return;
    }
    else if((*head)->info == val)
    {
        temp = *head;
        *head = (*head)->next;
        free(temp);
    }
    else
    {
        t1 = *head;

        while(t1 != NULL && t1->info != val)
        {
            t2 = t1;
            t1 = t1->next;
        }

        t2->next = t1->next;
        free(t1);
    }
}

void modify_sl(struct node **head,int val,int newVal)
{
    struct node *ptr;

    ptr = *head;

    if(ptr == NULL)
    {
        cout<<"\n Linked List Is Empty";
        return;
    }

    while(ptr != NULL && ptr->info != val)
    {
        ptr = ptr->next;
    }

    val = newVal;

    ptr->info = val;
}

void display_sl(struct node **head)
{
    struct node *ptr;

    ptr = *head;

    if(ptr == NULL)
    {
        cout<<"\n Linked List Is Empty";
        return;
    }

    while (ptr != NULL)
    {
        cout << "\n"
             << ptr->info;
        ptr = ptr->next;
    }
}