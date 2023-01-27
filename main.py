import random
import tqdm

class Card:
    def __init__(self, val, color):
        self.val_str = val
        self.color = color

    def get_num(self):
        if self.val_str in list(map(str, range(1, 11))):
            return int(self.val_str)
        if self.val_str in ['J', 'Q', 'K']:
            return 10

    def to_string(self):
        return self.val_str, self.color


class CardSet:
    def __init__(self):
        type1 = [Card(i, '梅花') for i in list(map(str, range(1, 11))) + ['J', 'Q', 'K']]
        type2 = [Card(i, '红桃') for i in list(map(str, range(1, 11))) + ['J', 'Q', 'K']]
        type3 = [Card(i, '黑桃') for i in list(map(str, range(1, 11))) + ['J', 'Q', 'K']]
        type4 = [Card(i, '方片') for i in list(map(str, range(1, 11))) + ['J', 'Q', 'K']]
        self.set = type1 + type2 + type3 + type4

    def shuffle(self):
        random.shuffle(self.set)

    def to_string(self):
        return [i.to_string() for i in self.set]


class Player:
    def __init__(self, name):
        self.name = name
        self.win_times = 0
        self.cards = []
        self.total_val = 0

    def get_cards(self, cardset: CardSet):
        if self.name == '玩家':
            for i in range(0, 9, 2):
                self.cards.append(cardset.set[i])
        else:
            for i in range(1, 10, 2):
                self.cards.append(cardset.set[i])

    def show_hand(self):
        return [i.to_string() for i in self.cards]

    def compute_val(self):
        pure_val_ls = [i.get_num() for i in self.cards]  # 0 1 2 3 4
        combines = []
        for i in range(0, 3):
            for j in range(i + 1, 4):
                for k in range(j + 1, 5):
                    combines.append((pure_val_ls[i], pure_val_ls[j], pure_val_ls[k]))
        if is_exist_niu(combines)[0]:
            niu_nums = is_exist_niu(combines)[1]
            for i in niu_nums:
                pure_val_ls.remove(i)
            self.total_val = sum(pure_val_ls) % 10
            if self.total_val == 0:
                self.total_val += 10
        else:
            self.total_val = -1
        return self.total_val

    def destroy_hand(self):
        self.cards = []
        self.total_val = 0

    def win(self):
        self.win_times += 1


def is_exist_niu(ls):
    for i in ls:
        if sum(i) % 10 == 0:
            return True, i
    return False, -1


if __name__ == '__main__':
    cards = CardSet()
    master = Player('庄家')
    player = Player('玩家')
    times = 100000
    for i in tqdm.trange(times):
        cards.shuffle()
        master.get_cards(cards)
        player.get_cards(cards)
        master_val = master.compute_val()
        player_val = player.compute_val()

        if master_val > player_val:
            master.win()
        if master_val < player_val:
            player.win()
        master.destroy_hand()
        player.destroy_hand()
    print('庄家获胜次数', master.win_times)
    print('玩家获胜次数', player.win_times)
    print('玩家获胜的概率为', player.win_times / times)
