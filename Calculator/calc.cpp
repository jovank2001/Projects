#include <iostream>
using namespace std;

#include "calc.h"
#include <cstring>

Calc::Calc(int argcIn, char* argvIn[])
{
  inFix = new char[strlen(argvIn[1])+1];
  strcpy(inFix, argvIn[1]);
  if (!CheckTokens(argvIn[1]) || !CheckParens(argvIn[1]))
  {
    cout << "Invalid expression detected" << endl;
    exit(EXIT_FAILURE);
  }
  
  //Make values 
  values = new int[26];
  for (int o = 0; o < 26; o++)
    values[o] = 0;
  //Fill values
  int numOps = argcIn;
  for (int i = 2; i < numOps; i++)
     values[i-2] = atoi(argvIn[i]);

  InFixToPostFix();
}

Calc::~Calc()
{
  delete values;
  delete inFix;
  delete postFix;
}

bool Calc::CheckTokens(char* tempArr)
{
  
  for (int i = 0; tempArr[i] != '\0'; i++)
  {
    if(tempArr[i] != '(' && tempArr[i] != ')' && !isdigit(tempArr[i]) && !isalpha(tempArr[i]) && int(tempArr[i]) != 42 && int(tempArr[i]) != 43 && int(tempArr[i]) != 45 && int(tempArr[i]) != 47)
    {
      return false;
      cout << "Bad Tokens" << endl;
    }
  }

  return true;
}

bool Calc::CheckParens(char* tempArr)
{
  int openTally = 0;
  int closeTally = 0;
  for (int i = 0; tempArr[i] != '\0'; i++)
  {
    if (tempArr[i] == '(')
      openTally++;
    if (tempArr[i] == ')')
      closeTally++;
  }

  if (openTally == closeTally)
   return true;
  else
   return false;
}

void Calc::InFixToPostFix()
{
  //Make space
  postFix = new char[strlen(inFix)+1];
  Stack* stk = new Stack; 
  int p = 0;
  //Main loop
  for (int k = 0; inFix[k] != '\0'; k++)
  {
    if (isalpha(inFix[k]))
    {
      postFix[p] = inFix[k];
      p++;
    }
    if (inFix[k] == '(')
      stk->Push(inFix[k]);
    if (int(inFix[k]) == 42 || int(inFix[k]) == 43 || int(inFix[k]) == 45 || int(inFix[k]) == 47 )
      stk->Push(inFix[k]);
    if (inFix[k] == ')')
    {
      while (stk->Peek() != '(')
      {
        postFix[p] = stk->Peek();
        p++;
        stk->Pop();
      }
      stk->Pop();
    }

  }
}

int Calc::Evaluate()
{
  Stack* stk = new Stack; 
  int result = 0;
  for (int k = 0; postFix[k] != '\0'; k++)
  {
    if (isalpha(postFix[k]))
      stk->Push(postFix[k]);
    else
    {
      char op2 = stk->Peek();
      stk->Pop();
      char op1 = stk->Peek();
      stk->Pop();
      //Multiplication
      if (int(postFix[k]) == 42)
        result = values[op1 - 'A'] * values[op2 - 'A'];
      //Addition
      if (int(postFix[k]) == 43)
        result = values[op1 - 'A'] + values[op2 - 'A'];
      //Subtraction
      if (int(postFix[k]) == 45)
        result = values[op1 - 'A'] - values[op2 - 'A'];
      //Division
      if (int(postFix[k]) == 47)
        result = values[op1 - 'A'] / values[op2 - 'A'];
    }
 }
 return result;
}

void Calc::DisplayInFix()
{
 cout << "inFix: " << endl;
  for (int k = 0; inFix[k] != '\0'; k++)
    cout << inFix[k];
  cout << endl;
}

void Calc::DisplayPostFix()
{
 cout << "postFix: " << endl;
 for (int k = 0; postFix[k] != '\0'; k++)
   cout << postFix[k];
 cout << endl;
}
