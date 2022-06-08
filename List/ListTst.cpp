#include <iostream>
using namespace std;
#include "10-List.h"


int main()
{
  //Print Test
  /*//Use of a static list 
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  cout << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  cout << endl;

  delete lst1; //necessary to invoke destructor on dynamic list
  cout << endl;
  */

  /*//Is empty  Test
  //Use of a static list 
  ListT lst;
  if (lst.IsEmpty())
    cout << "It is empty" << endl;
  else
    cout << "It is not empty" << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  if (lst1->IsEmpty())
    cout << "It is empty" << endl;
  else
    cout << "It is not empty" << endl;
 
  delete lst1;
  cout << endl;
  */

  /*//Get length Test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  cout << "Length: " << lst.GetLength();
  cout << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  lst1->GetLength();
  cout << "Length: " << lst1->GetLength();
  cout << endl;
 
  delete lst1;
  cout << endl;
  */

  /*//Put Item H Test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  cout << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  cout << endl;
 
  delete lst1;
  cout << endl;*/


  /*//Get Item H Test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  cout << endl;
  cout << "Item at header: " << lst.GetItemH() << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  cout << endl;
  cout << "Item at header: " << lst1->GetItemH() << endl;

  delete lst1;
  cout << endl;*/

  /*//Delete Item H Test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  cout << endl;
  lst.DeleteItemH();
  cout << "List after deleted header: " << endl;
  lst.Print();
  cout << endl << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  cout << endl;
  lst1->DeleteItemH();
  cout << "List after deleted header: " << endl;
  lst1->Print();

  delete lst1;
  cout << endl;*/
  
  /*//Find Item Test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  cout << endl;
  cout << "The number 3 is at index: " << lst.Find(3) << endl;
  cout << endl << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  cout << endl;
  cout << "The number 30 is at index: " << lst1->Find(30) << endl;

  delete lst1;
  cout << endl;*/

  /*//Delete item test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.PutItemH(2);
  lst.Print();
  cout << endl;
  cout << "The list after deleting all 2's and how many there were: "  << lst.DeleteItem(2) << endl;
  lst.Print();
  cout << endl << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->PutItemH(20);
  lst1->Print();
  cout << endl;
  cout << "The list after deleting all 20's, and how many there were: "  << lst1->DeleteItem(20) << endl;
  lst1->Print();

  delete lst1;
  cout << endl;*/
  
  /*//PtrTo Test MOVE PtrTo function declaration into public
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  node* temp = lst.PtrTo();
  cout << endl;
  cout << "The item in the second to last node:"  << (*temp).item << endl;
  cout << endl << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  node* temp1 = lst1->PtrTo();
  cout << endl;
  cout << "The item in the second to last node:"  << (*temp1).item << endl;

  delete lst1;
  cout << endl;*/
 
  /*//Put Item T Test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  lst.PutItemT(7);
  cout << "List after putting 7 at tail: " << endl;
  lst.Print();
  cout << endl << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  lst1->PutItemT(70);
  cout << "List after putting 70 at tail: " << endl;
  lst1->Print();
  cout << endl;
 
  delete lst1;
  cout << endl;*/

  /*//Get Item T Test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  cout << endl;
  cout << "Item at tail: " << lst.GetItemT() << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  cout << endl;
  cout << "Item at tail: " << lst1->GetItemT() << endl;

  delete lst1;
  cout << endl;*/

  /*//Delete Item T Test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.Print();
  lst.DeleteItemT();
  cout << "List after deleting tail: " << endl;
  lst.Print();
  cout << endl << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->Print();
  lst1->DeleteItemT();
  cout << "List after deleting tail: " << endl;
  lst1->Print();
  cout << endl;
 
  delete lst1;
  cout << endl;*/

  /*//Find item test
  //Use of a static list
  ListT lst;
  for (int i = 0; i < 5; i++) 
    lst.PutItemH(i);
  lst.PutItemH(2);
  lst.Print();
  cout << endl;
  cout << "How many 2's that are in the list: "  << lst.FindItem(2) << endl;
  cout << endl << endl;
  //Use of a dynamic list
  ListT* lst1 = new ListT;
  for (int i = 0; i < 5; i++)
    lst1->PutItemH(10*i);
  lst1->PutItemH(20);
  lst1->Print();
  cout << endl;
  cout << "How many 20's there are in the list: "  << lst1->FindItem(20) << endl;

  delete lst1;
  cout << endl;*/

 return 0;
}
