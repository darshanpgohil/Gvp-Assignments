// Write menu driven program to
// Implement simple queue 1) insert 2)
// delete 3) modify
// 4) display

#include <iostream.h>
#include <conio.h>

void Qinsert(int[], int *, int *, int);
int Qdelete(int[], int *, int *);
void Qpeep(int[], int *);
void Qmodify(int[], int *, int *, int, int);
void Qdisplay(int[], int *, int *);

void main()
{
    int q[10], front = -1, rear = -1, ch, val, delVal, pos;

    do
    {
	cout << "\n 1. Insert \n 2. Delete \n 3. Peep \n 4. Modify \n 5. Display \n 6. Exit \n";

	cout << "\n Enter Your Choice : ";
	cin >> ch;

	switch (ch)
	{
	case 1:
	    cout << "\n Enter The Val : ";
	    cin >> val;

	    Qinsert(q, &front, &rear, val);
	    break;

	case 2:
	    delVal = Qdelete(q, &front, &rear);

	    if (delVal != -1)
		cout << "\n Deleted Value : " << delVal;
	    break;

	case 3:
	    Qpeep(q, &front);
	    break;

	case 4:
	    cout << "\n Enter The Position : ";
	    cin >> pos;
	    cout << "\n Enter The Value : ";
	    cin >> val;
	    Qmodify(q, &front, &rear, pos, val);
	    break;

	case 5:
	    Qdisplay(q, &front, &rear);
	    break;

	case 6:
	    cout << "Program Is Ended";
	    break;

	default:
	    cout << "\n Wrong Choice";
	}
    } while (ch != 6);
}

void Qinsert(int q[10], int *front, int *rear, int val)
{
    if (*rear == 9)
    {
        cout << "\n Queue is overflow";
        return;
    }

    *rear = *rear + 1;
    q[*rear] = val;

    if (*front == -1)
    {
        *front = 0;
    }
}

int Qdelete(int q[10], int *front, int *rear)
{
    int temp = 0;

    if (*front == -1)
    {
        cout << "\n Queue is Empty";
        return -1;
    }

    temp = q[*front];

    if (*front == *rear)
    {
        *front = *rear = -1;
    }
    else
    {
        *front = *front + 1;
    }

    return temp;
}

void Qpeep(int q[10], int *front)
{
    if (*front == -1)
    {
        cout << "\n Queue Is Underflow";
        return;
    }

    cout << "Peek Element : " << q[*front];
}

void Qmodify(int q[10], int *front, int *rear, int pos, int val)
{
    if (*front == -1)
    {
        cout << "\n Queue Is Empty";
        return;
    }

    if (pos < *front || pos > *rear)
    {
        cout << "\n Invalid Position";
        return;
    }

    q[pos] = val;

    cout << "\n Queue Is Value Modify Successfully";
}

void Qdisplay(int q[10], int *front, int *rear)
{
    int i = *front;

    if (*front == -1)
    {
        cout << "\n Queue Is Empty";
        return;
    }

    while (i <= *rear)
    {
        cout << " " << q[i];
        i = i + 1;
    }
}