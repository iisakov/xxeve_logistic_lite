import sqlite3
import requests


def get_conn():
    return sqlite3.connect('sqlite-latest.sqlite')


def get_solar_system_by_name(conn, solar_system_name):
    select_str = f'''
        SELECT 
            mr.regionName,
            mc.constellationName,
            mss.*
        FROM mapSolarSystems mss
        JOIN mapConstellations mc on mss.constellationID = mc.constellationID 
        JOIN mapRegions mr on mss.regionID = mr.regionID
        WHERE mss.solarSystemName = '{solar_system_name}' '''

    cursor = conn.execute(select_str)
    result = {cursor.description[i][0]: value for i, value in enumerate(cursor.fetchone())}
    return result


def get_many_solar_system_by_name(conn, solar_system_name_list):
    result = {}
    solar_system_name_list_str = "'" + "', '".join(solar_system_name_list) + "'"
    select_str = f'''
        SELECT 
            mr.regionName,
            mc.constellationName,
            mss.*
        FROM mapSolarSystems mss
        JOIN mapConstellations mc on mss.constellationID = mc.constellationID 
        JOIN mapRegions mr on mss.regionID = mr.regionID
        WHERE mss.solarSystemName in ({solar_system_name_list_str}) '''

    cursor = conn.execute(select_str)
    for row in cursor.fetchall():
        result[row[5]] = {cursor.description[i][0]: value for i, value in enumerate(row)}
    return result if len(result) == len(solar_system_name_list) else False


def get_solar_system_by_id(conn, solar_system_id):
    select_str = f'''
        SELECT 
            mr.regionName,
            mc.constellationName,
            mss.*
        FROM mapSolarSystems mss
        JOIN mapConstellations mc on mss.constellationID = mc.constellationID 
        JOIN mapRegions mr on mss.regionID = mr.regionID
        WHERE mss.solarSystemID = '{solar_system_id}' '''
    cursor = conn.execute(select_str)
    result = {cursor.description[i][0]: value for i, value in enumerate(cursor.fetchone())}
    return result


def get_many_solar_system_by_id(conn, solar_system_id_list):
    result = {}
    solar_system_id_list_str = ", ".join([str(solar_system_id) for solar_system_id in solar_system_id_list])
    select_str = f'''
        SELECT 
            mr.regionName,
            mc.constellationName,
            mss.*
        FROM mapSolarSystems mss
        JOIN mapConstellations mc on mss.constellationID = mc.constellationID 
        JOIN mapRegions mr on mss.regionID = mr.regionID
        WHERE mss.solarSystemID in ({solar_system_id_list_str}) '''
    cursor = conn.execute(select_str)

    for row in cursor.fetchall():
        result[row[5]] = {cursor.description[i][0]: value for i, value in enumerate(row)}
    return result if len(result) == len(solar_system_id_list) else False


def get_all_stargate_by_solar_system_id(conn, solar_system_id):
    result = []
    select_str = f''' SELECT distinct
            md.itemID as 'stargateID',
            mj.destinationID as 'destinationStargateID',
            mss.solarSystemName || '-' || (SELECT 
                mss.solarSystemName 
            FROM mapDenormalize md
            JOIN mapSolarSystems mss on md.solarSystemID = mss.solarSystemID
            WHERE md.itemID = mj.destinationID) as 'stargateName',
            md.solarSystemID,
            mss.solarSystemName,
            md.constellationID,
            md.regionID,
            md.x,
            md.y,
            md.z
        from mapDenormalize md
        join invGroups ig on md.groupID = ig.groupID
        join mapSolarSystems mss on md.solarSystemID = mss.solarSystemID
        join mapJumps mj on md.itemID = mj.stargateID
        where ig.groupName = 'Stargate' and mss.solarSystemName = {solar_system_id} '''
    cursor = conn.execute(select_str)

    for row in cursor.fetchall():
        result.append({cursor.description[i][0]: value for i, value in enumerate(row)})
    return result


def get_all_stargate_by_many_solar_system_id(conn, solar_system_id_list):
    result = {}
    solar_system_id_list_str = ", ".join([str(solar_system_id) for solar_system_id in solar_system_id_list])
    select_str = f''' SELECT distinct
            md.itemID as 'stargateID',
            mj.destinationID as 'destinationStargateID',
            mss.solarSystemName || '-' || (SELECT 
                mss.solarSystemName 
            FROM mapDenormalize md
            JOIN mapSolarSystems mss on md.solarSystemID = mss.solarSystemID
            WHERE md.itemID = mj.destinationID) as 'stargateName',
            md.solarSystemID,
            mss.solarSystemName,
            md.constellationID,
            md.regionID,
            md.x,
            md.y,
            md.z
        from mapDenormalize md
        join invGroups ig on md.groupID = ig.groupID
        join mapSolarSystems mss on md.solarSystemID = mss.solarSystemID
        join mapJumps mj on md.itemID = mj.stargateID
        where ig.groupName = 'Stargate' and mss.solarSystemID in ({solar_system_id_list_str}) '''
    cursor = conn.execute(select_str)
    for row in cursor.fetchall():
        if row[4] not in result:
            result[row[4]] = []
        result[row[4]].append({cursor.description[i][0]: value for i, value in enumerate(row)})
    return result if len(result) == len(solar_system_id_list) else False


def get_all_objects_by_many_solar_system_id(conn, solar_system_id_list):
    result = {}

    solar_system_id_list_str = ", ".join([str(solar_system_id) for solar_system_id in solar_system_id_list])
    select_str = f'''SELECT 
            mss.solarSystemName,
            itemID as objectID,
            itemName as objectName,
            md.solarSystemID,
            md.x,
            md.y,
            md.z
        FROM mapDenormalize md 
        join mapSolarSystems mss on md.solarSystemID = mss.solarSystemID
        WHERE md.solarSystemID in ({solar_system_id_list_str})'''
    cursor = conn.execute(select_str)
    for row in cursor.fetchall():
        if row[0] not in result:
            result[row[0]] = []
        result[row[0]].append({cursor.description[i][0]: value for i, value in enumerate(row)})
    return result if len(result) == len(solar_system_id_list) else False


def get_all_objects_by_solar_system_id(conn, solar_system_id):
    result = []
    select_str = f'''SELECT 
            mss.solarSystemName,
            itemID as objectID,
            itemName as objectName,
            md.solarSystemID,
            md.x,
            md.y,
            md.z
        FROM mapDenormalize md 
        join mapSolarSystems mss on md.solarSystemID = mss.solarSystemID
        where solarSystemID = {solar_system_id} '''
    cursor = conn.execute(select_str)

    for row in cursor.fetchall():
        result.append({cursor.description[i][0]: value for i, value in enumerate(row)})
    return result


def get_entity_by_tipe_id(conn, tipe_id):
    result = {}
    select_str = f'''
        SELECT 
            *
        FROM invTypes it 
        WHERE it.typeID = {tipe_id}'''
    cursor = conn.execute(select_str)
    result = {cursor.description[i][0]: value for i, value in enumerate(cursor.fetchone())}
    return result


def get_db():
    requests.get('https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2')
