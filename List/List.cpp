#include <iostream>
using namespace std;

#include "List.h"

ListT::ListT()
{
  length = 0;
  head = NULL;
  tail = NULL;
}

ListT::~ListT()
{
}

bool ListT::IsEmpty() const
{
  if (head == NULL)
    return true;
  else
    return false;
}

int ListT::GetLength() const
{
  return length;
}

void ListT::PutItemH(const itemType newItem)
{
  
  node* n = new node();
  n->item = newItem;
  n->next = head;
  head = n;
  if (length == 0)
    tail = n;
  length++;
 // n = NULL;
}

itemType ListT::GetItemH() const
{
 itemType itemH;
 itemH = head->item;
 return itemH;
}

void ListT::DeleteItemH()
{
  node* n = new node();
  n = head;
  head = head->next;
  delete n;
}
	
void ListT::Print() const
{
  node* n = new node();
  n = head;
  while (n != NULL)
  {
    cout << n->item << "\t";
    n = n->next;
  }
}

int ListT::FindItem(const itemType target) const
{
  int numTargets = 0;
  node* n = new node();
  n = head;
  while (n != NULL)
  {
    if (n->item == target)
      numTargets++;
    n = n->next;
  }
  return numTargets;
}

int ListT::DeleteItem(const itemType target)
{
  int numTargets = 0;
  node *curr = new node(); 
  node *prev = new node();
 
  //If item is at the head
  if (head->item == target)
  {
    DeleteItemH();
    numTargets++;
  }
  
  curr = head;

  while (curr != NULL)
  {
    if (curr->item == target)
    {
      numTargets++;
      prev->next = curr->next;
    }
    prev = curr;
    curr = curr->next;
  }
   
  return numTargets;
}

node* ListT::PtrTo()
{
  node* PtrTo;
  
  node *curr = new node(); 
  node *prev = new node();
  curr = head;
  while (curr != tail)
  {
    prev = curr;
    curr = curr->next;
  }
  //Set PtrTo
  PtrTo = prev;
  return PtrTo;
}

void ListT::PutItemT(const itemType itemIn)
{
  node* n = new node();
  n->item = itemIn;
  n->next = NULL;
  tail->next = n;
  tail = n;
  length++;

}

itemType ListT::GetItemT() const
{
  itemType contents = tail->item;
  return contents;
}
   
void ListT::DeleteItemT()
{
  node* n = new node();
  n = tail;
  tail = PtrTo();
  tail->next = NULL;
  delete n;
}
