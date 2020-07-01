import re
import time
from datetime import date, datetime, timedelta


def timeit(method, number):
    args = loader(number)
    ts = time.time()
    result = method(args)
    te = time.time()
    print('%r method took %f ms to be executed' % (method.__name__, (te - ts) * 1000))
    print("Result : ")
    print(result)

def loader(n):
    return [data.replace('\n', '') for data in open("./adventofcode/adventofcodeday" + str(n) + ".txt", "r")]

def DayOnePartOne(data):
    result = int()
    for number in data:
        result += int(number)
    return result


def DayOnePartTwo(data):
    result = int()
    setsvalues = set([0])
    while True:
        for number in data:
            result += number
            if result in setsvalues:
                return result
            else:
                setsvalues.add(result)

def DayTwoPartOne(data):
    count2 = count3 = int()
    for string in data:
        current_cache = []
        count2_attrib = count3_attrib = False
        for letters in string:
            not_passed = True
            for cache in current_cache:
                if cache[0] == letters:
                    cache[1] += 1 
                    not_passed = False
                    break
            if (not_passed == True):
                current_cache.append([letters,1])
        for items in current_cache:
            if items[1] == 3:
                count3_attrib = True
            if items[1] == 2:
                count2_attrib = True
        if count3_attrib:
            count3 += 1
        if count2_attrib:
            count2 += 1
    return(count2*count3)
            

def DayTwoPartTwo(data):
    result = str()
    diff_table = list()
    for n, s1 in enumerate(data, 1):
        for s2 in data[n:]:
            diff_table = list()
            for i in range(len(s1)):
                if s1[i] != s2[i]:
                    diff_table.append(i)
            if (len(diff_table) == 1):
                for n2, letters in enumerate(s1):
                    if n2 == diff_table[0]:
                        continue
                    result += letters
    return result

def DayThreePartOne(data):
    mapper = dict()
    total = int()
    for instruction in [list(map(int, d[1:].replace('@', ',').replace(':', ',').replace('x', ',').replace(' ', '').split(',')))[:-1] for d in data]:
        for x in range(instruction[2]):
            if ((instruction[0] + x) in mapper) == False:
                    mapper[instruction[0] + x] = dict()
            for y in range(instruction[3]):
                if ((instruction[1] + y) in mapper[instruction[0] + x]):
                    mapper[instruction[0] + x][instruction[1] + y] += 1
                else:
                    mapper[instruction[0] + x][instruction[1] + y] = 1
    for x2 in mapper.values():
        for y2 in x2:
            if x2[y2] > 1:
                total += 1
    return total
        
def DayThreePartTwo(data):
    mapper = dict()
    id_tables = dict()
    for instruction in [list(map(int, d[1:].replace('@', ',').replace(':', ',').replace('x', ',').replace(' ', '').split(','))) for d in data]:
        id_tables[instruction[0]] = True
        for x in range(instruction[3]):
            if ((instruction[1] + x) in mapper) == False:
                    mapper[instruction[1] + x] = dict()
            for y in range(instruction[4]):
                if ((instruction[2] + y) in mapper[instruction[1] + x]):
                    mapper[instruction[1] + x][instruction[2] + y].append(instruction[0]) 
                else:
                    mapper[instruction[1] + x][instruction[2] + y] = [instruction[0]]
    for x2 in mapper.values():
        for y2 in x2:
            if len(x2[y2]) > 1:
                for item in x2[y2]:
                    if item in id_tables:
                        id_tables.pop(item)
    return [k for k in id_tables.keys()][0]

def DayFourPartOne(data):
    guardtime = [list(map(lambda value: int(value) if value.isdigit() else str(value),d[1:].replace(']', '').replace(' ', '-', 2).replace(':', '-').split('-'))) for d in data]
    [guardtime.sort(key=lambda x: x[(4 - i)]) for i in range(0, 5)]
    guardnexttosleep = guardcache = list()
    guardcounter = dict()
    temptime = datetime(guardtime[0][0], guardtime[0][1],guardtime[0][2], 23) - timedelta(days=1)
    for item in guardtime:
        currenttime = datetime(item[0],item[1],item[2],item[3],item[4])
        if not (temptime < currenttime and currenttime < (temptime+timedelta(hours=2))):
            guardcache.clear()
            guardnexttosleep.clear()
            temptime = datetime(item[0], item[1], item[2], 23) - (timedelta(days=1) if(item[3] == 00) else timedelta(seconds=0))
        if item[5] == "falls asleep":
            guardcache.append([guardnexttosleep[0], currenttime])
            guardnexttosleep.pop(0)
            continue
        if item[5] == "wakes up":
            if guardcache[0][0] not in guardcounter:
                guardcounter[guardcache[0][0]] = [dict(),0]
            for item in range(guardcache[0][1].minute, currenttime.minute):
                if (currenttime-timedelta(seconds=60)).time().minute not in guardcounter[guardcache[0][0]][0]:
                    guardcounter[guardcache[0][0]][0][(currenttime-timedelta(seconds=60)).time().minute] = int()
                guardcounter[guardcache[0][0]][0][(currenttime-timedelta(seconds=60)).time().minute] += 1  
            guardcounter[guardcache[0][0]][1] += int(((currenttime-guardcache[0][1]).total_seconds())/60)
            guardnexttosleep.append(guardcache[0][0])
            guardcache.pop(0)
            continue
        processing = re.search(r' #(\d+) ', item[5])
        if processing != None:
            guardnexttosleep.append(processing.group(1))
            continue
    print(guardcounter)
    return int(max(guardcounter[max(guardcounter, key=lambda key: guardcounter[key][1])][0], key=lambda k: (guardcounter[max(guardcounter, key=lambda key: guardcounter[key][1])][0][k]))) * int(max(guardcounter, key=lambda key: guardcounter[key][1]))

timeit(DayFourPartOne, 4)
