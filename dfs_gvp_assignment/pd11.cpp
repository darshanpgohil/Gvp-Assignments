#include<iostream.h>
#include<stdlib.h>
#include<conio.h>

struct node
{
	struct node *lptr;
	int info;
	struct node *rptr;
};

void dbl_insert(struct node*,struct node**,struct node**,struct node **,int);
void dbl_delete(struct node**,struct node**,int);
void dbl_display(struct node**);

void main()
{
	struct node *nd,*head=NULL,*tail=NULL,*temp=NULL;

	int val,ch=0;

	while(1)
	{
		cout<<"\n 1. Insert \n 2. Delete \n 3. Display \n 4. Exit \n";

		cout<<"\n Enter The Ch : ";
		cin>>ch;

		switch(ch)
		{
			case 1: cout<<"\n Enter The Val : ";
				cin>>val;
				dbl_insert(nd,&head,&tail,&temp,val);
				break;

			case 2: cout<<"\n Enter The Val : ";
				cin>>val;
				dbl_delete(&head,&tail,val);
				break;

			case 3: dbl_display(&head);
				break;

			case 4: exit(0);
				break;

			default: cout<<"\n Wrong Choice!!!";
		}
	}
}

void dbl_insert(struct node *nd,struct node **head,struct node **tail,struct node **temp,int val)
{
	nd=(struct node*)malloc(sizeof(struct node));
	nd->lptr = NULL;
	nd->info = val;
	nd->rptr = NULL;

	if(*head == NULL)
	{
		*head = *tail = nd;
	}
	else if((*head)->info > val)
	{
		nd->rptr = *head;
		(*head)->lptr = nd;
		*head = nd;
	}
	else if((*tail)->info < val)
	{
		(*tail)->rptr = nd;
		nd->lptr = *tail;
		*tail = nd;
	}
	else
	{
		*temp = *head;

		while(*temp != NULL && (*temp)->info < val)
		{
			*temp = (*temp)->rptr;
		}

		(*temp)->lptr->rptr = nd;
		nd->lptr = (*temp)->lptr;
		nd->rptr = *temp;
		(*temp)->lptr = nd;
	}
}

void dbl_delete(struct node **head,struct node **tail,int val)
{
	struct node *tmp;

	if(*head == NULL)
	{
		cout<<"\n Doublly Linked List Empty";
		return;
	}

	if((*head)->info == val)
	{
		tmp = *head;

		(*head)->rptr->lptr = NULL;
		*head = (*head)->rptr;

		free(tmp);
	}
	else if((*tail)->info == val)
	{
		tmp = *tail;

		(*tail)->lptr->rptr = NULL;
		*tail = (*tail)->lptr;

		free(tmp);
	}
	else
	{
		tmp = *head;

		while(tmp != NULL && tmp->info != val)
		{
			tmp=tmp->rptr;
		}

		if(tmp->info != val)
		{
			cout<<"\n Node Data Not Found!!!";
			return;
		}


		tmp->lptr->rptr = tmp->rptr;
		tmp->rptr->lptr = tmp->lptr;
		free(tmp);
	}
}

void dbl_display(struct node **head)
{
	struct node *tmp;

	tmp = *head;

	if(tmp == NULL)
	{
		cout<<"\n Doublly Linked List Empty";
	}

	while(tmp != NULL)
	{
		cout<<"\n"<<tmp->info;
		tmp= tmp->rptr;
	}
}