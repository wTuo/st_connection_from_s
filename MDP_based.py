import networkx as nx
import random
import os
import copy

#(p, tcost, dcost)

# class edges_data(object):
#     def __init__(self, G, ):
#         self.

# a dic which maps e to (p, tcost, dcost), #p is the destroy probability 

class state(object):
#G is a type of networkx.Graph
    def __init__(self, G, src, det):
# graph_status is a dictionary which represents a map:(v1,v2) -> {0,1,2}(one-dimention with elements 0,1,2)   
#initial state (s, (2,2,2,2,2,...))

        self.graph_status = {}
        for e in G.edges():
            self.graph_status[e] = 2

        self.detected = []
        self.loc = src
    #reachable_vertex is a list
        self.reachable_vertex = [src]
    #undetected is a list with element type of e 
        # self.undetected = [e for e in G]
    #action_set is a list of element type of (v_e, e) where v_e is a end point lies in reachable_vertex
        self.action_set =[]
        # for e in G:
        #     if src in e:
        #         self.action_set.append(e)
        for endp in G[src]:
            self.action_set.append((src, (src, endp)))
        self.tmp_graph = nx.Graph()

#'e' is denoted by 2-element tuple

    def edge_fail(self, e):
        # print "fail"
        self.graph_status[e] = 0
        #update action_set
        # print "before:", self.action_set
        self.action_set = list(filter(lambda x: ( x[1] != e and (x[1][1],x[1][0]) != e ), self.action_set))
        # print "after:", self.action_set
        self.detected.append(e)
        # print self.action_set
        # os._exit(0)
        return self

    def edge_valid(self, e):
        # print "valid"
        self.graph_status[e] = 1
    #update location
        if e[0] in self.reachable_vertex:
            self.loc = e[1]
        else:
            self.loc = e[0]
    #update reachable_vertex
        self.reachable_vertex.append(self.loc)

    #update tmp_graph
        self.tmp_graph.add_edge(e[0],e[1], tcost = EDGES_DATA[e][1])

        #update action_set
        # print "before:", self.action_set
        pure_eset = []
        for a in self.action_set:
            pure_eset.append(a[1])
        for endp in G[self.loc]:
            ae = (self.loc, endp)
            ae_ = (endp, self.loc)
            if ae in pure_eset or ae_ in pure_eset:
                # print ae
                continue
            if ae in self.detected or ae_ in self.detected:
                continue
            self.action_set.append((self.loc, (self.loc, endp)))
            # self.action_set = list(filter(lambda x: (x[1] != ae and (x[1][1],x[1][0]) != ae) , self.action_set))
        self.action_set = list(filter(lambda x: (x[1] != e and (x[1][1],x[1][0]) != e) , self.action_set))
        # print "after:", self.action_set
        self.detected.append(e)
        return self
    # def update_self():
        #action_set
        #undetected
        #reachable_vertex
        #loc



    # def update_from_(state, flg):


def MDP_based(EDGES_DATA, src, det, init_state):
    #put state.tmp_graph as G
    def tran_cost(G,vm,vn):
        if vm == vn:
            return 0
        return nx.shortest_path_length(G, vm, vn, 'tcost')
    def check_terminating(state):
        # print id(state)
        if state.loc == det:
            return True
        gen_G_forcheck = nx.Graph()
        for e,status in state.graph_status.iteritems():
            if status == 1 or status == 2:
                gen_G_forcheck.add_edge(*e)
        # print gen_G_forcheck.edges()
        flg =True
        if src not in gen_G_forcheck.nodes() or det not in gen_G_forcheck.nodes():
            flg = False
    
        if not flg or not nx.has_path(gen_G_forcheck, src, det):
            return True
        return False

    PI={}
    def utilityf(state, depth):
        # print id(state)
        # print depth
        if check_terminating(state):
            # print id(state)
            return 0
        if len(state.action_set) == 0:
            # print "xxxxxxx"
            raise
        c = -99999999
        # print "depth:", depth, state.action_set
        for e in state.action_set:
            # print "depth:", depth, "e", e
            # print EDGES_DATA[e[1]][2]
            s_evalid = copy.deepcopy(state)
            s_efail = copy.deepcopy(state)
            tmp_c = -(tran_cost(state.tmp_graph, state.loc, e[0]) + EDGES_DATA[e[1]][2]) + \
                        EDGES_DATA[e[1]][0]*utilityf(s_efail.edge_fail(e[1]), depth + 1) + (1-EDGES_DATA[e[1]][0])*utilityf(s_evalid.edge_valid(e[1]), depth + 1)
            if tmp_c > c:
                c = tmp_c
                e_star = e[1]
                PI[state] = e[1]
        return c
    depth = 0
    print utilityf(init_state, depth+1 )
    return PI


if __name__ == "__main__":
    # EDGES_DATA = {(0,1):(0.5, 1, 1000),
    #               (1,0):(0.5, 1, 1000),
    #               (0,2):(0.5,1, 2),
    #               (2,0):(0.5,1, 2),
    #             (1,3):(0.5,1,2),
    #             (3,1):(0.5,1,2),
    #             (2,3):(0.5,1,2),
    #             (3,2):(0.5,1,2),
    #             (3,4):(0.5,1,2),
    #             (4,3):(0.5,1,2),
    #             (4,5):(0.5,1,2),
    #             (5,4):(0.5,1,2),
    #             (4,6):(0.5,1,2),
    #             (6,4):(0.5,1,2),
    #             (5,7):(0.5,1,2),
    #             (7,5):(0.5,1,2),
    #             (6,7):(0.5,1,2),
    #             (7,6):(0.5,1,2)}
    # edgelist = [(0,1),(0,2),(1,3),(2,3),(3,4),(4,5),(4,6),(5,7),(6,7)]
    # EDGES_DATA = {(0,1):(0.5,1,10000),
    #               (1,0):(0.5,1,10000),
    #               (0,2):(0.5,1,2),
    #               (2,0):(0.5,1,2),
    #             (1,3):(0.5,1,2),
    #             (3,1):(0.5,1,2),
    #             (2,3):(0.5,1,2),
    #               (3,2):(0.5,1,2),
    #             (3,4):(0.5,1,2),
    #             (4,3):(0.5,1,2)
    # }
    # edgelist = [(0,1),(0,2),(1,3),(2,3),(3,4)]
    EDGES_DATA = {(0,2): (0.5, 0, 20),
                  (2,0): (0.5, 0, 20),
                  (2,3): (0.5, 0, 20),
                  (3,2): (0.5, 0, 20),
                  (0,1): (0.75, 0, 6),
                  (1,0): (0.75, 0, 6),
                  (1,3): (0.75, 0, 6),
                  (3,1): (0.75, 0, 6),
    }
    edgelist = [(0,1), (1,3),(0,2),(2,3)]
    # EDGES_DATA = {(0,1): (0.5, 0, 2),
    #               (1,0): (0.5, 0, 2),
    #               (1,2): (0.5, 0, 3),
    #               (2,1): (0.5, 0, 3)
    # }
    # edgelist = [(0,1),(1,2)]
    # EDGES_DATA = {(0,1): (0.5, 0, 2),
    #               (1,0): (0.5, 0, 2),
    #               (1,3): (0.5, 0, 3),
    #               (3,1): (0.5, 0, 3),
    #               (0,2): (0.5, 0, 4),
    #               (2,0): (0.5, 0, 4),
    #               (2,3): (0.5, 0, 5),
    #               (3,2): (0.5, 0, 5),
    # }
    # edgelist = [(0,1), (1,3),(0,2),(2,3)]

    count = 0
    G = nx.Graph()
    G.add_edges_from(edgelist)
    inits = state(G, 0, 3)
    inits_ = copy.deepcopy(inits)
    get_pi = MDP_based(EDGES_DATA, 0, 3, inits)
    print get_pi[inits]

    
