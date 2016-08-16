#HELPER CLASS
class Member:
    def __init__(self, name, sponsor, asset, mentor = None):
        #name, sponsor, asset, and mentor are values of a node
        #mentor and sponsor are Member objects to make search easier in later functions
        #children is a list of Member objects which are a node's children
        self.name = name
        self.sponsor = sponsor
        self.asset = asset
        self.mentor = mentor
        self.children = []

#HELPER FUNCTIONS
def gather_lists(list_):
    #new_list adds together lists inside list_
    new_list = []
    for l in list_:
        new_list += l #for every list inside list_ add to new_list
    return new_list


def search_helper(node, member):
    #this helper function enables search of tree based on member name
    if node.name == member: #this is the base case. If true it returns the Member object
        return [node]
    elif node.children:
        #if children of node exist
        #use recurvise function to check base case for every child of node
        #use gather_list to put together returned node lists
        return gather_lists([search_helper(i, member) for i in node.children])
    else:
        return [] #in the case that both above conditions fail return empty list

def next_arrest(node, arrest_list):
    #child is the Member object which would be arrested next if it exists and is not arrested already
    #initially it is none
    child = None
    childasset = 0

    if node.children is not []: #checks if node has children
        for i in node.children:
            if i.asset > childasset and i.name not in arrest_list:
                #checks if a child has assets greater than the saved child with greatest assets
                #and checks if a child is not already arrests
                childasset = i.asset #if conditions pass the childasset is saved as this child's assets
                child = i #if conditions pass the child is saved as this child

    if node.sponsor and node.mentor and node.sponsor != node.mentor:
        #checks if sponsor and mentor for node exist and are not the same
        if node.sponsor.name not in arrest_list and node.mentor.name not in arrest_list:
            #checks that node sponsor and mentor are not arrested
            #next conditions check which one of child, sponsor, or mentor has greatest assets and returns that Member as next_arrest
            if childasset > node.sponsor.asset and childasset > node.mentor.asset:
                return child
            elif node.mentor.asset > childasset and node.mentor.asset > node.sponsor.asset:
                return node.mentor
            elif node.sponsor.asset > childasset and node.sponsor.asset > node.mentor.asset:
                return node.sponsor
        elif node.sponsor.name not in arrest_list and node.mentor.name in arrest_list:
            #checks that node sponsor is not arrested but node mentor is
            #next conditions check which one of child or sponsor has highest assets and returns that Member as next_arrest
            if childasset > node.sponsor.asset:
                return child
            elif node.sponsor.asset > childasset:
                return node.sponsor
        elif node.sponsor.name in arrest_list and node.mentor.name not in arrest_list:
            #checks that node sponsor is arrested and node mentor is not
            #next conditons check which one of child or mentor has highest assets and returns that Member as next_arrest
            if childasset > node.mentor.asset:
                return child
            elif node.mentor.asset > childasset:
                return node.mentor
        elif node.sponsor.name in arrest_list and node.mentor.name in arrest_list:
            #checks if both node sponsor and mentor are arrest and the returns child as next_arrest
            return child

    else:
        #checks if node sponsor and node mentor are the same
        #checks if node sponsor is not arrested
        if node.sponsor.name not in arrest_list:
            #checks if child has greater assets than node sponsor and returns child if True
            if childasset > node.sponsor.asset:
                return child
            #otherwise returns sponsor if sponsor has greater assets
            elif childasset < node.sponsor.asset:
                return node.sponsor
        elif node.sponsor.name in arrest_list:
            #checks if node sponsor is arrests, if True returns child as next_arrest
            return child

#MAIN CLASS

class Network(object):
    """A pyramid network.

    This class represents a pyramid network. The network topology can be loaded
    from a file, and it can find the best arrest scenario to maximize the seized
    asset.

    You may, if you wish, change the API of this class to add extra public
    methods or attributes. Make sure that you do not change the public methods
    that were defined in the handout. Otherwise, you may fail test results for
    those methods.

    """
    # === Attributes ===
    def __init__(self):
        self.leader = None #initiates leader as root of Tree as Member object
        self.data = [] #initiates a list of all nodes as Member objects in the Tree

    def load_log(self, log_file_name):
        """Load the network topology from the log log_file_name.

        TODO: Complete this part
        """

        open_log_file = open(log_file_name)
        #goes through every line of log_file_name
        for i in open_log_file:
            details = i.strip().split('#')
            #if a line has length 2 means it the root
            if len(details) == 2:
                #the root is saved in self.leader
                #the root is saved in self.data
                self.leader = Member(details[0], Member('None', 'None', 0, 'None'), int(details[1]))
                self.data.append(self.leader)
            else:
                #if length of line is not 2 it is not the root
                #makes sponsor object for the Member by extracting it from self.data
                for i in self.data:
                    if i.name == details[1]:
                        sponsor = i
                #appends Member object to self.data
                self.data.append(Member(details[0],sponsor,int(details[2])))

        #takes each Member object is self.data and loops through self.data again until
        #if condition is met and the object's child is found, then appends
        #child object in Member object's children list
        for i in self.data:
            for j in self.data:
                if i.name == j.sponsor.name:
                    i.children.append(j)

        #saves root's mentor as Member object with values None and asset 0
        self.leader.mentor = Member('None', 'None', 0, 'None')
        #takes each Member object in self.data
        for i in self.data:
            for j in range(len(i.children)):
                #takes each child of Member object
                #if it is the first child then the Member object is saved as the child's Mentor
                if j == 0:
                    i.children[j].mentor = i
                else:
                #if not first child then the child's mentor is saved as the child before it
                    i.children[j].mentor = i.children[j-1]

    def sponsor(self, member_name):
        """Return the sponsor name of member with name member_name.

        TODO: Complete this part
        """
        #uses search_helper to return Member object with name member_name as list
        result = search_helper(self.leader, member_name)
        #returns Member object's sponsor name
        return result[0].sponsor.name

    def mentor(self, member_name):
        """Return the mentor name of member with name member_name.

        TODO: Complete this part
        """
        #uses search_helper to return Member object with name member_name as list
        result = search_helper(self.leader, member_name)
        #returns Member object's mentor name
        return result[0].mentor.name


    def assets(self, member_name):
        """Return the assets of member with name member_name.

        TODO: Complete this part
        """
        #uses search_helper to return Member object with name member_name as list
        result = search_helper(self.leader, member_name)
        #returns Member object's assets
        return int(result[0].asset)


    def children(self, member_name):
        """Return the name of all children of member with name member_name.

        TODO: Complete this part
        """
        #uses search_helper to return Member object with name member_name as list
        result = search_helper(self.leader, member_name)
        result_children = [] #list to append Member object children
        #loops through Member object children and appends children to result_children
        for child in result[0].children:
            result_children.append(child.name)
        return result_children


    def best_arrest_assets(self, maximum_arrest):
        """Search for the amount of seized assets in the best arrest scenario
        that maximizes the seized assets. Consider all members as target zero.

        TODO: Complete this part
        """
        assets_list = [] #initiates list to append total assets for each target zero arrest
        for i in self.data:#loops through self.data to pick each target zero
            arrest_list = [i.name] #creates arrest list for each target zero
                #and appends target zero name to it
                #creates variable arrests_left to be arrests left after target zero arrest
            arrests_left = maximum_arrest-1
                #creates total to sum total assets of arrested members
            total = int(i.asset)
                #uses next_arrest helper to return next best arrest
            next_one = next_arrest(i, arrest_list)
            while arrests_left != 0:
                    #while number of arrests a not 0
                    #if next_arrest is None break from loop
                if next_one is None:
                        break
                else:
                        #else add next_one's assets to total
                    total += int(next_one.asset)
                        #reduce arrests_left by 1
                    arrests_left -= 1
                        #add next_one to arrest_list
                    arrest_list.append(next_one.name)
                        #return the next best arrest
                    next_one = next_arrest(next_one, arrest_list)
                #append total to asset_list
            assets_list.append(total)
        #return the max of asset_list
        return max(assets_list)

    def best_arrest_order(self, maximum_arrest):
        """Search for list of member names in the best arrest scenario that
        maximizes the seized assets. Consider all members as target zero,
        and the order in the list represents the order that members are
        arrested.

        TODO: Complete this part
        """

        assets_list = [] #initiates list to append total assets for each target zero arrest
        main_list = [] #initiates list to append list of arrest_list for each target zero
        for i in self.data:
            #loops through self.data to get target zero
            arrest_list = [i.name]
            #create arrest_list and append target zero
            arrests_left = maximum_arrest-1
            #arrests_left gives the number of arrests_left
            total = int(i.asset)
            #total is the sum of assets from arrests
            next_one = next_arrest(i, arrest_list)
            #next_one returns the next best arrest
            while arrests_left != 0:
                #while number of arrests are not 0
                if next_one is None:
                    #break out of loop if next_one is None
                    break
                else:
                    #else add next_one's assets to total
                    total += int(next_one.asset)
                    #reduce arrests_left by 1
                    arrests_left -= 1
                    #add next_one's name to arrest_list
                    arrest_list.append(next_one.name)
                    #return next_best arrest
                    next_one = next_arrest(next_one, arrest_list)
            #add total to assets_list
            assets_list.append(total)
            #add arrest_list to main_list
            main_list.append(arrest_list)

        max_asset = assets_list[0] #save max_asset as first value of assets_list
        index = 0 #save index as 0
        for i in range(len(assets_list)):
        #loop through assets list
        #if asset in index i is greater than max_asset
        #save max_asset as asset in index i
        #and save index i
            if assets_list[i] > max_asset:
                max_asset = assets_list[i]
                index = i
        #return the arrest_list in main_list with index i         
        return main_list[index]


if __name__ == "__main__":
    # A sample example of how to use a network object
    network = Network()
    network.load_log("topology1.txt")
    member_name = "Liam"
    print(member_name + "'s sponsor is " + network.sponsor(member_name))
    print(member_name + "'s mentor is " + network.mentor(member_name))
    print(member_name + "'s asset is " + str(network.assets(member_name)))
    print(member_name + "'s childrens are " + str(network.children(member_name)))
    maximum_arrest = 4
    print("The best arrest scenario with the maximum of " + str(maximum_arrest)\
          + " arrests will seize " + str(network.best_arrest_assets(maximum_arrest)))
    print("The best arrest scenario with the maximum of " + str(maximum_arrest)\
          + " arrests is: " + str(network.best_arrest_order(maximum_arrest)))
