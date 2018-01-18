#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib2
import json
import sys, time
import curses
class fetch_kraken:
    def __init__(self):
        self.is_stop = False
        self.num = 50
        self.target_symbol = ('BTC','ETH','XRP', 'BCH', 'LTC',  'DASH', 'USDT', 'DOGE')
        self.method = ('depth','ticker','trades', 'info')
        self.trade_list = ('XXBTZUSD', 'XLTCZUSD', 'BCHUSD', 'XETHZUSD', 'XXRPZUSD') 
        #self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
	self.base_url = 'https://api.kraken.com/0/public/Ticker?pair='
        self.send_headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
 'Connection':'keep-alive'
} 
    def stop(self):
        self.is_stop = True
        curses.endwin()
        print('stopped')

    def get_ticker(self):
        ticker_url = self.base_url+','.join(self.trade_list)
        print(ticker_url)
        #self.stdscr = curses.initscr()
        #self.stdscr = curses.initscr()
        self.stdscr = curses.newwin(50, 80, 12, 80)
        #self.stdscr = curses.newpad(600, 800)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        while not self.is_stop:
            cur_pos_x = 0;
            req = urllib2.Request(ticker_url, headers=self.send_headers)
            res = urllib2.urlopen(req)
            page = res.read()
            json_obj_all = json.loads(page)
            json_obj = json_obj_all['result']
            #print(page)
            self.stdscr.addstr(cur_pos_x,0,'Kraken\n'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) ), curses.color_pair(3))
            cur_pos_x += 2;
            print_head =  "Symbol \t\tLast($) \tBuy \t\tSell"
            self.stdscr.addstr(cur_pos_x,0,print_head,curses.color_pair(3))
            cur_pos_x += 1;
            for pair in self.trade_list:
                color_index = 1

                if pair in self.trade_list:
                    #print_content =  "sym:%7s \tprice:%10s \tper:%5s"%(json_obj[i]['symbol'], json_obj[i]['price_usd'], json_obj[i]['percent_change_24h']);
                    print_content =  "%7s \t%7.2f \t%7.2f \t%7.2f"%(pair, float(json_obj[pair]['c'][0]), float(json_obj[pair]['b'][0]), float(json_obj[pair]['a'][0]));
                    if not True:
                        color_index = 2
                    self.stdscr.addstr(cur_pos_x,0,print_content,curses.color_pair(color_index))
                    cur_pos_x += 1

                #print "hi:%d\r"%i
                #stdscr.addstr(i, 0,  "hi:%d"%i)
                #sys.stdout.flush()
                self.stdscr.refresh()
            time.sleep(2)
if __name__ == "__main__":
    curses.initscr()
    info = fetch_kraken()
    try:
        info.get_ticker()
    except KeyboardInterrupt as e:
        info.stop()
    

    
