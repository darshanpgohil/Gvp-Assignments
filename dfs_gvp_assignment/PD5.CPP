// Write menu driven program to
// Implement double queue 1) insert 2)
// delete 3) modify
// 4) display

#include <iostream.h>
#include <conio.h>
#include <stdlib.h>

void insert_dqueue(int[], int *, int *, int *, int *, int);
int delete_dqueue(int[], int *, int *, int *, int *);
void peep_dqueue(int[], int, int);
void modify_dqueue(int[], int *, int *, int *, int *);
void display_dqueue(int[], int *, int *, int *, int *);

void main()
{
	int q[10], f1 = -1, r1 = -1, f2 = 10, r2 = 10, val = 0, ch = 0, deletedValue = 0;

	do
	{
		cout << "\n 1.Insert \n 2.Delete \n 3.Peep \n 4.Modify \n 5.Display \n 6.Exit \n";

		cout << "\n Enter The ch : ";
		cin >> ch;

		switch (ch)
		{
		case 1:
			cout << "\n Enter The Value : ";
			cin >> val;
			insert_dqueue(q, &f1, &r1, &f2, &r2, val);
			break;

		case 2:
			deletedValue = delete_dqueue(q, &f1, &r1, &f2, &r2);
			if (deletedValue == -1)
			{
				cout << "\n Dequeue is Empty";
			}
			else
				cout << "\n Deleted Value : " << deletedValue;
			break;

		case 3:
			peep_dqueue(q, f1, f2);
			break;

		case 4:
			modify_dqueue(q,&f1,&r1,&f2,&r2);
			break;

		case 5:
			display_dqueue(q, &f1, &r1, &f2, &r2);
			break;

		case 6:
			exit(0);
			break;

		default:
			cout<<"\n Wrong Choice";
		}
	} while (1);
}

void insert_dqueue(int q[10], int *f1, int *r1, int *f2, int *r2, int val)
{
	int ch = 0;

	if (*r1 == *r2 - 1)
	{
		cout << "\n dqueue is full";
		return;
	}

	cout << "\n 1.insert value in first queue \n 2. insert value in second queue\n";

	cout << "\n Enter Your Choice : ";
	cin >> ch;

	if (ch == 1)
	{
		*r1 = *r1 + 1;
		q[*r1] = val;

		if (*f1 == -1)
		{
			*f1 = *f1 + 1;
		}
	}
	else if (ch == 2)
	{
		*r2 = *r2 - 1;
		q[*r2] = val;

		if (*f2 == 10)
		{
			*f2 = *f2 - 1;
		}
	}
	else
	{
		cout << "\n Please Enter Choice Only (1 or 2)";
		return;
	}
}

int delete_dqueue(int q[10], int *f1, int *r1, int *f2, int *r2)
{
	int ch, temp;

	cout << "\n 1. Delete In First Queue \n 2. Delete In Second Queue";

	cout << "\n Enter Your Choice : ";
	cin >> ch;

	if (ch == 1)
	{
		if (*f1 == -1)
		{
			cout << "\n First Queue Is Empty";
			return -1;
		}

		temp = q[*f1];

		if (*f1 == *r1)
		{
			*f1 = *r1 = -1;
		}
		else
		{
			*f1 = *f1 + 1;
		}

		return temp;
	}
	else if (ch == 2)
	{
		if (*f2 == 10)
		{
			cout << "\n Second Queue Is Empty";
			return -1;
		}

		temp = q[*f2];

		if (*f2 == *r2)
		{
			*f2 = *r2 = 10;
		}
		else
		{
			*f2 = *f2 - 1;
		}

		return temp;
	}
	else
	{
		cout << "\n Wrong Choice";
		return -1;
	}
}

void peep_dqueue(int q[10], int f1, int f2)
{
	int ch;

	cout << "\n 1. First Queue Value \n 2. Second Queue Value";

	cout<<"\n Enter The PeepChoice : ";
	cin >> ch;

	if (ch == 1)
	{
		if (f1 == -1)
		{
			cout << "\n Queue Is Empty";
			return;
		}

		cout << "\n First Queue Value : " << q[f1];
	}
	else if (ch == 2)
	{
		if (f2 == 10)
		{
			cout << "\n Queue Is Empty";
			return;
		}

		cout << "\n Second Queue Value : " << q[f2];
	}
	else
	{
		cout << "\n Wrong Choice";
		return;
	}
}

void modify_dqueue(int q[10], int *f1, int *r1, int *f2, int *r2)
{
	int ch, pos, val;

	cout << "\n 1.modify in Pre-dequeue \n 2. modify in De-dequeue";

	cout << "\n Enter The Ch : ";
	cin >> ch;

	if (ch == 1)
	{
		cout << "\n Enter The Position : ";
		cin >> pos;
		
		cout << "\n Enter The Value : ";
		cin >> val;

		if (*f1 == -1)
		{
			cout << "\n Pre-dequeue is empty";
			return;
		}

		if (pos < *f1 || pos > *r1)
		{
			cout << "\n Invalid Position";
			return;
		}

		q[pos] = val;

		cout<<"\n Pre-dequeue Value Updated Successfully";
	}
	else if (ch == 2)
	{
		cout << "\n Enter The Position : ";
		cin >> pos;
		
		cout << "\n Enter The Value : ";
		cin >> val;

		if (*f2 == 10)
		{
			cout << "\n Pre-dequeue is empty";
			return;
		}

		if (pos > *f2 || pos < *r2)
		{
			cout << "\n Invalid Position";
			return;
		}

		q[pos] = val;

		cout<<"\n De-dequeue Value Updated Successfully";
	}
	else
	{
		cout << "\n Wrong Choice Please Select Choice in (1 OR 2)";
	}
}

void display_dqueue(int q[10], int *f1, int *r1, int *f2, int *r2)
{
	int ch, i = 0;

	cout << "\n 1. Display First Queue \n 2. Display Second Queue";
	cout << "\n Enter Your Choice : ";
	cin >> ch;

	if (ch == 1)
	{
		if (*f1 == -1)
		{
			cout << "\n First Queue Is Empty";
			return;
		}

		i = *f1;

		while (i <= *r1)
		{
			cout << "\n Queue 1 : " << q[i];
			i = i + 1;
		}
	}
	else if (ch == 2)
	{
		if (*f2 == 10)
		{
			cout << "\n Second Queue Is Empty";
			return;
		}

		i = *f2;

		while (i >= *r2)
		{
			cout << "\n Second Queue : " << q[i];
			i = i - 1;
		}
	}
	else
	{
		cout << "\n Wrong Choice";
		return;
	}
}