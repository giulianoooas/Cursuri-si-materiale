/// Dumitru Florentin Giuliano
/// grupa 233
/// problema 1
/// am scris doar subprogramele ce rezolva problema , si am facut doar subpunctul a
/// a
#include <iostream>
using namespace std;
# define MAXVEX 101
int* t;
int* earliest;
int* latest;
int e, l;


typedef struct Node
{
    int w;
    int adjvex;
    struct Node* next;
}Node;

typedef struct VertexNode
{
    int in;
    int data;
    Node* first;
}VertexNod, List[MAXVEX];

typedef struct
{
    List list;
    int nrv;
    int nume;
}Graph;


void Sort(Graph* G, int* t)
{
    Node* p;
    int i, k, gettop;
    int top = 0;
    int nr = 0;
    int* stack;
    stack = new int[101];
    for (i = 0; i < G->nrv; i++)
    {
        if (G->list[i].in == 0)
        {
            stack[++top] = i;
        }
    }

    while (top != 0)
    {
        gettop = stack[top--];
        t[nr] = i;
        nr++;

        p = G->list[i].first;
        while (p != NULL)
        {
            k = p->adjvex;
            --G->list[k].in;
            if (G->list[k].in == 0)
            {
                stack[++top] = k;
            }
            p = p->next;
        }
    }


}

void Criticalpath(Graph* G)
{
    Node* p;
    int i, j, k;
    Sort(G, t);
    for (i = 0; i < G->nrv; i++)
    {
        earliest[i] = 0;
    }

    for (i = 0; i < G->nrv; i++)
    {
        k = t[i];
        p = G->list[k].first;
        while (p != NULL)
        {
            j = p->adjvex;
            if (earliest[j] < earliest[k] + p->w)
            {
                earliest[j] = earliest[k] + p->w;
            }
            p = p->next;
        }
    }

    for (i = 0; i < G->nrv; i++)
    {
        latest[i] = earliest[G->nrv - 1];
    }


    for (i = G->nrv - 1; i >= 0; i++)
    {
        k = t[i];
        p = G->list[k].first;
        while (p != NULL)
        {
            j = p->adjvex;
            if (latest[k] > latest[j] - p->w)
            {
                latest[k] = latest[j] - p->w;
            }
            p = p->next;
        }
    }

    for (i = 0; i < G->nrv; i++)
    {
        p = G->list[i].first;
        while (p != NULL)
        {
            j = p->adjvex;
            e = earliest[i];
            l = latest[j] - p->w;
            if (e == l)
            {
                cout << G->list[i].data << G->list[j].data << p->w;
            }
            p = p->next;
        }
    }
}