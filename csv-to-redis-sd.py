import csv, redis, json
import sys

REDIS_HOST = 'localhost'
ORGAOS = "orgaos-II"
SUGESTAO = "sugestao-I"
TURMAS_COMPONETES = "turmas-componentes-III"

def read_csv_data(csv_file):
    with open(csv_file, encoding='utf-8') as csvf:
        csv_data = csv.reader(csvf, delimiter=',')
        return [(r) for r in csv_data]

def build_key(key_index, db_key, line):
    key = line[int(key_index)]
    return key 

def store_data(conn, data, key_index, db_key):
    dict_to_store = {}
    header = data[0]
    header_clean = []
    id_count = 1
    for field in header:
        field = field.replace('"','')
        header_clean.append(field)
    header_clean.insert(0, "Id")

    for line in data:
        line_fix = line
        line_fix.insert(0, str(id_count))
        key = build_key(key_index, db_key, line_fix)
        count = 0
        dict_to_store["key"] = key[1:]
        # for attribute in line:
        #     if attribute != "2018.1" and attribute != "2018.2":
        #         dict_to_store[header_clean[count]] = attribute.replace(".", "")
        #     else:
        #         dict_to_store[header_clean[count]] = attribute
            #count = count + 1
        #dict_to_redis_hset(conn, (db_key[1] + str(key)), dict_to_store)
        conn.setnx(line_fix[0],line_fix)
        id_count = id_count + 1
    return data        

def dict_to_redis_hset(r, hkey, dict_to_store):
    return all([r.hset(hkey, k, v) for k, v in dict_to_store.items()])

def which_db(csv_file):
    db_key = []
    if csv_file == ORGAOS:
        db = "orgaos"
        namespace = "OrgaoOferta"
        db_key = [db, namespace]
    elif csv_file == SUGESTAO:
        db = "sugestao"
        namespace = "Sugestao"
        db_key = [db, namespace]
    elif csv_file == TURMAS_COMPONETES:
        db = "turmas-componentes"
        namespace = "TurmaOferta"
        db_key = [db, namespace]
    return db_key

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
    db_key = which_db(csv_file)

    try:
        data = read_csv_data(sys.argv[1])
        conn = redis.StrictRedis(host=REDIS_HOST)
        entry_data = (json.dumps(store_data(conn, data, key_index, db_key)))
        print ("Dados registrados com sucesso!")
        pass
    except Exception as e:
        raise print("Ocorreu um problema...")

if '__main__' == __name__:
    main()