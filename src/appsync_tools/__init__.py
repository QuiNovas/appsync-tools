from decimal import Decimal
from json import loads
from json.decoder import JSONDecodeError
from .router import Router

router = Router()


def _formatAuroraRecord(record, meta):
    r = {}
    i = 0
    values = [None if list(field.keys())[0] == 'isNull' and list(field.values())[0] else list(field.values())[0] for field in record]
    for value in values:
        try:
            value = loads(value)
        except (JSONDecodeError, TypeError):
            pass
        r[meta[i]["name"]] = value
        i += 1
    return r


def prettyParseAurora(results, type_attribute=None):
    response = []
    if "columnMetadata" not in results:
        raise Exception("Query results must include columnMetada")
    for record in ("records" in results and results["records"]) or []:
        response.append(_formatAuroraRecord(record, results["columnMetadata"]))

    return typify(response, type_attribute=type_attribute) if type_attribute else response


def prettyParseDynamo(items, type_attribute=None):
    items = items.get('Items') or items.get('Item')

    if isinstance(items, dict):
        is_single = True
        items = [items]
    else:
        is_single = False

    def parseList(dynamoList):
        i = 0
        for d in dynamoList:
            dynamoType = list(d.keys())[0]
            dynamoList[i] = typeMap[dynamoType](d[dynamoType])
            i += 1
        return dynamoList

    def parseMap(dynamoMap):
        for d in dynamoMap:
            dynamoType = list(dynamoMap[d].keys())[0]
            dynamoMap[d] = typeMap[dynamoType](dynamoMap[d][dynamoType])
        return dynamoMap

    typeMap = {
        'S': lambda x: x,
        'N': lambda x: (int, Decimal)[len(x.split('.')) - 1](x),
        'L': parseList,
        'B': lambda x: x,
        'BS': parseList,
        'BOOL': lambda x: x,
        'NS': parseList,
        'NULL': lambda x: None,
        'SS': list,
        'M': parseMap
    }

    i = 0
    for item in items:
        newItem = {}
        for attributeName in item.keys():
            dynamoType = next(iter(item[attributeName]))
            val = typeMap[dynamoType](item[attributeName][dynamoType])
            newItem[attributeName] = val
        items[i] = newItem
        i += 1

    if is_single:
        items = items[0]

    return typify(items, type_attribute=type_attribute) if type_attribute else items


def typify(res, type_attribute="type"):
    if isinstance(res, list):
        for item in res:
            if item.get(type_attribute):
                item["__typename"] = item[type_attribute]
    elif isinstance(res, dict):
        if res.get(type_attribute):
            res["__typename"] = res[type_attribute]
    return res
