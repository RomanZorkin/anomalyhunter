import re
from typing import List


def modify_name(origin_name: str):
    res = re.split('\W+', origin_name)   
    return res


def get_match(asset: List[str], material: List[str], match_level: int):
    match_level = match_level/100
    matches = []
    #print(asset, material)
    for a in asset:
        if not a or a in matches:
            continue

        for m in material:
            if not m or m in matches:
                continue
            longest, sub_len = max(len(a), len(m)), 0            

            while sub_len < min(len(a), len(m)):
                if a[sub_len] == m[sub_len]:                    
                    sub_len += 1                    
                else:
                    break
            
            if sub_len/longest > match_level:                
                matches.append(a[0:sub_len])
    #print(matches)
    return matches


def count_level(asset, material, matches):
    asset_match = len(matches) / len(asset)
    material_match = len(matches) / len(material)
    return max(asset_match, material_match)


def main(word_1=None, word_2=None):
    word_1 = 'Ножницы для стрижки волос прямые дл 175'
    word_2 = 'Маска для сварщика'
    target_match_level = 50
    asset = modify_name(word_1)
    material = modify_name(word_2)        
    matches = get_match(material, asset, target_match_level)
    print(matches)
    return count_level(asset, material, matches)
    #print('Match level: ', actual_match_level)

if __name__ == '__main__':
    print(main())