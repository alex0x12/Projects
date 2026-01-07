#include <complex.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>

#include <math.h>

#include "rpn_utils.h"


static char format[16] = "%0.3f";


static void set_format(const char* arg)
{
  size_t fs=sizeof(format);
  memset(format,0,fs);
  
  char *rs=NULL; 
  str_construct(&rs,"%0.",arg,"f",NULL);
  size_t len = strnlen(rs,fs-1);
  strncpy(format,rs,len);
  
  free(rs);
}


static double fact(double v)
{
  if(v<=1) return 1;
  return v * fact(v-1);
}

static double min(double a, double b)
{
  return a>=b?b:a;
}

static double max(double a, double b)
{
  return a<=b?b:a;
}

static void rpn_count(const Token* token, status_t status)
{
  static Stack *st=NULL;
  
  char* endptr=NULL;
  if(status==HALT)
  {
    printf("Res: %s\n",top(&st)->sym);
    destroy_stack(&st);
    st=NULL;
    return;
  }
  if(!token || !token->sym) return;
  
  token_t type = token->type;
  char* sym = token->sym;
  if(type==NUMBER)
  {
    push(&st,token);
    return;
  }
  if (type==CONSTANT)
  {
    push(&st,token);
    free(top(&st)->sym);
    char buffer[64];
    if(!strcmp(sym,"e"))
    {
      snprintf(buffer,64,format,M_E);
    }
    else if(!strcmp(sym,"p"))
    {
      snprintf(buffer,64,format,M_PI);
    }
    top(&st)->sym=strdup(buffer);
    return;
  }
  //Token* ops = getops_by_type(type);
  double rs;
  if(type==UNAOP)
  {
    rs=strtod(top(&st)->sym,&endptr);
    if(!strcmp(sym,"%"))
      rs/=100.0;
    else if(!strcmp(sym,"!"))
      rs=fact(rs);
    else if(!strcmp(sym,"~"))
      rs=-1*rs;
    else if(!strcmp(sym,"_%"))
    {
      double percent=strtod(top(&st)->sym,&endptr);
      pop(&st);
      double val=strtod(top(&st)->sym,&endptr);
      
      rs=(val/100.0)*percent;

      char buffer[64]; 
      snprintf(buffer,64,format,rs);
      push_inplace(&st,buffer,NUMBER,NONE,0);
      return;
    }
    else
      return;
  }
  else if(type==BINOP||type==FLOATOP)
  {
    double lop,rop;
    rop=strtod(top(&st)->sym,&endptr);
    pop(&st);
    lop=strtod(top(&st)->sym,&endptr);
    if(!strcmp(sym,"+"))
      rs=lop+rop;
    else if(!strcmp(sym,"-"))
      rs=lop-rop;
    else if(!strcmp(sym,"*"))
      rs=lop*rop;
    else if(!strcmp(sym,"/"))
      rs=lop/rop;
    else if(!strcmp(sym,"^"))
      rs=pow(lop,rop);
    else 
      return;
  }
  else if(type==FUNCTION)
  {
    double sarg, farg;
    sarg=strtod(top(&st)->sym,&endptr);
    if(!strcmp(sym,"ln"))
    {
      rs=log(sarg); 
    }
    else if(!strcmp(sym,"cos"))
    {
      rs=cos(sarg);
    }
    else if(!strcmp(sym,"sin"))
    {
      rs=sin(sarg);
    }
    else if(!strcmp(sym,"tan"))
    {
      rs=tan(sarg);
    }
    else if(!strcmp(sym,"cot"))
    {
      rs=cos(sarg)/sin(sarg);
    }
    else if(!strcmp(sym,"exp"))
    {
      rs=exp(sarg);
    }
    else if(!strcmp(sym,"sqrt"))
    {
      rs=sqrt(sarg);
    }
    else 
    {
      pop(&st);
      farg=strtod(top(&st)->sym,&endptr);
      if(!strcmp(sym,"log"))
      {
        rs=log(sarg)/log(farg);
      }
      else if(!strcmp(sym,"min"))
      {
        rs=min(farg,sarg);
      }
      else if(!strcmp(sym,"max"))
      {
        rs=max(farg,sarg);
      }
    }
  }

  char** t=&top(&st)->sym;
  *t=realloc(*t,64);
  snprintf(*t,64,format,rs);
}

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
      rpn_count(top(&st),ACTIVE);
      str_append(&rs,top(&st)->sym);
      pop(&st);
    }
    destroy_stack(&st);
    if(rs)
    {
      printf("RPN: %s\n",rs);
      free(rs);
    }
    rs=NULL;
    st=NULL;
    rpn_count(NULL,HALT);
    return;
  }
  if(!token || !token->sym) return;
  switch(token->type)
  {
    case NUMBER:
    case CONSTANT:
      rpn_count(token,ACTIVE);
      str_append(&rs,token->sym);
      break;
    case UNAOP:
      if(strcmp(token->sym,"~"))
      {
        rpn_count(token,ACTIVE);
        str_append(&rs,token->sym);
      }
      else
        push(&st,token);
      break;
    case FUNCTION:
      push(&st,token);
      break;
    case LPAREN:
      push(&st,token);
      break;
    case FLOATOP:
    case BINOP:
    {
      while(get_size(&st) && !check_priority(top(&st),token))
      {
        rpn_count(top(&st),ACTIVE);
        str_append(&rs,top(&st)->sym);
        pop(&st);
      }
      push(&st,token);
      break;
    }
    case RPAREN:
      while(get_size(&st) && top(&st)->type!=LPAREN)
      {
        rpn_count(top(&st),ACTIVE);
        str_append(&rs,top(&st)->sym);
        pop(&st);
      }
      pop(&st);
      if(get_size(&st) && top(&st)->type==FUNCTION)
      {
        rpn_count(top(&st),ACTIVE);
        str_append(&rs,top(&st)->sym);
        pop(&st);
      }
      break;
    case DELIM:
      while(get_size(&st) && top(&st)->type!=LPAREN)
      {
        rpn_count(top(&st),ACTIVE);
        str_append(&rs,top(&st)->sym);
        pop(&st);
      }
      break;
    default:
      break;
  }

}

static void tokenize(const char* const arg)
{
  size_t len=strlen(arg);
  if(!len) return;
  size_t i=0;
  const Token* token=NULL;
  int prev_priority = 0;
  token_t prev_type=UNDEF;
  bool met_floatop=false;
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
      prev_priority=0;
      Token* tmp=create_token(buffer,NUMBER,NONE,0);
      rpn_parse(tmp,ACTIVE);
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
        prev_priority=token->priority;
        rpn_parse(token,ACTIVE);
      }
      continue;
    }

    token=find_token_ch(arg[i]);
    
    if(!token)
    {
      i++;
      continue;
    }
    
    if(!strcmp(token->sym,"%")&&met_floatop)
    {
      met_floatop=false;
      token=find_token("_%");
    }

    if(token->type==FLOATOP)
    {
      met_floatop=true;
      token_t cur_type=UNDEF;
      if(!prev_type)
      {
        cur_type=UNAOP;
      }
      else
      {
        switch(prev_type)
        {
          case LPAREN:
          case BINOP:
          case DELIM:
          case FLOATOP:
          case UNAOP:
            if(prev_priority==4)
              cur_type=BINOP;
            else
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
          rpn_parse(uminus,ACTIVE);
          prev_priority=uminus->priority;
        }
        prev_type=cur_type;
        i++;
        continue;
      }
    }
    
    prev_priority=token->priority;
    prev_type=token->type;
    rpn_parse(token,ACTIVE);
    i++;
  }
  rpn_parse(token,HALT);
} 

int main(int argc, char** argv)
{
  if(argc<2)
  {
    fprintf(stderr,"Example: %s '1+0.25' -p 3\n\n",argv[0]);
    fprintf(stderr,"Option [p] is for precision.\n");
    fprintf(stderr,"You must provide at least 1 argument!\n");
    return 1;
  }
  
  int opt;
  while((opt=getopt(argc,argv,":p:"))!=-1)
  {
    switch(opt)
    {
      case ':':
        fprintf(stderr,"%c needs an argument!\n",optopt);
        return 1;
      case 'p':
        size_t i=0;
        while(isdigit(optarg[i]))
          i++;
        if(i<strlen(optarg)||optarg[0]=='0')
        {
          fprintf(stderr,"%c - only positive numbers allowed!\n",opt);
          return 1;
        }
        set_format(optarg);
        break;
      default:
        break;
    }
  }
  int i=1;
  do{
    printf("\nExpression %d: [ %s ]\n",i++,argv[optind]);
    tokenize(argv[optind++]);
  } while(optind<argc);
  return 0;
}
