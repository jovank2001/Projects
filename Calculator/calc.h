
/*
File Name: calc.h
To Execute: ./calc "(A+B)" 73 22
*/

#ifndef CALC
#define CALC

#include "stack2.h"

class Calc 
{ 
  public: 
  /* 
  pre: none 
  post:
	  If 'B' is in the expression, its value is stored in position 1 .... If 'Z'
	  is in the expresion, its value is stored in position 25.  
  */
  Calc(int argcIn, char* argvIn[]);

  /*
  pre: none
  post: all dynamically declared memory within calc has been returned to the stack. 
  */
  ~Calc();

  /*
  pre: instance of Calc exists. 
  post: infix expression displayed
 */
  void DisplayInFix();

  /*
  pre: instance of Calc exists
  post: postfix exression displayed 
 */
  void DisplayPostFix();
 
  /*
  pre: instance of Calc exists
  post: value of expression input at the command line is computed and returned. 
        technique is that described in class.
 */
  int Evaluate();

 private:
  /*
  pre:  none. Invoked from constructor. 
  post: returns true if all characters in the infix expression are legal,
        false otherwise  Legal characters are ')', '(', '+','-','*','/',
        'A' ... 'Z'   
  */
  bool CheckTokens(char* tempArr); 

  /*
   pre:  All input tokens are legal. Invoked from constructor.
   post: Using the stack technique discussed in class, returns true 
         if parentheses are balanced, false otherwise
  */
  bool CheckParens(char* tempArr);

  /*
  pre: instance of Calc exists.  All tokens are legal and parens are balanced.
  post: postFix points to a dynamically declared array holding the postfix version
        of the the input infix expression.  
 */
  void InFixToPostFix();

  
  Stack* stk;      //used for CheckParens, InFixToPostFix, Evaluate 
  char*  inFix;    //null-terminated string that holds infix expression  
  char*  postFix;  //null-terminated string that holds the post-fix
  int*   values;   //pointer to array whose function is described in item 4 of
                   //of the constructor specs, above. 


};
#endif 
