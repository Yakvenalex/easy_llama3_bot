import json
from sqlalchemy import Integer, String, BigInteger, TIMESTAMP, JSON, Boolean
from create_bot import db_manager
import asyncio


# функция, которая создаст таблицу с пользователями
async def create_table_users(table_name='users'):
    async with db_manager as client:
        columns = [
            {"name": "user_id", "type": BigInteger, "options": {"primary_key": True, "autoincrement": False}},
            {"name": "full_name", "type": String},
            {"name": "user_login", "type": String},
            {"name": "in_dialog", "type": Boolean},
            {"name": "date_reg", "type": TIMESTAMP},
        ]
        await client.create_table(table_name=table_name, columns=columns)


async def create_table_dialog_history(table_name='dialog_history'):
    async with db_manager as client:
        columns = [
            {"name": "id", "type": Integer, "options": {"primary_key": True, "autoincrement": True}},
            {"name": "user_id", "type": BigInteger},
            {"name": "message", "type": JSON}
        ]
        await client.create_table(table_name=table_name, columns=columns)


# функция, для получения информации по конкретному пользователю
async def get_user_data(user_id: int, table_name='users'):
    async with db_manager as client:
        user_data = await client.select_data(table_name=table_name, where_dict={'user_id': user_id}, one_dict=True)
    return user_data


# функция, для получения всех пользователей (для админки)
async def get_all_users(table_name='users', count=False):
    async with db_manager as client:
        all_users = await client.select_data(table_name=table_name)
    if count:
        return len(all_users)
    else:
        return all_users


# функция, для добавления пользователя в базу данных
async def insert_user(user_data: dict, table_name='users', conflict_column='user_id'):
    async with db_manager as client:
        await client.insert_data_with_update(table_name=table_name,
                                             records_data=user_data,
                                             conflict_column=conflict_column,
                                             update_on_conflict=False)


async def get_dialog_history(db_client, user_id: int, table_name='dialog_history'):
    dialog_history_msg = []
    dialog_history = await db_client.select_data(table_name=table_name, where_dict={'user_id': user_id})
    for msg in dialog_history:
        message = json.loads(msg.get('message'))
        dialog_history_msg.append(message)
    return dialog_history_msg


async def add_message_to_dialog_history(user_id: int, message: dict, table_name='dialog_history', return_history=False):
    async with db_manager as client:
        await client.insert_data_with_update(table_name=table_name,
                                             records_data={'user_id': user_id,
                                                           'message': json.dumps(message)},
                                             conflict_column='id')
        if return_history:
            dialog_history = await get_dialog_history(client, user_id)
            return dialog_history


async def update_dialog_status(client, user_id: int, status: bool, table_name='users'):
    await client.update_data(table_name=table_name,
                             where_dict={'user_id': user_id},
                             update_dict={'in_dialog': status})


async def clear_dialog(user_id: int, dialog_status: bool, table_name='dialog_history'):
    async with db_manager as client:
        await client.delete_data(table_name=table_name, where_dict={'user_id': user_id})
        await update_dialog_status(client, user_id, dialog_status)


async def get_dialog_status(user_id: int, table_name='users'):
    async with db_manager as client:
        user_data = await client.select_data(table_name=table_name, where_dict={'user_id': user_id}, one_dict=True)
    return user_data.get('in_dialog')