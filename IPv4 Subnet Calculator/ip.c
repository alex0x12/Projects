/* IPV4 SUBNET CALCULATOR IN C*/
/* NO ADDITIONAL LIBS USED */

#include <stdio.h>

#define MAX_U32 0xFFFFFFFF

typedef unsigned int u32;
typedef unsigned char u8;

/* Address, mask, free mask bits, buffer */
static u32 address=0;
static u32 mask=MAX_U32;
static u8 c_mask=0;
static char buf[24];

u8
length(const char* str)
{
  u8 i;
  for(i=0;str[i]!='\0';i++);
  return i;
}

u32
pw(u8 d)
{
  u32 res=2;
  for(u8 i=1;i<d;i++)
    res<<=1;
  return res;
}

u8
check_bounds(void)
{
  if(address==MAX_U32)
    puts("255.255.255.255 reserved for broadcast");
  else if(address==0)
    puts("0.0.0.0 reserved for default route");
  else if(((address>>24)&0xFF)==0x7F)
    puts("127.0.0.0 reserved for loopback");
  else
    return 1;
  return 0xFF;
}

u8
b_parse(const char* str)
{
  u8 dots=0;
  for(u8 i=0;i<length(str);i++)
  {
    if(str[i]=='.') dots++;
  }
  if(dots!=3)
  {
    printf("Wrong address format!\n");
    return 0xFF;
  }
  u8 _mask=0;
  u8 pos=24;
  u8 _address=0;
  u8 i=0;
  u8 foundmask=false;
  while(i<length(str))
  {
    if(str[i]=='.' || str[i]=='/')
    {
      address+=(_address<<pos);
      if(str[i]=='/')
      {
        foundmask=true;
        i++;
        break;
      }
      _address=0;
      pos-=8;
    }
    else
    {
      _address=_address*10+(str[i]-'0');
    }
    i++;
  }
  if(foundmask)
  {
    for(i;i<length(str);i++)
    {
      _mask=(_mask*10+(str[i]-'0'));
    }
    if(_mask>32)
    {
      printf("Wrong address format!\nMask can't be bigger than 32.\n");
      return 0xFF;
    }
    mask-=pw(32-_mask)-1;
    c_mask=32-_mask;
  }
  else
  {
    address+=(_address<<pos);
  }
  address=(address&mask);
  return check_bounds();
}

char*
get_addr(const u32 _address)
{
  char blocks[4][5];
  char* format;
  u32 tmp;
  for(u8 octet=0;octet<4;octet++)
  {
    tmp=(_address>>(8*octet))&0xFF;
    format=octet?"%u.":"%u";
    snprintf(blocks[octet],5,format,tmp);
  }
  snprintf(buf,sizeof(buf),"%s%s%s%s",blocks[3],blocks[2],blocks[1],blocks[0]);
  return buf;
}

void
_print(void)
{
  printf("Subnet: %s/%d\n",get_addr(address&mask),32-c_mask);
  printf("Hosts: %d\n",pw(c_mask)-2);
  printf("Begin: %s\n",get_addr((address&mask)+1));
  printf("End: %s\n",get_addr((address&mask)+pw(c_mask)-2));
  printf("Broadcast: %s\n\n",get_addr((address&mask)+pw(c_mask)-1));
}

u32
atou(const char* str)
{
  u32 num=0;
  for(u8 i=0;i<length(str);i++)
  {
    if(str[i]>='0' && str[i]<='9')
      num=num*10+str[i]-'0';
  }
  return num;
}

void
_sort(u32 *arr,const u8 size)
{
  if(size<2) return;
  u32 tmp=arr[0];
  for(u8 i=0;i<size-1;i++)
  {
    for(u8 j=0;j<size-i-1;j++)
    {
        if(arr[j]<arr[j+1])
        {
          tmp=arr[j];
          arr[j]=arr[j+1];
          arr[j+1]=tmp;
        }
    }
  }
}

u8
main(int argc,char** argv)
{
  if(argc<2)
  {
    printf("Usage: %s aaa.aaa.aaa.aaa/mm [subnet1 subnet2 ...]\n",argv[0]);
    return 1;
  }
  if(b_parse(argv[1])==0xFF) return 1;
  _print();
  if(argc>2)
  {
    printf("------------------------\n\n");
    u8 size=argc-2;
    u32 parts[size];
    u32 hosts_sum=0;
    u32 hosts_available=pw(c_mask);
    for(u8 i=0;i<size;i++)
      parts[i]=atou(argv[i+2]);
    _sort(parts,size);
    for(u8 i=0;i<size;i++)
    {
      for(c_mask=0;pw(c_mask)-2<parts[i];c_mask++);
      hosts_sum+=pw(c_mask);
      if(hosts_sum>hosts_available)
      {
        printf("Too much subnets!\nCan't provide so many hosts.\n");
        return 1;
      }
      mask=MAX_U32-(pw(c_mask)-1);
      _print();
      address+=pw(c_mask);
    }
  }
  return 0;
}
