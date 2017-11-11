"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 1000.0

def max_idx_limit(data, limit='inf'):  
    """ 
    return a list of index and value of  
    maximun values in data 
    """  
    maxvals = []  
    for idx in range(len(data)):  
        item = data[idx]  
        if item > limit:  
            continue  
        elif len(maxvals) == 0:  
            maxvals.append((idx, item))  
        elif item == maxvals[0][1]:  
            maxvals.append((idx, item))  
        elif item > maxvals[0][1]:  
            maxvals = [(idx, item)]  
    return maxvals 

def min_idx(data):  
    """ 
    return a list of index and value of  
    minimun values in data 
    """  
    minvals = []  
    for idx in range(len(data)):  
        item = data[idx]  
        if len(minvals) == 0:  
            minvals.append((idx, item))  
        elif item == minvals[0][1]:  
            minvals.append((idx, item))  
        elif item < minvals[0][1]:  
            minvals = [(idx, item)]  
    return minvals  

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies_baked = 0.0  
        self._cookies_in_bank = 0.0  
        self._cookies_per_second = 1.0  
        self._session_time = 0.0  
        self._session_history = [(0.0, None, 0.0, 0.0)]  
        self._time_until = 'inf' 
        
    def __str__(self):
        """
        Return human readable state
        """
        #string  = "Time: %1f Current Cookies: %f CPS: %.1f Total Cookies: %.1f _history (length: %d): %s"   
        #return string % (self._current_time,self._current_cookies,self._current_cps,self._total_cookies,len(self._game_history),self._game_history)
      
        return str("================================\n" +  
                   "Game Time:          " + str(self._session_time) + "\n" +  
                   "Cookies in Bank:    " + str(self._cookies_in_bank) + "\n" +  
                   "Cookies per Second: " + str(self._cookies_per_second) + "\n" +  
                   "Cookies Baked:      " + str(self._cookies_baked))  

    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies_in_bank
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cookies_per_second
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._session_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._session_history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        
        if self._cookies_in_bank < cookies:
            self._time_until = math.ceil((cookies - self._cookies_in_bank) / self._cookies_per_second)
            
        else:
            self._time_until = 0.0
        
        return self._time_until

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._session_time += time
            self._cookies_in_bank += time * self._cookies_per_second
            self._cookies_baked += time * self._cookies_per_second

    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._cookies_in_bank:
            self._cookies_per_second += additional_cps
            self._cookies_in_bank -= cost
            self._session_history.append((float(self._session_time), item_name, cost, float(self._cookies_baked)))

            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clicker_state = ClickerState()  
    while clicker_state.get_time() <= duration:   
        build_info_clone = build_info.clone()  
        cookies = clicker_state.get_cookies()  
        cps = clicker_state.get_cps()  
        history = clicker_state.get_history()  
        time_left = duration - clicker_state.get_time()  
          
        item_name = strategy(cookies, cps, history, time_left, build_info_clone)  
        if item_name == None:  
            clicker_state.wait(time_left)  
            break  
  
        cost = build_info_clone.get_cost(item_name)  
        additional_cps = build_info_clone.get_cps(item_name)  
          
        if cookies >= cost:  
            time_to_purchase = 0  
        elif clicker_state.time_until(cost) > time_left:  
            time_to_purchase = time_left  
        else:  
            time_to_purchase = clicker_state.time_until(cost)  
  

        clicker_state.wait(time_to_purchase)  
        clicker_state.buy_item(item_name, cost, additional_cps)  

        build_info.update_item(item_name)  
          
        if cookies < cost and clicker_state.time_until(cost) > time_left:  
            break  

    return clicker_state  

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    
    items = build_info.build_items()
    
    cheapest_item = items[0]
    cheapest_cost = build_info.get_cost(cheapest_item)

    
    for item in items[1:]:
        if cheapest_cost > build_info.get_cost(item):
            cheapest_cost = build_info.get_cost(item)
            cheapest_item = item
            
    if cookies + cps* time_left >= cheapest_cost:
        return cheapest_item
    else:
        return None


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    build_info_expensive = build_info.clone()  
    item_cost_list = [build_info_expensive.get_cost(item) for item in build_info_expensive.build_items()]  
  
    # get the affordable cost in the time left.  
    afford_cost = cookies + cps * time_left  
      
    # get the expensive cost you can afford in the time left  
    index_cost_list = max_idx_limit(item_cost_list, afford_cost)  
      
    if len(index_cost_list) == 0:  
        return None   
    else:  
        index = random.choice(index_cost_list)[0]  
        return build_info_expensive.build_items()[index]  


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    build_info_best = build_info.clone()   
      
    item_list = []  
    qor_list = []  
    prod_dict = {}  
    # get the item list you can afford in the time left  
    for item in build_info_best.build_items():  
        if build_info_best.get_cost(item) <= cookies + cps * time_left:  
            item_list.append(item)  
            item_qor  = build_info_best.get_cps(item) / (build_info_best.get_cost(item) * (cps + build_info_best.get_cps(item)))  
            item_prod = build_info_best.get_cps(item) * math.ceil(time_left - math.ceil((build_info_best.get_cost(item)) / cps) )  
            item_k    = 2  
            if time_left // math.ceil((build_info_best.get_cost(item)) / cps)  < 20:  
                item_k **= (time_left // math.ceil((build_info_best.get_cost(item)) / cps))  
            prod_dict[item] = item_prod * item_k  
            qor_list.append(item_qor)  

    if len(item_list) == 0:  
        return None  
    else:  
        index = random.choice(max_idx_limit(qor_list))[0]  
        item_best = item_list[index]  
      
    for item in prod_dict:  
        if build_info_best.get_cost(item) < build_info_best.get_cost(item_best):  
            if prod_dict[item] > prod_dict[item_best]:  
                item_best = item  
    return item_best   
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    
