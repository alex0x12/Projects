#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "rpn_utils.h"

static bool check_priority(const Token* st_top, const Token* token)
{
  if(!st_top || !token) return true;
  int f = st_top->priority;
  int s = token->priority;
  if(f>s) return false;
  if(f==s)
  {
    switch(token->assoc)
    {
      case LEFT: return false;
      case RIGHT: return true;
      default: return true;
    }
  }
  return true; 
}

static void rpn_parse(const Token* token, status_t status)
{
  /*
  if(status!=HALT)
  {
    static int calls=0;
    printf("%d - Token: %s\n",calls,token->sym);
    calls++;
  }
  */
  static char* rs=NULL;
  static Stack* st=NULL;
  if(status==HALT)
  {
    while(get_size(&st))
    {
      str_append(&rs,top(&st)->sym);
      pop(&st);
    }
    if(rs)
    {
      puts(rs);
      free(rs);
    }
    destroy_stack(&st);
    return;
  }
  if(!token || !token->sym) return;
  switch(token->type)
  {
    case NUMBER:
      str_append(&rs,token->sym);
      break;
    case UNAOP:
      if(strcmp(token->sym,"~"))
        str_append(&rs,token->sym);
      else
        push(&st,token);
      break;
    case FUNCTION:
      push(&st,token);
      break;
    case LPAREN:
      push(&st,token);
      break;
    case BINOP:
    {
      while(get_size(&st) && !check_priority(top(&st),token))
      {
        str_append(&rs,top(&st)->sym);
        pop(&st);
      }
      push(&st,token);
      break;
    }
    case RPAREN:
      while(get_size(&st) && top(&st)->type!=LPAREN)
      {
        str_append(&rs,top(&st)->sym);
        pop(&st);
      }
      pop(&st);
      if(get_size(&st) && top(&st)->type==FUNCTION)
      {
        str_append(&rs,top(&st)->sym);
        pop(&st);
      }
      break;
    case DELIM:
      while(get_size(&st) && top(&st)->type!=LPAREN)
      {
        str_append(&rs,top(&st)->sym);
        pop(&st);
      }
      break;
    default:
      break;
  }

}

static void tokenize(const char* const arg, token_cb callback)
{
  size_t len=strlen(arg);
  if(!len) return;
  size_t i=0;
  const Token* token=NULL;
  token_t prev_type=UNDEF;
  bool floating_op=false; // <-- to divide +- and %! handling (SUCKS)
  while(i<len)
  {
    if(isdigit(arg[i])) 
    {
      char buffer[64]={0};
      size_t j=0;
      bool found_dot=false;
      while(isdigit(arg[i])||arg[i]=='.')
      {
        if(arg[i]=='.')
        {
          if(!found_dot)
            found_dot=true;
          else
          {
            i++;
            continue;
          }
        }
        buffer[j++]=arg[i++];
      }
      buffer[j]=0;
      
      prev_type=NUMBER; 
      Token* tmp=create_token(buffer,NUMBER,NONE,0);
      callback(tmp,ACTIVE);
      destroy_token(tmp);
      continue;
    }
    else if(isalpha(arg[i]))
    {
      char buffer[64]={0};
      size_t j=0;
      while(isalpha(arg[i]))
        buffer[j++]=arg[i++];
      buffer[j]=0;

      token=find_token(buffer);
      if(token)
      {
        prev_type=token->type;
        callback(token,ACTIVE);
      }
      continue;
    }

    token=find_token_ch(arg[i]);
    
    if(!token)
    {
      i++;
      continue;
    }

    if(!strcmp(token->sym,"+") || !strcmp(token->sym,"-"))
    {
      token_t cur_type=UNDEF;
      if(!prev_type)
      {
        cur_type=UNAOP;
      }
      else
      {
        switch(prev_type)
        {
          case UNAOP:
            cur_type=floating_op?UNAOP:BINOP;
            break;
          case LPAREN:
          case BINOP:
          case DELIM:
            cur_type=UNAOP;
            break;
          default:
            cur_type=BINOP;
            break;
        }
      }
      if(cur_type==UNAOP)
      {
        if(!strcmp(token->sym,"-"))
        {
          const Token* uminus = find_token("~");
          callback(uminus,ACTIVE);
        }
        prev_type=cur_type;
        i++;
        continue;
      }
    }
   
    floating_op=(!strcmp(token->sym,"-")) || (!strcmp(token->sym,"+"));
    prev_type=token->type;
    callback(token,ACTIVE);
    i++;
  }
  callback(token,HALT);
} 

int main(int argc, char** argv)
{
  if(argc!=2) return 1;
  tokenize(argv[1],rpn_parse);
  return 0;
}
