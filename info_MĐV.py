import numpy as np
# id_tags la tham so dau vao
## dict chay tu 1, april tag chay tu 0
# id = id+1
# Khai báo từ điển
# goc sua voi huong nhin thang, x huong mat, y sang trai
dictionary = {

    1: {'ID': 0, 'r_o_i': [[0], [0], [0], [1]],'phi': 0},
    2: {'ID': 1, 'r_o_i': [[1.8], [0], [0], [1]],'phi': 0},
    3: {'ID': 2, 'r_o_i': [[3.6], [0], [0], [1]],'phi': 0},

    4: {'ID': 3, 'r_o_i': [[5.4], [0], [0], [1]] ,'phi': 0},
    5: {'ID': 4, 'r_o_i': [[7.2], [0], [0], [1]],'phi': 0},
    6: {'ID': 5, 'r_o_i': [[9], [0], [0], [1]],'phi': 0},

    7: {'ID': 6, 'r_o_i': [[10.8], [0], [0], [1]],'phi': 0},
    8: {'ID': 7, 'r_o_i': [[12.6], [0], [0], [1]],'phi': 0},
    9: {'ID': 8, 'r_o_i': [[14.4], [0], [0], [1]],'phi': 0},

    10: {'ID': 9, 'r_o_i': [[16.2], [0], [0], [1]],'phi': 0},
    11: {'ID': 10, 'r_o_i': [[18.0], [0], [0], [1]],'phi': 0},
    12: {'ID': 11, 'r_o_i': [[19.8], [0], [0], [1]],'phi': 0},

    13: {'ID': 12, 'r_o_i': [[21.6], [0], [0], [1]],'phi': 0},
    # 14: {'ID': 13, 'r_o_i': [[21.6 + 0.76-0.345], [-0.7], [0], [1]],'phi': 0},
    15: {'ID': 14, 'r_o_i': [[21.6 + 0.73], [-1.05], [0], [1]],'phi': -np.pi/2 +0.1},

    16: {'ID': 15, 'r_o_i': [[21.6 + 0.73], [-2.83], [0], [1]],'phi': -np.pi/2},
    17: {'ID': 16, 'r_o_i': [[21.6 + 0.73], [-4.63], [0], [1]],'phi': -np.pi/2},
    18: {'ID': 17, 'r_o_i': [[21.6 + 0.73], [-6.43], [0], [1]],'phi': -np.pi/2},

    19: {'ID': 18, 'r_o_i': [[21.6 + 0.76], [-8.23], [0], [1]],'phi': -np.pi/2},
    20: {'ID': 19, 'r_o_i': [[21.6 + 0.76], [-10.03], [0], [1]],'phi': -np.pi/2},
    21: {'ID': 20, 'r_o_i': [[21.6 + 0.76], [-11.83], [0], [1]],'phi': -np.pi/2},

    22: {'ID': 21, 'r_o_i': [[21.6 + 0.76], [-12.83], [0], [1]],'phi': -np.pi/2},
    23: {'ID': 22, 'r_o_i': [[21.6 + 0.76+0.54], [-12.83-0.7], [0], [1]],'phi': 0},#### sua
    24: {'ID': 23, 'r_o_i': [[25.16-0.76-0.76], [-13.78], [0], [1]],'phi': 0},

    25: {'ID': 24, 'r_o_i': [[26.96-0.76-0.76], [-13.78], [0], [1]],'phi': 0},
    26: {'ID': 25, 'r_o_i': [[28.76-0.76-0.76], [-13.78], [0], [1]],'phi': 0},
    27: {'ID': 26, 'r_o_i': [[30.56-0.76-0.76], [-13.78], [0], [1]],'phi': 0},

    28: {'ID': 27, 'r_o_i': [[32.36-0.76-0.76], [-13.78], [0], [1]],'phi': 0},
    29: {'ID': 28, 'r_o_i': [[34.16-0.76-0.76], [-13.78], [0], [1]],'phi': 0},
    30: {'ID': 29, 'r_o_i': [[35.96-0.76-0.76], [-13.78], [0], [1]],'phi': 0},

    31: {'ID': 30, 'r_o_i': [[37.76-0.76-0.76], [-13.78], [0], [1]],'phi': 0},
    32: {'ID': 31, 'r_o_i': [[38.76-0.76-0.76], [-13.78], [0], [1]],'phi': 0},

    36: {'ID': 35, 'r_o_i': [[21.6 + 0.76-0.53], [-0.56], [0], [1]],'phi': -np.pi/2},


}

# Hàm trích xuất thông tin r_o_i từ từ điển dựa trên ID
def get_r_o_i_by_id(id):
    # if id is not None:
        # print("id", id)
    if (id +1) in dictionary:
        entry = dictionary[id+1]
        phi = entry["phi"] 
        # phi = np.deg2rad(phi)
        r_O_i = entry["r_o_i"]
        # print("phi", phi)
        c = np.cos(phi)
        s = np.sin(phi)
        T = [[c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]
        return T, r_O_i, phi
    else:
        print("loi ID_tag_ not found _ -------")
        return None



# id = 1 # Thay đổi ID ở đây để kiểm tra các giá trị khác
# r_o_i = get_r_o_i_by_id(id)
# print(r_o_i)





# goc ban dau voi huong nhin thang, x sang phai, y huong mat
# dictionary = {

#     1: {'ID': 0, 'r_o_i': [[0], [0], [0], [1]],'phi': 90},
#     2: {'ID': 1, 'r_o_i': [[0], [1.8], [0], [1]],'phi': 90},
#     3: {'ID': 2, 'r_o_i': [[0], [3.6], [0], [1]],'phi': 90},

#     4: {'ID': 3, 'r_o_i': [[0], [5.4], [0], [1]] ,'phi': 90},
#     5: {'ID': 4, 'r_o_i': [[0], [7.2], [0], [1]],'phi': 90},
#     6: {'ID': 5, 'r_o_i': [[0], [9.0], [0], [1]],'phi': 90},

#     7: {'ID': 6, 'r_o_i': [[0], [10.8], [0], [1]],'phi': 90},
#     8: {'ID': 7, 'r_o_i': [[0], [12.6], [0], [1]],'phi': 90},
#     9: {'ID': 8, 'r_o_i': [[0], [14.4], [0], [1]],'phi': 90},

#     10: {'ID': 9, 'r_o_i': [[0], [16.2], [0], [1]],'phi': 90},
#     11: {'ID': 10, 'r_o_i': [[0], [18.0], [0], [1]],'phi': 90},
#     12: {'ID': 11, 'r_o_i': [[0], [19.8], [0], [1]],'phi': 90},

#     13: {'ID': 12, 'r_o_i': [[0], [21.6], [0], [1]],'phi': 90},
#     14: {'ID': 13, 'r_o_i': [[0], [23.4], [0], [1]],'phi': 90},
#     15: {'ID': 14, 'r_o_i': [[1.03], [24.16], [0], [1]],'phi': 0},

#     16: {'ID': 15, 'r_o_i': [[2.83], [24.16], [0], [1]],'phi': 0},
#     17: {'ID': 16, 'r_o_i': [[4.63], [24.16], [0], [1]],'phi': 0},
#     18: {'ID': 17, 'r_o_i': [[6.43], [24.16], [0], [1]],'phi': 0},

#     19: {'ID': 18, 'r_o_i': [[8.23], [24.16], [0], [1]],'phi': 0},
#     20: {'ID': 19, 'r_o_i': [[10.03], [24.16], [0], [1]],'phi': 0},
#     21: {'ID': 20, 'r_o_i': [[11.83], [24.16], [0], [1]],'phi': 0},

#     22: {'ID': 21, 'r_o_i': [[12.83], [24.16], [0], [1]],'phi': 0},
#     23: {'ID': 22, 'r_o_i': [[13.78], [24.16], [0], [1]],'phi': 0},
#     24: {'ID': 23, 'r_o_i': [[13.78], [25.16], [0], [1]],'phi': 90},

#     25: {'ID': 24, 'r_o_i': [[13.78], [26.96], [0], [1]],'phi': 90},
#     26: {'ID': 25, 'r_o_i': [[13.78], [28.76], [0], [1]],'phi': 90},
#     27: {'ID': 26, 'r_o_i': [[13.78], [30.56], [0], [1]],'phi': 90},

#     28: {'ID': 27, 'r_o_i': [[13.78], [32.36], [0], [1]],'phi': 90},
#     29: {'ID': 28, 'r_o_i': [[13.78], [34.16], [0], [1]],'phi': 90},
#     30: {'ID': 29, 'r_o_i': [[13.78], [35.96], [0], [1]],'phi': 90},

#     31: {'ID': 30, 'r_o_i': [[13.78], [37.76], [0], [1]],'phi': 90},
#     32: {'ID': 31, 'r_o_i': [[13.78], [38.76], [0], [1]],'phi': 90},

# }