#include <iostream>
using namespace std;

#include "calc.h"
#include <cstring>


Calc::Calc(char* argvIn)
{
  inFix = new char[strlen(argvIn)+1];
  strcpy(inFix, argvIn);
 
  if(CheckTokens() == false)
  {
    cout << "Invalid character" << endl;
    exit(EXIT_FAILURE);
  }
  MakeValueTbl();
  Parse();
  CheckParens();
  DisplayInFix();
}

Calc::~Calc()
{
  delete []inFix;
}

bool Calc::CheckTokens()
{
  string eq = inFix;
  int i = 0;
  bool returnVal = false;
  while(eq[i] != '\0')
  {
    if(eq[i]  == '*' || eq[i] == '/' || eq[i] == '+' || eq[i] == '-')
      returnVal = true;
  
    if(eq[i] <= 48 && eq[i] >= 57)
      returnVal = true;

    if(eq[i] == '(' || eq[i] == ')')
      returnVal == true;
    i++;
  }
 return returnVal;
}

void Calc::MakeValueTbl()
{
  int arr[26];
  valueTbl = arr;
  for(int i = 0; i < 26; i++)
    valueTbl[i] = 0;
}


void Calc::Parse()
{

  char* ptr;
  char* tmp = new char[strlen(inFix) + 1];
  char* str = new char[strlen(inFix) + 1];
  strcpy(str, inFix);
  int* tokens = new int[26];
  char delimiters[] = " ()+_*/";

  //turn char into digits
  int i = 0;
  ptr = strtok(str,delimiters);
  while (ptr != NULL)
  {
    tokens[i] = atoi(ptr); 
    ptr = strtok(NULL,delimiters);
    i++;
  }
  
  //fill valueTbl
  for (int j = 0; j < i; j++)
    valueTbl[j] = tokens[j];
   
  i = 0;
  int x = 0; 
  valueIdx = 0;
  
  while(inFix[i] != '\0')
  {
    if(inFix[i] == '(' || inFix[i] == ')')
      tmp[x] = inFix[i];
    else if(inFix[i]  == '*' || inFix[i] == '/' || inFix[i] == '+' || inFix[i] == '-')
      tmp[x] = inFix[i];
    else
      {
        tmp[x] = valueIdx + 65;
        i = FindLast(i) - 1;
        valueIdx++;
      }
    i++;
    x++;   
  } 
  
  delete []inFix;
  inFix = tmp;
  tmp = NULL;
}

bool Calc::CheckParens()
{
  Stack *stk = new Stack;
  int i = 0;
  char ch = inFix[i];
  bool bal = true;
  
  while(inFix[i] != '\0')
  {
    if(ch == '(')
      stk->Push(ch);
    else if(ch == ')')
      stk->Push(ch);
    else
    {
     if (!stk->IsEmpty())
       stk->Pop();
     else
       bal = false; 
    }
    i++;
  }
  if(bal && stk->IsEmpty())
    return true;
  return false;
}


int Calc::FindLast(int cur)
{
  char ch = inFix[cur];
  while(ch >= '0' && ch <= '9')
  {
    cur++;
    ch = inFix[cur];
  }
  return cur;
}

void Calc::DisplayInFix()
{
  for(int i = 0; i < strlen(inFix)+1; i++)
    cout << inFix[i];
}
