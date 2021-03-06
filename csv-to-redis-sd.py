import csv, redis, json
import sys
import utm

REDIS_HOST = 'localhost'

def read_csv_data(csv_file):
    with open(csv_file, encoding='utf-8') as csvf:
        csv_data = csv.reader(csvf, delimiter=',')
        return [(r) for r in csv_data]

def build_key(key_index, db_key, line):
    key = line[int(key_index)]
    return key 

def store_data(conn, data, key_index):
    dict_to_store = {}
    header = data[0]
    header_clean = []
    id_count = 1
    for field in header:
        field = field.replace('"','')
        header_clean.append(field)
    header_clean.insert(0, "Id")
    header_clean.append("x")
    header_clean.append("y")
    data.pop(0)

    for line in data:
        line_fix = line
        line_fix.insert(0, str(id_count))
        count = 0
        cord_x = int(line_fix[7])
        cord_y = int(line_fix[8])

        if cord_x != 0 and cord_y !=0:
            utm_value = utm.to_latlon(cord_x, cord_y, 25, 'L')
            line_fix.append(utm_value[0])
            line_fix.append(utm_value[1])
        else:
            utm_value = None
            line_fix.append(utm_value)
            line_fix.append(utm_value)
        
        count2 = 0
        for field in line_fix:
            dict_to_store[str(header_clean[count2])] = str(line_fix[count2])
            count2 = count2 + 1 

        conn.setnx(line_fix[0],dict_to_store)
        id_count = id_count + 1
    return data        

def main():
    args_len = len(sys.argv)
    if args_len < 3:
        sys.exit("Utilize %s path/to/file.csv key_index key_index key_index..." % __file__)
    elif args_len == 3:
        key_index = sys.argv[2]
    else:
        key_index = []
        for i in range (args_len):
            if i != 0 and i != 1:
                key_index.append(sys.argv[i])
    csv_file = sys.argv[1].split("/")[-1][:-4]

    try:
        data = read_csv_data(sys.argv[1])
        conn = redis.StrictRedis(host=REDIS_HOST)
        entry_data = (json.dumps(store_data(conn, data, key_index)))
        print ("Dados registrados com sucesso!")
        pass
    except Exception as e:
        raise print("Ocorreu um problema...")

if '__main__' == __name__:
    main()