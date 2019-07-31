import json

def main():
    _TWS = [(x,y) for x in [0,7,14] for y in [0,7,14]]
    _TWS.remove((7,7))
    _DWS = [(7 + dx*ffset,7+dy*ffset) for ffset in range(3,7) for dx in [-1,1] for dy in [-1,1]] 
    _DWS.append((7,7))

    # Double letters

    _DLS = [(x0+dx*mx,y0+dy*my)
            for x0,dx in [(0,1),(14,-1)] 
                for y0,dy in [(0,1),(14,-1)]
                    for mx,my in [(0,3),(2,6),(3,7),(6,6),(3,0),(6,2),(7,3)]]

    # Triple letters
    _TLS = [(x0+dx*mx,y0+dy*my) 
            for x0,dx in [(0,1),(14,-1)]
                for y0,dy in [(0,1),(14,-1)]
                    for mx,my in [(5,1),(5,5),(1,5)]]

    bonus_things = []

    _bonusType = None
    
    to_dump = {poss_bonus: coords_lst for coords_lst, poss_bonus in [(_DLS,"L2"),(_DWS,"W2"),(_TWS,"W3"),(_TLS,"L3")]}
    dump = json.dumps(to_dump)
    with open("bonus_tiles.json", "w") as bonuses:
        bonuses.write(dump)

if __name__ == '__main__':
    main()
