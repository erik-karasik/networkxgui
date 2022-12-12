import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class Programm(tk.Tk):
    def __init__(self):
        super().__init__()
        # Создадим экземпляр класса nx.Graph
        self.G = nx.Graph()
        self.geometry('1200x600+50+50')
        self.widgets()
        self.nodesList = []
        self.edgesList = []
        self.weightList=[]
        self.pathList = []
        self.f = plt.Figure(figsize=(5, 5), dpi=100)
        self.plot = tk.Label(self,image="")
        self.test()

    def widgets(self):
        tk.Label(self, text="input tab").grid(row=0, column=1)
        tk.Label(self, text="add nodes sep by space").grid(row=1)
        tk.Label(self, text="add edges in format n,n").grid(row=2)
        tk.Label(self, text="add weights in format n,n,w").grid(row=3)
        self.addNodesBox = tk.Entry(self)
        self.addNodesBox.grid(row=1, column=1)
        self.addEdgesBox = tk.Entry(self)
        self.addEdgesBox.grid(row=2, column=1)
        self.addWeightBox = tk.Entry(self)
        self.addWeightBox.grid(row=3, column=1)
        tk.Button(self,text='add', command=self.addNodes).grid(row=1, column=2)
        tk.Button(self, text='add', command=self.addEdges).grid(row=2, column=2)
        tk.Button(self, text='add', command=self.addWeight).grid(row=3, column=2)
        tk.Label(self, text="del tab").grid(row=0,column=4)
        tk.Label(self, text="del nodes sep by space").grid(row=1,column=3)
        tk.Label(self, text="del edges in format n,n").grid(row=2,column=3)
        tk.Label(self, text="del weights in format n,n,w").grid(row=3, column=3)
        self.removeNodesBox = tk.Entry(self)
        self.removeNodesBox.grid(row=1, column=4)
        self.removeEdgesBox = tk.Entry(self)
        self.removeEdgesBox.grid(row=2, column=4)
        self.removeWeightsBox = tk.Entry(self)
        self.removeWeightsBox.grid(row=3, column=4)
        tk.Button(self, text='del', command=self.removeNodes).grid(row=1, column=5)
        tk.Button(self, text='del', command=self.removeEdges).grid(row=2, column=5)
        tk.Button(self, text='del', command=self.removeWeights).grid(row=3, column=5)
        tk.Button(self, text='load graph', command=self.loadGraph).grid(row=1, column=7)
        tk.Button(self, text='sefe graph', command=self.saveGraph).grid(row=2, column=7)
        self.pathFrame = tk.Frame(self)
        self.pathFrame.grid(row=0,column=6,rowspan=4)
        tk.Label(self.pathFrame, text="path tab").grid(row=0, column=0, columnspan=2)
        tk.Label(self.pathFrame, text="path in format n n").grid(row=1, column=0,columnspan=2)
        self.pathBox=tk.Entry(self.pathFrame)
        self.pathBox.grid(row=2,column=0,columnspan=2)
        tk.Button(self.pathFrame,text='find path Dijkstra’s',command=self.path).grid(row=3,column=0)
        tk.Button(self.pathFrame, text='find path BFS', command=self.pathBFS).grid(row=3, column=1)
        tk.Button(self,text='reload',command=self.vis).grid(row=1,column=8)

        self.info = tk.Text(self,width=20)
        self.info.grid(row=4,column=0)
    def test(self):
        self.addNodesBox.insert(0,'1 2 3 4 5 6')
        self.addNodes()
        self.addEdgesBox.insert(0,'1,2 2,3 3,4 4,5 5,6 6,1 1,4')
        self.addEdges()
        self.addWeightBox.insert(0,'1,2,5 2,3,4 3,4,6 4,5,9 5,6,5 6,1,1 1,4,2')
        self.addWeight()
    def path(self):
        nodesList = self.pathBox.get().split(" ")
        self.addNodesBox.delete(0, "end")
        if self.checkNode(nodesList[0]) or self.checkNode(nodesList[1]): return False
        else:
            predecessors, _ = nx.floyd_warshall_predecessor_and_distance(self.G)
            self.pathList = nx.reconstruct_path(nodesList[0], nodesList[1], predecessors)
            self.vis()
    def pathBFS(self):
        nodesList = self.pathBox.get().split(" ")
        self.addNodesBox.delete(0, "end")
        if self.checkNode(nodesList[0]) or self.checkNode(nodesList[1]): return False
        else:
            explored=[]
            queue = [[nodesList[0]]]
            if nodesList[0] == nodesList[1]:
                self.addNodesBox.insert(0, "same nodes")
                return
            while queue:
                path = queue.pop(0)
                node = path[-1]
                if node not in explored:
                    neighbours = self.G[node]
                    for neighbour in neighbours:
                        new_path = list(path)
                        new_path.append(neighbour)
                        queue.append(new_path)
                        if neighbour == nodesList[1]:
                            self.pathList = [str(i) for i in new_path]
                            self.vis()
                            return
                    explored.append(node)
            return
    def saveGraph(self):
        f = filedialog.asksaveasfile(initialdir="/",mode='w', defaultextension=".grf")
        if f is None: return
        f.write(str(self.nodesList)+"\n"+str(self.edgesList))
        f.close()
    def loadGraph(self):
        file = filedialog.askopenfilename(initialdir='/',filetypes=(("graph", ".grf"), ("All Files", "*.*")))
        # inserting data to text editor
        content = open(file)
        data = content.readlines()
        self.G.remove_edges_from(self.edgesList)
        self.G.remove_nodes_from(self.nodesList)
        for i in data[0]:
            if self.checkNode(i):
                self.G.add_node(i)
                self.nodesList.append(i)
        for i in data[1]:
            if self.checkEdge(i):
                self.G.add_edge(i[0],i[1])
                self.edgesList.append(i)
        self.vis()
    def vis(self):
        plt.figure()
        if len(self.weightList)==0:
            nx.draw_circular(self.G, node_color='red', node_size=1000, with_labels=True)
        elif len(self.pathList)==0:
            wei=nx.get_edge_attributes(self.G,'weight')
            pos = nx.spring_layout(self.G)
            nx.draw(self.G,pos,with_labels=True,font_weight='bold')
            nx.draw_networkx_edge_labels(self.G,pos,edge_labels=wei)
        else:
            edges = [(a, b) for a, b in zip(self.pathList, self.pathList[1:])]
            weights = nx.get_edge_attributes(self.G, 'weight')
            pos = nx.circular_layout(self.G)
            nx.draw_networkx(self.G, pos=pos)
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=weights)
            nx.draw_networkx_edges(self.G, pos=pos, edgelist=edges, edge_color="r", width=3)
            title = "Shortest path between [{}] and [{}]: {}" \
                .format("s", "v", " -> ".join(self.pathList))
        plt.savefig("tmpplot.png")
        image = Image.open("tmpplot.png")
        display = ImageTk.PhotoImage(image)
        self.plot = tk.Label(self,image=display)
        self.plot.grid(row=4, rowspan=6, column=1,columnspan=6)
        notes = self.G.nodes(data=False)
        j = 0
        self.info.insert(0.0,"a")
        self.info.delete(0.0,tk.END)
        for i in notes:
            nei = [n for n in self.G.neighbors(i)]
            self.info.insert(tk.END,f'neighbors of {i} ({len(nei)}): {nei} \n')
            #tk.Label(self, text=f"neighbors of {i} ({len(nei)}): {nei}").grid(row=4+j, column=0)
            j+=1
        self.info.insert(tk.END,f"number of nodes: {len(notes)}")
        #tk.Label(self, text=f"number of nodes: {len(notes)}").grid(row=4+len(notes)+1, column=0)
    def checkNode(self,node): return node != '' and node != " " and node not in self.nodesList
    def checkEdge(self,edge):
        return len(edge) == 2 and (edge not in self.edgesList or (edge[1], edge[0]) not in self.edgesList) and \
               edge[0] in self.nodesList and edge[1] in self.nodesList
    def checkWEdge(self,edge):
        return ((edge[0],edge[1]) in self.edgesList or (edge[1], edge[0]) in self.edgesList)
    def addNodes(self):
        nodesList = self.addNodesBox.get().split(" ")
        self.addNodesBox.delete(0,"end")
        for i in nodesList[:]:
            if self.checkNode(i):self.nodesList.append(i)
            else: nodesList.remove(i)
        if len(self.nodesList)>0:
            self.G.add_nodes_from(nodesList)
            self.vis()
    def addEdges(self):
        edgesList = self.addEdgesBox.get().split(" ")
        self.addEdgesBox.delete(0, "end")
        edgeList = []
        for i in edgesList[:]:
            edge = tuple(i.split(","))
            if self.checkEdge(edge):
                self.edgesList.append(edge)
                edgeList.append(edge)
            else: edgesList.remove(i)
        if len(edgeList) > 0:
            self.G.add_edges_from(edgeList)
        self.vis()
    def addWeight(self):
        weightsList=self.addWeightBox.get().split(" ")
        self.addWeightBox.delete(0,"end")
        weightList=[]
        for i in weightsList[:]:
            edge = tuple(i.split(","))
            if (edge[0],edge[1],float(edge[2])) not in self.weightList and \
                    (edge[1], edge[0], float(edge[2])) not in self.weightList:
                if self.checkEdge((edge[0],edge[1])):
                    self.weightList.append((edge[0],edge[1],float(edge[2])))
                    weightList.append((edge[0],edge[1],float(edge[2])))
                    self.edgesList.append((edge[0],edge[1]))
                elif self.checkWEdge(edge):
                    self.removeEdge((edge[0],edge[1]))
                    self.weightList.append((edge[0],edge[1],float(edge[2])))
                    weightList.append((edge[0],edge[1],float(edge[2])))
                    self.edgesList.append((edge[0],edge[1]))
        if len(weightList) > 0:
            self.G.add_weighted_edges_from(weightList)
        self.vis()
    def removeNode(self,nodeIndex):
        self.G.remove_node(nodeIndex)
        self.vis()
    def removeNodes(self):
        nodesList = self.removeNodesBox.get().split(" ")
        self.removeNodesBox.delete(0, "end")
        for i in nodesList[:]:
            if i == '' or i == " " or i not in self.nodesList: nodesList.remove(i)
            else: self.nodesList.remove(i)
        if len(nodesList)>0:
            self.G.remove_nodes_from(nodesList)
        self.vis()
    def removeEdge(self, edge):
        if edge in self.edgesList: self.edgesList.remove(edge)
        else: self.edgesList.remove((edge[1], edge[0]))
        self.G.remove_edge(edge[0],edge[1])
    def removeEdges(self):
        edgesList = self.removeEdgesBox.get().split(" ")
        self.addEdgesBox.delete(0, "end")
        edgeList = []
        for i in edgesList[:]:
            edge = tuple(i.split(","))
            if edge not in self.edgesList and (edge[1], edge[0]) not in self.edgesList: edgesList.remove(i)
            elif edge[0] not in self.nodesList or edge[1] not in self.nodesList: edgesList.remove(i)
            else:
                if edge in self.edgesList:
                    self.edgesList.remove(edge)
                else:
                    self.edgesList.remove((edge[1], edge[0]))
                edgeList.append(edge)

        if len(edgeList) > 0:
            self.G.remove_edges_from(edgeList)
        self.vis()
    def removeWeights(self):
        edgesList = self.removeWeightsBox.get().split(" ")
        self.addEdgesBox.delete(0, "end")
        edgeList = []
        print(self.edgesList,self.weightList)

        for i in edgesList[:]:
            edge = tuple(i.split(","))
            flag=False
            for j in self.weightList[:]:
                if edge==(j[0],j[1]) or edge==(j[1],j[0]):
                    self.weightList.remove(j)
                    flag=True
            if flag:
                if (edge[0],edge[1]) in self.edgesList:
                    self.edgesList.remove((edge[0],edge[1]))
                else:
                    self.edgesList.remove((edge[1],edge[0]))
                edgeList.append(edge)

        if len(edgeList) > 0:
            self.G.remove_edges_from(edgeList)
        self.vis()

if __name__=='__main__':
    app = Programm()
    app.mainloop()