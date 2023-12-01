import re
from typing import Union
from app.dates_normalization import convert_date_to_standard_format, convert_time_period_to_format
from app.dates_normalization import POSSIBLE_DATE_KEYS_PARTS, POSSIBLE_TIME_PEDIOD_KEYS_PARTS


def postprocess_deal_data(incoming_data: Union[list, dict]) -> dict:
    """
    General deals postprocessing block, 
    which merge incoming deal tree/trees if needed and normalize it values;

    Args:
    incoming_data: list or dict. Deal tree/trees

    Returns:
    postprocessed_data: dict.
    """
    if isinstance(incoming_data, list):
        preprocessed_data = incoming_data[0]
        for d in incoming_data[1:]:
            merge_deals_items(preprocessed_data, d)
    else:
        preprocessed_data = incoming_data
    postprocessed_data = merge_deals_numbered_keys(preprocessed_data)
    merge_lists_of_dicts(preprocessed_data)
    normalize_deal_values(postprocessed_data)
    return postprocessed_data


def merge_deals_items(item1: dict, item2: dict) -> None:
    """
    Merge two incoming deals dicts.
    Also merge nested dicts and lists values with the same key
    """
    for key in item2:
        if key in item1:
            if isinstance(item1[key], dict) and isinstance(item2[key], dict):
                merge_deals_items(item1[key], item2[key])
            elif isinstance(item1[key], list) and not isinstance(item2[key], list):
                item1[key].append(item2[key])
            elif isinstance(item1[key], list) and isinstance(item2[key], list):
                item1[key].extend(item2[key])
            else:
                item1[key] = [item1[key], item2[key]]
        else:
            item1[key] = item2[key]


def merge_lists_of_dicts(incoming_data: dict) -> dict:
    """
    Format data like [{}, {}] to {}
    """
    for key, value in incoming_data.items():
        if isinstance(value, dict):
            merge_lists_of_dicts(value)
        elif isinstance(value, list):
            if isinstance(value[0], dict):
                new_dict = dict()
                for v in value:
                    new_dict.update(v)
                incoming_data[key] = new_dict


def merge_deals_numbered_keys(incoming_data: dict) -> dict:
    """
    Search keys according to 'any[<number>]' template and merge it as 'any' key
    """
    result_data = dict()
    for key, value in incoming_data.items():
        match = re.match(r"(\w+)\[\d+\]", key)
        if match:
            special_key = match.group(1)
            if existing_value := result_data.get(special_key):
                if isinstance(existing_value, dict):
                    result_data[special_key].update(value)
                elif isinstance(existing_value, list):
                    result_data[special_key].append(value)
                else:
                    result_data[special_key] = [existing_value, value]
            else:
                result_data[special_key] = value
        else:
            result_data[key] = value
    return result_data


def normalize_deal_values(incoming_data: dict) -> None:
    """
    General deal values normalization block,
    which recursively checks each key and value inside incoming deal data
    """
    for key, value in incoming_data.items():
        if isinstance(value, dict):
            normalize_deal_values(value)
            continue
        elif isinstance(value, list):
            for v in value:
                if isinstance(v, dict):
                    normalize_deal_values(v)
        if any((p in key.lower() for p in POSSIBLE_DATE_KEYS_PARTS)):
            incoming_data[key] = convert_date_to_standard_format(value)
        elif any((p in key.lower() for p in POSSIBLE_TIME_PEDIOD_KEYS_PARTS)):
            incoming_data[key] = convert_time_period_to_format(value)
