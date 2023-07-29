import queue

class Backtest:
    def __init__(self):
        self._macd_queue = queue.Queue()
        self._previous_macd_diff = None
        self._macd_sum = 0
        self._is_invested = False
        self._is_market_buy_order = False
        self._is_market_sell_order = False
        self._cash = 100000
        self._shares = 0
        self._orders = 0
        self._entry_price = None
        self._entry_date = None
        self._wins = 0
        self._losses = 0
        self._total_win_percentage = 0
        self._total_max_win_percentage = 0
        self._total_loss_percentage = 0
        self._total_max_loss_percentage = 0
        self._total_trade_days = 0
        self._max_win_percentage = 0
        self._max_loss_percentage = 0

    def process_orders(self, row):
        if self.is_market_sell_order:
            self.cash += self.shares * row['Open']
            self.shares = 0
            self.is_market_sell_order = False
            self.is_invested = False
            self.orders += 1
            exit_price = row['Open']
            if exit_price > self.entry_price:
                self.wins += 1
                self.total_max_win_percentage += self.max_win_percentage
                self.total_win_percentage += (exit_price / self.entry_price - 1) * 100
            else:
                self.losses += 1
                self.total_max_loss_percentage += self.max_loss_percentage
                self.total_loss_percentage += (exit_price / self.entry_price - 1) * 100
            entry_price = None
            # total_trade_days += (entry_date - datetime.strptime(row['Date'], '%Y-%m-%d')).days
            self.total_trade_days += (row['Date'] - self.entry_date).days
            self.entry_date = None

            max_win_percentage = 0
            max_loss_percentage = 0

        if self.is_market_buy_order:
            self.shares += float(self.cash / row['Open'])
            self.cash = 0
            self.is_market_buy_order = False
            self.is_invested = True
            self.orders += 1
            self.entry_price = row['Open']
            self.entry_date = row['Date']

        if self.is_invested:
            return_percentage = (row['Close'] - self.entry_price) / self.entry_price * 100
            self.max_win_percentage = max(self.max_win_percentage, return_percentage)
            self.max_loss_percentage = min(self.max_loss_percentage, return_percentage)

    def print_results(self):
        self.orders = self.orders / 2
        print("cash " + str(self.cash))
        print("return " + str((self.cash / 100000 - 1) * 100))
        print("orders " + str(self.orders))
        print("wins " + str(self.wins))
        print("losses " + str(self.losses))
        print("win percentage " + str(0 if self.wins == 0 else self.total_win_percentage / self.wins))
        print("loss_percentage " + str(0 if self.losses == 0 else self.total_loss_percentage / self.losses))
        print(self.entry_date)
        print("average trade days " + str(0 if self.orders == 0 else self.total_trade_days / self.orders))
        wins = 1 if self.wins == 0 else self.wins
        losses = 1 if self.losses == 0 else self.losses
        print("max win percentage:" + str(self.total_max_win_percentage / wins))
        print("max loss percentage:" + str(self.total_max_loss_percentage / losses))

    @property
    def macd_queue(self):
        return self._macd_queue

    @macd_queue.setter
    def macd_queue(self, value):
        self._macd_queue = value

    @property
    def previous_macd_diff(self):
        return self._previous_macd_diff

    @previous_macd_diff.setter
    def previous_macd_diff(self, value):
        self._previous_macd_diff = value

    @property
    def macd_sum(self):
        return self._macd_sum

    @macd_sum.setter
    def macd_sum(self, value):
        self._macd_sum = value

    @property
    def is_invested(self):
        return self._is_invested

    @is_invested.setter
    def is_invested(self, value):
        self._is_invested = value

    @property
    def is_market_buy_order(self):
        return self._is_market_buy_order

    @is_market_buy_order.setter
    def is_market_buy_order(self, value):
        self._is_market_buy_order = value

    @property
    def is_market_sell_order(self):
        return self._is_market_sell_order

    @is_market_sell_order.setter
    def is_market_sell_order(self, value):
        self._is_market_sell_order = value

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, value):
        self._cash = value

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        self._shares = value

    @property
    def orders(self):
        return self._orders

    @orders.setter
    def orders(self, value):
        self._orders = value

    @property
    def entry_price(self):
        return self._entry_price

    @entry_price.setter
    def entry_price(self, value):
        self._entry_price = value

    @property
    def entry_date(self):
        return self._entry_date

    @entry_date.setter
    def entry_date(self, value):
        self._entry_date = value

    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, value):
        self._wins = value

    @property
    def losses(self):
        return self._losses

    @losses.setter
    def losses(self, value):
        self._losses = value

    @property
    def total_win_percentage(self):
        return self._total_win_percentage

    @total_win_percentage.setter
    def total_win_percentage(self, value):
        self._total_win_percentage = value

    @property
    def total_max_win_percentage(self):
        return self._total_max_win_percentage

    @total_max_win_percentage.setter
    def total_max_win_percentage(self, value):
        self._total_max_win_percentage = value

    @property
    def total_loss_percentage(self):
        return self._total_loss_percentage

    @total_loss_percentage.setter
    def total_loss_percentage(self, value):
        self._total_loss_percentage = value

    @property
    def total_max_loss_percentage(self):
        return self._total_max_loss_percentage

    @total_max_loss_percentage.setter
    def total_max_loss_percentage(self, value):
        self._total_max_loss_percentage = value

    @property
    def total_trade_days(self):
        return self._total_trade_days

    @total_trade_days.setter
    def total_trade_days(self, value):
        self._total_trade_days = value

    @property
    def max_win_percentage(self):
        return self._max_win_percentage

    @max_win_percentage.setter
    def max_win_percentage(self, value):
        self._max_win_percentage = value

    @property
    def max_loss_percentage(self):
        return self._max_loss_percentage

    @max_loss_percentage.setter
    def max_loss_percentage(self, value):
        self._max_loss_percentage = value
