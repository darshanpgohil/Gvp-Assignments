#include<iostream.h>
#include<stdlib.h>

struct node
{
    int info;
    struct node *next;
};

void insert_linked_list_stack(struct node **,int);
void delete_linked_list_stack(struct node **);
void peek_linked_list_stack(struct node **);
void display_linked_list_stack(struct node **);

void main()
{
    struct node *top = NULL;
    int ch,val;

    do
    {
	cout<<"\n 1. Insert \n 2. Delete \n 3. Peek \n 4. Display \n 5. Exit \n";

	cout<<"\n Enter The Ch : ";
	cin>>ch;

	switch(ch)
	{
	    case 1: cout<<"\n Enter The Val : ";
		    cin>>val;
		    insert_linked_list_stack(&top,val);
		    break;

	    case 2: delete_linked_list_stack(&top);
		   break;

	    case 3: peek_linked_list_stack(&top);
		   break;

	    case 4: display_linked_list_stack(&top);
		   break;

	    case 5: exit(0);
		    break;

            default: cout<<"\n Wrong Choice";
        }
    } while (1);
    
}

void insert_linked_list_stack(struct node **top,int val)
{
    struct node *nd;

    nd = (struct node *)malloc(sizeof(struct node));

    nd->info = val;
    nd->next = *top;

    *top = nd;

    cout<<val<<" Value Inserted Successfully";
}

void delete_linked_list_stack(struct node **top)
{
    struct node *temp;
    if(*top == NULL)
    {
        cout<<"\n Stack Underflow";
        return;
    }

    temp = *top;

    cout<<"\n"<<(*top)->info<<" Value Poped";
    *top = (*top)->next;

    delete temp;
}

void peek_linked_list_stack(struct node **top)
{
    if(*top == NULL)
    {
        cout<<"\n Stack Underflow";
    }

    cout<<"Peek Value : "<<(*top)->info<<endl;
}

void display_linked_list_stack(struct node **top)
{
    struct node *temp;

    temp = *top;

    if(temp == NULL)
    {
        cout<<"\n Stack Underflow";
        return;
    }

    while(temp != NULL)
    {
        cout<<"\n"<<temp->info<<endl;
        temp = temp->next;
    }
}