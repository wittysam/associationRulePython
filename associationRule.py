from itertools import combinations


############################# 函示定義（以下有主程式分割線） #############################
# 此函式是用來修剪Database，讓其Size小一點
# 原理：
# -----------------------------------------
# k = 1，所有不符合 min_supp的item          |
# 都可以直接從 database移除。                |
# 因為任何有包含這些 item的 itemSet，         |
# 也不可能符合 min_supp。                    |
# -----------------------------------------
# 計算時間大約 7 分鐘
def filter_dictionary(dictionary, supp):

    filtered_dict = {}
    # key 是 item 編號
    # value 是出現在Transactions的次數
    for key, value in dictionary.items():
        if value >= supp:
            filtered_dict[key] = value
        else:
            # 14000 種 item 沒有超過 support
            # Transactions 約有 90000
            # Time Complexity 為 14000 * 90000
            for id in Transactions.keys():
                # 此Key 可以從Database Remove
                if key in Transactions[id]:
                    Transactions[id].remove(key)
                    # 若是空了，就刪除此筆Transactions
                    # Tid 的總數目已經記住了
                    if Transactions[id] == None:
                        del Transactions[id]

    return filtered_dict


def ck_Generate(itemSet_k, k):
    # k 生成 k + 1
    # 輸入keys會是多組tuple
    k_list = list(itemSet_k.keys())
    new_k_list = set()
    new_k_list_dict = dict()
    while k_list != None:

        # 兩個itemSet取交集
        # 交集的長度若是k - 1，則兩個大小為k的itemSet，可以生成出 k + 1的itemSet
        length = len(k_list)

        for i in range(length):
            for j in range(i + 1, length):
                # 遍歷整個itemSet
                intersection = set(k_list[i]) & set(k_list[j])
                # print(f"產生的交集{intersection}")

                # 交集的大小是k - 1，則可以合併此兩個itemSet
                if len(intersection) == k - 1:
                    # 聯集邏輯運算
                    union = set(k_list[i]) | set(k_list[j])

                    # 使用Downward closure property
                    combinations_of_candidate = combinations(list(sorted(union)), k)
                    add_to_newk = True
                    for c in combinations_of_candidate:
                        if c not in k_list:
                            add_to_newk = False
                            break
                    if add_to_newk == True:
                        new_k_list.add(tuple(sorted(union)))

        # Turn set into list
        new_k_list = list(new_k_list)

        # print(new_k_list)
        for iSet in new_k_list:
            iSet = set(tuple(sorted(iSet)))
            count = 0
            # check the combination is the subset of each id in the Transactions
            # Don't use issubset() function
            for id in range(1, Tid + 1):
                # check the item combination is in the transaction
                # combination is a tuple
                # Turn tuple into set
                if iSet & Transactions[id] == iSet:
                    count += 1
            if count >= supp:
                new_k_list_dict[tuple(sorted(iSet))] = count
        return new_k_list_dict


############################# 主程式從以下開始 #############################

# 初始參數
itemSet = []
itemSet_k1 = {}
Tid = 0
Transactions = {}  # Tid: [int set]

# 讀入input產生Transactions，此Transactions 是個 dictionary。key為Tid, value為 integer list，裝載 購買的item set
with open("input.txt", "r") as f:
    for line in f:
        # Tid 從 1開始
        Tid += 1
        # Transactions 購買的item是使用set儲存： (1, 2, 3, ..., etc.)
        Transactions[Tid] = set()
        # 字串處理
        line = line.split()
        line = [int(number) for number in line]
        for number in line:
            tuple_number = list()
            tuple_number.append(number)
            tuple_number = tuple(tuple_number)
            itemSet_k1[tuple_number] = itemSet_k1.get(tuple_number, 0) + 1
            # 建立Transaction的表格
            Transactions[Tid].add(number)
        if "str" in line:
            break
itemSet.append(itemSet_k1)
# User Defined Parameters
min_supp = float(
    input("Please enter minimum support(The input should range between 0 to 1): ")
)
min_conf = float(
    input("Please enter minimum confidence(The input should range between 0 to 1): ")
)
supp = int(min_supp * Tid) + 1
print(f"The Acceptable Support for Items: {supp}")
# supp 是 min_supp * Tid
"""
1. min_supp = 0.1時，需要跑7分鐘
2. min_supp = 0.05時，需要跑10分鐘
3. min_supp = 0.01時，需要跑15分鐘
4. min_supp = 0.001時，需要跑 20分鐘
"""
itemSet_k1 = filter_dictionary(itemSet_k1, supp)
# Downward closure property
# We need a list to
itemSet_list = []
# Initialization
# min_supp = 0.01時，執行時間大量上升
# 因為需要以Combination生成Candidates => 大約需要執行 3分鐘
# min_supp = 0.001時，執行
itemSet_k = itemSet_k1
itemSet = []
itemSet.append(itemSet_k1)
k = 1
while True:
    itemSet_new = ck_Generate(itemSet_k, k)
    if itemSet_new == {}:
        break
    else:
        itemSet.append(itemSet_new)
        k += 1
        itemSet_k = itemSet_new
# itemSet
# k
# n 從 k = 3 倒數到 k = 2
for n in range(k, 1, -1):
    # itemSet[3 -1 =2] 從 k = 3開始 iterate
    for iS in itemSet[n - 1]:
        # Ex: 3 -> combination 2 with
        # k = 3往下可以做subset分析， k = 2 到 k = 1
        for q in range(n - 1, 0, -1):
            subset = combinations(list(iS), q)
            for n_m_1 in subset:
                if n_m_1 == {}:
                    continue
                confidence = itemSet[n - 1][iS] / itemSet[q - 1][tuple(n_m_1)]
                if confidence >= min_conf:
                    # 格式Matching
                    if len(set(n_m_1)) == 1 and len(set(iS) - set(n_m_1)) == 1:
                        print(
                            f"{int(set(n_m_1))} -> {int(set(iS) - set(n_m_1))} ({confidence})"
                        )
                    elif len(set(n_m_1)) == 1:
                        print(
                            f"{int(set(n_m_1))} -> {set(iS) - set(n_m_1)} ({confidence})"
                        )
                    elif len(set(iS) - set(n_m_1)) == 1:
                        print(
                            f"{int(set(n_m_1))} -> {set(iS) - set(n_m_1)} ({confidence})"
                        )
                    else:
                        print(f"{set(n_m_1)} -> {set(iS) - set(n_m_1)} ({confidence})")
