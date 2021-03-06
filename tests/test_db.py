import Sindri.db
from tests.db_compound import methane


def test_db_cursor():
    name = methane["Name"]
    formula = methane["Formula"]
    Sindri.db.init()  # verificar problemas com isso aqui
    table_name = "v_all_properties_including_correlations"
    query = (
        "SELECT * FROM "
        + table_name
        + " WHERE Formula LIKE '%"
        + formula
        + "%'"
        + " AND Name LIKE '%"
        + name
        + "%'"
    )
    Sindri.db.cursor.execute(query)
    results = Sindri.db.cursor.fetchall()
    res = results[0]

    dict_names = [
        "Formula",
        "Name",
        "CAS",
        "Mol. Wt.",
        "Tfp_K",
        "Tb_K",
        "Tc_K",
        "Pc_bar",
        "Vc_cm3/mol",
        "Zc",
        "omega",
        "Tcpmin_K",
        "Tcpmax_K",
        "a0",
        "a1",
        "a2",
        "a3",
        "a4",
        "CpIG",
        "Cpliq",
        "ANTOINE_A",
        "ANTOINE_B",
        "ANTOINE_C",
        "Pvmin_bar",
        "Tmin_K",
        "Pvmax_bar",
        "Tmax_K",
    ]

    res2 = []
    for i in range(len(res)):
        if i == 11:
            tmin = None
            tmax = None
            if res[i] and "-" in res[i]:
                temps = res[i].split("-")
                tmin = float(temps[0])
                tmax = float(temps[1])

            res2.append(tmin)
            res2.append(tmax)
        else:
            res2.append(res[i])

    mydict = dict(zip(dict_names, res2))

    assert mydict == methane
